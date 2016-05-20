using UnityEngine;
using System.Collections.Generic;
using UnityEngine.Windows.Speech;
using HoloToolkit.Unity;
using HoloToolkit.Sharing;
public class OrbPlacement : Singleton<OrbPlacement>
{


    public bool GotTransform { get; private set; }
    // Called by GazeGestureManager when the user performs a Select gesture
    void OnSelect()
    {
        // TODO: Get the candidate position
        Debug.Log("Clicked!");
        this.gameObject.transform.Translate(Vector3.up);
    }

    void Start()
    {
        // We care about getting updates for the anchor transform.
        CustomMessages.Instance.MessageHandlers[CustomMessages.TestMessageID.StageTransform] = this.OnStageTransfrom;

        // And when a new user join we will send the anchor transform we have.
        SharingSessionTracker.Instance.SessionJoined += Instance_SessionJoined;
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