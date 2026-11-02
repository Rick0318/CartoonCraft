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
