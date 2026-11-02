#version 120
varying vec4 vColor;
uniform float rainStrength;

void main() {
    // Cielo cartoon: gradiente azul intenso
    vec3 zenith  = vec3(0.25, 0.55, 1.00);
    vec3 horizon = vec3(0.70, 0.88, 1.00);
    float t = clamp(vColor.g * 1.4, 0.0, 1.0);
    vec3 sky = mix(horizon, zenith, t);

    // Lluvia gris cartoon
    sky = mix(sky, vec3(0.60, 0.65, 0.72), rainStrength * 0.6);

    // Quantize suave (toon sky)
    sky = floor(sky * 8.0) / 8.0;

    gl_FragColor = vec4(sky, 1.0);
}
