package com.cartooncraft.bosspets;

public class BossPetsGoals {

    public static void registerAll() {
        BossPetsMod.LOGGER.info("[BossPets] Goals registered.");
    }

    public static float calcHp(float base, int level) {
        if (level <= 1) return base;
        return base * (1.0f + 0.10f * (level - 1));
    }

    public static float calcDamage(float base, int level) {
        if (level <= 1) return base;
        return base * (1.0f + 0.08f * (level - 1));
    }

    public static boolean abilityUnlocked(int level, int requiredLevel) {
        return level >= requiredLevel;
    }
}
