<script setup lang="ts">
import type { Notification } from '@/types/notification'
import { formatDistanceToNow } from 'date-fns'
import { ru } from 'date-fns/locale'

defineProps<{
    notification: Notification
}>()
</script>

<template>
    <div class="group flex gap-4 p-3 rounded-lg hover:bg-muted transition-colors cursor-pointer">
        <div class="flex-shrink-0 mt-0.5 w-2">
            <span v-if="!notification.read"
                class="flex h-2 w-2 rounded-full bg-destructive transition-all group-hover:scale-110" />
        </div>

        <div class="flex-1 space-y-1">
            <div class="flex items-center justify-between gap-4">
                <p class="text-sm font-medium leading-none">
                    {{ notification.title }}
                </p>
                <time :datetime="notification.date" class="text-xs text-muted-foreground whitespace-nowrap">
                    {{ formatDistanceToNow(new Date(notification.date), { addSuffix: true, locale: ru }) }}
                </time>
            </div>
            <p class="text-sm text-muted-foreground line-clamp-2">
                {{ notification.description }}
            </p>
        </div>
    </div>
</template>
