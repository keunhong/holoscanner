using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class EndgameScript : MonoBehaviour
{
    GameObject instructionstext;
    IEnumerator timingcoroutine;
    string[] instructions =
    {
        "The journey is over, \nbut we have a secret to share...",
        "This game was a ruse, \na cunning affair.",
        "The orbs you found\n were deliberately placed...","...to move you around\n and scan the space.",
        "Now take a look around\n at what you've scanned!"
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
        for (; instructionindex < instructions.Length; instructionindex++)
        {
            yield return new WaitForSeconds(5.0f);
            state = TitleState.INSTRUCTIONSOUTTRIGGER;
        }
        state = TitleState.WAITTRIGGERED;
    }

    public void endGame()
    {
        state = TitleState.INITIAL;
        GetComponent<AudioSource>().Play();
    }

    TitleState state;
    // Use this for initialization
    void Start()
    {
        state = TitleState.GAMESTART;
        instructionstext = GameObject.Find("EndText");
    }

    IEnumerator activateMeshes()
    {
        yield return new WaitForSecondsRealtime(1);
        GameObject.Find("SpatialMapping").GetComponent<HoloToolkit.Unity.SpatialMappingManager>().ShowMeshes();
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
            gameObject.GetComponent<HoloToolkit.Unity.Billboard>().enabled = false;
            gameObject.GetComponent<HoloToolkit.Unity.SimpleTagalong>().enabled = false;
            state = TitleState.WAITOUT;
            StartCoroutine(activateMeshes());
        }
    }
}
