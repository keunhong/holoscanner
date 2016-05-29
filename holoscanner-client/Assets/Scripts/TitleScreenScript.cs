using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class TitleScreenScript : MonoBehaviour
{
    GameObject titletext, instructionstext, taptext;
    enum TitleState
    {
        INITIAL,
        INSTRUCTIONSIN,
        INSTRUCTIONS,
        INSTRUCTIONSOUTTRIGGER,
        INSTRUCTIONSOUT,
        TAPIN,
        TAP
    };

    IEnumerator timing()
    {
        state = TitleState.INITIAL;
        yield return new WaitForSeconds(5.0f);
        state = TitleState.INSTRUCTIONSOUTTRIGGER;
    }

    public void gameStarted()
    {
        titletext.GetComponent<Fade>().startcolor = Color.black;
        instructionstext.GetComponent<Fade>().startcolor = Color.black;
        taptext.GetComponent<Fade>().startcolor = Color.black;
        gameObject.GetComponent<Fade>().fadeOut();
        titletext.GetComponent<Fade>().fadeOut();
        taptext.GetComponent<Fade>().fadeOut();
    }

    TitleState state;
    // Use this for initialization
    void Start()
    {
        state = TitleState.INITIAL;
        titletext = GameObject.Find("TitleText");
        instructionstext = GameObject.Find("InstructionText");
        taptext = GameObject.Find("StartGameText");
    }

    // Update is called once per frame
    void Update()
    {
        if (state == TitleState.INITIAL)
        {
            StartCoroutine(timing());
            titletext.GetComponent<Fade>().show(false);
            gameObject.GetComponent<Fade>().show(false);
            instructionstext.GetComponent<Fade>().show(false);
            taptext.GetComponent<Fade>().show(false);
            state = TitleState.INSTRUCTIONSIN;
            gameObject.GetComponent<Fade>().fadeIn();
            titletext.GetComponent<Fade>().fadeIn();
        } else if (state == TitleState.INSTRUCTIONSIN && gameObject.GetComponent<Fade>().state == Fade.FadeState.IN) {
            state = TitleState.INSTRUCTIONS;
            instructionstext.GetComponent<Fade>().fadeIn();
        } else if (state == TitleState.INSTRUCTIONSOUTTRIGGER) {
            state = TitleState.INSTRUCTIONSOUT;
            instructionstext.GetComponent<Fade>().fadeOut();
        } else if (state == TitleState.INSTRUCTIONSOUT && instructionstext.GetComponent<Fade>().state == Fade.FadeState.OUT)
        {
            state = TitleState.TAPIN;
            taptext.transform.Translate(new Vector3(0, 0.005f, 0));
            taptext.GetComponent<Fade>().fadeIn();
        }
    }
}
