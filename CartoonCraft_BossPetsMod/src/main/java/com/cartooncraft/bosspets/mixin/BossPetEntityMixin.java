package com.cartooncraft.bosspets.mixin;

import com.cartooncraft.bosspets.BossPetsItems;
import net.minecraft.entity.mob.ElderGuardianEntity;
import net.minecraft.entity.mob.EvokerEntity;
import net.minecraft.entity.mob.MobEntity;
import net.minecraft.entity.mob.RavagerEntity;
import net.minecraft.entity.mob.ShulkerEntity;
import net.minecraft.entity.mob.WardenEntity;
import net.minecraft.entity.boss.WitherEntity;
import net.minecraft.entity.boss.dragon.EnderDragonEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.item.ItemStack;
import net.minecraft.nbt.NbtCompound;
import net.minecraft.text.Text;
import net.minecraft.util.ActionResult;
import net.minecraft.util.Hand;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(MobEntity.class)
public abstract class BossPetEntityMixin {

    @Inject(method = "interact", at = @At("HEAD"), cancellable = true)
    private void cartooncraft$interact(PlayerEntity player, Hand hand, CallbackInfoReturnable<ActionResult> cir) {
        MobEntity self = (MobEntity) (Object) this;
        ItemStack stack = player.getStackInHand(hand);
        if (stack.isEmpty()) return;

        NbtCompound nbt = self.getPersistentData();

        if (stack.isOf(BossPetsItems.BOSS_SOUL_GEM)) {
            if (!isBoss(self) || self.getWorld().isClient) return;

            int progress = nbt.getInt("BossPetTameProgress");
            int cost = getTameCost(self);
            progress += 1;
            nbt.putInt("BossPetTameProgress", progress);

            if (progress >= cost) {
                nbt.putBoolean("BossPetTamed", true);
                nbt.putInt("BossPetLevel", 1);
                nbt.putString("BossPetOwnerUuid", player.getUuidAsString());
                nbt.putInt("BossPetTameProgress", 0);
                player.sendMessage(Text.literal("§a" + getBossName(self) + " is now your pet!"), true);
                if (!player.getAbilities().creativeMode) {
                    stack.decrement(1);
                }
                cir.setReturnValue(ActionResult.SUCCESS);
                return;
            }

            player.sendMessage(Text.literal("§e" + getBossName(self) + " is being tamed... (" + progress + "/" + cost + ")"), true);
            if (!player.getAbilities().creativeMode) {
                stack.decrement(1);
            }
            cir.setReturnValue(ActionResult.SUCCESS);
            return;
        }

        if (stack.isOf(BossPetsItems.BOSS_ESSENCE) && nbt.getBoolean("BossPetTamed")) {
            if (self.getWorld().isClient) return;

            String ownerUuid = nbt.getString("BossPetOwnerUuid");
            if (!player.getUuidAsString().equals(ownerUuid)) {
                player.sendMessage(Text.literal("§cThis is not your pet."), true);
                return;
            }

            int level = nbt.getInt("BossPetLevel");
            if (level >= 10) {
                player.sendMessage(Text.literal("§6Your pet is already at maximum level."), true);
                return;
            }

            level += 1;
            nbt.putInt("BossPetLevel", level);
            player.sendMessage(Text.literal("§d" + getBossName(self) + " reached level " + level + "!"), true);
            if (!player.getAbilities().creativeMode) {
                stack.decrement(1);
            }
            cir.setReturnValue(ActionResult.SUCCESS);
        }
    }

    private boolean isBoss(MobEntity entity) {
        return entity instanceof WardenEntity
                || entity instanceof EnderDragonEntity
                || entity instanceof WitherEntity
                || entity instanceof ElderGuardianEntity
                || entity instanceof RavagerEntity
                || entity instanceof EvokerEntity
                || entity instanceof ShulkerEntity;
    }

    private int getTameCost(MobEntity entity) {
        if (entity instanceof EnderDragonEntity) return 8;
        if (entity instanceof WitherEntity) return 7;
        if (entity instanceof WardenEntity) return 5;
        if (entity instanceof ElderGuardianEntity) return 4;
        if (entity instanceof RavagerEntity) return 3;
        if (entity instanceof EvokerEntity) return 3;
        if (entity instanceof ShulkerEntity) return 2;
        return 3;
    }

    private String getBossName(MobEntity entity) {
        if (entity instanceof WardenEntity) return "Warden";
        if (entity instanceof EnderDragonEntity) return "Ender Dragon";
        if (entity instanceof WitherEntity) return "Wither";
        if (entity instanceof ElderGuardianEntity) return "Elder Guardian";
        if (entity instanceof RavagerEntity) return "Ravager";
        if (entity instanceof EvokerEntity) return "Evoker";
        if (entity instanceof ShulkerEntity) return "Shulker";
        return "Boss";
    }
}
