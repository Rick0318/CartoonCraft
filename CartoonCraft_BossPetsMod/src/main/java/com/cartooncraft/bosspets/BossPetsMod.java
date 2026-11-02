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
