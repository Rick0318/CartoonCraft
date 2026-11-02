# 🎨 CartoonCraft — Minecraft Mod Pack

> Pack completo de mods, texturas, shaders y animaciones estilo **cartoon** para Minecraft Java y Bedrock (última versión).

---

## 📦 Contenido del repositorio

| Archivo | Descripción | Plataforma |
|---|---|---|
| `CartoonCraft_TexturePack_JAVA.zip` | Texture pack cartoon | Java Edition |
| `CartoonCraft_TexturePack_BEDROCK.zip` | Texture pack cartoon | Bedrock Edition |
| `CartoonCraft_TexturePack.mcpack` | Texture pack (doble clic para instalar) | Bedrock Edition |
| `CartoonCraft_Shader.zip` | Shader cel-shading | Java (Iris/OptiFine) |
| `CartoonCraft_AnimationsMod_JAVA.zip` | Mod de movimientos cartoon | Java Fabric |
| `CartoonCraft_AnimationsMod_BEDROCK.zip` | Animaciones cartoon | Bedrock Edition |
| `CartoonCraft_AnimationsMod.mcpack` | Animaciones (doble clic para instalar) | Bedrock Edition |
| `CartoonCraft_BossPetsMod_JAVA.zip` | Mod mascotas-jefe | Java Fabric |
| `CartoonCraft_BossPetsMod_BEDROCK.zip` | Mascotas-jefe | Bedrock Edition |
| `CartoonCraft_BossPetsMod.mcaddon` | Mascotas-jefe (doble clic para instalar) | Bedrock Edition |

---

## 🎨 Texture Pack — CartoonCraft

Estilo cartoon moderado: colores saturados, contornos suaves y **relieve visible** en los bloques que lo necesitan.

### Bloques incluidos (28 texturas)
- Tierra, piedra, cobblestone, arena, grava
- Madera de roble (tronco + tablas + hojas)
- Agua, lava, nieve, hielo
- Ladrillos, netherrack, obsidiana, glowstone
- Piedra profunda, calcita, amatista
- End stone, alma de arena, shroomlight, magma...

### Características
- ✅ Resolución **16×16** (fiel al estilo Minecraft)
- ✅ Contorno cartoon en todos los bloques
- ✅ Highlight superior + sombra inferior (sensación 3D)
- ✅ Relieve real en piedra, madera, ladrillo, netherrack, obsidiana

---

## 🌟 Shader — CartoonCraft Cel Shading

Compatible con **Iris 1.7+** y **OptiFine HD U I5+**.

### Efectos
- **Cel-shading** en 4 bandas de luz (efecto dibujado a mano)
- **Outline** automático en bordes de bloques
- **Cielo cartoon** cuantizado (colores por bandas, no gradiente continuo)
- **Agua animada** con brillos tipo toon
- **Niebla suave** estilizada
- **Sombras** mejoradas (1024px)
- **Post-process**: FXAA anti-aliasing + saturación cartoon + viñeta

---

## 🎬 Mod de Animaciones — CartoonCraft Animations

Movimientos cartoon con **squash & stretch** para el jugador.

| Animación | Efecto cartoon |
|---|---|
| Caminar | Balanceo de brazos 35°, rebote en Y |
| Correr | Inclinación -14°, swing 50° |
| Saltar | Squash 0.85x al despegar, stretch 1.18x en el aire |
| Nadar | Mariposa exagerada ±55° |
| Agacharse | Cuerpo aplastado 0.78x, inclinación 25° |
| Idle | Balanceo suave de cabeza y brazos |

### Instalación Java
- Requiere **Fabric 1.21.4** + **Fabric API**
- Compilar con `./gradlew build` o usar con **Figura**

### Instalación Bedrock
- Doble clic en `CartoonCraft_AnimationsMod.mcpack`

---

## 🐉 Mod Boss Pets — CartoonCraft Boss Pets

¡Doma a los jefes más poderosos y llévalos como mascota!

