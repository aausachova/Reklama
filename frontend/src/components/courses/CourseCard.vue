<template>
    <div class="group  bg-card border rounded-xl overflow-hidden hover:border-primary/50 transition-colors">
        <div class="p-4 h-full flex flex-col justify-between ">
            <div class="flex gap-2 mb-4">
                <Badge>{{ getCategoryName(course.category) }}</Badge>
                <Badge variant="secondary">{{ course.experience_level }}</Badge>
            </div>

            <div class="flex items-center justify-center   relative rounded-lg overflow-hidden mb-4">
                <img :src="getCourseImage(course)" :alt="course.title" class=" max-w-full h-auto  " />
            </div>
            <h3 class="text-xl font-semibold line-clamp-2 mb-4">{{ course.title }}</h3>

            <div>
                <div class="space-y-2">
                    <Progress :model-value="(course.completed_lessons / course.total_lessons) * 100" />
                    <div class="flex justify-between text-sm text-muted-foreground">
                        <span>{{ course.duration }} часов</span>
                        <span>Уроков {{ course.completed_lessons }}/{{ course.total_lessons }}</span>
                    </div>
                </div>

                <div class="flex gap-2 mt-4">
                    <Button variant="outline" class="flex-1" @click.stop="$emit('openDetails', course)">
                        О курсе
                    </Button>
                    <Button class="flex-1" v-if="!course.is_participant" @click.stop="joinCourse(course)">Поступить</Button>
                    <Button class="flex-1" v-else disabled>Заявка подана</Button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import apiClient from '@/lib/axios';
import type { Course } from '@/types/course';

defineProps<{
    course: Course
}>();

defineEmits<{
    openDetails: [course: Course]
}>();

const joinCourse = async (course: Course) => {
    await apiClient.post(`/api/courses/enroll`, { course_id: course.id });
    course.is_participant = true
};

const getCourseImage = (course: Course) => {
    if(course.experience_level === 'Без опыта') return '/img/Card-2.png';
    return '/img/Card-1.png';
};

const getCategoryName = (id: string) => {
    const categories: Record<string, string> = {
        'ai': 'Искусственный интеллект',
        'tech': 'Современные технологии',
        'dev': 'Разработка',
        'business': 'Бизнес'
    };
    return categories[id] || id;
};
</script>
