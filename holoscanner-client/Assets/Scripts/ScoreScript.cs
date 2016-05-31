using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class ScoreScript : MonoBehaviour {
    int state = -1;
    public void showScoreboard()
    {
        List<Fade> fades = new List<Fade>();
        gameObject.GetComponentsInChildren<Fade>(fades);
        foreach (Fade f in fades) f.fadeIn();
        if (gameObject.GetComponent<Fade>() != null) gameObject.GetComponent<Fade>().fadeIn();
        state = 1;
    }
    public void setScoreboardLocation(Vector3 pos)
    {
        gameObject.transform.position = pos;
    }
    // Use this for initialization
    void Start () {
	}
    IEnumerator holdScoreboad()
    {
        state = 2;
        yield return new WaitForSeconds(3.0f);
        state = 3;
    }
	
	// Update is called once per frame
	void Update () {
        if (state == -1)
        {
            List<Fade> fades = new List<Fade>();
            gameObject.GetComponentsInChildren<Fade>(fades);
            foreach (Fade f in fades) f.show(false);
            if (gameObject.GetComponent<Fade>() != null) gameObject.GetComponent<Fade>().show(false);
            state = 0;
        }
	    else if (state == 1)
        {
            StartCoroutine(holdScoreboad());
        }
        else if (state == 3)
        {
            state = 4;
            List<Fade> fades = new List<Fade>();
            gameObject.GetComponentsInChildren<Fade>(fades);
            foreach (Fade f in fades) f.fadeOut();
            if (gameObject.GetComponent<Fade>() != null) gameObject.GetComponent<Fade>().fadeOut();
        }
	}

    public void UpdateScores(Holoscanner.Proto.GameState gs)
    {
        List<TextMesh> textels = new List<TextMesh>();
        gameObject.GetComponentsInChildren<TextMesh>(textels);
        List<Holoscanner.Proto.Client> sc = new List<Holoscanner.Proto.Client>(gs.Clients);
        sc.Sort((a, b) => a.Score.CompareTo(b.Score));
        for (int i = 0; i < textels.Count; i++)
        {
            if (i < gs.Clients.Count)
            {
                string s = gs.Clients[i].DeviceId + ": " + gs.Clients[i].Score.ToString();
                Debug.Log(s);
                textels[i].text = s;
                textels[i].color = new Color(1.0f, 1.0f, 1.0f);
            } else
            {
                textels[i].text = "";
            }
        }
    }
}
