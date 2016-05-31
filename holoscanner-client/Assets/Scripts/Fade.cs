using UnityEngine;
using System.Collections;

public class Fade : MonoBehaviour {
    public int duration = 30;
    public Color endcolor;
    public Color startcolor;
    bool istextrender = true;
    IEnumerator coroutine;
    int currstep = 0;
    public enum FadeState
    {
        FADING_IN,
        FADING_OUT,
        OUT,
        IN
    };
    public FadeState state { get; private set; }
    public Color getCurrentColor()
    {
        if (istextrender) return gameObject.GetComponent<TextMesh>().color;
        else return gameObject.GetComponent<Renderer>().material.color;
    }
    IEnumerator doFadeIn()
    {
        state = FadeState.FADING_IN;
        gameObject.GetComponent<Renderer>().enabled = true;
        for (; currstep < duration; currstep++)
        {
            Color c = Color.Lerp(startcolor, endcolor, (currstep + 1.0f) / duration);
            if (istextrender) gameObject.GetComponent<TextMesh>().color = c;
            else gameObject.GetComponent<Renderer>().material.color = c;
            yield return null;
        }
        currstep = duration - 1;
        state = FadeState.IN;
        coroutine = null;
    }
    IEnumerator doFadeOut()
    {
        state = FadeState.FADING_OUT;
        for (; currstep >= 0; currstep--)
        {
            Color c = Color.Lerp(startcolor, endcolor, (currstep + 1.0f) / duration);
            if (istextrender) gameObject.GetComponent<TextMesh>().color = c;
            else gameObject.GetComponent<Renderer>().material.color = c;
            yield return null;
        }
        currstep = 0;
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
    public void stopAnimation()
    {
        if (coroutine != null) StopCoroutine(coroutine);
        coroutine = null;
    }
    public void show(bool showobject)
    {
        if (!showobject) stopAnimation();
        gameObject.GetComponent<Renderer>().enabled = showobject;
        if (istextrender) gameObject.GetComponent<TextMesh>().color = showobject?endcolor:startcolor;
        else gameObject.GetComponent<Renderer>().material.color = showobject?endcolor:startcolor;
        currstep = showobject ? duration - 1 : 0;
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
        currstep = 0;
    }
	
	// Update is called once per frame
	void Update () {
	    
	}
}
