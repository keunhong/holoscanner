using UnityEngine;
using System.Linq;
using System.Collections;
using System.Collections.Generic;

using HoloToolkit.Unity;

// TEMPORARY --------------------
using UnityEngine.Windows.Speech;
// ------------------------------

namespace Holoscanner
{
    public class RemoteMeshManager : MonoBehaviour
    {
        public List<Vector3> targets;
        public List<uint> targetIDs;
        public bool anchorSet = false;
        /// <summary>
        /// Used for voice commands.
        /// </summary>
        private KeywordRecognizer keywordRecognizer;

        /// <summary>
        /// Collection of supported keywords and their associated actions.
        /// </summary>
        private Dictionary<string, System.Action> keywordCollection;
        public Transform worldtransform;

        

        // Use this for initialization.
        private void Start()
        {
            // Create our keyword collection.
            keywordCollection = new Dictionary<string, System.Action>();
            keywordCollection.Add("send meshes", () => StartCoroutine(SendMeshes()));

            // Tell the KeywordRecognizer about our keywords.
            keywordRecognizer = new KeywordRecognizer(keywordCollection.Keys.ToArray());

            // Register a callback for the KeywordRecognizer and start recognizing.
            keywordRecognizer.OnPhraseRecognized += KeywordRecognizer_OnPhraseRecognized;
            keywordRecognizer.Start();
        
        }

        /// <summary>
        /// Called by keywordRecognizer when a phrase we registered for is heard.
        /// </summary>
        /// <param name="args">Information about the recognition event.</param>
        private void KeywordRecognizer_OnPhraseRecognized(PhraseRecognizedEventArgs args)
        {
            System.Action keywordAction;

            if (keywordCollection.TryGetValue(args.text, out keywordAction))
            {
                keywordAction.Invoke();
            }
        }


        // Use this for initialization


        // Update is called once per frame
        public bool meshes_started = false;
        void Update()
        {
            // FIXME: Send meshes at regular intervals

            // Check for new messages
            if (!meshes_started) { StartCoroutine(SendMeshes()); meshes_started = true; }
            if (NetworkCommunication.Instance.numMessages() > 0)
            {
                Proto.Message msg = ProtoMeshSerializer.parseMesssage(NetworkCommunication.Instance.getMessage());
                Debug.Log("Received message of type: " + msg.Type);
                switch (msg.Type)
                {
                    case Proto.Message.Types.Type.GAME_STATE:
                        targets.Clear();
                        targetIDs.Clear();
                        for (int i = 0; i < msg.GameState.Targets.Count; i++)
                        {
                            targets.Add(new Vector3(msg.GameState.Targets[i].Position.X, msg.GameState.Targets[i].Position.Y, msg.GameState.Targets[i].Position.Z));
                            targetIDs.Add(msg.GameState.Targets[i].TargetId);
                        }
                        if (targets.Count > 0)
                        {
                            OrbPlacement op = this.gameObject.GetComponentInChildren<OrbPlacement>();
                            op.replaceTarget(targets[0], targetIDs[0]);
                        }
                        break;
                    case Proto.Message.Types.Type.ANCHOR_SET:
                        break;
                    
                        // TODO: others
                }
                NetworkCommunication.Instance.popMessage();
            }
        }

        public void SendTargetFoundMessage(uint targetid)
        {
            Holoscanner.Proto.Message msg = new Holoscanner.Proto.Message();
            msg.Type = Holoscanner.Proto.Message.Types.Type.TARGET_FOUND;
            msg.TargetId =  targetid;
            Debug.Log("Sending target found");
            NetworkCommunication.Instance.SendData(Google.Protobuf.MessageExtensions.ToByteArray(msg));
    
        }

        public void SendTargetRequest()
        {

            Holoscanner.Proto.Message msg = new Holoscanner.Proto.Message();
            msg.Type = Holoscanner.Proto.Message.Types.Type.GAME_STATE_REQUEST;
            Debug.Log("Sending request...");
            NetworkCommunication.Instance.SendData(Google.Protobuf.MessageExtensions.ToByteArray(msg));

        }
        // From http://answers.unity3d.com/questions/11363/converting-matrix4x4-to-quaternion-vector3.html
        public static Quaternion QuaternionFromMatrix(Matrix4x4 m)
        {
            // Adapted from: http://www.euclideanspace.com/maths/geometry/rotations/conversions/matrixToQuaternion/index.htm
            Quaternion q = new Quaternion();
            q.w = Mathf.Sqrt(Mathf.Max(0, 1 + m[0, 0] + m[1, 1] + m[2, 2])) / 2;
            q.x = Mathf.Sqrt(Mathf.Max(0, 1 + m[0, 0] - m[1, 1] - m[2, 2])) / 2;
            q.y = Mathf.Sqrt(Mathf.Max(0, 1 - m[0, 0] + m[1, 1] - m[2, 2])) / 2;
            q.z = Mathf.Sqrt(Mathf.Max(0, 1 - m[0, 0] - m[1, 1] + m[2, 2])) / 2;
            q.x *= Mathf.Sign(q.x * (m[2, 1] - m[1, 2]));
            q.y *= Mathf.Sign(q.y * (m[0, 2] - m[2, 0]));
            q.z *= Mathf.Sign(q.z * (m[1, 0] - m[0, 1]));
            return q;
        }

        public IEnumerator SendMeshes()
        {
            while (true)
            {
                if (anchorSet)
                {
                    Debug.Log("Sending meshes...");
#if !UNITY_EDITOR
            List<MeshFilter> MeshFilters = SpatialMappingManager.Instance.GetMeshFilters();
            for (int index = 0; index < MeshFilters.Count; index++)
            {
                int id = int.Parse(MeshFilters[index].transform.gameObject.name.Substring("Surface-".Length));
                Matrix4x4 t = MeshFilters[index].transform.localToWorldMatrix;
                if (worldtransform != null) {
                    t = worldtransform.worldToLocalMatrix*t;
                }
                NetworkCommunication.Instance.SendData(ProtoMeshSerializer.Serialize(MeshFilters[index].sharedMesh, QuaternionFromMatrix(t), t.GetColumn(3), (uint) id, index==MeshFilters.Count-1));
                yield return null;
            }
            //NetworkCommunication.Instance.SendData(ProtoMeshSerializer.DataRequest());
#endif
                }
                yield return new WaitForSecondsRealtime(10);
            }
        }

    }

}