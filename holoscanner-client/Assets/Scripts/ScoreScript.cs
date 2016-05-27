using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class ScoreScript : MonoBehaviour {
    Color endtextcolor, endscoreboardcolor;
    int state = 0;
    void enableScoreboard(bool enable)
    {
        //gameObject.GetComponent<Renderer>().enabled = enable;
        /*List<TextMesh> renderers = new List<TextMesh>();
        gameObject.GetComponentsInChildren<TextMesh>(renderers);
        foreach (TextMesh r in renderers) r.color = enable? endtextcolor : Color.black;*/
    }
    void setColors(float t)
    {
        /*Color newcol = Color.Lerp(Color.black, endscoreboardcolor, t);
        newcol.a = t;
        gameObject.GetComponent<Renderer>().material.color = newcol;
        //Debug.Log(newcol.ToString());*/
        List<TextMesh> renderers = new List<TextMesh>();
        gameObject.GetComponentsInChildren<TextMesh>(renderers);
        Color newcol = Color.Lerp(Color.black, endtextcolor, t);
        foreach (TextMesh r in renderers)
        {
            r.color = newcol;
        }
    }
    public void showScoreboard()
    {
        setColors(0);
        enableScoreboard(true);
        StartCoroutine(fadeIn());
    }
    IEnumerator fadeIn()
    {
        for (int i = 0; i < 30; i++)
        {
            setColors((i + 1) / 30.0f);
            yield return null;
        }
        state = 1;
    }
    IEnumerator fadeOut()
    {
        for (int i = 0; i < 30; i++)
        {
            setColors(1 - (i + 1) / 30.0f);
            yield return null;
        }
        enableScoreboard(false);
        state = 0;
    }
    public void setScoreboardLocation(Vector3 pos)
    {
        gameObject.transform.transform.position = pos;
    }
    // Use this for initialization
    void Start () {
        endscoreboardcolor = gameObject.GetComponent<MeshRenderer>().material.color;
        endtextcolor = gameObject.GetComponentInChildren<TextMesh>().color;

        enableScoreboard(false);
	}
    IEnumerator holdScoreboad()
    {
        state = 2;
        yield return new WaitForSeconds(3.0f);
        state = 3;
    }
	
	// Update is called once per frame
	void Update () {
	    if (state == 1)
        {
            StartCoroutine(holdScoreboad());
        } else if (state == 3)
        {
            state = 4;
            StartCoroutine(fadeOut());
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
