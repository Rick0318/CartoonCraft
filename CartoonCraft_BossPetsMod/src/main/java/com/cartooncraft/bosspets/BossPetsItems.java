package com.cartooncraft.bosspets;

import net.fabricmc.fabric.api.item.v1.FabricItemSettings;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.sound.SoundEvents;
import net.minecraft.text.Text;
import net.minecraft.util.Hand;
import net.minecraft.util.Identifier;
import net.minecraft.util.Rarity;
import net.minecraft.util.TypedActionResult;
import net.minecraft.world.World;

public class BossPetsItems {

    public static Item BOSS_ESSENCE;
    public static Item TOON_TETHER;
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

        BossPetsMod.LOGGER.info("[BossPets] Items registered.");
    }

    static class BossEssenceItem extends Item {
        BossEssenceItem(Settings settings) {
            super(settings);
        }

        @Override
        public TypedActionResult<ItemStack> use(World world, PlayerEntity user, Hand hand) {
            ItemStack stack = user.getStackInHand(hand);
            if (!world.isClient) {
                user.playSound(SoundEvents.BLOCK_AMETHYST_BLOCK_CHIME, 1.0F, 1.2F);
                user.sendMessage(Text.literal("§dBoss essence used."), true);
            }
            return TypedActionResult.success(stack, world.isClient);
        }
    }

    static class ToonTetherItem extends Item {
        ToonTetherItem(Settings settings) {
            super(settings);
        }

        @Override
        public TypedActionResult<ItemStack> use(World world, PlayerEntity user, Hand hand) {
            ItemStack stack = user.getStackInHand(hand);
            if (!world.isClient) {
                user.playSound(SoundEvents.ENTITY_ENDERMAN_TELEPORT, 1.0F, 0.8F);
                user.sendMessage(Text.literal("§aYour pet summoned."), true);
            }
            return TypedActionResult.success(stack, world.isClient);
        }
    }
}
