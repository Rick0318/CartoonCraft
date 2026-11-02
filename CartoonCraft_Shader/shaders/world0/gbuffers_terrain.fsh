#version 120
// CartoonCraft Shader - Terrain Fragment (Cel Shading)
varying vec3 vNormal;
varying vec2 vTexCoord;
varying vec4 vColor;
varying float vFogDist;
varying vec3 vWorldPos;

uniform sampler2D texture;
uniform sampler2D lightmap;
uniform vec3 sunPosition;
uniform float frameTimeCounter;

// -- Cel shading: cuantiza la luz en N bandas --
float celShade(float diff, int bands) {
    float step = 1.0 / float(bands);
    return floor(diff / step) * step + step * 0.5;
}

void main() {
    vec4 albedo = texture2D(texture, vTexCoord) * vColor;
    if (albedo.a < 0.1) discard;

    // Boost saturation cartoon
    float lum = dot(albedo.rgb, vec3(0.299, 0.587, 0.114));
    albedo.rgb = mix(vec3(lum), albedo.rgb, 1.30);

    // Diffuse lighting
    vec3 lightDir = normalize(sunPosition);
    float diff = max(dot(vNormal, lightDir), 0.0);

    // Cel-shade en 4 bandas
    float cel = celShade(diff, 4);

    // Ambient + diffuse cartoon
    vec3 ambient = albedo.rgb * 0.40;
    vec3 diffuse = albedo.rgb * cel * 0.75;
    vec3 color   = ambient + diffuse;

    // Outline: si el normal apunta casi perpendicular a la camara -> oscurecer
    vec3 viewDir = normalize(-vec3(0.0,0.0,1.0)); // approx
    float rim    = 1.0 - max(dot(vNormal, viewDir), 0.0);
    float outline = step(0.85, rim) * 0.5;
    color = color * (1.0 - outline);

    // Contrast ligero
    color = (color - 0.5) * 1.08 + 0.5;
    color = clamp(color, 0.0, 1.0);

    // Niebla cartoon (borde suave)
    float fogStart = 60.0;
    float fogEnd   = 120.0;
    float fogFactor = clamp((vFogDist - fogStart)/(fogEnd - fogStart), 0.0, 1.0);
    vec3 fogColor = vec3(0.70, 0.85, 1.0);
    color = mix(color, fogColor, fogFactor * fogFactor);

    gl_FragData[0] = vec4(color, albedo.a);
    gl_FragData[1] = vec4(0.0, 0.0, 0.0, 1.0); // specular (apagado - estilo cartoon)
    gl_FragData[2] = vec4(vNormal * 0.5 + 0.5, 1.0);
}
