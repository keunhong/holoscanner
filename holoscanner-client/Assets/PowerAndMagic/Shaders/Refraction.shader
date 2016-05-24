Shader "FantasyParticles/Refraction" {	
	Properties {
		_Dist("Distortion amount", Float) = 10.0
		_DistortTex("Distortion map", 2D) = "" {}
		_Brighten("Brighten", Range(0,4)) = 0
	}

	Category {
		
		Tags { "Queue"="Overlay" "RenderType"="Transparent" }

		Cull Off 
		Lighting Off 
		ZWrite Off 
		Fog { Color (0,0,0,0) }
		ZTest LEqual

		SubShader {

			GrabPass {
				Name "BASE"
				Tags { "LightMode" = "Always" }
			}

			Pass {
			
			Name "BASE"
			Tags { "LightMode" = "Always" }
			Blend SrcAlpha OneMinusSrcAlpha

			CGPROGRAM
			#pragma vertex vert
			#pragma fragment frag
			#pragma fragmentoption ARB_precision_hint_fastest
			#pragma multi_compile_particles
			#include "UnityCG.cginc"

			sampler2D _DistortTex;
			half _Dist;
			half _Brighten;
			
			sampler2D _GrabTexture;
			float4 _GrabTexture_TexelSize;

			struct appdata_t {
				float4 vertex : POSITION;
				fixed4 color  : COLOR;
				float2 uv     : TEXCOORD0;
			};

			struct v2f {
				float4 vertex : POSITION;
				fixed4 color  : COLOR;
				float4 screenUV : TEXCOORD0;
				float2 texUV : TEXCOORD1;
			};

			
			v2f vert (appdata_t v) 
			{
				v2f o;

				o.vertex = mul(UNITY_MATRIX_MVP, v.vertex);
				o.screenUV = ComputeGrabScreenPos(o.vertex);
				o.texUV = v.uv;
				o.color = v.color;

				return o;
			}

			half4 frag(v2f i) : COLOR
			{	
				half2 bump = 2.0 * tex2D(_DistortTex, i.texUV).rg - 1.0;
				bump.y = -bump.y;
				
				// alpha channel of vertex color scales the amount of distortion
				half2 bumpAmount = i.color.a *  bump;
				half2 offset = bumpAmount * _Dist * _GrabTexture_TexelSize.xy;
				i.screenUV.xy = offset * 10 + i.screenUV.xy;
		
				half4 col = tex2Dproj(_GrabTexture, i.screenUV);
		
				half3 tint = 1.0 + i.color * _Brighten * dot(bumpAmount.xy, bumpAmount.xy);
				return half4(col.rgb * tint, 1);
			}
			
			ENDCG
			}
		}
	}
}
