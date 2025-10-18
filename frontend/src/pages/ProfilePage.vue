<template>
    <section class="max-w-[1024px] h-full mx-auto p-4">
        <div class="grid grid-cols-1 lg:grid-cols-[280px_1fr] gap-6">
            <div class="flex flex-col items-center text-center space-y-3">
                <Avatar class="h-24 w-24">
                    <AvatarImage :src="'/'" :alt="authStore.user?.username" />
                    <AvatarFallback class="dark:bg-muted text-2xl font-bold bg-primary !text-white">
                        {{ userInitials }}
                    </AvatarFallback>
                </Avatar>
                <div class="space-y-1">
                    <h2 class="text-xl font-semibold">{{ authStore.user?.username }}</h2>
                    <p class="text-sm text-muted-foreground">{{ $t('profile.subtitle') }}</p>
                    <p class="text-[10px] text-muted-foreground/50 select-all">ID: {{ authStore.user?.id }}</p>
                </div>
                <Button variant="outline" class="w-full gap-2" @click="isEditing = true">
                    <Pencil class="size-4" />
                    {{ $t('profile.edit.button') }}
                </Button>
            </div>

            <div class="space-y-6 lg:border-l lg:pl-6">
                <div class="flex items-center gap-2">
                    <h2 class="text-2xl font-semibold">Профиль</h2>
                    <LottieAnimation :src="'/Eyes.tgs'" :height="40" :width="40" renderer="svg" />
                </div>

                <StatCard :stats="stats" />

                <div class="space-y-4">
                    <div class="flex items-center gap-2">
                        <Trophy class="size-5" />
                        <h3 class="font-semibold">Достижения</h3>
                    </div>
                    <p class="text-sm text-muted-foreground">Ваши заработанные достижения и награды</p>

                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                        <div v-for="achievement in achievements" :key="achievement.id"
                            class="dark:bg-input bg-white  group relative flex flex-col items-center p-4 rounded-lg border transition-all duration-200"
                            :class="[

                                achievement.unlocked
                                    ? 'bg-card hover:bg-accent/50'
                                    : 'bg-muted/50 hover:bg-muted opacity-50'
                            ]">
                            <div class="mb-3" :class="{ 'grayscale': !achievement.unlocked }">
                                <LottieAnimation :src="achievement.icon" :width="48" :height="48" renderer="svg"
                                    :disabled="!achievement.unlocked" />
                            </div>
                            <h3 class="font-medium text-sm text-center">{{ achievement.name }}</h3>
                            <p class="text-xs text-muted-foreground text-center mt-1">
                                {{ achievement.description }}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { Button } from '@/components/ui/button'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Pencil, Trophy } from 'lucide-vue-next'
import LottieAnimation from '@/components/animations/LottieAnimation.vue';
import StatCard from '@/components/statistics/StatCard.vue';


const authStore = useAuthStore()
const isEditing = ref(false)

const userInitials = computed(() => {
    if (!authStore.user?.username) return 'U'
    return authStore.user.username.slice(0, 1).toUpperCase()
})

const stats = computed(() => [
    {
        key: 'level',
        icon: '/Star.tgs',
        value: authStore.user?.level.toString() || '0',
        title: 'Уровень'
    },
    {
        key: 'achievements',
        icon: '/Trophy.tgs',
        value: authStore.user?.unlockedAchievementsCount.toString() || '0',
        title: 'Достижения'
    },
    {
        key: 'certificates',
        icon: '/Education.tgs',
        value: authStore.user?.certificatesCount.toString() || '0',
        title: 'Сертификаты'
    }
]);

const achievements = computed(() => authStore.user?.achievements || []);
</script>
