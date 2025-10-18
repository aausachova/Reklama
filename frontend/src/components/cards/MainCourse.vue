<template>
    <Card class="relative flex h-full flex-col overflow-hidden sm:flex-row">

        <div class="flex w-full flex-col gap-6 p-6 sm:w-1/2">
            <CardHeader class="p-0">
                <CardTitle class="text-2xl font-semibold line-clamp-1">
                    {{ title }}
                </CardTitle>
                <CardDescription class="text-sm line-clamp-3">
                    {{ description }}
                </CardDescription>
            </CardHeader>
            <CardContent class="mt-auto p-0">
                <hr class="mb-4 border-t border-border" />
                <div class="flex justify-between text-sm text-muted-foreground">
                    <time :datetime="expiryDate">Доступен до {{ formattedExpiryDate }}</time>
                    <span>Уроков: {{ lessonsCompleted }}/{{ totalLessons }}</span>
                </div>
                <Button size="lg" class="mt-4 w-full font-semibold sm:w-auto"
                    aria-label="Продолжить курс по продуктовому менеджменту">
                    Продолжить курс
                </Button>
            </CardContent>
            <div class=" absolute top-4 right-4 py-3 px-7 bg-card border rounded-[22px] text-sm font-semibold  ">
                Extra
            </div>
        </div>
        <div class="hidden h-full w-1/2 bg-[url('/img/Card-1.png')] bg-cover bg-center bg-no-repeat sm:block"
            role="presentation"></div>
    </Card>
</template>

<script setup lang="ts">
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

import { Button } from '../ui/button';
import { computed } from 'vue';



interface CourseCardProps {
    title: string;
    description: string;
    expiryDate: string; 
    lessonsCompleted: number;
    totalLessons: number;
    badge: string;
}

const props = withDefaults(defineProps<CourseCardProps>(), {
    title: 'Продуктовый менеджмент',
    description:
        'Для специалистов, которые хотят овладеть актуальными компетенциями для управления продуктовым портфелем, создания и продвижения продукта',
    expiryDate: '2025-12-31',
    lessonsCompleted: 7,
    totalLessons: 20,
    badge: 'Extra',
});

const formattedExpiryDate = computed(() => {
    const date = new Date(props.expiryDate);
    return date.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' });
});

</script>

<style scoped></style>