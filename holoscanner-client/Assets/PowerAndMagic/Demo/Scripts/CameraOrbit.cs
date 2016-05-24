using UnityEngine;
using System.Collections;

namespace DeerCat
{
	/// <summary>
	/// Simple orbiting camera class for Demo
	/// </summary>
	public class CameraOrbit : MonoBehaviour
	{
		public float distance = 10.0f;

		private float speed = 10.0f;

		private float yMinLimit = -20f;
		private float yMaxLimit = 80f;

		private float distanceMin = 5f;
		private float distanceMax = 15f;

		private float x = 0.0f;
		private float y = 0.0f;

		void Start()
		{
			Vector3 angles = transform.eulerAngles;
			x = angles.y;
			y = angles.x;
		}

		void LateUpdate()
		{
			if (Input.GetMouseButton(0))
			{
				x += Input.GetAxis("Mouse X") * speed;
				y -= Input.GetAxis("Mouse Y") * speed;

				y = ClampAngle(y, yMinLimit, yMaxLimit);

				Quaternion rotation = Quaternion.Euler(y, x, 0);

				distance = Mathf.Clamp(distance - Input.GetAxis("Mouse ScrollWheel") * 5, distanceMin, distanceMax);

				Vector3 offset = Vector3.back * distance;
				Vector3 position = rotation * offset;

				transform.rotation = rotation;
				transform.position = position;
			}
		}

		public static float ClampAngle(float angle, float min, float max)
		{
			if (angle < -360)
				angle += 360;
			if (angle > 360)
				angle -= 360;
			return Mathf.Clamp(angle, min, max);
		}
	}
}
