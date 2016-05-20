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

#region Temporary
        /// <summary>
        /// Used for voice commands.
        /// </summary>
        private KeywordRecognizer keywordRecognizer;

        /// <summary>
        /// Collection of supported keywords and their associated actions.
        /// </summary>
        private Dictionary<string, System.Action> keywordCollection;

        private List<Vector3> targets;

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
#endregion

        /*
        // Use this for initialization
        void Start()
        {

        }*/

        // Update is called once per frame
        void Update()
        {
            // FIXME: Send meshes at regular intervals

            // Check for new messages
            if (NetworkCommunication.Instance.numMessages() > 0)
            {
                Proto.Message msg = ProtoMeshSerializer.parseMesssage(NetworkCommunication.Instance.getMessage());
                switch (msg.Type)
                {
                    case Proto.Message.Types.Type.GAME_STATE:
                        targets.Clear();
                        for (int i = 0; i < msg.GameState.Targets.Count; i++)
                        {
                            targets.Add(new Vector3(msg.GameState.Targets[i].Position.X, msg.GameState.Targets[i].Position.Y, msg.GameState.Targets[i].Position.Z));
                        }
                        break;
                    case Proto.Message.Types.Type.ANCHOR_SET:
                        break;
                        // TODO: others
                }
                NetworkCommunication.Instance.popMessage();
            }
        }

        private void SendTargetFoundMessage(int targetid)
        {
            Holoscanner.Proto.Message msg = new Holoscanner.Proto.Message();
            msg.Type = Holoscanner.Proto.Message.Types.Type.TARGET_FOUND;
            msg.TargetId = (uint) targetid;
            NetworkCommunication.Instance.SendData(Google.Protobuf.MessageExtensions.ToByteArray(msg));
        }

        private IEnumerator SendMeshes()
        {
#if !UNITY_EDITOR
            List<MeshFilter> MeshFilters = SpatialMappingManager.Instance.GetMeshFilters();
            for (int index = 0; index < MeshFilters.Count; index++)
            {
                int id = int.Parse(MeshFilters[index].transform.gameObject.name.Substring("Surface-".Length));
                NetworkCommunication.Instance.SendData(ProtoMeshSerializer.Serialize(MeshFilters[index].sharedMesh, MeshFilters[index].transform, (uint) id, index==MeshFilters.Count-1));
                yield return null;
            }
            NetworkCommunication.Instance.SendData(ProtoMeshSerializer.DataRequest());
#endif
            yield return null;
        }
    }

}