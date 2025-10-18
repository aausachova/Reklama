<template>
    <div class="flex flex-col sm:flex-row bg-card gap-6 rounded-xl p-6 border cursor-pointer hover:bg-accent/5 transition-colors"
        @click="router.push(`/events/${event.id}`)">
        <div class="flex flex-col items-center gap-4 sm:min-w-[180px]">
            <img :src="event.company.logo" :alt="event.company.name" class="max-w-[120px]" />
            <p class="font-semibold">{{ event.company.name }}</p>
        </div>
        <div class="flex flex-col justify-between flex-1">
            <div class="w-full sm:w-2/3">
                <h3 class="font-semibold text-2xl mb-2">{{ event.title }}</h3>
                <p class="text-sm text-muted-foreground">{{ event.description }}</p>
            </div>
            <div
                class="flex flex-col sm:flex-row w-full justify-between items-start sm:items-end gap-4 sm:gap-0 mt-4 sm:mt-0">
                <p class="text-sm">Доступен: до
                    <span class="font-semibold">{{ event.endDate }}</span>
                </p>
                <div class="text-sm">
                    Кол-во решений:
                    <p>
                        <span class="font-semibold text-2xl">
                            {{ event.solutions.current }}
                        </span>
                        из {{ event.solutions.total }}
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import type { Event } from '@/types/event';

const props = defineProps<{
    event: Event
}>();

const router = useRouter();
</script>
