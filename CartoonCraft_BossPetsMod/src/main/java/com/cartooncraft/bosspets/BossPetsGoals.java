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
