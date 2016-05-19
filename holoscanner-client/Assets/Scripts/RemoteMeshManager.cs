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

        // Use this for initialization.
        private void Start()
        {
            // Create our keyword collection.
            keywordCollection = new Dictionary<string, System.Action>();
            keywordCollection.Add("send meshes", () => SendMeshes());

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
        }

        private void SendMeshes()
        {
#if !UNITY_EDITOR
            List<MeshFilter> MeshFilters = SpatialMappingManager.Instance.GetMeshFilters();
            int num_faces = 0;
            int num_verts = 0;
            Debug.Log("Loop iterations: " + MeshFilters.Count);

            for (int index = 0; index < MeshFilters.Count; index++)
            {
                
                List<Mesh> meshesToSend = new List<Mesh>();
               MeshFilter filter = MeshFilters[index];
                Mesh source = filter.sharedMesh;
                Mesh clone = new Mesh();
                List<Vector3> verts = new List<Vector3>();
                verts.AddRange(source.vertices);
                num_verts += verts.Count;
                
                
                for (int vertIndex = 0; vertIndex < verts.Count; vertIndex++)
                {
                    verts[vertIndex] = filter.transform.TransformPoint(verts[vertIndex]);
                }


                num_faces += source.triangles.Length;
               clone.SetVertices(verts);
                
                clone.SetTriangles(source.triangles, 0);
                meshesToSend.Add(clone);

                byte[] serialized = ProtoMeshSerializer.Serialize(meshesToSend[0]);
 
             
                
                RemoteMeshSource.Instance.SendData(serialized);

                //RemoteMeshSource.Instance.Update();
                
                clone.Clear();
                clone = null;

                meshesToSend.Clear();
                meshesToSend = null;
                serialized = null;
                verts.Clear();
                verts = null;

                System.GC.Collect();
                System.GC.WaitForPendingFinalizers();


                // meshesToSend.Clear();


            }
#endif
        }
    }

}