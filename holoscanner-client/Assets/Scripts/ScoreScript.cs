using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class ScoreScript : MonoBehaviour {
    int state = -1;
    public string clientName;
    Dictionary<string, Color> colormap;
    public void showScoreboard()
    {
        List<Fade> fades = new List<Fade>();
        gameObject.GetComponentsInChildren<Fade>(fades);
        foreach (Fade f in fades) f.fadeIn();
        if (gameObject.GetComponent<Fade>() != null) gameObject.GetComponent<Fade>().fadeIn();
        state = 1;
    }
    public void showPlayerColor()
    {
        /*var headPosition = Camera.main.transform.position;
        var gazeDirection = Camera.main.transform.forward;
        setScoreboardLocation(headPosition + 2.0f*gazeDirection);
        List<TextMesh> textels = new List<TextMesh>();
        gameObject.GetComponentsInChildren<TextMesh>(textels);
        List<Fade> fades = new List<Fade>();
        gameObject.GetComponentsInChildren(fades);
        for (int i = 0; i < textels.Count; i++)
        {
            if (i > 0) textels[i].text = "";
            else
            {
                textels[i].text = "You are " + clientName + " player";
                textels[i].color = colormap.ContainsKey(clientName) ? colormap[clientName] : Color.white;
                fades[i].endcolor = textels[i].color;
            }
        }
        showScoreboard();*/
    }
    public void setScoreboardLocation(Vector3 pos)
    {
        gameObject.transform.position = pos;
    }
    // Use this for initialization
    void Start () {
        colormap = new Dictionary<string, Color>()
        {
            { "Blue", new Color(0.392f, 0.71f, 0.965f) },
            { "Orange", new Color(1.0f, 0.718f, 0.302f) },
            { "Green", new Color(0.682f, 0.835f, 0.506f)},
            { "Pink", new Color(0.957f, 0.561f, 0.694f) }
        };
    }
    IEnumerator holdScoreboad()
    {
        state = 2;
        yield return new WaitForSeconds(4.0f);
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
        List<Fade> fades = new List<Fade>();
        gameObject.GetComponentsInChildren(fades);
        List<Holoscanner.Proto.Client> sc = new List<Holoscanner.Proto.Client>(gs.Clients);
        sc.Sort((a, b) => b.Score.CompareTo(a.Score));
        int j = 0;
        for (int i = 0; i < textels.Count; i++)
        {
            if (j < sc.Count)
            {
                if (sc[j].DeviceId == "__server__")
                {
                    j++;
                    i--;
                    continue;
                }
                if (sc[j].Nickname == clientName)
                {
                    textels[i].text = "You: " + sc[j].Score.ToString();
                    textels[i].fontStyle = FontStyle.Bold;
                }
                else {
                    textels[i].fontStyle = FontStyle.Normal;
                    string s = sc[j].Nickname + ": " + sc[j].Score.ToString();
                    textels[j].text = s;
                }
                textels[i].color = colormap.ContainsKey(sc[j].Nickname)?colormap[sc[j].Nickname]:Color.white;
                fades[i].endcolor = textels[i].color;
                j++;
            } else
            {
                textels[i].text = "";
            }
        }
    }
}
