using UnityEngine;
using System.Collections;

public class Fade : MonoBehaviour {
    public int duration = 30;
    public Color endcolor;
    public Color startcolor;
    bool istextrender = true;
    IEnumerator coroutine;
    public enum FadeState
    {
        FADING_IN,
        FADING_OUT,
        OUT,
        IN
    };
    public FadeState state { get; private set; }
    IEnumerator doFadeIn()
    {
        state = FadeState.FADING_IN;
        gameObject.GetComponent<Renderer>().enabled = true;
        for (int i = 0; i < duration; i++)
        {
            Color c = Color.Lerp(startcolor, endcolor, (i + 1.0f) / duration);
            if (istextrender) gameObject.GetComponent<TextMesh>().color = c;
            else gameObject.GetComponent<Renderer>().material.color = c;
            yield return null;
        }
        state = FadeState.IN;
        coroutine = null;
    }
    IEnumerator doFadeOut()
    {
        state = FadeState.FADING_OUT;
        for (int i = 0; i < duration; i++)
        {
            Color c = Color.Lerp(startcolor, endcolor, 1 - (i + 1.0f) / duration);
            if (istextrender) gameObject.GetComponent<TextMesh>().color = c;
            else gameObject.GetComponent<Renderer>().material.color = c;
            yield return null;
        }
        gameObject.GetComponent<Renderer>().enabled = false;
        state = FadeState.OUT;
        coroutine = null;
    }
    public void fadeIn()
    {
        if (coroutine != null) StopCoroutine(coroutine);
        coroutine = doFadeIn();
        StartCoroutine(coroutine);
    }
    public void fadeOut()
    {
        if (coroutine != null) StopCoroutine(coroutine);
        coroutine = doFadeOut();
        StartCoroutine(coroutine);
    }
    public void show(bool showobject)
    {
        gameObject.GetComponent<Renderer>().enabled = showobject;
        if (istextrender) gameObject.GetComponent<TextMesh>().color = showobject?endcolor:startcolor;
        else gameObject.GetComponent<Renderer>().material.color = showobject?endcolor:startcolor;
    }
	// Use this for initialization
	void Start () {
        if (gameObject.GetComponent<TextMesh>() == null)
        {
            istextrender = false;
        }
        if (istextrender) endcolor = gameObject.GetComponent<TextMesh>().color;
        else endcolor = gameObject.GetComponent<Renderer>().material.color;
        state = FadeState.OUT;
    }
	
	// Update is called once per frame
	void Update () {
	    
	}
}
