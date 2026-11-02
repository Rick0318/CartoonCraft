#version 120
// CartoonCraft Shader - Terrain Vertex
attribute vec4 mc_Entity;
attribute vec2 mc_midTexCoord;

varying vec3 vNormal;
varying vec2 vTexCoord;
varying vec4 vColor;
varying float vFogDist;
varying vec3 vWorldPos;

uniform mat4 gbufferModelView;
uniform mat4 gbufferModelViewInverse;
uniform mat4 gbufferProjection;
uniform vec3 cameraPosition;
uniform float frameTimeCounter;

void main() {
    vTexCoord = (gl_TextureMatrix[0] * gl_MultiTexCoord0).xy;
    vColor    = gl_Color;
    vNormal   = normalize(gl_NormalMatrix * gl_Normal);

    vec4 worldPos = gbufferModelViewInverse * (gl_ModelViewMatrix * gl_Vertex);
    vWorldPos = worldPos.xyz + cameraPosition;

    // Waving leaves & water (entity 10011 = leaves, 10012 = water)
    vec4 pos = gl_Vertex;
    float entityId = mc_Entity.x;
    if (entityId == 10011.0 || entityId == 10012.0) {
        float wave = sin(frameTimeCounter * 2.0 + vWorldPos.x * 0.8 + vWorldPos.z * 0.8) * 0.03;
        pos.y += wave;
        pos.x += wave * 0.5;
    }

    gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * pos;
    vFogDist    = length((gl_ModelViewMatrix * pos).xyz);
}
