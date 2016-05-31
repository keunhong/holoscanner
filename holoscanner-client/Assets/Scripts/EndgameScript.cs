﻿using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class EndgameScript : MonoBehaviour
{
    GameObject instructionstext;
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
        for (; instructionindex < instructions.Length - 1; instructionindex++)
        {
            yield return new WaitForSeconds(5.0f);
            state = TitleState.INSTRUCTIONSOUTTRIGGER;
        }
        state = TitleState.WAITTRIGGERED;
    }

    public void endGame()
    {
        state = TitleState.INITIAL;
    }

    TitleState state;
    // Use this for initialization
    void Start()
    {
        state = TitleState.GAMESTART;
        instructionstext = GameObject.Find("InstructionText");
    }

    // Update is called once per frame
    void Update()
    {
        if (state == TitleState.GAMESTART)
        {
            gameObject.GetComponent<Fade>().show(false);
            instructionstext.GetComponent<Fade>().show(false);
            state = TitleState.WAIT;
        }
        else if (state == TitleState.INITIAL)
        {
            state = TitleState.SCREENIN;
            gameObject.GetComponent<Fade>().fadeIn();
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
        }
        else if (state == TitleState.INSTRUCTIONSOUTTRIGGER)
        {
            instructionstext.GetComponent<Fade>().fadeOut();
            state = TitleState.INSTRUCTIONSOUT;
        }
        else if (state == TitleState.INSTRUCTIONSOUT && instructionstext.GetComponent<Fade>().state == Fade.FadeState.OUT)
        {
            instructionstext.GetComponent<TextMesh>().text = instructions[instructionindex];
            instructionstext.GetComponent<Fade>().fadeIn();
            state = TitleState.INSTRUCTIONSIN;
        }
        else if (state == TitleState.WAITTRIGGERED)
        {
            // TODO: Fix location
            state = TitleState.WAITOUT;
        }
    }
}
