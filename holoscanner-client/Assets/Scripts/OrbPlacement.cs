﻿using UnityEngine;
using System.Collections.Generic;
using UnityEngine.Windows.Speech;
using HoloToolkit.Unity;
using HoloToolkit.Sharing;
using Holoscanner;
public class OrbPlacement : Singleton<OrbPlacement>
{

    public uint targetID;
    public bool active = false;
    public bool GotTransform { get; private set; }
    // Called by GazeGestureManager when the user performs a Select gesture
    void OnSelect()
    {
        // TODO: Get the candidate position
        Debug.Log("Clicked!");
        Explode();
        targetFound();
    }

    void Explode()
    {
        //   this.gameObject.PlayAnimation....
        this.gameObject.GetComponent<Renderer>().enabled = false;
        this.gameObject.GetComponent<AudioSource>().enabled = false;
        
    }

    void targetFound()
    {
        //send "target found" message
        //get new targets
        //replace target
        Holoscanner.RemoteMeshManager rmm = this.GetComponentInParent<Holoscanner.RemoteMeshManager>();
        rmm.SendTargetFoundMessage(targetID);
        rmm.SendTargetRequest(); 
    }

    public void replaceTarget(Vector3 t_pos, uint t_id)
    {
        this.gameObject.transform.position = t_pos;
        targetID = t_id;
        this.gameObject.GetComponent<Renderer>().enabled = true;
        this.gameObject.GetComponent<AudioSource>().enabled = true;
    }

    public void activate()
    {
        if (active) return;
        active = true;  
        // this.gameObject.GetComponent<Renderer>().material.SetColor("_Color",new Color(150,150,150));
       // this.gameObject.GetComponent<Renderer>().materials[1].SetColor("_EmissionColor", new Color(0, 255, 0));
        Debug.Log("Activating...");
    }

    public void deactivate()
    {
        if (!active) return;
        active = false;
        //this.gameObject.GetComponent<Renderer>().material.SetColor("_Color", new Color(97, 97, 97));
       // this.gameObject.GetComponent<Renderer>().materials[1].SetColor("_EmissionColor", new Color(0, 0, 0));
        Debug.Log("Deactivating...");
    }

    void Start()
    {
        // We care about getting updates for the anchor transform.
        CustomMessages.Instance.MessageHandlers[CustomMessages.TestMessageID.StageTransform] = this.OnStageTransfrom;

        // And when a new user join we will send the anchor transform we have.
        SharingSessionTracker.Instance.SessionJoined += Instance_SessionJoined;
        
       
        this.gameObject.GetComponent<Renderer>().enabled = false;
        this.gameObject.GetComponent<AudioSource>().enabled = false;

    }

    private void Instance_SessionJoined(object sender, SharingSessionTracker.SessionJoinedEventArgs e)
    {
        if (GotTransform)
        {
            CustomMessages.Instance.SendStageTransform(transform.localPosition, transform.localRotation);
        }
    }


    void Update()
    {
        if (GotTransform)
        {
            if (ImportExportAnchorManager.Instance.AnchorEstablished)
            {
                // Here, activate the sound.
            }
        }
        else
        {
            //transform.position = Vector3.Lerp(transform.position, ProposeTransformPosition(), 0.2f);
        }
    }

    Vector3 ProposeTransformPosition()
    {
        // Put the anchor 2m in front of the user.
        Vector3 retval = Camera.main.transform.position + Camera.main.transform.forward * 2;

        return retval;
    }


    void OnStageTransfrom(NetworkInMessage msg)
    {
        // We read the user ID but we don't use it here.
        msg.ReadInt64();

        this.gameObject.transform.localPosition = CustomMessages.Instance.ReadVector3(msg);
        this.gameObject.transform.localRotation = CustomMessages.Instance.ReadQuaternion(msg);

        // The first time, we'll want to send the message to the anchor to do its animation and
        // swap its materials.

        GotTransform = true;
    }

    public void ResetStage()
    {
        // We'll use this later.
    }
}