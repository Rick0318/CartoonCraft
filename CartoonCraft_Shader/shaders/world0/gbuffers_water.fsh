#version 120
// CartoonCraft Shader - Water (Toon)
varying vec2 vTexCoord;
varying vec4 vColor;
varying float vFogDist;
varying vec3 vNormal;

uniform sampler2D texture;
uniform float frameTimeCounter;

void main() {
    vec4 albedo = texture2D(texture, vTexCoord) * vColor;

    // Color agua cartoon
    vec3 waterColor = vec3(0.15, 0.55, 0.90);
    float alpha = 0.72;

    // Brillo animado
    float wave = sin(vTexCoord.x * 8.0 + frameTimeCounter * 2.5) *
                 cos(vTexCoord.y * 8.0 + frameTimeCounter * 2.0);
    wave = wave * 0.5 + 0.5;
    float highlight = step(0.75, wave) * 0.35;

    vec3 color = waterColor + highlight;
    color = clamp(color, 0.0, 1.0);

    float fogFactor = clamp((vFogDist - 60.0) / 60.0, 0.0, 1.0);
    color = mix(color, vec3(0.70, 0.85, 1.0), fogFactor * fogFactor);

    gl_FragColor = vec4(color, alpha);
}
