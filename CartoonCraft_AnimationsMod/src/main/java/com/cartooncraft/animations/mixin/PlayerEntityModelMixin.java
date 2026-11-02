package com.cartooncraft.animations.mixin;

import com.cartooncraft.animations.CartoonTransformRegistry;
import net.minecraft.client.render.entity.model.PlayerEntityModel;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.player.PlayerEntity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(PlayerEntityModel.class)
public abstract class PlayerEntityModelMixin<T extends LivingEntity> {

    @Inject(method = "setAngles", at = @At("TAIL"))
    private void cartooncraft$setAngles(T entity,
                                        float limbAngle,
                                        float limbDistance,
                                        float animationProgress,
                                        float headYaw,
                                        float headPitch,
                                        CallbackInfo ci) {
        if (!(entity instanceof PlayerEntity)) {
            return;
        }

        PlayerEntityModel<?> model = (PlayerEntityModel<?>) (Object) this;
        if (model.body == null || model.head == null || model.leftArm == null || model.rightArm == null || model.leftLeg == null || model.rightLeg == null) {
            return;
        }

        model.body.pivotY += CartoonTransformRegistry.bodyBobY * 16.0F;
        model.head.pivotY += CartoonTransformRegistry.bodyBobY * 16.0F;

        model.leftArm.pitch += CartoonTransformRegistry.armSwingLeft;
        model.rightArm.pitch += CartoonTransformRegistry.armSwingRight;
        model.leftLeg.pitch += CartoonTransformRegistry.legSwingLeft;
        model.rightLeg.pitch += CartoonTransformRegistry.legSwingRight;

        model.body.pitch += CartoonTransformRegistry.bodyTilt;
        model.head.pitch += CartoonTransformRegistry.headNod;

        model.body.yScale = CartoonTransformRegistry.squashY;
        model.leftLeg.yScale = CartoonTransformRegistry.squashY;
        model.rightLeg.yScale = CartoonTransformRegistry.squashY;
    }
}
