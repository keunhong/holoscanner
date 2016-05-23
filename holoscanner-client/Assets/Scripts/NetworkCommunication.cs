// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License. See LICENSE in the project root for license information.

using System.Collections.Generic;
using UnityEngine;

#if !UNITY_EDITOR
using Windows.Networking.Sockets;
using Windows.Storage.Streams;
using Windows.Networking;
using Windows.Foundation;
using System.Runtime.InteropServices.WindowsRuntime;
#endif

namespace HoloToolkit.Unity
{
    /// <summary>
    /// NetworkCommunication will try to send meshes from the HoloLens to a remote system that is running the Unity editor.
    /// </summary>
    public class NetworkCommunication : Singleton<NetworkCommunication>
    {
        [Tooltip("The IPv4 Address of the machine running the Unity editor. Copy and paste this value from RemoteMeshTarget.")]
        public string ServerIP;

        [Tooltip("The connection port on the machine to use.")]
        public int ConnectionPort = 11000;


        /// <summary>
        /// Tracks the network connection to the remote machine we are sending meshes to.
        /// </summary>
        

        /// <summary>
        /// Tracks if we are currently sending a mesh.
        /// </summary>
        private bool Sending = false;

        /// <summary>
        /// Temporary buffer for the data we are sending.
        /// </summary>
        private byte[] nextDataBufferToSend;

        /// <summary>
        /// Temporary buffer for the (partial) current message we are receiving
        /// </summary>
        private byte[] currentReceivedMessage;
        private uint currentlength;
 
        /// <summary>
        /// A queue of data buffers to send.
        /// </summary>
        private Queue<byte[]> dataQueue = new Queue<byte[]>();

        private Queue<byte[]> messageQueue = new Queue<byte[]>();

        /// <summary>
        /// If we cannot connect to the server, we will wait before trying to reconnect.
        /// </summary>
        private float deferTime = 0.0f;
 
        /// <summary>
        /// If we cannot connect to the server, this is how long we will wait before retrying.
        /// </summary>
        private float timeToDeferFailedConnections = 10.0f;
   
        public int numMessages() { return messageQueue.Count;  }
        public byte[] getMessage() { return messageQueue.Peek(); }
        public void popMessage() { messageQueue.Dequeue(); }
        public void SendData(byte[] dataBufferToSend)
        {
            byte[] lenbytes = System.BitConverter.GetBytes((ulong)dataBufferToSend.Length);
            byte[] msgbytes = new byte[lenbytes.Length + dataBufferToSend.Length];
            lenbytes.CopyTo(msgbytes, 0);
            dataBufferToSend.CopyTo(msgbytes, lenbytes .Length);
            dataQueue.Enqueue(msgbytes);
            lenbytes = null;
        }
#if !UNITY_EDITOR 
        private StreamSocket networkConnection;
        public void Start()
        {
            currentReceivedMessage = null;
            // Setup a connection to the server.
            HostName networkHost = new HostName(ServerIP.Trim());
            networkConnection = new StreamSocket();

            // Connections are asynchronous.  
            // !!! NOTE These do not arrive on the main Unity Thread. Most Unity operations will throw in the callback !!!
            IAsyncAction outstandingAction = networkConnection.ConnectAsync(networkHost, ConnectionPort.ToString());
            AsyncActionCompletedHandler aach = new AsyncActionCompletedHandler(NetworkConnectedHandler);
            outstandingAction.Completed = aach;
        }
        public void Update()
        {
            // Check to see if deferTime has been set.  
            // DeferUpdates will set the Sending flag to true for 
            // deferTime seconds.  
            if (deferTime > 0.0f)
            {
                DeferUpdates(deferTime);
                deferTime = 0.0f;
            }

            // If we aren't sending a mesh, but we have a mesh to send, send it.
            if (!Sending && dataQueue.Count > 0)
            {
                byte[] nextPacket = dataQueue.Dequeue();
                SendDataOverNetwork(nextPacket);
            }
        }
        private void ListenForMessageHeader()
        {
            IBuffer buffer = new Windows.Storage.Streams.Buffer(sizeof(ulong));
            IAsyncOperationWithProgress<IBuffer, uint> newmessagereceived = networkConnection.InputStream.ReadAsync(buffer, sizeof(ulong), new InputStreamOptions());
            newmessagereceived.Completed = new AsyncOperationWithProgressCompletedHandler<IBuffer, uint>(MessageHeaderReceived);
        }
        public void MessageHeaderReceived(IAsyncOperationWithProgress<IBuffer, uint> asyncInfo, AsyncStatus status)
        {
            byte[] bytes = WindowsRuntimeBufferExtensions.ToArray(asyncInfo.GetResults());
            Debug.Log("Lengthbytes: " + bytes[0] + " " + bytes[1] + " " + bytes[2] + " " + bytes[3] + " " + bytes[4] + " " + bytes[5] + " " + bytes[6] + " " + bytes[7]);
            ulong length = System.BitConverter.ToUInt64(bytes,0);
            if (length == 0)
            {
                ListenForMessageHeader();
                return;
            }
            currentReceivedMessage = new byte[length];
            currentlength = 0;
            Debug.Log("Receiving new message length " + length);
            ListenForMessage();
        }
        private void ListenForMessage()
        {
            IBuffer buffer = new Windows.Storage.Streams.Buffer((uint) currentReceivedMessage.Length);
            IAsyncOperationWithProgress<IBuffer, uint> newmessagereceived = networkConnection.InputStream.ReadAsync(buffer, (uint) currentReceivedMessage.Length, new InputStreamOptions());
            newmessagereceived.Completed = new AsyncOperationWithProgressCompletedHandler<IBuffer, uint>(MessageReceived);
        }
        public void MessageReceived(IAsyncOperationWithProgress<IBuffer, uint> asyncInfo, AsyncStatus status)
        {
            byte[] bytes = WindowsRuntimeBufferExtensions.ToArray(asyncInfo.GetResults());
            Debug.Log("Processing message of total length " + bytes.Length);
            for (int i = 0; i < bytes.Length; i++)
            {
                currentReceivedMessage[currentlength++] = bytes[i];
            }
            if (currentlength == currentReceivedMessage.Length)
            {
                Debug.Log("Finished receiving message of length " + currentlength);
                messageQueue.Enqueue(currentReceivedMessage);
                currentlength = 0;
                currentReceivedMessage = null;
                ListenForMessageHeader();
            } else
            {
                ListenForMessage();
            }
        }
        /// <summary>
        /// Handles waiting for some amount of time before trying to reconnect.
        /// </summary>
        /// <param name="timeout">Time in seconds to wait.</param>
        void DeferUpdates(float timeout)
        {
            Sending = true;
            Invoke("EnableUpdates", timeout);
        }