### Jefes domesticables

| Jefe | Gemas para domar | HP (Nv.1) | Daño (Nv.1) | Habilidad especial |
|---|---|---|---|---|
| 🟢 **Warden** | 5 | 250 HP | 25 | Sonic Boom |
| 🟣 **Ender Dragon** | 8 | 300 HP | 30 | Dragon Breath |
| ⬛ **Wither** | 7 | 280 HP | 28 | Wither Skull |
| 🔵 **Elder Guardian** | 4 | 160 HP | 18 | Mining Fatigue |
| 🔴 **Ravager** | 3 | 180 HP | 20 | Ravage Charge |
| 🟡 **Evoker** | 3 | 120 HP | 14 | Fang Summon |
| 🟤 **Shulker** | 2 | 100 HP | 12 | Levitation Shell |

### Ítems nuevos

#### 🟣 Boss Soul Gem (Gema de Alma de Jefe)
Drop raro de jefes. Úsala para domar.
```
Crafteo:  A N A
          N D N
          A N A
A = Amethyst Shard | N = nada | D = Diamond
→ x4 Boss Soul Gem
```

#### 💜 Boss Essence (Esencia de Jefe)  
Potencia a tu mascota +1 nivel (máx 10). Cada nivel: +10% HP, +8% daño, +5% velocidad.
```
Crafteo:  E P E
          E S E
          E P E
E = Ender Pearl | P = Echo Shard | S = Nether Star
→ x2 Boss Essence
```

#### 🟢 Toon Tether (Correa Cartoon)
Invoca o guarda a tu mascota-jefe.
```
Crafteo:  S L S
          L B L
          S L S
S = Slime Ball | L = String | B = Boss Essence
→ x1 Toon Tether
```

### Sistema de niveles
- Nivel máximo: **10**
- Cada nivel: HP +10%, Daño +8%, Velocidad +5%
- Las habilidades especiales se desbloquean progresivamente

### Cómo domar un jefe
1. Crafteá **Boss Soul Gem**
2. Ve al jefe (recomendado: debilitarlo primero)
3. Click derecho con la gema → barra de progreso
4. Repite hasta completar el coste de gemas
5. ¡El jefe es ahora tu mascota! Usa **Toon Tether** para invocarlo

---

## 🔧 Instalación

### Java Edition (Fabric 1.21.4)
1. Instala [Fabric Loader 0.16.5+](https://fabricmc.net)
2. Instala [Fabric API](https://modrinth.com/mod/fabric-api)
3. Copia los `.zip` de mods en `.minecraft/mods/`
4. Copia `CartoonCraft_TexturePack_JAVA.zip` en `.minecraft/resourcepacks/`
5. Copia `CartoonCraft_Shader.zip` en `.minecraft/shaderpacks/` (necesita [Iris](https://irisshaders.net))

### Bedrock Edition (Windows)
1. Doble clic en `CartoonCraft_TexturePack.mcpack` → instala automáticamente
2. Doble clic en `CartoonCraft_AnimationsMod.mcpack` → instala automáticamente
3. Doble clic en `CartoonCraft_BossPetsMod.mcaddon` → instala automáticamente
4. En tu mundo: **Configuración → Paquetes de recursos / Paquetes de comportamiento → Activar**

> ⚠️ El shader no está disponible para Bedrock Edition (Minecraft Bedrock usa Render Dragon, un sistema diferente).

---

## 📋 Requisitos

| | Java Edition | Bedrock Edition |
|---|---|---|
| Versión Minecraft | 1.21.4 | 1.21.0+ |
| Loader | Fabric 0.16.5+ | No necesario |
| API | Fabric API | No necesario |
| Shader | Iris 1.7+ / OptiFine | ❌ No compatible |

---

## 📜 Licencia

MIT License — libre para usar, modificar y distribuir.

---

*Generado con CartoonCraft Generator — Minecraft 1.21.4*
