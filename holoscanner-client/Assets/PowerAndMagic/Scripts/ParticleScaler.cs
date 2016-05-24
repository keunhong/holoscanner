using UnityEngine;
using System.Collections;

namespace DeerCat
{
	public class ParticleScaler : MonoBehaviour
	{
		// functionality is all within the editor script.
		[Range(0.01f, 10.0f)]
		public float scale = 1.0f;
	}
}
