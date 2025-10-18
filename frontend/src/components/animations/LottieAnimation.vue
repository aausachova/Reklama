<template>
    <div ref="container" :style="{ width: width + 'px', height: height + 'px' }" @click="handleClick"
        :class="{ 'cursor-pointer': !repeat && !disabled }" />
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';
import lottie, { type AnimationItem } from 'lottie-web';
import { useWindowFocus } from '@vueuse/core';
import { animationCache } from '@/services/animationCache';

const props = defineProps<{
    src?: string;
    width?: number;
    height?: number;
    repeat?: boolean;
    renderer?: 'svg' | 'canvas';
    json?: object;
    disabled?: boolean; 
}>();

const container = ref<HTMLElement | null>(null);
let animation: AnimationItem | null = null;
const isCompleted = ref(false);
const isPlaying = ref(false);
const windowFocus = useWindowFocus();
const wasPlayingBeforeBlur = ref(false);

watch(windowFocus, (isFocused) => {
    if (props.disabled || !animation) return;

    if (isFocused) {
        if (wasPlayingBeforeBlur.value && animation.isPaused) {
            animation.play();
            isPlaying.value = true;
        }
    } else {
        wasPlayingBeforeBlur.value = isPlaying.value;
        if (!animation.isPaused) {
            animation.pause();
            isPlaying.value = false;
        }
    }
});

const restartAnimation = () => {
    if (props.disabled || !animation) return;

    isCompleted.value = false;
    isPlaying.value = true;
    animation.goToAndPlay(0);
};

const handleClick = () => {
    if (props.disabled || props.repeat || isPlaying.value) return;

    restartAnimation();
};

const loadAnimation = async () => {
    try {
        let animationData: any;

        if (props.json) {
            animationData = props.json;
        } else if (props.src) {
            animationData = await animationCache.getAnimation(props.src);
        } else {
            throw new Error('Either src or json prop must be provided');
        }

        if (container.value) {
            animation = lottie.loadAnimation({
                container: container.value,
                renderer: props.renderer || 'svg',
                loop: props.repeat ?? false,
                autoplay: !props.disabled && windowFocus.value,
                animationData,
            });


            if (props.disabled) {
                animation.goToAndStop(0);
            } else {
                animation.addEventListener('complete', () => {
                    isCompleted.value = true;
                    isPlaying.value = false;
                });

                animation.addEventListener('enterFrame', () => {
                    if (!animation?.isPaused) {
                        isPlaying.value = true;
                    }
                });
            }
        }
    } catch (error) {
        console.error('Failed to load animation:', error);
    }
};

onMounted(() => {
    loadAnimation();
});

onUnmounted(() => {
    if (animation) {
        animation.destroy();
        animation = null;
    }
});
</script>