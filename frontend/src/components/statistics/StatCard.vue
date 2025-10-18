<template>
    <div class="flex flex-wrap gap-4 lg:ml-auto w-full lg:w-auto">
        <div v-for="stat in stats" :key="stat.key"
            class="dark:bg-input bg-white text-card-foreground rounded-lg border p-4 flex-1 lg:w-[180px] min-w-[150px]">
            <div class="flex flex-col gap-1">
                <div class="flex items-center gap-2 text-sm font-medium">
                    <LottieAnimation :disabled="true" :src="stat.icon" :height="20" :width="20" renderer="svg" />
                    {{ stat.title }}
                </div>
                <div class="text-2xl font-bold mt-1">{{ stat.value }}</div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import LottieAnimation from '@/components/animations/LottieAnimation.vue';

interface Stat {
    key: string;
    icon: string;
    value: string;
    title: string;
}

defineProps<{
    stats: Stat[]
}>();
</script>
