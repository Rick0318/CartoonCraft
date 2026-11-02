#version 120
uniform sampler2D texture;
void main() {
    vec4 c = texture2D(texture, gl_TexCoord[0].xy);
    if (c.a < 0.5) discard;
    gl_FragColor = c;
}
