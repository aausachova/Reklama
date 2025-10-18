<template>
    <Popover>
        <PopoverTrigger as-child>
            <Button variant="outline" class="relative bg-card h-8 w-8 p-0">
                <BellIcon class="size-4" />
                <span v-if="hasUnread"
                    class="absolute -right-0.5 -top-0.5 flex h-2.5 w-2.5 items-center justify-center rounded-full bg-destructive ring-2 ring-background" />
            </Button>
        </PopoverTrigger>

        <PopoverContent align="end" :class="[
            'p-0',
            appStore.isMobile ? 'w-[92vw]' : 'w-[380px]'
        ]">
            <div class="flex items-center justify-between border-b px-4 py-3">
                <h2 class="font-medium">Уведомления</h2>
                <span class="text-xs text-muted-foreground">
                    {{ unreadCount }} новых
                </span>
            </div>

            <ScrollArea class="h-[calc(var(--vh,1vh)*50)]">
                <div class="px-1 py-2">
                    <template v-if="isLoading">
                        <div v-for="i in 6" :key="i" class="space-y-2 p-3">
                            <Skeleton class="h-5 w-[60%]" />
                            <Skeleton class="h-4 w-[80%]" />
                        </div>
                    </template>

                    <template v-else-if="notifications.length > 0">
                        <NotificationItem v-for="notification in notifications" :key="notification.id"
                            :notification="notification" />
                    </template>

                    <template v-else>
                        <div class="flex flex-col items-center justify-center py-8 px-4">
                            <p class="text-sm text-muted-foreground text-center">
                                У вас пока нет уведомлений
                            </p>
                        </div>
                    </template>
                </div>
            </ScrollArea>
        </PopoverContent>
    </Popover>
</template>



<script setup lang="ts">
import { BellIcon } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { ScrollArea } from '../ui/scroll-area'
import type { Notification } from '@/types/notification'
import { onMounted, ref, computed } from 'vue'
import NotificationItem from './NotificationItem.vue'
import { useAppStore } from '@/stores/appStore'

const appStore = useAppStore()

const isLoading = ref(true)
const notifications = ref<Notification[]>([])
const unreadCount = computed(() =>
    notifications.value.filter(n => !n.read).length
)

const hasUnread = computed(() => unreadCount.value > 0)

async function fetchNotifications() {
    isLoading.value = true
    await new Promise(resolve => setTimeout(resolve, 1500))

    notifications.value = [
        {
            id: 1,
            title: 'Новое сообщение',
            description: 'Александр отправил вам новое сообщение по проекту "Разработка UI компонентов"',
            date: new Date(Date.now() - 1000 * 60 * 2).toISOString(),
            read: false
        },
        {
            id: 2,
            title: 'Обновление системы',
            description: 'Доступно новое обновление системы. Рекомендуем обновиться для получения новых функций и исправлений.',
            date: new Date(Date.now() - 1000 * 60 * 60).toISOString(),
            read: true
        },
        {
            id: 3,
            title: 'Завершение задачи',
            description: 'Задача "Создание компонента уведомлений" была успешно завершена',
            date: new Date(Date.now() - 1000 * 60 * 60 * 3).toISOString(),
            read: false
        }
    ]

    isLoading.value = false
}

onMounted(() => {
    fetchNotifications()
})

</script>