        /// <summary>
        /// Stops waiting to reconnect.
        /// </summary>
        void EnableUpdates()
        {
            Sending = false;
        }

        /// <summary>
        /// Queues up a data buffer to send over the network.
        /// </summary>
        /// <param name="dataBufferToSend">The data buffer to send.</param>
       

        /// <summary>
        /// Sends the data over the network.
        /// </summary>
        /// <param name="dataBufferToSend">The data buffer to send.</param>
        private void SendDataOverNetwork(byte[] dataBufferToSend)
        {
            if (Sending)
            {
                // This shouldn't happen, but just in case.
                Debug.Log("one at a time please");
                return;
            }
            if (networkConnection == null)
            {
                Debug.Log("Network connection not yet initialized");
                return;
            }

            // Track that we are sending a data buffer.
            Sending = true;

            nextDataBufferToSend = dataBufferToSend;
            
            IAsyncOperationWithProgress<uint, uint> newmessagereceived = networkConnection.OutputStream.WriteAsync(nextDataBufferToSend.AsBuffer());
            AsyncOperationWithProgressCompletedHandler<uint, uint> aowpch = new AsyncOperationWithProgressCompletedHandler<uint, uint>(DataSentHandler);
            newmessagereceived.Completed = aowpch;
        }

        /// <summary>
        /// Called when a connection attempt complete, successfully or not.  
        /// !!! NOTE These do not arrive on the main Unity Thread. Most Unity operations will throw in the callback !!!
        /// </summary>
        /// <param name="asyncInfo">Data about the async operation.</param>
        /// <param name="status">The status of the operation.</param>
        public void NetworkConnectedHandler(IAsyncAction asyncInfo, AsyncStatus status)
        {
            // Status completed is successful.
            if (status == AsyncStatus.Completed)
            {
                Debug.Log("network connected");
                ListenForMessageHeader();
            }
            else
            {
                Debug.Log("Failed to establish connection. Error Code: " + asyncInfo.ErrorCode);
                // In the failure case we'll requeue the data and wait before trying again.
                networkConnection.Dispose();
                networkConnection = null;
                // And set the defer time so the update loop can do the 'Unity things' 
                // on the main Unity thread.
                deferTime = timeToDeferFailedConnections;
            }
        }

        /// <summary>
        /// Called when sending data has completed.
        /// !!! NOTE These do not arrive on the main Unity Thread. Most Unity operations will throw in the callback !!!
        /// </summary>
        /// <param name="operation">The operation in flight.</param>
        /// <param name="status">The status of the operation.</param>
        public void DataSentHandler(IAsyncOperationWithProgress<uint, uint> asyncInfo, AsyncStatus status)
        {
            // If we failed, requeue the data and set the deferral time.
            if (status == AsyncStatus.Error)
            {
                Debug.Log("Error sending message, retrying...");
                // didn't send, so requeue
                dataQueue.Enqueue(nextDataBufferToSend);
                //Sending = false;
               // SendData(nextDataBufferToSend);
                deferTime = timeToDeferFailedConnections;
            }
            else
            {
                // If we succeeded, clear the sending flag so we can send another mesh
                Sending = false;
            }
        }
#endif
    }
}
