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
        private ScoreScript ss;
        public bool anchorSet = false;
        public bool gameOver = false;
        public bool gamestarted { get; private set; }
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
            ss = GameObject.Find("Scoreboard").GetComponent<ScoreScript>();
            // Create our keyword collection.
           // keywordCollection = new Dictionary<string, System.Action>();
     //       keywordCollection.Add("send meshes", () => StartCoroutine(SendMeshes()));

            // Tell the KeywordRecognizer about our keywords.
           // keywordRecognizer = new KeywordRecognizer(keywordCollection.Keys.ToArray());

            // Register a callback for the KeywordRecognizer and start recognizing.
         //   keywordRecognizer.OnPhraseRecognized += KeywordRecognizer_OnPhraseRecognized;
         //   keywordRecognizer.Start();
        
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
            if (!meshes_started) { StartCoroutine(SendMeshes()); meshes_started = true; StartCoroutine(SendPosition()); }
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
                            StartCoroutine(op.replaceTarget(targets[0], targetIDs[0]));                          
                        }
                        ss.UpdateScores(msg.GameState);
                        break;
                    case Proto.Message.Types.Type.START_GAME:
                        gamestarted = true;
                        GameObject.Find("TitleScreen").GetComponent<TitleScreenScript>().gameStarted();
                        break;
                    case Proto.Message.Types.Type.CLIENT_SET_NICKNAME:
                        ss.clientName = msg.DeviceId;
                        ss.showPlayerColor();
                        Debug.Log("New name " + msg.DeviceId);
                        break;
                    case Proto.Message.Types.Type.VERIFIED:
                        GameObject.Find("TitleScreen").GetComponent<TitleScreenScript>().showTitle();
                        break;
                    case Proto.Message.Types.Type.END_GAME:
                        gameOver = true;
                        GameObject.Find("EndgameScreen").GetComponent<EndgameScript>().endGame();
                        GameObject.Find("orb").GetComponent<OrbPlacement>().setComponentsEnabled(false);
                        break;
                    
                        // TODO: others
                }
                NetworkCommunication.Instance.popMessage();
            }
        }

        public void StartGameRequest()
        {
            //request that the server starts the game and sends out targets to everyone.
            //server should only send out targets once it has received the start game request from all the joined clients. in the future we can fix it so that it doesn't start until it has received this from 3 clients

            //for now, just request state. but change this in future:

            Holoscanner.Proto.Message msg = new Holoscanner.Proto.Message();
            msg.Type = Holoscanner.Proto.Message.Types.Type.CLIENT_READY;
            Debug.Log("Sending start-game request...");
            NetworkCommunication.Instance.SendData(Google.Protobuf.MessageExtensions.ToByteArray(msg));

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

        public IEnumerator SendPosition()
        {
            while (true)
            {
                if (gameOver) break;
                if (anchorSet)
                {
                    Holoscanner.Proto.Message msg = new Holoscanner.Proto.Message();
                    msg.Type = Holoscanner.Proto.Message.Types.Type.CLIENT_POSITION;
                    Transform t = GameObject.Find("SpatialMapping").transform;
                    Vector3 t_pos = t.InverseTransformPoint(GameObject.Find("Main Camera").transform.position);
                    Vector3 axis; float angle;
                    GameObject.Find("Main Camera").transform.rotation.ToAngleAxis(out angle, out axis);
                    axis = t.InverseTransformDirection(axis);
                    Quaternion t_ori = Quaternion.AngleAxis(angle, axis);
                    msg.ClientPosition = new Proto.ClientPosition();
                    msg.ClientPosition.Position = new Proto.Vec3D();
                    msg.ClientPosition.Rotation = new Proto.Vec4D();
                    msg.ClientPosition.Position.X = t_pos.x;
                    msg.ClientPosition.Position.Y = t_pos.y;
                    msg.ClientPosition.Position.Z = t_pos.z;
                    msg.ClientPosition.Rotation.X = t_ori.x;
                    msg.ClientPosition.Rotation.Y = t_ori.y;
                    msg.ClientPosition.Rotation.Z = t_ori.z;
                    msg.ClientPosition.Rotation.W = t_ori.w;
                    NetworkCommunication.Instance.SendData(Google.Protobuf.MessageExtensions.ToByteArray(msg));
                }
                yield return new WaitForSecondsRealtime(0.05f);
            }
        }

        public IEnumerator SendMeshes()
        {
            while (true)
            {
                if (gameOver) break;
                if (anchorSet)
                {
                    Debug.Log("Sending meshes...");
#if !UNITY_EDITOR
                    if (SpatialMappingManager.Instance == null || SpatialMappingManager.Instance.GetMeshFilters() == null)
                    {
                        Debug.Log("Spatial Stuff was NULL!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
                        yield return null; continue;
                    }
                    List<MeshFilter> MeshFilters = SpatialMappingManager.Instance.GetMeshFilters();
                    
                    for (int index = 0; index < MeshFilters.Count; index++)
                     {
                        if (MeshFilters[index] == null)
                        {
                            Debug.Log("index null");
                            continue;
                        }
                        int id = int.Parse(MeshFilters[index].transform.gameObject.name.Substring("Surface-".Length));
                        Matrix4x4 t = MeshFilters[index].transform.localToWorldMatrix;
                    
                        if (worldtransform != null)
                        {
                            t = worldtransform.worldToLocalMatrix*t;
                        }
                        byte[] data = ProtoMeshSerializer.Serialize(MeshFilters[index].sharedMesh, QuaternionFromMatrix(t), t.GetColumn(3), (uint)id, index == MeshFilters.Count - 1, index == 0);
                        yield return null;
                NetworkCommunication.Instance.SendData(data);
                   
                        yield return null;
            }
            //NetworkCommunication.Instance.SendData(ProtoMeshSerializer.DataRequest());
#endif
                }
                yield return new WaitForSecondsRealtime(5);
            }
        }

    }

}
