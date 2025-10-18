<template>
    <section class="dot-pattern min-h-screen w-full bg-background place-items-center px-4 overflow-hidden grid">
        <div class="grid lg:grid-cols-2 items-center gap-8 max-w-[700px] w-full">
            <LottieAnimation class="mx-auto" :src="animationSrc" :height="250" :width="250" renderer="svg" />

            <div class="text-center lg:text-left space-y-4 order-1 lg:order-2">
                <h1 class="text-7xl sm:text-8xl font-bold tracking-tight text-primary bg-clip-text ">
                    {{ errorCode }}
                </h1>
                <div class="space-y-6">
                    <p class="text-xl text-muted-foreground">
                        {{ $t(errorMessage) }}
                    </p>
                    <Button asChild variant="outline" size="lg"
                        class="gap-2 transition-colors hover:bg-primary hover:text-primary-foreground dark:hover:text-foreground">
                        <RouterLink to="/">
                            <ArrowLeft class="w-4 h-4" />
                            {{ $t('error.backHome') }}
                        </RouterLink>
                    </Button>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-vue-next';
import LottieAnimation from '@/components/animations/LottieAnimation.vue';

interface Props {
    errorCode?: string;
    errorMessage?: string;
    animationSrc?: string;
}

withDefaults(defineProps<Props>(), {
    errorCode: '404',
    errorMessage: '',
    animationSrc: '/SearchingDuck.tgs',
});

</script>

<style scoped>
/*.dot-pattern {
    --dot-color: #5f5f5f;
    --dot-size: 1px;

    --dot-space: 22px;
    --gradient-color: var(--background);
    background: radial-gradient(circle, transparent 0%, var(--gradient-color) 100%),
        linear-gradient(90deg, var(--gradient-color) calc(var(--dot-space) - var(--dot-size)), transparent 1%) center / var(--dot-space) var(--dot-space),
        linear-gradient(var(--gradient-color) calc(var(--dot-space) - var(--dot-size)), transparent 1%) center / var(--dot-space) var(--dot-space),
        var(--dot-color);
} */
</style>