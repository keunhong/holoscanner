using UnityEngine;
using System.Collections.Generic;
using UnityEngine.Windows.Speech;
using HoloToolkit.Unity;
using HoloToolkit.Sharing;
using Holoscanner;

using System.Collections;
public class OrbPlacement : Singleton<OrbPlacement>
{

    public uint targetID;
    bool foundOnThisHololens = false;
    bool audioOn = true;
    bool startOrb = true;
    bool isEnabled = false;
    public bool GotTransform { get; private set; }
    // Called by GazeGestureManager when the user performs a Select gesture
    void OnSelect()
    {
        // TODO: Get the candidate position
        if (foundOnThisHololens) return;
        Debug.Log("Successfully clicked on orb!");
        foundOnThisHololens = true;
        StartCoroutine(Explode());
       
        targetFound();
    }
    public Vector3 getPositionAhead()
    {
        var headPosition = Camera.main.transform.position;
        var gazeDirection = Camera.main.transform.forward;

        RaycastHit hitInfo;
        if (Physics.Raycast(headPosition, gazeDirection, out hitInfo, 2))
        {
            return hitInfo.point - gazeDirection/20;
        } else
        {
            return headPosition + 2*gazeDirection;
        }
    }
    public void setComponentsEnabled(bool enable)
    {
        if (isEnabled == enable)
        {
            Debug.Log("Warning: Trying to set state to what it already was...returning");
            return;
        }
        GameObject.Find("MagicBlast1").GetComponent<ParticleSystem>().Stop();
        GameObject.Find("MagicBlast1").GetComponent<ParticleSystem>().Clear();
        gameObject.GetComponent<MeshCollider>().enabled = enable;
        foreach (ParticleSystem sys in GameObject.Find("EnergyBall3").GetComponents<ParticleSystem>())
        {
            if (enable) sys.Play();
            ParticleSystem.EmissionModule em = sys.emission;
            em.enabled = enable;
        }
        foreach (ParticleSystem sys in GameObject.Find("EnergyBall3").GetComponentsInChildren<ParticleSystem>())
        {
            if (enable) sys.Play();
            ParticleSystem.EmissionModule em = sys.emission;
            em.enabled = enable;
        }
        GameObject.Find("MagicBlast1").GetComponent<ParticleSystem>().Play();
        Debug.Log("Setting playsound to:" + enable);
        gameObject.GetComponent<RandomNote>().playSound = enable;
        isEnabled = enable;

    }
    private System.Collections.IEnumerator setComponentsEnabledDelay(bool enable, float delay)
    {
        yield return new WaitForSeconds(delay);
        setComponentsEnabled(enable);
    }
    IEnumerator Explode()
    {
        if (foundOnThisHololens) playFastChime();
        else playSlowChime();
        GameObject go = GameObject.Find("Scoreboard");
        ScoreScript ss = go.GetComponent<ScoreScript>();
        ss.setScoreboardLocation(getPositionAhead());
        ss.showScoreboard();
        setComponentsEnabled(false);
        yield return new WaitForSecondsRealtime(2.4f);

        audioOn = false;
    }

    void targetFound()
    {
        Holoscanner.RemoteMeshManager rmm = this.GetComponentInParent<Holoscanner.RemoteMeshManager>();
        if (startOrb) { rmm.StartGameRequest(); startOrb = false; }
        else
            rmm.SendTargetFoundMessage(targetID);
        //rmm.SendTargetRequest(); 
    }

    void playSlowChime()
    {
        GameObject.Find("MagicBlast1").GetComponents < AudioSource >()[1].Play();
    }

    void playFastChime()
    {
        GameObject.Find("MagicBlast1").GetComponents < AudioSource >()[0].Play();
    }

    public IEnumerator replaceTarget(Vector3 t_pos, uint t_id)
    {
        //disable randomsound
        //yield for length of sousnd
        //replace object
        if (!foundOnThisHololens) StartCoroutine(Explode());
        while (audioOn) yield return null;
        this.gameObject.transform.localPosition = t_pos;
        targetID = t_id;
        setComponentsEnabled(true);
        audioOn = true;
        foundOnThisHololens = false;
    }

    void Start()
    {
        // We care about getting updates for the anchor transform.
        CustomMessages.Instance.MessageHandlers[CustomMessages.TestMessageID.StageTransform] = this.OnStageTransfrom;

        // And when a new user join we will send the anchor transform we have.
        SharingSessionTracker.Instance.SessionJoined += Instance_SessionJoined;

        gameObject.GetComponent<RandomNote>().playSound = false;
    }

    private void Instance_SessionJoined(object sender, SharingSessionTracker.SessionJoinedEventArgs e)
    {
        if (GotTransform)
        {
            CustomMessages.Instance.SendStageTransform(transform.localPosition, transform.localRotation);
            GameObject.Find("HologramCollection").GetComponent<Holoscanner.RemoteMeshManager>().anchorSet = true;
            Debug.Log("Trying to set the anchor correctly.");
        }
        
    }


    void Update()
    {
        if (GotTransform)
        {
            if (ImportExportAnchorManager.Instance.AnchorEstablished)
            {
                // Here, activate the sound.
                GameObject.Find("HologramCollection").GetComponent<Holoscanner.RemoteMeshManager>().anchorSet = true;
                Debug.Log("Trying to set the anchor correctly.");
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
        GameObject.Find("HologramCollection").GetComponent<Holoscanner.RemoteMeshManager>().anchorSet = true;
        Debug.Log("Trying to set the anchor correctly.");
    }

    public void ResetStage()
    {
        // We'll use this later.
    }
} 