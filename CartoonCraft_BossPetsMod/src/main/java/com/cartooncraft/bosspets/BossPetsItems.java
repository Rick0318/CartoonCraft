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
