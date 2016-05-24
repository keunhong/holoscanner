using UnityEngine;
using UnityEditor;
using System.Collections;

namespace DeerCat
{
	[CustomEditor(typeof(ParticleScaler))]
	public class ParticleScalerEditor : Editor
	{
		SerializedProperty scaleProp;

		private ParticleScaler particleScaler;

		void OnEnable()
		{
			particleScaler = target as ParticleScaler;
			scaleProp = serializedObject.FindProperty("scale");
		}

		public override void OnInspectorGUI()
		{
			serializedObject.Update();

			float prevScale = scaleProp.floatValue;
			EditorGUILayout.PropertyField(scaleProp);

			scaleProp.floatValue = Mathf.Max(0.01f, scaleProp.floatValue);
			if (scaleProp.floatValue != prevScale)
			{
				float scaleFactor = scaleProp.floatValue / prevScale;
				RescaleParticles(particleScaler.gameObject, scaleFactor);
			}

			serializedObject.ApplyModifiedProperties();
		}

		private void RescaleParticles(GameObject go, float factor)
		{
			ParticleSystem[] particleSystems = go.GetComponentsInChildren<ParticleSystem>();
			for (int i = 0; i < particleSystems.Length; ++i)
				RescaleParticles(particleSystems[i], factor);
		}

		private void RescaleParticles(ParticleSystem particleSystem, float factor)
		{
			Undo.RecordObject(particleSystem, "Scale Particles");

			// the public ParticleSystem api doesn't expose all the parameters that we need to change when scaling the particle system, 
			// so we need to go direct into the serialized object and poke the properties there.
			SerializedObject system = new SerializedObject(particleSystem);

			system.FindProperty("InitialModule.startSize.scalar").floatValue *= factor;
			system.FindProperty("InitialModule.startSpeed.scalar").floatValue *= factor;
			system.FindProperty("InitialModule.gravityModifier").floatValue *= factor;
			system.FindProperty("ShapeModule.radius").floatValue *= factor;
			system.FindProperty("ShapeModule.boxX").floatValue *= factor;
			system.FindProperty("ShapeModule.boxY").floatValue *= factor;
			system.FindProperty("ShapeModule.boxZ").floatValue *= factor;
			system.FindProperty("VelocityModule.x.scalar").floatValue *= factor;
			system.FindProperty("VelocityModule.y.scalar").floatValue *= factor;
			system.FindProperty("VelocityModule.z.scalar").floatValue *= factor;
			system.FindProperty("ClampVelocityModule.x.scalar").floatValue *= factor;
			system.FindProperty("ClampVelocityModule.y.scalar").floatValue *= factor;
			system.FindProperty("ClampVelocityModule.z.scalar").floatValue *= factor;
			system.FindProperty("ForceModule.x.scalar").floatValue *= factor;
			system.FindProperty("ForceModule.y.scalar").floatValue *= factor;
			system.FindProperty("ForceModule.z.scalar").floatValue *= factor;
			system.FindProperty("SizeBySpeedModule.range").vector2Value *= factor;
			system.FindProperty("RotationBySpeedModule.range").vector2Value *= factor;
			system.FindProperty("ColorBySpeedModule.range").vector2Value *= factor;
			
			system.ApplyModifiedProperties();

			ParticleTurbulence turbulence = particleSystem.GetComponent<ParticleTurbulence>();
			if (turbulence != null)
			{
				Undo.RecordObject(turbulence, "Scale Particles");
				SerializedObject turb = new SerializedObject(turbulence);
				turb.FindProperty("amplitude").floatValue *= factor;
				turb.FindProperty("frequency").floatValue /= factor;
				turb.ApplyModifiedProperties();
			}
		}
	}
}
