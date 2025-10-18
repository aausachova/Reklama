<template>
    <section class="px-4">
        <div class="mb-3.5">
            <h1 class="text-2xl font-semibold mb-0">
                Газпром Академия –
            </h1>
            <p class="text-sm">
                актуальный календарь и платформа для хакатонов, ML соревнований, CTF и соревнований <br> по
                алгоритмическому программированию в России
            </p>
        </div>
        <div class=" bg-card border px-6 py-5  rounded-full mb-4  relative ">
            <span class=" text-2xl font-semibold"> Всей кейсы</span>
            <img class=" absolute right-8 -top-[100%]" src="/img/Present.png" />
        </div>
        <div v-if="pending" class="flex flex-col gap-4">
            <EventSkeleton v-for="i in 4" :key="i" />
        </div>
        <div v-else-if="events.length" class="flex flex-col gap-4">
            <EventCard v-for="event in events" :key="event.id" :event="event" />
        </div>
        <div v-else class="text-center py-8 text-muted-foreground">
            Нет доступных мероприятий
        </div>
    </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import EventCard from '@/components/events/EventCard.vue';
import EventSkeleton from '@/components/events/EventSkeleton.vue';
import { getEvents } from '@/api/events';
import type { Event } from '@/types/event';

const events = ref<Event[]>([]);
const pending = ref(true);

onMounted(async () => {
    try {
        events.value = await getEvents();
    } finally {
        pending.value = false;
    }
});
</script>
