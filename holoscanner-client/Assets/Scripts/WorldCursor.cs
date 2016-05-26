﻿using UnityEngine;

public class WorldCursor : MonoBehaviour
{
    private MeshRenderer meshRenderer;
    float last_depth = 1.0f;

    // Use this for initialization
    void Start()
    {
        // Grab the mesh renderer that's on the same object as this script.
        meshRenderer = this.gameObject.GetComponentInChildren<MeshRenderer>();
    }

    // Update is called once per frame
    void Update()
    {
        // Do a raycast into the world based on the user's
        // head position and orientation.
        var headPosition = Camera.main.transform.position;
        var gazeDirection = Camera.main.transform.forward;

        RaycastHit hitInfo;
        if (Physics.Raycast(headPosition, gazeDirection, out hitInfo,Mathf.Infinity,1<<8))
        {
            // If the raycast hit a hologram...
            float depthOfCursor = hitInfo.distance;
            if (depthOfCursor > 2.0f) { depthOfCursor = 2.0f; meshRenderer.material.color = Color.red; }
            else { meshRenderer.material.color = Color.green; }
            // Display the cursor mesh.
            meshRenderer.enabled = true;
            // Move the cursor to the point where the raycast hit.
            this.transform.position = headPosition + gazeDirection * depthOfCursor;//hitInfo.point;
            // Rotate the cursor to hug the surface of the hologram.
            this.transform.rotation =
                Quaternion.FromToRotation(Vector3.up, -gazeDirection);
            last_depth = depthOfCursor;

            //if (hitInfo.collider.gameObject.name == "orb")
            //{
            //    meshRenderer.enabled = true;
            //}
            //else
            //{
            //    meshRenderer.enabled = false;
            //}
        }
        else
        {
            // If the raycast did not hit a hologram, hide the cursor mesh.
            meshRenderer.enabled = false;
            //this.transform.position = headPosition + gazeDirection * last_depth;
            //this.transform.rotation = Quaternion.FromToRotation(Vector3.up, -gazeDirection);
        }
    }
}
