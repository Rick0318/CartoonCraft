#version 120
// CartoonCraft Shader - Post-Process Composite
varying vec2 texCoord;

uniform sampler2D gcolor;
uniform sampler2D gdepth;
uniform sampler2D gnormal;
uniform float viewWidth;
uniform float viewHeight;

// FXAA ligero
vec3 fxaa(sampler2D tex, vec2 uv) {
    vec2 pixel = 1.0 / vec2(viewWidth, viewHeight);
    vec3 c  = texture2D(tex, uv).rgb;
    vec3 n  = texture2D(tex, uv + vec2(0, pixel.y)).rgb;
    vec3 s  = texture2D(tex, uv - vec2(0, pixel.y)).rgb;
    vec3 e  = texture2D(tex, uv + vec2(pixel.x, 0)).rgb;
    vec3 w  = texture2D(tex, uv - vec2(pixel.x, 0)).rgb;
    float lc = dot(c, vec3(0.299,0.587,0.114));
    float ln = dot(n, vec3(0.299,0.587,0.114));
    float ls = dot(s, vec3(0.299,0.587,0.114));
    float le = dot(e, vec3(0.299,0.587,0.114));
    float lw = dot(w, vec3(0.299,0.587,0.114));
    float range = max(max(max(max(lc,ln),ls),le),lw)
                - min(min(min(min(lc,ln),ls),le),lw);
    if (range < 0.05) return c;
    return (c+n+s+e+w) / 5.0;
}

// Vignette cartoon
float vignette(vec2 uv) {
    vec2 d = uv - 0.5;
    return 1.0 - dot(d,d) * 1.2;
}

void main() {
    vec3 color = fxaa(gcolor, texCoord);

    // Saturaci?n cartoon en post
    float lum = dot(color, vec3(0.299,0.587,0.114));
    color = mix(vec3(lum), color, 1.18);

    // Leve vignette
    color *= vignette(texCoord);
    color  = clamp(color, 0.0, 1.0);

    // Gamma
    color = pow(color, vec3(1.0/2.1));

    gl_FragColor = vec4(color, 1.0);
}
