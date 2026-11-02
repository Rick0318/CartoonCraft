package com.cartooncraft.bosspets.mixin;

import com.cartooncraft.bosspets.BossPetsItems;
import com.cartooncraft.bosspets.BossPetsGoals;
import net.minecraft.entity.mob.PathAwareEntity;
import net.minecraft.entity.mob.MobEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.item.ItemStack;
import net.minecraft.nbt.NbtCompound;
import net.minecraft.util.ActionResult;
import net.minecraft.util.Hand;
import net.minecraft.text.Text;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import java.util.UUID;

/**
 * Mixin base aplicado a MobEntity.
 * Detecta click con Boss Soul Gem -> inicia proceso de doma.
 * Detecta click con Boss Essence  -> sube nivel a la mascota.
 */
@Mixin(MobEntity.class)
public abstract class BossPetEntityMixin {

    @Inject(at = @At("HEAD"), method = "interact", cancellable = true)
    private void onInteract(PlayerEntity player, Hand hand, CallbackInfoReturnable<ActionResult> cir) {
        MobEntity self = (MobEntity)(Object) this;
        ItemStack held = player.getStackInHand(hand);
        NbtCompound nbt = self.writeNbt(new NbtCompound());

        // -- Domar con Boss Soul Gem ---------------------
        if (held.isOf(BossPetsItems.BOSS_SOUL_GEM) && !self.isAlive() == false) {
            if (!isBoss(self)) return;
            if (self.world.isClient) return;

            int gems = nbt.getInt("BossPetTameProgress") + 1;
            int cost = getTameCost(self);
            nbt.putInt("BossPetTameProgress", gems);

            if (gems >= cost) {
                // DOMADO
                nbt.putBoolean("IsBossPet", true);
                nbt.putInt("BossPetLevel", 1);
                nbt.putUuid("BossPetOwner", player.getUuid());
                nbt.putInt("BossPetTameProgress", 0);
                self.readNbt(nbt);
                self.setAiDisabled(false);
                player.sendMessage(Text.literal("?a?" + getBossName(self) + " es ahora tu mascota! ?7(Nivel 1)"), false);
                player.getInventory().removeStack(player.getInventory().selectedSlot, 1);
                cir.setReturnValue(ActionResult.SUCCESS);
            } else {
                self.readNbt(nbt);
                player.sendMessage(Text.literal("?e" + getBossName(self) + " ?7est? siendo domado... ?b("+ gems +"/"+ cost +")"), true);
                player.getInventory().removeStack(player.getInventory().selectedSlot, 1);
                cir.setReturnValue(ActionResult.SUCCESS);
            }
            return;
        }

        // -- Potenciar con Boss Essence ------------------
        if (held.isOf(BossPetsItems.BOSS_ESSENCE) && nbt.getBoolean("IsBossPet")) {
            if (!player.getUuid().equals(nbt.getUuid("BossPetOwner"))) {
                player.sendMessage(Text.literal("?cNo es tu mascota."), true);
                return;
            }
            if (self.world.isClient) return;
            int level = nbt.getInt("BossPetLevel");
            if (level >= 10) {
                player.sendMessage(Text.literal("?6?Mascota al nivel m?ximo!"), true);
                return;
            }
            level++;
            nbt.putInt("BossPetLevel", level);

            // Escalar HP y da?o
            float baseHp  = nbt.getFloat("BossPetBaseHp");
            float baseDmg = nbt.getFloat("BossPetBaseDmg");
            float newHp   = BossPetsGoals.calcHp(baseHp, level);
            float newDmg  = BossPetsGoals.calcDamage(baseDmg, level);
            nbt.putFloat("BossPetCurrentHp", newHp);
            nbt.putFloat("BossPetCurrentDmg", newDmg);
            self.readNbt(nbt);
            self.setMaxHealth(newHp);
            self.setHealth(newHp);

            player.sendMessage(Text.literal(
                "?d?" + getBossName(self) + " ?dsube al nivel ?e"+ level +"?d! HP: ?a"+(int)newHp+" ?dDa?o: ?c"+(int)newDmg), false);
            player.getInventory().removeStack(player.getInventory().selectedSlot, 1);
            cir.setReturnValue(ActionResult.SUCCESS);
        }
    }

    private boolean isBoss(MobEntity e) {
        return e instanceof net.minecraft.entity.mob.WardenEntity
            || e instanceof net.minecraft.entity.boss.dragon.EnderDragonEntity
            || e instanceof net.minecraft.entity.boss.WitherEntity
            || e instanceof net.minecraft.entity.boss.ElderGuardianEntity
            || e instanceof net.minecraft.entity.mob.RavagerEntity
            || e instanceof net.minecraft.entity.mob.EvokerEntity
            || e instanceof net.minecraft.entity.mob.ShulkerEntity;
    }

    private int getTameCost(MobEntity e) {
        if (e instanceof net.minecraft.entity.boss.dragon.EnderDragonEntity) return 8;
        if (e instanceof net.minecraft.entity.boss.WitherEntity)             return 7;
        if (e instanceof net.minecraft.entity.mob.WardenEntity)              return 5;
        if (e instanceof net.minecraft.entity.boss.ElderGuardianEntity)      return 4;
        return 3;
    }

    private String getBossName(MobEntity e) {
        if (e instanceof net.minecraft.entity.mob.WardenEntity)              return "Warden";
        if (e instanceof net.minecraft.entity.boss.dragon.EnderDragonEntity) return "Ender Dragon";
        if (e instanceof net.minecraft.entity.boss.WitherEntity)             return "Wither";
        if (e instanceof net.minecraft.entity.boss.ElderGuardianEntity)      return "Elder Guardian";
        if (e instanceof net.minecraft.entity.mob.RavagerEntity)             return "Ravager";
        if (e instanceof net.minecraft.entity.mob.EvokerEntity)              return "Evoker";
        if (e instanceof net.minecraft.entity.mob.ShulkerEntity)             return "Shulker";
        return "Jefe";
    }
}
