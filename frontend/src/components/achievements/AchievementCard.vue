<template>
    <div class="achievement-card-wrapper w-full h-[324px]">
        <div class="achievement-card">
            <div class="achievement-front rounded-lg">
                <div class="relative flex items-center justify-center mb-6">
                    <div class="bg-muted/50 rounded-full size-[120px] flex items-center justify-center">
                        <img :src="icon" :alt="name" class="size-16" />
                    </div>
                    <div v-if="level" class="absolute -bottom-3 text-nowrap rounded-full px-3 py-0.5 text-sm font-medium"
                        :class="levelClasses[levelKey]">
                        {{ levelText }}
                    </div>
                </div>

                <h3 class="font-semibold text-lg mb-6">{{ name }}</h3>

                <div class="text-sm text-muted-foreground mt-2.5">
                    {{ levelDisplay }}
                </div>
            </div>

            <div class="achievement-back bg-accent p-6 flex flex-col h-full rounded-lg">
                <h3 class="font-semibold text-lg mb-6">{{ name }}</h3>
                <p class="text-sm text-muted-foreground mb-auto">
                    {{ description }}
                </p>
                <time v-if="date" class="text-xs text-muted-foreground">
                    Получено: {{ formatDate(date) }}
                </time>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

type AchievementLevel = 'junior' | 'strong_junior' | 'middle' | 'strong_middle' | 'senior';

const props = defineProps<{
    name: string;
    subtitle: string;
    level?: AchievementLevel;
    icon: string;
    description: string;
    date?: string;
}>();

const levelMapper: Record<AchievementLevel, string> = {
    junior: '1/5',
    strong_junior: '2/5',
    middle: '3/5',
    strong_middle: '4/5',
    senior: '5/5'
};

const levelClasses: Record<AchievementLevel, string> = {
    junior: 'bg-blue-100 text-blue-800 border-blue-200',
    strong_junior: 'bg-green-100 text-green-800 border-green-200',
    middle: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    strong_middle: 'bg-orange-100 text-orange-800 border-orange-200',
    senior: 'bg-purple-100 text-purple-800 border-purple-200'
};

const levelTextMapper: Record<AchievementLevel, string> = {
    junior: 'Junior',
    strong_junior: 'Strong Junior',
    middle: 'Middle',
    strong_middle: 'Strong Middle',
    senior: 'Senior'
};

const levelKey = computed(() => props.level?.toLowerCase() as AchievementLevel);
const levelDisplay = computed(() => levelMapper[levelKey.value]);
const levelText = computed(() => levelTextMapper[levelKey.value] || props.subtitle);

const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
};
</script>

<style scoped>
/* Стили остаются без изменений */
.achievement-card-wrapper {
    perspective: 1000px;
}

.achievement-card {
    position: relative;
    width: 100%;
    height: 100%;
    transition: transform 0.6s;
    transform-style: preserve-3d;
    cursor: pointer;
}

.achievement-card-wrapper:hover .achievement-card {
    transform: rotateY(180deg);
}

.achievement-front,
.achievement-back {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    border: 1px solid var(--border);
}

.achievement-front {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: var(--card);
}

.achievement-back {
    transform: rotateY(180deg);
}
</style>