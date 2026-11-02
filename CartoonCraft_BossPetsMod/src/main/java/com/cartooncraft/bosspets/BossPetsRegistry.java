package com.cartooncraft.bosspets;

import net.minecraft.entity.EntityType;
import net.minecraft.entity.mob.*;
import java.util.List;

public class BossPetsRegistry {

    public record BossSpec(
            EntityType<?> type,
            String id,
            int tameCost,
            float basePetHp,
            float baseDamage,
            int maxLevel,
            String ability
    ) {}

    public static final List<BossSpec> SPECS = List.of(
            new BossSpec(EntityType.WARDEN, "warden", 5, 250f, 25f, 10, "sonic_boom"),
            new BossSpec(EntityType.ENDER_DRAGON, "ender_dragon", 8, 300f, 30f, 10, "dragon_breath"),
            new BossSpec(EntityType.WITHER, "wither", 7, 280f, 28f, 10, "wither_skull"),
            new BossSpec(EntityType.ELDER_GUARDIAN, "elder_guardian", 4, 160f, 18f, 8, "mining_fatigue"),
            new BossSpec(EntityType.RAVAGER, "ravager", 3, 180f, 20f, 8, "ravage_charge"),
            new BossSpec(EntityType.EVOKER, "evoker", 3, 120f, 14f, 8, "fang_summon"),
            new BossSpec(EntityType.SHULKER, "shulker", 2, 100f, 12f, 8, "levitation_shell")
    );

    public static void registerAll() {
        BossPetsMod.LOGGER.info("[BossPets] {} boss entries registered.", SPECS.size());
    }
}
