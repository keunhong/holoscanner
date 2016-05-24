Shader "FantasyParticles/SimpleDistortAdditive" {

	Properties {
		_MainTex ("Main Texture", 2D) = "white" {}
		_NoiseTex ("Distortion", 2D) = "white" {}
		_Color ("Color", Color) = (1,1,1,1)
		_DistortionScale("Distortion Scale", Range(0,2)) = 1
		_DistortionAmount("Distortion Amount", Range(0,0.5)) = 0.1
		_DistortionScrollX("Distortion Scroll X", float) = 0
		_DistortionScrollY("Distortion Scroll Y", float) = 0
		_InvFade ("Soft Particles Factor", Range(0.01,3.0)) = 1.0
	}
	
	SubShader {
	Tags { "Queue"="Transparent" "IgnoreProjector"="True" "RenderType"="Transparent" }

	ZWrite Off
	Cull Off 
	Lighting Off
	Blend SrcAlpha One

	Pass {
		CGPROGRAM

		#pragma vertex vert
		#pragma fragment frag
		#pragma multi_compile_particles

		#include "UnityCG.cginc"

		sampler2D _MainTex;
		sampler2D _NoiseTex;
		half4 _Color;
		half _DistortionScale;
		half _DistortionAmount;
		half _DistortionScrollX;
		half _DistortionScrollY;

		// for soft particles
		sampler2D_float _CameraDepthTexture;
		float _InvFade;

		struct vertexInput {
			float4 vertex : POSITION;
			fixed4 color  : COLOR;
			float2 uv : TEXCOORD0;
		};

		struct fragmentInput {
			float4 vertex : SV_POSITION;
			fixed4 color  : COLOR;
			float2 mainUV : TEXCOORD0;
			float2 noiseUV : TEXCOORD1;
			#ifdef SOFTPARTICLES_ON
				float4 projPos : TEXCOORD2;
			#endif
		};

		fragmentInput vert(vertexInput v)
		{
			fragmentInput o;
			o.vertex = mul (UNITY_MATRIX_MVP, v.vertex);
			
			o.mainUV = v.uv;
			o.noiseUV = (v.uv + float2(_DistortionScrollX, _DistortionScrollY) * _Time.y) * _DistortionScale;	
			o.color = v.color * _Color;

			#ifdef SOFTPARTICLES_ON
				o.projPos = ComputeScreenPos (o.vertex);
				COMPUTE_EYEDEPTH(o.projPos.z);
			#endif

			return o;
		}

		half4 frag(fragmentInput i) : SV_Target 
		{
			half2 noise = 2.0 * tex2D(_NoiseTex, i.noiseUV).xy - 1;
			
			half2 offset = noise * _DistortionAmount;
			half4 col = tex2D(_MainTex, i.mainUV + offset);

			#ifdef SOFTPARTICLES_ON
				float sceneZ = LinearEyeDepth (SAMPLE_DEPTH_TEXTURE_PROJ(_CameraDepthTexture, UNITY_PROJ_COORD(i.projPos)));
				float partZ = i.projPos.z;
				float fade = saturate (_InvFade * (sceneZ-partZ));
				i.color.a *= fade;
			#endif

			return col * i.color;
		}	        

		ENDCG

		}
    }
}
