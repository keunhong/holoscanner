using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.Reflection;

public static class CopyClass
{
    public static T AddComponent<T>(this GameObject go, T toAdd) where T : Component
    {
        return go.AddComponent<T>().GetCopyOf(toAdd) as T;
    }
    public static T GetCopyOf<T>(this Component comp, T other) where T : Component
    {
        System.Type type = comp.GetType();
        if (type != other.GetType()) return null; // type mis-match
        BindingFlags flags = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.DeclaredOnly;
        IEnumerable<PropertyInfo> pinfos = type.GetProperties(flags);
        foreach (var pinfo in pinfos)
        {
            if (pinfo.CanWrite)
            {
                try
                {
                    pinfo.SetValue(comp, pinfo.GetValue(other, null), null);
                }
                catch { } // In case of NotImplementedException being thrown. For some reason specifying that exception didn't seem to catch it, so I didn't catch anything specific.
            }
        }
        IEnumerable<FieldInfo> finfos = type.GetFields(flags);
        foreach (var finfo in finfos)
        {
            finfo.SetValue(comp, finfo.GetValue(other));
        }
        return comp as T;
    }
}

public class RandomNote : MonoBehaviour {
    List<AudioSource> audio;
    int idx;
    int maxidx;
    System.Random rng;
    public bool playSound = true;
    public float speed = 3.0f;
    int sourceid = 0;
    int numcomponents = 8;
    bool offbeat = false;

    // Use this for initialization
    void Start () {
        maxidx = 10;
        idx = 3;
        for (int i = 1; i < numcomponents; i++)
        {
            AudioSource audiosource = GetComponent<AudioSource>();
            gameObject.AddComponent<AudioSource>(audiosource);
        }
        audio = new List<AudioSource>();
        GetComponents<AudioSource>(audio);
        rng = new System.Random();
        StartCoroutine(outputSound());
	}
	
    IEnumerator outputSound()
    {
        float cliplength = 2.4f;
        while (true)
        {
            if (!playSound) yield return null;
            foreach (AudioSource asource in audio) asource.enabled = true;
            
            double t0 = AudioSettings.dspTime + 0.05f;
            audio[sourceid].time = idx * cliplength;
            audio[sourceid].PlayScheduled(t0);
            audio[sourceid].SetScheduledEndTime(t0 + cliplength);
            int tidx = idx;
            do
            {
                int r = (rng.Next() % 4) - 2;
                if (r >= 0) r++;
                tidx = idx + r;
            } while (tidx < 0 || tidx >= maxidx);
            idx = tidx;
            sourceid = (sourceid+1)%numcomponents;
            if (rng.Next() % 2 == 0 || offbeat)
            {
                offbeat = !offbeat;
                yield return new WaitForSeconds(cliplength / (2*speed));
            }
            else {
                yield return new WaitForSeconds(cliplength / speed);
            }
        }
    }
	// Update is called once per frame
	void Update () {

	}
}
