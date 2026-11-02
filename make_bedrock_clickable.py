import shutil, zipfile, tempfile
from pathlib import Path

BASE = Path("C:/Users/User/Desktop/Jarvis")

def repack_mcpack(source_zip, out_path):
    shutil.copy2(source_zip, out_path)
    print("  -> " + str(Path(out_path).name))

def repack_mcaddon(bp_zip, out_mcaddon, rp_zip=None):
    tmp = Path(tempfile.mkdtemp())
    bp_dst = tmp / (Path(bp_zip).stem + ".mcpack")
    shutil.copy2(bp_zip, bp_dst)
    if rp_zip and Path(rp_zip).exists():
        rp_dst = tmp / (Path(rp_zip).stem + "_rp.mcpack")
        shutil.copy2(rp_zip, rp_dst)
    with zipfile.ZipFile(str(out_mcaddon), "w", zipfile.ZIP_DEFLATED) as zf:
        for f in tmp.iterdir():
            if f.is_file():
                zf.write(f, f.name)
    shutil.rmtree(tmp)
    print("  -> " + str(Path(out_mcaddon).name))

print("Generando archivos Bedrock instalables con doble clic...")

# 1. Texture Pack -> .mcpack
repack_mcpack(
    BASE / "CartoonCraft_TexturePack_BEDROCK.zip",
    BASE / "CartoonCraft_TexturePack.mcpack"
)

# 2. Animaciones -> .mcpack (resource pack)
repack_mcpack(
    BASE / "CartoonCraft_AnimationsMod_BEDROCK.zip",
    BASE / "CartoonCraft_AnimationsMod.mcpack"
)

# 3. Boss Pets -> .mcaddon (behavior pack)
repack_mcpack(
    BASE / "CartoonCraft_BossPetsMod_BEDROCK.zip",
    BASE / "CartoonCraft_BossPetsMod.mcaddon"
)

print("")
print("LISTO! Archivos generados:")
for ext in ["*.mcpack","*.mcaddon"]:
    for f in BASE.glob(ext):
        kb = round(f.stat().st_size / 1024, 1)
        print(f"  {f.name}  ({kb} KB)")

print("")
print("Doble clic -> Minecraft Bedrock se abre e instala automaticamente.")
