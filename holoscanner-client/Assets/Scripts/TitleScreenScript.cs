using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class TitleScreenScript : MonoBehaviour
{
    GameObject titletext, instructionstext, waitingtext;
    IEnumerator timingcoroutine;
    string[] instructions =
    {
        "Achieve Zen by finding the orbs\nbefore the other players",
        "Let sound guide you along your journey",
        "Air tap orb to start game"
    };
    int instructionindex = 0;
    enum TitleState
    {
        INITIAL,                   // Just started
        SCREENIN,                  // fading in screen
        SCREEN,                    // faded in screen
        INSTRUCTIONSIN,            // fading in text for instructionindex
        INSTRUCTIONS,              // faded in text, waiting
        INSTRUCTIONSOUTTRIGGER,    // fading out text for instructionindex
        INSTRUCTIONSOUT,           // done fading out text for instructionindex
        WAITTRIGGERED,             // start final fadeout of text for waiting text
        WAITOUT,                   // fading out text for waiting text
        WAITIN,                    // fading in waiting text
        WAIT,                      // faded in waiting text
        GAMESTART,
    };

    IEnumerator timing()
    {
        for (; instructionindex < instructions.Length-1; instructionindex++)
        {
            yield return new WaitForSeconds(5.0f);
            state = TitleState.INSTRUCTIONSOUTTRIGGER;
        }
    }
    public void waitingForPlayers()
    {
        state = TitleState.WAITTRIGGERED;
    }

    public void gameStarted()
    {
        state = TitleState.GAMESTART;
        StopCoroutine(timingcoroutine);
        titletext.GetComponent<Fade>().startcolor = Color.black;
        instructionstext.GetComponent<Fade>().startcolor = Color.black;
        waitingtext.GetComponent<Fade>().startcolor = Color.black;
        titletext.GetComponent<Fade>().endcolor = titletext.GetComponent<Fade>().getCurrentColor();
        instructionstext.GetComponent<Fade>().endcolor = instructionstext.GetComponent<Fade>().getCurrentColor();
        waitingtext.GetComponent<Fade>().endcolor = waitingtext.GetComponent<Fade>().getCurrentColor();
        titletext.GetComponent<Fade>().show(true);
        instructionstext.GetComponent<Fade>().show(true);
        waitingtext.GetComponent<Fade>().show(true);
        gameObject.GetComponent<Fade>().fadeOut();
        titletext.GetComponent<Fade>().fadeOut();
        instructionstext.GetComponent<Fade>().fadeOut();
        waitingtext.GetComponent<Fade>().fadeOut();
    }

    TitleState state;
    // Use this for initialization
    void Start()
    {
        state = TitleState.INITIAL;
        titletext = GameObject.Find("TitleText");
        instructionstext = GameObject.Find("InstructionText");
        waitingtext = GameObject.Find("WaitingText");
    }

    // Update is called once per frame
    void Update()
    {
        if (state == TitleState.INITIAL)
        {
            titletext.GetComponent<Fade>().show(false);
            gameObject.GetComponent<Fade>().show(false);
            instructionstext.GetComponent<Fade>().show(false);
            waitingtext.GetComponent<Fade>().show(false);
            state = TitleState.SCREENIN;
            gameObject.GetComponent<Fade>().fadeIn();
            titletext.GetComponent<Fade>().fadeIn();
        }
        else if (state == TitleState.SCREENIN && gameObject.GetComponent<Fade>().state == Fade.FadeState.IN)
        {
            instructionstext.GetComponent<TextMesh>().text = instructions[instructionindex];
            instructionstext.GetComponent<Fade>().fadeIn();
            timingcoroutine = timing();
            StartCoroutine(timingcoroutine);
            state = TitleState.INSTRUCTIONSIN;
        }
        else if (state == TitleState.INSTRUCTIONSIN && instructionstext.GetComponent<Fade>().state == Fade.FadeState.IN)
        {
            // wait
            state = TitleState.INSTRUCTIONS;
        } else if (state == TitleState.INSTRUCTIONSOUTTRIGGER)
        {
            instructionstext.GetComponent<Fade>().fadeOut();
            state = TitleState.INSTRUCTIONSOUT;
        }
        else if (state == TitleState.INSTRUCTIONSOUT && instructionstext.GetComponent<Fade>().state == Fade.FadeState.OUT)
        {
            instructionstext.GetComponent<TextMesh>().text = instructions[instructionindex];
            instructionstext.GetComponent<Fade>().fadeIn();
            state = TitleState.INSTRUCTIONSIN;
        } else if (state == TitleState.WAITTRIGGERED)
        {
            instructionstext.GetComponent<Fade>().fadeOut();
            state = TitleState.WAITOUT;
        }
        else if (state == TitleState.WAITOUT && instructionstext.GetComponent<Fade>().state == Fade.FadeState.OUT)
        {
            state = TitleState.WAITIN;
            waitingtext.transform.Translate(new Vector3(0, 0.01f, 0));
            waitingtext.GetComponent<Fade>().fadeIn();
        }
    }
}
