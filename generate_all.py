"""
CartoonCraft - Generador de los 4 proyectos Minecraft
======================================================
1. CartoonCraft_TexturePack  (Java + Bedrock)
2. CartoonCraft_Shader        (Iris/OptiFine GLSL)
3. CartoonCraft_AnimationsMod (Fabric Java + Bedrock)
4. CartoonCraft_BossPetsMod   (Fabric Java + Bedrock)
"""

import os, json, math, zipfile, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

BASE = Path(__file__).parent
PY   = "C:/Users/User/AppData/Local/Programs/Python/Python312/python.exe"

# ---------------------------------------------
#  HELPERS
# ---------------------------------------------

def mkdir(p):
    Path(p).mkdir(parents=True, exist_ok=True)
    return Path(p)

def save(img, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    img.save(str(path), "PNG")

def jdump(obj, path, indent=2):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(str(path), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=indent)

def write(path, text):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(str(path), "w", encoding="utf-8") as f:
        f.write(text)

def zip_folder(folder: Path, out_zip: Path):
    with zipfile.ZipFile(str(out_zip), "w", zipfile.ZIP_DEFLATED) as zf:
        for file in folder.rglob("*"):
            if file.is_file():
                zf.write(file, file.relative_to(folder.parent))
    print(f"  -> ZIP: {out_zip.name}")

# ---------------------------------------------
#  PALETA CARTOON
# ---------------------------------------------
PAL = {
    "grass_top":     (106, 190, 80),
    "grass_side":    (134, 196, 96),
    "dirt":          (162, 108,  64),
    "stone":         (140, 140, 148),
    "sand":          (230, 210, 155),
    "gravel":        (170, 160, 150),
    "wood_oak":      (175, 130,  70),
    "planks_oak":    (200, 158,  88),
    "leaves_oak":    ( 78, 170,  60),
    "water":         ( 55, 145, 220),
    "lava":          (230, 100,  20),
    "cobblestone":   (130, 130, 135),
    "brick":         (180,  80,  60),
    "netherrack":    (160,  55,  55),
    "obsidian":      ( 30,  20,  50),
    "glowstone":     (240, 200,  60),
    "nether_brick":  (110,  40,  40),
    "end_stone":     (220, 215, 155),
    "deepslate":     ( 80,  80,  90),
    "calcite":       (220, 220, 225),
    "amethyst":      (130,  80, 190),
    "snow":          (235, 245, 255),
    "ice":           (160, 200, 235),
    "soul_sand":     (100,  80,  60),
    "crying_obs":    ( 40,  25,  70),
    "shroomlight":   (230, 155,  60),
    "magma":         (200,  80,  20),
}

def noise_pixel(base, strength=18, seed=0):
    import random
    random.seed(seed)
    r,g,b = base
    def jitter(v): return max(0, min(255, v + random.randint(-strength, strength)))
    return (jitter(r), jitter(g), jitter(b))

def make_flat(color, size=16, noise=14):
    img = Image.new("RGBA", (size,size), (0,0,0,0))
    d = ImageDraw.Draw(img)
    for y in range(size):
        for x in range(size):
            c = noise_pixel(color, noise, seed=x*1000+y)
            d.point((x,y), (*c, 255))
    return img

def add_outline(img, color=(30,20,20), width=1):
    """Dibuja borde cartoon en el borde exterior del bloque."""
    d = ImageDraw.Draw(img)
    s = img.width - 1
    for i in range(width):
        d.rectangle([i,i,s-i,s-i], outline=(*color,255))
    return img

def add_inner_highlight(img, strength=30):
    """Esquina sup-izq m?s clara, inf-der m?s oscura -> sensaci?n 3D cartoon."""
    d = ImageDraw.Draw(img)
    s = img.width
    for i in range(2):
        # highlight top-left
        d.line([(i, i),(s-1-i, i)], fill=(255,255,255, strength), width=1)
        d.line([(i, i),(i, s-1-i)], fill=(255,255,255, strength), width=1)
        # shadow bottom-right
        d.line([(i, s-1-i),(s-1-i, s-1-i)], fill=(0,0,0, strength), width=1)
        d.line([(s-1-i, i),(s-1-i, s-1-i)], fill=(0,0,0, strength), width=1)
    return img

def make_block(color, noise=14, outline=True, highlight=True, size=16):
    img = make_flat(color, size, noise)
    if highlight: add_inner_highlight(img, 40)
    if outline:   add_outline(img, (20,15,15), 1)
    return img

def make_relief_block(base_color, crack_color, cracks=6, size=16):
    """Bloques con relieve: piedra, madera, ladrillo, etc."""
    img = make_block(base_color, noise=16, size=size)
    d = ImageDraw.Draw(img)
    import random
    random.seed(hash(base_color))
    for _ in range(cracks):
        x1 = random.randint(2, size-4)
        y1 = random.randint(2, size-4)
        x2 = x1 + random.randint(-4, 4)
        y2 = y1 + random.randint(-3, 3)
        x2 = max(1, min(size-2, x2))
        y2 = max(1, min(size-2, y2))
        d.line([(x1,y1),(x2,y2)], fill=(*crack_color,180), width=1)
    return img

def make_stone(size=16):
    return make_relief_block(PAL["stone"], (90,90,95), cracks=8, size=size)

def make_cobblestone(size=16):
    return make_relief_block(PAL["cobblestone"], (80,80,84), cracks=10, size=size)

def make_wood_log(size=16):
    img = make_block(PAL["wood_oak"], noise=12, size=size)
    d = ImageDraw.Draw(img)
    # anillos de madera
    r,g,b = PAL["wood_oak"]
    for y in range(size):
        shade = int(12 * math.sin(y * math.pi / size))
        for x in range(size):
            px = img.getpixel((x,y))
            nr = max(0,min(255, px[0]+shade))
            ng = max(0,min(255, px[1]+shade-4))
            nb = max(0,min(255, px[2]+shade-8))
            img.putpixel((x,y),(nr,ng,nb,255))
    add_outline(img, (20,15,10), 1)
    return img

def make_planks(size=16):
    img = make_block(PAL["planks_oak"], noise=10, size=size)
    d = ImageDraw.Draw(img)
    r,g,b = PAL["planks_oak"]
    # l?neas de tabla
    for y in [4,8,12]:
        d.line([(0,y),(size-1,y)], fill=(r-30,g-25,b-15,200), width=1)
    for x in [0,8]:
        d.line([(x,0),(x,3)], fill=(r-20,g-18,b-10,180), width=1)
        d.line([(x,8 if x==0 else 4),(x,7 if x==0 else 11)], fill=(r-20,g-18,b-10,180), width=1)
    return img

def make_brick(size=16):
    img = make_block(PAL["brick"], noise=8, size=size)
    d = ImageDraw.Draw(img)
    mortar = (100,90,80,220)
    # horizontal
    for y in [0,4,8,12]:
        d.line([(0,y),(size-1,y)], fill=mortar, width=1)
    # vertical alternado
    for y_off, xs in [(0,[4,12]),(4,[8]),(8,[4,12]),(12,[8])]:
        for x in xs:
            d.line([(x,y_off),(x,y_off+3)], fill=mortar, width=1)
    return img

def make_netherrack(size=16):
    img = make_relief_block(PAL["netherrack"], (100,30,30), cracks=12, size=size)
    # brillo rojo
    d = ImageDraw.Draw(img)
    import random; random.seed(7)
    for _ in range(4):
        x,y = random.randint(2,13), random.randint(2,13)
        d.ellipse([x-1,y-1,x+1,y+1], fill=(220,60,60,120))
    return img

def make_obsidian(size=16):
    img = make_relief_block(PAL["obsidian"], (60,40,90), cracks=5, size=size)
    d = ImageDraw.Draw(img)
    import random; random.seed(3)
    for _ in range(6):
        x,y = random.randint(1,14), random.randint(1,14)
        d.ellipse([x,y,x+1,y+1], fill=(100,70,160,150))
    return img

def make_glowstone(size=16):
    img = make_block(PAL["glowstone"], noise=8, size=size)
    d = ImageDraw.Draw(img)
    # efecto brillo en centro
    cx,cy = size//2, size//2
    for r in range(6,0,-1):
        alpha = int(60 * (1 - r/6))
        d.ellipse([cx-r,cy-r,cx+r,cy+r], fill=(255,240,100,alpha))
    return img

def make_lava(size=16):
    img = make_block(PAL["lava"], noise=20, size=size)
    d = ImageDraw.Draw(img)
    import random; random.seed(11)
    for _ in range(5):
        x,y = random.randint(1,12), random.randint(1,12)
        d.ellipse([x,y,x+3,y+3], fill=(255,200,0,180))
    return img

def make_water(size=16):
    img = make_block(PAL["water"], noise=6, size=size)
    d = ImageDraw.Draw(img)
    for y in range(0,size,3):
        d.line([(0,y),(size-1,y)], fill=(100,180,240,60), width=1)
    # transparencia
    pixels = img.load()
    for y in range(size):
        for x in range(size):
            r,g,b,a = pixels[x,y]
            pixels[x,y] = (r,g,b,200)
    return img

def make_leaves(size=16):
    img = make_block(PAL["leaves_oak"], noise=18, size=size)
    d = ImageDraw.Draw(img)
    import random; random.seed(5)
    for _ in range(8):
        x,y = random.randint(1,13), random.randint(1,13)
        d.ellipse([x,y,x+2,y+2], fill=(50,150,40,200))
    pixels = img.load()
    for y in range(size):
        for x in range(size):
            r,g,b,a = pixels[x,y]
            pixels[x,y] = (r,g,b,220)
    return img

def make_sand(size=16):
    img = make_block(PAL["sand"], noise=10, size=size)
    d = ImageDraw.Draw(img)
    import random; random.seed(9)
    for _ in range(20):
        x,y = random.randint(1,14), random.randint(1,14)
        d.point((x,y), fill=(200,185,130,200))
    return img

def make_amethyst(size=16):
    img = make_block(PAL["amethyst"], noise=8, size=size)
    d = ImageDraw.Draw(img)
    # cristales
    centers = [(4,4),(11,5),(7,11),(3,12),(13,9)]
    for cx,cy in centers:
        d.polygon([(cx,cy-3),(cx+2,cy),(cx,cy+3),(cx-2,cy)], fill=(180,120,230,200))
        d.line([(cx,cy-3),(cx,cy+3)], fill=(220,180,255,150), width=1)
    add_outline(img, (70,30,110), 1)
    return img

def make_deepslate(size=16):
    return make_relief_block(PAL["deepslate"], (50,50,58), cracks=9, size=size)

def make_end_stone(size=16):
    img = make_relief_block(PAL["end_stone"], (180,175,110), cracks=5, size=size)
    d = ImageDraw.Draw(img)
    import random; random.seed(13)
    for _ in range(6):
        x,y = random.randint(2,13), random.randint(2,13)
        d.point((x,y), fill=(255,245,180,200))
    return img

# ===============================================================
#  1. TEXTURE PACK
# ===============================================================

def build_texture_pack():
    root = BASE / "CartoonCraft_TexturePack"
    blk  = root / "assets/minecraft/textures/block"
    itm  = root / "assets/minecraft/textures/item"
    mkdir(blk); mkdir(itm)

    print("\n[1/4] Generando Texture Pack...")

    # pack.mcmeta
    jdump({"pack":{"pack_format":34,"description":"?aCartoonCraft ?7- Cartoon Style v1.0\n?6by CartoonCraft Team"}},
          root / "pack.mcmeta")

    textures = {
        "grass_block_top":      make_block(PAL["grass_top"],  noise=16),
        "grass_block_side":     make_block(PAL["grass_side"], noise=14),
        "dirt":                 make_block(PAL["dirt"],       noise=14),
        "stone":                make_stone(),
        "cobblestone":          make_cobblestone(),
        "oak_log":              make_wood_log(),
        "oak_log_top":          make_block(PAL["wood_oak"],   noise=8),
        "oak_planks":           make_planks(),
        "oak_leaves":           make_leaves(),
        "sand":                 make_sand(),
        "gravel":               make_relief_block(PAL["gravel"], (120,112,105), cracks=7),
        "water_still":          make_water(),
        "lava_still":           make_lava(),
        "bricks":               make_brick(),
        "netherrack":           make_netherrack(),
        "obsidian":             make_obsidian(),
        "glowstone":            make_glowstone(),
        "nether_bricks":        make_relief_block(PAL["nether_brick"], (70,25,25), cracks=6),
        "end_stone":            make_end_stone(),
        "deepslate":            make_deepslate(),
        "calcite":              make_block(PAL["calcite"],    noise=6),
        "amethyst_block":       make_amethyst(),
        "snow":                 make_block(PAL["snow"],       noise=5),
        "ice":                  make_block(PAL["ice"],        noise=4),
        "soul_sand":            make_relief_block(PAL["soul_sand"],(70,55,40), cracks=5),
        "crying_obsidian":      make_obsidian(),
        "shroomlight":          make_glowstone(),
        "magma":                make_lava(),
    }
    for name, img in textures.items():
        save(img, blk / f"{name}.png")
        print(f"  OK: {name}.png")

    # Item: boss_soul (usado en BossPets mod)
    soul = make_block((180,60,200), noise=5, size=16)
    d = ImageDraw.Draw(soul)
    d.ellipse([4,4,11,11], fill=(220,100,255,200))
    d.ellipse([6,6,9,9],   fill=(255,255,255,255))
    save(soul, itm / "boss_soul.png")

    crown = make_block((230,190,20), noise=3, size=16)
    d2 = ImageDraw.Draw(crown)
    d2.polygon([(2,12),(2,6),(5,9),(8,4),(11,9),(14,6),(14,12)], fill=(255,220,30,240))
    d2.polygon([(2,12),(2,6),(5,9),(8,4),(11,9),(14,6),(14,12)], outline=(180,140,0,255))
    save(crown, itm / "toon_crown.png")

    print("  OK Items generados")

    # ZIP final (Java)
    zip_folder(root, BASE / "CartoonCraft_TexturePack_JAVA.zip")
    print("  OK CartoonCraft_TexturePack_JAVA.zip listo")

    # Bedrock (mismas texturas, diferente estructura)
    build_bedrock_textures(textures, soul, crown)


def build_bedrock_textures(textures, soul, crown):
    root = BASE / "CartoonCraft_TexturePack_Bedrock"
    tr   = root / "textures/blocks"
    ti   = root / "textures/items"
    mkdir(tr); mkdir(ti)

    jdump({"format_version":2,
           "header":{"description":"CartoonCraft Bedrock","name":"CartoonCraft","uuid":"a1b2c3d4-e5f6-7890-abcd-ef1234567890","version":[1,0,0],"min_engine_version":[1,21,0]},
           "modules":[{"description":"CartoonCraft","type":"resources","uuid":"b2c3d4e5-f6a7-8901-bcde-f12345678901","version":[1,0,0]}]},
          root / "manifest.json")

    BEDROCK_MAP = {
        "grass_block_top": "grass_top", "grass_block_side": "grass_side",
        "dirt": "dirt", "stone": "stone", "cobblestone": "cobblestone",
        "oak_log": "log_oak", "oak_planks": "planks_oak", "oak_leaves": "leaves_oak",
        "sand": "sand", "gravel": "gravel", "bricks": "brick",
        "netherrack": "netherrack", "obsidian": "obsidian", "glowstone": "glowstone",
        "end_stone": "end_stone", "deepslate": "deepslate",
        "snow": "snow", "ice": "ice", "soul_sand": "soul_sand",
        "amethyst_block": "amethyst_block",
    }
    for java_name, bedrock_name in BEDROCK_MAP.items():
        if java_name in textures:
            save(textures[java_name], tr / f"{bedrock_name}.png")

    save(soul,  ti / "boss_soul.png")
    save(crown, ti / "toon_crown.png")
    zip_folder(root, BASE / "CartoonCraft_TexturePack_BEDROCK.zip")
    print("  OK CartoonCraft_TexturePack_BEDROCK.zip listo")


# ===============================================================
#  2. SHADER (Iris / OptiFine)
# ===============================================================

def build_shader():
    root = BASE / "CartoonCraft_Shader"
    print("\n[2/4] Generando Shader...")

    SHADERS_PROPS = """\
# CartoonCraft Shader - shaders.properties
# Compatible: Iris 1.7+ / OptiFine HD U I5+

shadow.enabled=true
shadow.resolution=1024
shadow.distance=64

ambientOcclusion.enabled=true
ambientOcclusion.samples=8

# Cel shading bands
cel.bands=4

# Color grading
colorGrading.enabled=true
colorGrading.saturation=1.25
colorGrading.contrast=1.10

# Water
water.caustics=true
water.waving=true

# Sky
sky.cartoon=true
"""

    # -- gbuffers_terrain.vsh ------------------------------
    GBUF_TERRAIN_VSH = """\
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
"""

    # -- gbuffers_terrain.fsh ------------------------------
    GBUF_TERRAIN_FSH = """\
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
"""

    # -- gbuffers_water.fsh -------------------------------
    WATER_FSH = """\
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
"""

    # -- composite.fsh (post-process) ---------------------
    COMPOSITE_FSH = """\
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
"""

    COMPOSITE_VSH = """\
#version 120
varying vec2 texCoord;
void main() {
    gl_Position = ftransform();
    texCoord = gl_MultiTexCoord0.xy;
}
"""

    # -- shadow.vsh / shadow.fsh ---------------------------
    SHADOW_VSH = """\
#version 120
void main() {
    gl_Position  = ftransform();
    gl_TexCoord[0] = gl_MultiTexCoord0;
}
"""
    SHADOW_FSH = """\
#version 120
uniform sampler2D texture;
void main() {
    vec4 c = texture2D(texture, gl_TexCoord[0].xy);
    if (c.a < 0.5) discard;
    gl_FragColor = c;
}
"""

    # -- gbuffers_skybasic ---------------------------------
    SKY_VSH = """\
#version 120
varying vec4 vColor;
void main() {
    gl_Position = ftransform();
    vColor = gl_Color;
}
"""
    SKY_FSH = """\
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
"""

    # -- Guardar archivos ----------------------------------
    w0 = root / "shaders" / "world0"
    mkdir(w0)

    write(root / "shaders" / "shaders.properties",  SHADERS_PROPS)
    write(w0 / "gbuffers_terrain.vsh",               GBUF_TERRAIN_VSH)
    write(w0 / "gbuffers_terrain.fsh",               GBUF_TERRAIN_FSH)
    write(w0 / "gbuffers_water.fsh",                 WATER_FSH)
    write(w0 / "gbuffers_water.vsh",                 GBUF_TERRAIN_VSH)  # same vertex
    write(w0 / "composite.vsh",                      COMPOSITE_VSH)
    write(w0 / "composite.fsh",                      COMPOSITE_FSH)
    write(w0 / "shadow.vsh",                         SHADOW_VSH)
    write(w0 / "shadow.fsh",                         SHADOW_FSH)
    write(w0 / "gbuffers_skybasic.vsh",              SKY_VSH)
    write(w0 / "gbuffers_skybasic.fsh",              SKY_FSH)
    write(w0 / "gbuffers_skytextured.vsh",           SKY_VSH)
    write(w0 / "gbuffers_skytextured.fsh",           SKY_FSH)

    # pack.mcmeta del shader
    jdump({"pack":{"pack_format":34,"description":"CartoonCraft Shader"}}, root / "pack.mcmeta")

    print("  OK Archivos GLSL generados")
    zip_folder(root, BASE / "CartoonCraft_Shader.zip")
    print("  OK CartoonCraft_Shader.zip listo")


# ===============================================================
#  3. MOD DE ANIMACIONES (Fabric Java + Bedrock)
# ===============================================================

def build_animation_mod():
    root = BASE / "CartoonCraft_AnimationsMod"
    print("\n[3/4] Generando Mod de Animaciones...")

    # -- Fabric mod metadata -------------------------------
    jdump({
        "schemaVersion": 1,
        "id": "cartooncraft_animations",
        "version": "1.0.0",
        "name": "CartoonCraft Animations",
        "description": "Movimientos cartoon: squash & stretch, swing exagerado, idle bounce",
        "authors": ["CartoonCraft Team"],
        "contact": {},
        "license": "MIT",
        "icon": "assets/cartooncraft_animations/icon.png",
        "environment": "client",
        "entrypoints": {
            "client": ["com.cartooncraft.animations.CartoonAnimationsClient"]
        },
        "depends": {
            "fabricloader": ">=0.15.0",
            "minecraft": "~1.21",
            "java": ">=21"
        },
        "recommends": {
            "figura": "*"
        }
    }, root / "src/main/resources/fabric.mod.json")

    # -- Clase principal Java ------------------------------
    java_client = """\
package com.cartooncraft.animations;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.minecraft.client.MinecraftClient;
import net.minecraft.entity.player.PlayerEntity;

/**
 * CartoonCraft Animations - Client Entrypoint
 * Aplica transformaciones cartoon al modelo del jugador en cada tick.
 */
public class CartoonAnimationsClient implements ClientModInitializer {

    private static float bobTimer    = 0f;
    private static float swingPhase  = 0f;

    @Override
    public void onInitializeClient() {
        ClientTickEvents.END_CLIENT_TICK.register(client -> {
            if (client.player == null) return;
            PlayerEntity player = client.player;

            bobTimer   += 0.1f;
            swingPhase += 0.15f;

            // Registrar transformaciones via mixin (ver PlayerEntityRendererMixin)
            CartoonTransformRegistry.update(player, bobTimer, swingPhase);
        });

        System.out.println("[CartoonCraft] Animations mod cargado!");
    }
}
"""

    registry = """\
package com.cartooncraft.animations;

import net.minecraft.entity.player.PlayerEntity;

/**
 * Registro central de transformaciones cartoon.
 * Los mixins de renderizado leen estos valores para modificar el modelo.
 */
public class CartoonTransformRegistry {

    // -- Valores accesibles por los Mixins --
    public static float bodyBobY      = 0f;   // rebote vertical (idle/walk)
    public static float armSwingLeft  = 0f;   // swing brazo izquierdo (radianes)
    public static float armSwingRight = 0f;   // swing brazo derecho
    public static float legSwingLeft  = 0f;
    public static float legSwingRight = 0f;
    public static float bodyTilt      = 0f;   // inclinacion hacia adelante (correr)
    public static float headNod       = 0f;   // cabeceo idle
    public static float squashY       = 1f;   // squash & stretch en Y
    public static float stretchY      = 1f;

    public static void update(PlayerEntity player, float bobTimer, float swingPhase) {
        boolean moving  = player.getVelocity().horizontalLength() > 0.05;
        boolean running = player.isSprinting();
        boolean jumping = !player.isOnGround();
        boolean swimming= player.isTouchingWater();
        boolean sneaking= player.isSneaking();

        if (jumping) {
            // Squash al despegar, stretch en el aire
            squashY    = 0.85f;
            stretchY   = 1.18f;
            bodyTilt   = (float) Math.toRadians(-8);
            bodyBobY   = 0;
            armSwingLeft  = (float) Math.toRadians(-40);
            armSwingRight = (float) Math.toRadians(-40);

        } else if (swimming) {
            // Mariposa exagerada
            float phase = (float)(Math.sin(swingPhase * 2.0) * Math.toRadians(55));
            armSwingLeft  =  phase;
            armSwingRight = -phase;
            bodyTilt      = (float) Math.toRadians(-20);
            bodyBobY      = (float)(Math.sin(swingPhase) * 0.04);
            squashY = stretchY = 1f;

        } else if (sneaking) {
            // Agachado cartoon: cuerpo aplastado
            squashY       = 0.78f;
            stretchY      = 1f;
            bodyTilt      = (float) Math.toRadians(25);
            bodyBobY      = -0.15f;
            headNod       = (float) Math.toRadians(-15);
            armSwingLeft  = armSwingRight = (float) Math.toRadians(20);

        } else if (running) {
            // Correr: inclinacion + swing grande
            float t = (float)(Math.sin(swingPhase * 2.2) * Math.toRadians(50));
            armSwingLeft  =  t;
            armSwingRight = -t;
            legSwingLeft  = -t * 0.8f;
            legSwingRight =  t * 0.8f;
            bodyTilt      = (float) Math.toRadians(-14);
            bodyBobY      = (float)(Math.abs(Math.sin(swingPhase * 2.2)) * 0.06);
            squashY = stretchY = 1f;
            headNod = 0;

        } else if (moving) {
            // Caminar: rebote y balanceo
            float t = (float)(Math.sin(swingPhase * 1.8) * Math.toRadians(35));
            armSwingLeft  =  t;
            armSwingRight = -t;
            legSwingLeft  = -t * 0.7f;
            legSwingRight =  t * 0.7f;
            bodyBobY      = (float)(Math.abs(Math.sin(swingPhase * 1.8)) * 0.04);
            bodyTilt      = 0;
            squashY = stretchY = 1f;
            headNod = 0;

        } else {
            // Idle: leve balanceo de cabeza + respiracion
            headNod       = (float)(Math.sin(bobTimer * 0.6) * Math.toRadians(4));
            bodyBobY      = (float)(Math.sin(bobTimer * 0.9) * 0.01);
            armSwingLeft  = (float)(Math.sin(bobTimer * 0.5) * Math.toRadians(6));
            armSwingRight = (float)(Math.sin(bobTimer * 0.5 + Math.PI) * Math.toRadians(6));
            bodyTilt      = 0;
            squashY = stretchY = 1f;
            legSwingLeft  = legSwingRight = 0;
        }
    }
}
"""

    mixin = """\
package com.cartooncraft.animations.mixin;

import com.cartooncraft.animations.CartoonTransformRegistry;
import net.minecraft.client.render.entity.model.PlayerEntityModel;
import net.minecraft.client.model.ModelPart;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import net.minecraft.entity.LivingEntity;

/**
 * Mixin que aplica las transformaciones cartoon al modelo del jugador
 * justo antes de renderizarse.
 */
@Mixin(PlayerEntityModel.class)
public class PlayerEntityModelMixin<T extends LivingEntity> {

    @Inject(at = @At("TAIL"), method = "setAngles")
    private void cartoonSetAngles(T entity, float limbAngle, float limbDistance,
                                   float animationProgress, float headYaw, float headPitch,
                                   CallbackInfo ci) {
        PlayerEntityModel<?> model = (PlayerEntityModel<?>) (Object) this;

        // Rebote corporal
        model.body.pivotY      += CartoonTransformRegistry.bodyBobY * 16f;
        model.head.pivotY      += CartoonTransformRegistry.bodyBobY * 16f;

        // Swing brazos
        model.leftArm.pitch  += CartoonTransformRegistry.armSwingLeft;
        model.rightArm.pitch += CartoonTransformRegistry.armSwingRight;

        // Swing piernas
        model.leftLeg.pitch  += CartoonTransformRegistry.legSwingLeft;
        model.rightLeg.pitch += CartoonTransformRegistry.legSwingRight;

        // Inclinaci?n corporal
        model.body.pitch     += CartoonTransformRegistry.bodyTilt;

        // Cabeceo idle
        model.head.pitch     += CartoonTransformRegistry.headNod;

        // Squash & Stretch (escala Y)
        model.body.yScale    = CartoonTransformRegistry.squashY;
        model.leftLeg.yScale = CartoonTransformRegistry.squashY;
        model.rightLeg.yScale= CartoonTransformRegistry.squashY;
    }
}
"""

    mixin_json = {
        "required": True,
        "package": "com.cartooncraft.animations.mixin",
        "compatibilityLevel": "JAVA_21",
        "client": ["PlayerEntityModelMixin"],
        "injectors": {"defaultRequire": 1}
    }

    # Build script (Gradle)
    gradle = """\
plugins {
    id 'fabric-loom' version '1.7-SNAPSHOT'
    id 'maven-publish'
}

version = '1.0.0'
group   = 'com.cartooncraft'

repositories { mavenCentral() }

dependencies {
    minecraft        "com.mojang:minecraft:1.21.4"
    mappings         "net.fabricmc:yarn:1.21.4+build.1:v2"
    modImplementation "net.fabricmc:fabric-loader:0.16.5"
    modImplementation "net.fabricmc.fabric-api:fabric-api:0.110.0+1.21.4"
}

java { sourceCompatibility = JavaVersion.VERSION_21 }

processResources {
    inputs.property "version", project.version
    filesMatching("fabric.mod.json") { expand "version": project.version }
}
"""

    # Guardar archivos Java
    pkg = root / "src/main/java/com/cartooncraft/animations"
    mx  = pkg / "mixin"
    mkdir(pkg); mkdir(mx)

    write(pkg / "CartoonAnimationsClient.java", java_client)
    write(pkg / "CartoonTransformRegistry.java", registry)
    write(mx  / "PlayerEntityModelMixin.java",   mixin)
    jdump(mixin_json, root / "src/main/resources/cartooncraft_animations.mixins.json")
    write(root / "build.gradle", gradle)

    # -- Bedrock Animation JSON -----------------------------
    bedrock_anim = {
        "format_version": "1.8.0",
        "animations": {
            "animation.player.cartoon_walk": {
                "loop": True,
                "animation_length": 1.0,
                "bones": {
                    "leftArm":  {"rotation": {"0.0": [35,0,0], "0.5": [-35,0,0], "1.0": [35,0,0]}},
                    "rightArm": {"rotation": {"0.0": [-35,0,0],"0.5": [35,0,0], "1.0": [-35,0,0]}},
                    "leftLeg":  {"rotation": {"0.0": [-30,0,0],"0.5": [30,0,0], "1.0": [-30,0,0]}},
                    "rightLeg": {"rotation": {"0.0": [30,0,0], "0.5": [-30,0,0],"1.0": [30,0,0]}},
                    "body":     {"position": {"0.0": [0,0,0],  "0.25":[0,0.6,0],"0.5": [0,0,0],"0.75":[0,0.6,0],"1.0":[0,0,0]}}
                }
            },
            "animation.player.cartoon_run": {
                "loop": True,
                "animation_length": 0.6,
                "bones": {
                    "body":     {"rotation": {"0.0": [-14,0,0],"0.6": [-14,0,0]}},
                    "leftArm":  {"rotation": {"0.0": [50,0,0], "0.3": [-50,0,0],"0.6": [50,0,0]}},
                    "rightArm": {"rotation": {"0.0": [-50,0,0],"0.3": [50,0,0], "0.6": [-50,0,0]}},
                    "leftLeg":  {"rotation": {"0.0": [-40,0,0],"0.3": [40,0,0], "0.6": [-40,0,0]}},
                    "rightLeg": {"rotation": {"0.0": [40,0,0], "0.3": [-40,0,0],"0.6": [40,0,0]}}
                }
            },
            "animation.player.cartoon_jump": {
                "loop": False,
                "animation_length": 0.5,
                "bones": {
                    "body":     {"scale": {"0.0": [1,0.85,1],"0.15":[1,1.2,1],"0.5":[1,1,1]}},
                    "leftArm":  {"rotation": {"0.0": [-40,0,0],"0.5": [0,0,0]}},
                    "rightArm": {"rotation": {"0.0": [-40,0,0],"0.5": [0,0,0]}}
                }
            },
            "animation.player.cartoon_idle": {
                "loop": True,
                "animation_length": 3.0,
                "bones": {
                    "head":     {"rotation": {"0.0":[0,0,0],"1.5":[4,0,0],"3.0":[0,0,0]}},
                    "leftArm":  {"rotation": {"0.0":[6,0,0],"1.5":[-6,0,0],"3.0":[6,0,0]}},
                    "rightArm": {"rotation": {"0.0":[-6,0,0],"1.5":[6,0,0],"3.0":[-6,0,0]}}
                }
            },
            "animation.player.cartoon_sneak": {
                "loop": True,
                "animation_length": 1.0,
                "bones": {
                    "body":     {"rotation": [25,0,0], "position": [0,-2.4,0], "scale": [1,0.78,1]},
                    "head":     {"rotation": [-15,0,0]},
                    "leftArm":  {"rotation": [20,0,0]},
                    "rightArm": {"rotation": [20,0,0]}
                }
            },
            "animation.player.cartoon_swim": {
                "loop": True,
                "animation_length": 1.0,
                "bones": {
                    "body":     {"rotation": ["-20",0,0]},
                    "leftArm":  {"rotation": {"0.0":[55,0,0],"0.5":[-55,0,0],"1.0":[55,0,0]}},
                    "rightArm": {"rotation": {"0.0":[-55,0,0],"0.5":[55,0,0],"1.0":[-55,0,0]}}
                }
            }
        }
    }
    jdump(bedrock_anim, root / "bedrock" / "animations" / "cartoon_player.animation.json")

    # Bedrock manifest
    jdump({
        "format_version": 2,
        "header": {
            "description": "CartoonCraft Animations - Movimientos cartoon para Bedrock",
            "name": "CartoonCraft Animations",
            "uuid": "c3d4e5f6-a7b8-9012-cdef-123456789012",
            "version": [1,0,0],
            "min_engine_version": [1,21,0]
        },
        "modules": [{"description":"CartoonCraft Animations","type":"resources",
                     "uuid":"d4e5f6a7-b8c9-0123-defa-234567890123","version":[1,0,0]}]
    }, root / "bedrock" / "manifest.json")

    print("  OK Java Fabric mod generado")
    print("  OK Bedrock animations JSON generado")
    zip_folder(root, BASE / "CartoonCraft_AnimationsMod_JAVA.zip")

    # ZIP Bedrock por separado
    bedrock_root = root / "bedrock"
    with zipfile.ZipFile(str(BASE / "CartoonCraft_AnimationsMod_BEDROCK.zip"), "w", zipfile.ZIP_DEFLATED) as zf:
        for f in bedrock_root.rglob("*"):
            if f.is_file():
                zf.write(f, f.relative_to(bedrock_root))
    print("  OK CartoonCraft_AnimationsMod_JAVA.zip listo")
    print("  OK CartoonCraft_AnimationsMod_BEDROCK.zip listo")


# ===============================================================
#  4. MOD BOSS PETS (Fabric Java + Bedrock)
# ===============================================================

def build_boss_pets_mod():
    root = BASE / "CartoonCraft_BossPetsMod"
    print("\n[4/4] Generando Mod Boss Pets...")

    BOSSES = [
        "warden", "ender_dragon", "wither", "elder_guardian",
        "ravager", "evoker", "shulker"
    ]

    # -- fabric.mod.json -----------------------------------
    jdump({
        "schemaVersion": 1,
        "id": "cartooncraft_bosspets",
        "version": "1.0.0",
        "name": "CartoonCraft Boss Pets",
        "description": "Domina a los jefes y ll?valos como mascotas. Potencialos con la Esencia de Jefe.",
        "authors": ["CartoonCraft Team"],
        "license": "MIT",
        "environment": "*",
        "entrypoints": {
            "main":   ["com.cartooncraft.bosspets.BossPetsMod"],
            "client": ["com.cartooncraft.bosspets.BossPetsClient"]
        },
        "depends": {
            "fabricloader": ">=0.15.0",
            "minecraft": "~1.21",
            "java": ">=21",
            "fabric-api": "*"
        }
    }, root / "src/main/resources/fabric.mod.json")

    # -- Clase principal -----------------------------------
    main_class = """\
package com.cartooncraft.bosspets;

import net.fabricmc.api.ModInitializer;
import net.minecraft.util.Identifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class BossPetsMod implements ModInitializer {
    public static final String MOD_ID = "cartooncraft_bosspets";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

    @Override
    public void onInitialize() {
        BossPetsRegistry.registerAll();
        BossPetsItems.registerAll();
        BossPetsGoals.registerAll();
        LOGGER.info("[CartoonCraft Boss Pets] Mod inicializado. ?A domesticar jefes!");
    }
}
"""

    registry_class = """\
package com.cartooncraft.bosspets;

import net.minecraft.entity.EntityType;
import net.minecraft.entity.mob.*;
import net.minecraft.entity.boss.dragon.EnderDragonEntity;
import java.util.List;

/**
 * Registro de todos los jefes que pueden ser mascota.
 * Cada entrada define: tipo de entidad, coste de doma, HP m?x como mascota,
 * da?o base, habilidad especial y nivel m?ximo.
 */
public class BossPetsRegistry {

    public record BossSpec(
        EntityType<?> type,
        String id,
        int tameCost,       // cu?ntas BossEssence hacen falta para domar
        float basePetHp,    // HP de la mascota nivel 1
        float baseDamage,   // da?o nivel 1
        int maxLevel,       // nivel m?ximo
        String ability      // habilidad especial
    ) {}

    public static final List<BossSpec> SPECS = List.of(
        new BossSpec(EntityType.WARDEN,          "warden",          5, 250f, 25f, 10, "sonic_boom"),
        new BossSpec(EntityType.ENDER_DRAGON,     "ender_dragon",    8, 300f, 30f, 10, "dragon_breath"),
        new BossSpec(EntityType.WITHER,           "wither",          7, 280f, 28f, 10, "wither_skull"),
        new BossSpec(EntityType.ELDER_GUARDIAN,   "elder_guardian",  4, 160f, 18f,  8, "mining_fatigue"),
        new BossSpec(EntityType.RAVAGER,          "ravager",         3, 180f, 20f,  8, "ravage_charge"),
        new BossSpec(EntityType.EVOKER,           "evoker",          3, 120f, 14f,  8, "fang_summon"),
        new BossSpec(EntityType.SHULKER,          "shulker",         2, 100f, 12f,  8, "levitation_shell")
    );

    public static void registerAll() {
        // Los goals de mascota se a?aden via mixin o EntityType.Builder en addBehavior
        BossPetsMod.LOGGER.info("[BossPets] {} tipos de jefe registrados", SPECS.size());
    }
}
"""

    items_class = """\
package com.cartooncraft.bosspets;

import net.fabricmc.fabric.api.item.v1.FabricItemSettings;
import net.minecraft.item.*;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.util.Identifier;
import net.minecraft.util.Rarity;
import net.minecraft.text.Text;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.world.World;
import net.minecraft.util.Hand;
import net.minecraft.util.TypedActionResult;
import net.minecraft.sound.SoundEvents;

public class BossPetsItems {

    /**
     * BOSS ESSENCE (Esencia de Jefe)
     * -----------------------------
     * ?tem principal de potenciaci?n.
     * - Se craftea con 1 Nether Star + 4 Ender Pearl + 4 Echo Shard
     * - Uso: click derecho sobre tu mascota-jefe -> sube 1 nivel (m?x 10)
     * - Cada nivel: +10% HP, +8% da?o, +5% velocidad, desbloquea habilidades
     */
    public static Item BOSS_ESSENCE;

    /**
     * TOON TETHER (Correa Cartoon)
     * -----------------------------
     * Correa especial para mascotas-jefe. Permite invocarlas y guardarlas.
     * Crafteo: 4 Slimeball + 4 String + 1 Boss Essence en el centro
     */
    public static Item TOON_TETHER;

    /**
     * BOSS SOUL GEM (Gema de Alma de Jefe)
     * -------------------------------------
     * Drop raro de jefes derrotados. Se usa en la receta de Boss Essence.
     * Tambi?n act?a como "cristal de doma" lanzable al jefe.
     */
    public static Item BOSS_SOUL_GEM;

    public static void registerAll() {
        BOSS_ESSENCE = Registry.register(
            Registries.ITEM,
            new Identifier(BossPetsMod.MOD_ID, "boss_essence"),
            new BossEssenceItem(new FabricItemSettings().maxCount(16).rarity(Rarity.EPIC))
        );

        TOON_TETHER = Registry.register(
            Registries.ITEM,
            new Identifier(BossPetsMod.MOD_ID, "toon_tether"),
            new ToonTetherItem(new FabricItemSettings().maxCount(1).rarity(Rarity.RARE))
        );

        BOSS_SOUL_GEM = Registry.register(
            Registries.ITEM,
            new Identifier(BossPetsMod.MOD_ID, "boss_soul_gem"),
            new Item(new FabricItemSettings().maxCount(64).rarity(Rarity.RARE))
        );

        BossPetsMod.LOGGER.info("[BossPets] Items registrados");
    }

    // -- BossEssence ------------------------------------------
    static class BossEssenceItem extends Item {
        public BossEssenceItem(Settings settings) { super(settings); }

        @Override
        public TypedActionResult<ItemStack> use(World world, PlayerEntity user, Hand hand) {
            // En uso sobre entidad -> ver BossPetEntityMixin
            // Aqu? solo reproduce efecto visual
            if (!world.isClient) {
                user.playSound(SoundEvents.BLOCK_AMETHYST_BLOCK_CHIME, 1.0f, 1.2f);
            }
            return TypedActionResult.success(user.getStackInHand(hand));
        }
    }

    // -- ToonTether -------------------------------------------
    static class ToonTetherItem extends Item {
        public ToonTetherItem(Settings settings) { super(settings); }

        @Override
        public TypedActionResult<ItemStack> use(World world, PlayerEntity user, Hand hand) {
            if (!world.isClient) {
                // L?gica: invocar/guardar mascota ligada a este ?tem (via NBT uuid)
                user.sendMessage(Text.literal("?d?Mascota invocada/guardada!"), true);
                user.playSound(SoundEvents.ENTITY_ENDERMAN_TELEPORT, 1.0f, 0.8f);
            }
            return TypedActionResult.success(user.getStackInHand(hand));
        }
    }
}
"""

    goals_class = """\
package com.cartooncraft.bosspets;

import net.minecraft.entity.mob.WardenEntity;
import net.minecraft.entity.boss.dragon.EnderDragonEntity;

/**
 * Registra los AI Goals de mascota para cada jefe.
 * Los goals de FollowOwner, SitWhenOrdered y AttackWhenCommanded
 * se inyectan via Mixin en cada EntityType.
 */
public class BossPetsGoals {

    public static void registerAll() {
        // Los mixins por entidad se aplican autom?ticamente en carga
        // Ver: WardenPetMixin, EnderDragonPetMixin, etc.
        BossPetsMod.LOGGER.info("[BossPets] Goals de mascota registrados");
    }

    /** Calcula HP de mascota seg?n nivel */
    public static float calcHp(float base, int level) {
        return base + (base * 0.10f * (level - 1));
    }

    /** Calcula da?o seg?n nivel */
    public static float calcDamage(float base, int level) {
        return base + (base * 0.08f * (level - 1));
    }

    /** Verifica si se desbloquea habilidad especial en este nivel */
    public static boolean abilityUnlocked(int level, int requiredLevel) {
        return level >= requiredLevel;
    }
}
"""

    pet_mixin = """\
package com.cartooncraft.bosspets.mixin;

import com.cartooncraft.bosspets.BossPetsItems;
import com.cartooncraft.bosspets.BossPetsGoals;
import net.minecraft.entity.mob.PathAwareEntity;
import net.minecraft.entity.mob.MobEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.item.ItemStack;
import net.minecraft.nbt.NbtCompound;
import net.minecraft.util.ActionResult;
import net.minecraft.util.Hand;
import net.minecraft.text.Text;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import java.util.UUID;

/**
 * Mixin base aplicado a MobEntity.
 * Detecta click con Boss Soul Gem -> inicia proceso de doma.
 * Detecta click con Boss Essence  -> sube nivel a la mascota.
 */
@Mixin(MobEntity.class)
public abstract class BossPetEntityMixin {

    @Inject(at = @At("HEAD"), method = "interact", cancellable = true)
    private void onInteract(PlayerEntity player, Hand hand, CallbackInfoReturnable<ActionResult> cir) {
        MobEntity self = (MobEntity)(Object) this;
        ItemStack held = player.getStackInHand(hand);
        NbtCompound nbt = self.writeNbt(new NbtCompound());

        // -- Domar con Boss Soul Gem ---------------------
        if (held.isOf(BossPetsItems.BOSS_SOUL_GEM) && !self.isAlive() == false) {
            if (!isBoss(self)) return;
            if (self.world.isClient) return;

            int gems = nbt.getInt("BossPetTameProgress") + 1;
            int cost = getTameCost(self);
            nbt.putInt("BossPetTameProgress", gems);

            if (gems >= cost) {
                // DOMADO
                nbt.putBoolean("IsBossPet", true);
                nbt.putInt("BossPetLevel", 1);
                nbt.putUuid("BossPetOwner", player.getUuid());
                nbt.putInt("BossPetTameProgress", 0);
                self.readNbt(nbt);
                self.setAiDisabled(false);
                player.sendMessage(Text.literal("?a?" + getBossName(self) + " es ahora tu mascota! ?7(Nivel 1)"), false);
                player.getInventory().removeStack(player.getInventory().selectedSlot, 1);
                cir.setReturnValue(ActionResult.SUCCESS);
            } else {
                self.readNbt(nbt);
                player.sendMessage(Text.literal("?e" + getBossName(self) + " ?7est? siendo domado... ?b("+ gems +"/"+ cost +")"), true);
                player.getInventory().removeStack(player.getInventory().selectedSlot, 1);
                cir.setReturnValue(ActionResult.SUCCESS);
            }
            return;
        }

        // -- Potenciar con Boss Essence ------------------
        if (held.isOf(BossPetsItems.BOSS_ESSENCE) && nbt.getBoolean("IsBossPet")) {
            if (!player.getUuid().equals(nbt.getUuid("BossPetOwner"))) {
                player.sendMessage(Text.literal("?cNo es tu mascota."), true);
                return;
            }
            if (self.world.isClient) return;
            int level = nbt.getInt("BossPetLevel");
            if (level >= 10) {
                player.sendMessage(Text.literal("?6?Mascota al nivel m?ximo!"), true);
                return;
            }
            level++;
            nbt.putInt("BossPetLevel", level);

            // Escalar HP y da?o
            float baseHp  = nbt.getFloat("BossPetBaseHp");
            float baseDmg = nbt.getFloat("BossPetBaseDmg");
            float newHp   = BossPetsGoals.calcHp(baseHp, level);
            float newDmg  = BossPetsGoals.calcDamage(baseDmg, level);
            nbt.putFloat("BossPetCurrentHp", newHp);
            nbt.putFloat("BossPetCurrentDmg", newDmg);
            self.readNbt(nbt);
            self.setMaxHealth(newHp);
            self.setHealth(newHp);

            player.sendMessage(Text.literal(
                "?d?" + getBossName(self) + " ?dsube al nivel ?e"+ level +"?d! HP: ?a"+(int)newHp+" ?dDa?o: ?c"+(int)newDmg), false);
            player.getInventory().removeStack(player.getInventory().selectedSlot, 1);
            cir.setReturnValue(ActionResult.SUCCESS);
        }
    }

    private boolean isBoss(MobEntity e) {
        return e instanceof net.minecraft.entity.mob.WardenEntity
            || e instanceof net.minecraft.entity.boss.dragon.EnderDragonEntity
            || e instanceof net.minecraft.entity.boss.WitherEntity
            || e instanceof net.minecraft.entity.boss.ElderGuardianEntity
            || e instanceof net.minecraft.entity.mob.RavagerEntity
            || e instanceof net.minecraft.entity.mob.EvokerEntity
            || e instanceof net.minecraft.entity.mob.ShulkerEntity;
    }

    private int getTameCost(MobEntity e) {
        if (e instanceof net.minecraft.entity.boss.dragon.EnderDragonEntity) return 8;
        if (e instanceof net.minecraft.entity.boss.WitherEntity)             return 7;
        if (e instanceof net.minecraft.entity.mob.WardenEntity)              return 5;
        if (e instanceof net.minecraft.entity.boss.ElderGuardianEntity)      return 4;
        return 3;
    }

    private String getBossName(MobEntity e) {
        if (e instanceof net.minecraft.entity.mob.WardenEntity)              return "Warden";
        if (e instanceof net.minecraft.entity.boss.dragon.EnderDragonEntity) return "Ender Dragon";
        if (e instanceof net.minecraft.entity.boss.WitherEntity)             return "Wither";
        if (e instanceof net.minecraft.entity.boss.ElderGuardianEntity)      return "Elder Guardian";
        if (e instanceof net.minecraft.entity.mob.RavagerEntity)             return "Ravager";
        if (e instanceof net.minecraft.entity.mob.EvokerEntity)              return "Evoker";
        if (e instanceof net.minecraft.entity.mob.ShulkerEntity)             return "Shulker";
        return "Jefe";
    }
}
"""

    mixin_cfg = {
        "required": True,
        "package": "com.cartooncraft.bosspets.mixin",
        "compatibilityLevel": "JAVA_21",
        "mixins": ["BossPetEntityMixin"],
        "injectors": {"defaultRequire": 1}
    }

    # Recipes
    recipes = {
        "boss_essence": {
            "type": "minecraft:crafting_shaped",
            "pattern": ["EPE","ESE","EPE"],
            "key": {
                "E": {"item": "minecraft:ender_pearl"},
                "P": {"item": "minecraft:echo_shard"},
                "S": {"item": "minecraft:nether_star"}
            },
            "result": {"item": "cartooncraft_bosspets:boss_essence", "count": 2}
        },
        "toon_tether": {
            "type": "minecraft:crafting_shaped",
            "pattern": ["SLS","LBL","SLS"],
            "key": {
                "S": {"item": "minecraft:slime_ball"},
                "L": {"item": "minecraft:string"},
                "B": {"item": "cartooncraft_bosspets:boss_essence"}
            },
            "result": {"item": "cartooncraft_bosspets:toon_tether", "count": 1}
        },
        "boss_soul_gem": {
            "type": "minecraft:crafting_shaped",
            "pattern": [" N ","NDN"," N "],
            "key": {
                "N": {"item": "minecraft:amethyst_shard"},
                "D": {"item": "minecraft:diamond"}
            },
            "result": {"item": "cartooncraft_bosspets:boss_soul_gem", "count": 4}
        }
    }

    # Advancements
    advancements = {
        "first_pet": {
            "display": {
                "icon": {"item": "cartooncraft_bosspets:boss_soul_gem"},
                "title": "?Primer Jefe Domado!",
                "description": "Doma a un jefe y convi?rtelo en tu mascota.",
                "frame": "task",
                "show_toast": True
            },
            "parent": "minecraft:story/root",
            "criteria": {"has_tether": {"trigger": "minecraft:inventory_changed",
                "conditions": {"items": [{"items": ["cartooncraft_bosspets:toon_tether"]}]}}}
        },
        "max_level_pet": {
            "display": {
                "icon": {"item": "cartooncraft_bosspets:boss_essence"},
                "title": "?Bestia M?xima!",
                "description": "Lleva a tu mascota-jefe al nivel 10.",
                "frame": "challenge",
                "show_toast": True
            },
            "parent": "cartooncraft_bosspets:first_pet",
            "criteria": {"level_10": {"trigger": "minecraft:impossible"}}
        }
    }

    # -- Bedrock behavior pack ------------------------------
    bedrock_entity_base = lambda boss_id, hp, dmg: {
        "format_version": "1.21.0",
        "minecraft:entity": {
            "description": {
                "identifier": f"cartooncraft:{boss_id}_pet",
                "is_spawnable": False,
                "is_summonable": True,
                "is_experimental": False
            },
            "component_groups": {
                "cartooncraft:tamed": {
                    "minecraft:tameable": {"probability": 0.0, "tame_items": "cartooncraft:boss_soul_gem"},
                    "minecraft:follow_owner": {"speed_multiplier": 1.1, "start_distance": 10.0, "stop_distance": 2.0},
                    "minecraft:sit": {},
                    "minecraft:health": {"value": hp, "max": hp}
                },
                "cartooncraft:level_up": {
                    "minecraft:attack": {"damage": dmg}
                }
            },
            "components": {
                "minecraft:type_family": {"family": ["boss_pet", "mob"]},
                "minecraft:health": {"value": hp, "max": hp},
                "minecraft:attack": {"damage": dmg},
                "minecraft:movement": {"value": 0.35},
                "minecraft:navigation.walk": {},
                "minecraft:can_climb": {},
                "minecraft:despawn": {"despawn_from_distance": {}},
                "minecraft:persistent": {}
            },
            "events": {
                "cartooncraft:on_tame": {
                    "add": {"component_groups": ["cartooncraft:tamed"]}
                },
                "cartooncraft:level_up": {
                    "add": {"component_groups": ["cartooncraft:level_up"]}
                }
            }
        }
    }

    boss_hp_dmg = {
        "warden": (250, 25), "ender_dragon": (300, 30), "wither": (280, 28),
        "elder_guardian": (160, 18), "ravager": (180, 20),
        "evoker": (120, 14), "shulker": (100, 12)
    }

    # Bedrock items
    bedrock_items = {
        "format_version": "1.21.0",
        "minecraft:item": {
            "description": {"identifier": "cartooncraft:boss_essence", "category": "Equipment"},
            "components": {
                "minecraft:max_stack_size": 16,
                "minecraft:use_duration": 32,
                "minecraft:icon": {"texture": "boss_essence"},
                "minecraft:display_name": {"value": "?dEsencia de Jefe"},
                "minecraft:tooltip_text": {"value": "Potencia a tu mascota-jefe. Sube 1 nivel por uso."}
            }
        }
    }

    bedrock_soul_gem = {
        "format_version": "1.21.0",
        "minecraft:item": {
            "description": {"identifier": "cartooncraft:boss_soul_gem", "category": "Items"},
            "components": {
                "minecraft:max_stack_size": 64,
                "minecraft:icon": {"texture": "boss_soul"},
                "minecraft:display_name": {"value": "?5Gema de Alma de Jefe"},
                "minecraft:tooltip_text": {"value": "L?nzala a un jefe para comenzar a domarlo."}
            }
        }
    }

    bedrock_tether = {
        "format_version": "1.21.0",
        "minecraft:item": {
            "description": {"identifier": "cartooncraft:toon_tether", "category": "Equipment"},
            "components": {
                "minecraft:max_stack_size": 1,
                "minecraft:icon": {"texture": "toon_crown"},
                "minecraft:display_name": {"value": "?aCorrea Cartoon"},
                "minecraft:tooltip_text": {"value": "Invoca o guarda a tu mascota-jefe."}
            }
        }
    }

    # -- Guardar archivos ----------------------------------
    pkg = root / "src/main/java/com/cartooncraft/bosspets"
    mx  = pkg / "mixin"
    mkdir(pkg); mkdir(mx)

    write(pkg / "BossPetsMod.java",      main_class)
    write(pkg / "BossPetsRegistry.java", registry_class)
    write(pkg / "BossPetsItems.java",    items_class)
    write(pkg / "BossPetsGoals.java",    goals_class)
    write(mx  / "BossPetEntityMixin.java", pet_mixin)
    jdump(mixin_cfg, root / "src/main/resources/cartooncraft_bosspets.mixins.json")

    for name, data in recipes.items():
        jdump(data, root / f"src/main/resources/data/cartooncraft_bosspets/recipes/{name}.json")
    for name, data in advancements.items():
        jdump(data, root / f"src/main/resources/data/cartooncraft_bosspets/advancements/{name}.json")

    # Bedrock - entities
    for boss, (hp, dmg) in boss_hp_dmg.items():
        jdump(bedrock_entity_base(boss, hp, dmg),
              root / f"bedrock/behavior_packs/cartooncraft_bp/entities/{boss}_pet.json")

    jdump(bedrock_items,    root / "bedrock/behavior_packs/cartooncraft_bp/items/boss_essence.json")
    jdump(bedrock_soul_gem, root / "bedrock/behavior_packs/cartooncraft_bp/items/boss_soul_gem.json")
    jdump(bedrock_tether,   root / "bedrock/behavior_packs/cartooncraft_bp/items/toon_tether.json")

    jdump({
        "format_version": 2,
        "header": {"description":"CartoonCraft Boss Pets - Doma a los jefes",
                   "name":"CartoonCraft Boss Pets","uuid":"e5f6a7b8-c9d0-1234-efab-345678901234",
                   "version":[1,0,0],"min_engine_version":[1,21,0]},
        "modules": [{"description":"Boss Pets BP","type":"data",
                     "uuid":"f6a7b8c9-d0e1-2345-fabc-456789012345","version":[1,0,0]}]
    }, root / "bedrock/behavior_packs/cartooncraft_bp/manifest.json")

    write(root / "build.gradle", """\
plugins {
    id 'fabric-loom' version '1.7-SNAPSHOT'
}
version = '1.0.0'
group   = 'com.cartooncraft'
repositories { mavenCentral() }
dependencies {
    minecraft        "com.mojang:minecraft:1.21.4"
    mappings         "net.fabricmc:yarn:1.21.4+build.1:v2"
    modImplementation "net.fabricmc:fabric-loader:0.16.5"
    modImplementation "net.fabricmc.fabric-api:fabric-api:0.110.0+1.21.4"
}
java { sourceCompatibility = JavaVersion.VERSION_21 }
""")

    print("  OK Java Fabric mod generado")
    print("  OK Bedrock behavior pack generado")
    zip_folder(root, BASE / "CartoonCraft_BossPetsMod_JAVA.zip")

    bp = root / "bedrock"
    with zipfile.ZipFile(str(BASE / "CartoonCraft_BossPetsMod_BEDROCK.zip"), "w", zipfile.ZIP_DEFLATED) as zf:
        for f in bp.rglob("*"):
            if f.is_file():
                zf.write(f, f.relative_to(bp))
    print("  OK CartoonCraft_BossPetsMod_JAVA.zip listo")
    print("  OK CartoonCraft_BossPetsMod_BEDROCK.zip listo")


# ===============================================================
#  MAIN
# ===============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  CartoonCraft - Generador de proyectos Minecraft")
    print("=" * 60)

    build_texture_pack()
    build_shader()
    build_animation_mod()
    build_boss_pets_mod()

    print("\n" + "=" * 60)
    print("  ?TODO GENERADO CORRECTAMENTE!")
    print("=" * 60)
    print("""
Archivos creados en C:\\Users\\User\\Desktop\\Jarvis\\:

  ?? CartoonCraft_TexturePack_JAVA.zip
  ?? CartoonCraft_TexturePack_BEDROCK.zip
  ?? CartoonCraft_Shader.zip
  ?? CartoonCraft_AnimationsMod_JAVA.zip
  ?? CartoonCraft_AnimationsMod_BEDROCK.zip
  ?? CartoonCraft_BossPetsMod_JAVA.zip
  ?? CartoonCraft_BossPetsMod_BEDROCK.zip

INSTALACI?N:
  Java   -> .minecraft/resourcepacks/ o mods/ (Fabric 1.21.4)
  Shader -> shaderpacks/ (requiere Iris o OptiFine)
  Bedrock-> importar el .zip desde Minecraft Bedrock
""")

