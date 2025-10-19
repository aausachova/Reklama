<template>
    <section v-if="authStore.user.role !== 'moderator'" class="px-6 py-4">
        <div class="flex mb-4 items-center justify-between flex-wrap gap-3">
            <div>
                <h1 class="text-2xl font-semibold mb-1">
                    {{ pageTitle }}
                </h1>
                <p class="text-sm text-muted-foreground">
                    {{ pageDescription }}
                </p>
            </div>

            <div class="flex items-center gap-3">
                <RouterLink class="text-sm font-medium py-1.5 px-3 rounded-full transition"
                    :class="{ 'bg-accent text-white': $route.path === '/vacancies', 'hover:bg-muted': $route.path !== '/vacancies' }">
                    Вакансии
                </RouterLink>

                <RouterLink class="text-sm font-medium py-1.5 px-3 rounded-full transition"
                    :class="{ 'bg-accent text-white': $route.path === '/analytics', 'hover:bg-muted': $route.path !== '/analytics' }">
                    Аналитика
                </RouterLink>
            </div>
        </div>

        <div class="grid gap-4 lg:grid-cols-4 rounded-[32px]">
            <Card class="lg:col-span-3">
                <CardHeader class="flex justify-between items-center flex-wrap gap-3">
                    <div>
                        <CardTitle class="text-xl font-semibold">Показатели по найму</CardTitle>
                        <CardDescription>Динамика вакансий и откликов за период</CardDescription>
                    </div>

                    <div class="flex items-center gap-3 overflow-x-auto">
                        <Button variant="outline" class="bg-transparent shrink-0 whitespace-nowrap"
                            :class="{ 'bg-accent text-white': chartPeriod === 'month' }" @click="chartPeriod = 'month'">
                            30 дней
                        </Button>
                        <Button variant="outline" class="bg-transparent shrink-0 whitespace-nowrap"
                            :class="{ 'bg-accent text-white': chartPeriod === 'quarter' }"
                            @click="chartPeriod = 'quarter'">
                            3 месяца
                        </Button>
                    </div>
                </CardHeader>

                <CardContent class="h-full">
                    <div class="w-full h-[440px]">
                        <AreaChart :period="chartPeriod" />
                    </div>
                </CardContent>
            </Card>

            <div class="flex flex-col gap-4">
                <Card>
                    <CardHeader>
                        <CardTitle>Активные вакансии</CardTitle>
                        <CardDescription>Количество открытых позиций</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <p class="text-3xl font-bold">128</p>
                        <p class="text-xs text-muted-foreground">+14% за последний месяц</p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle> Кандидаты</CardTitle>
                        <CardDescription>Новые отклики</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <p class="text-3xl font-bold">312</p>
                        <p class="text-xs text-muted-foreground">-5% по сравнению с прошлым месяцем</p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle> Стажировки</CardTitle>
                        <CardDescription>Активные предложения от вузов</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <p class="text-3xl font-bold">42</p>
                        <p class="text-xs text-muted-foreground">6 новых за неделю</p>
                    </CardContent>
                </Card>
            </div>

            <Card class="lg:col-span-4">
                <CardHeader class="flex justify-between items-center flex-wrap gap-3">
                    <CardTitle>Последние активности</CardTitle>
                    <CardDescription>Обновления за последние 7 дней</CardDescription>
                </CardHeader>
                <CardContent>
                    <ul class="text-sm space-y-2">
                        <li class="flex justify-between items-center border-b pb-2">
                            <span>Компания «Нейротех» открыла вакансию <b>ML-инженер</b></span>
                            <span class="text-muted-foreground text-xs">2 часа назад</span>
                        </li>
                        <li class="flex justify-between items-center border-b pb-2">
                            <span>Добавлена стажировка от МГТУ по направлению «Frontend»</span>
                            <span class="text-muted-foreground text-xs">вчера</span>
                        </li>
                        <li class="flex justify-between items-center border-b pb-2">
                            <span>Пользователь <b>Иван Петров</b> получил оффер от компании «РосДрон»</span>
                            <span class="text-muted-foreground text-xs">3 дня назад</span>
                        </li>
                    </ul>
                </CardContent>
            </Card>
        </div>
    </section>
    <ModeratorPage v-else/>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { Button } from '@/components/ui/button'
import { Card, CardDescription, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import AreaChart from '@/components/charts/AreaChart.vue'
import { useAuthStore } from '@/stores/authStore'
import ModeratorPage from './ModeratorPage.vue'

const route = useRoute()
const chartPeriod = ref<'month' | 'quarter'>('month')
const authStore = useAuthStore()
const pageTitle = 'Панель управления'
const pageDescription = 'Единое пространство для мониторинга вакансий, кандидатов и стажировок'
</script>
