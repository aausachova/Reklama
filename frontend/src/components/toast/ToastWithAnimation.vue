<template>
    <div class="flex gap-3 items-center select-none">
        <LottieAnimation v-if="animationSrc" :src="animationSrc" :width="32" :height="32" renderer="canvas" />
        <div>
            <p class="font-medium">{{ message }}</p>
            <p v-if="description" class="text-muted-foreground">{{ description }}</p>
        </div>
    </div>
</template>
<script setup lang="ts">
import LottieAnimation from '@/components/animations/LottieAnimation.vue'

defineProps<{
    message: string
    description?: string
    animationSrc?: string
}>()
</script>
