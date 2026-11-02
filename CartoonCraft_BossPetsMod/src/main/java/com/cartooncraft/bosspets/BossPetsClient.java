package com.cartooncraft.bosspets;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.keybinding.v1.KeyBindingHelper;
import net.minecraft.client.option.KeyBinding;
import net.minecraft.text.Text;
import org.lwjgl.glfw.GLFW;

public class BossPetsClient implements ClientModInitializer {
    private static KeyBinding summonPetKey;

    @Override
    public void onInitializeClient() {
        summonPetKey = KeyBindingHelper.registerKeyBinding(new KeyBinding(
                "key.cartooncraft.summon_pet",
                GLFW.GLFW_KEY_K,
                "category.cartooncraft.bosspets"
        ));

        ClientTickEvents.END_CLIENT_TICK.register(client -> {
            if (client.player == null) return;
            while (summonPetKey.wasPressed()) {
                client.player.sendMessage(Text.literal("§aBoss pet toggle ready."), true);
            }
        });
    }
}
