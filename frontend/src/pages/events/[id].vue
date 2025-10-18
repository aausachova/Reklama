<template>
    <section class="px-6 py-10 max-w-6xl mx-auto">
        <!-- Назад -->
        <div class="mb-8">
            <Button variant="ghost" @click="router.back()" class="flex items-center gap-2">
                <ArrowLeft class="w-4 h-4" />
                Назад к вакансиям
            </Button>
        </div>

        <div v-if="vacancy" class="grid lg:grid-cols-3 gap-8">
            <!-- Основная информация -->
            <Card class="lg:col-span-2 p-6 shadow-sm">
                <CardHeader>
                    <CardTitle class="text-2xl font-semibold mb-2">{{ vacancy.title }}</CardTitle>
                    <CardDescription class="text-base text-muted-foreground">
                        {{ vacancy.company }} · {{ vacancy.city }}
                    </CardDescription>
                </CardHeader>

                <CardContent>
                    <div class="mt-6 space-y-4">
                        <div class="flex items-center justify-between">
                            <p class="text-lg font-semibold text-primary">
                                {{ vacancy.salary.toLocaleString() }} ₽
                            </p>
                            <span class="text-sm text-muted-foreground">
                                Опубликовано: {{ formatDate(vacancy.date) }}
                            </span>
                        </div>

                        <Separator />

                        <div>
                            <h3 class="text-base font-semibold mb-2">Описание</h3>
                            <p class="text-sm text-muted-foreground leading-relaxed">
                                {{ vacancy.description }}
                            </p>
                        </div>

                        <div v-if="vacancy.requirements?.length">
                            <h3 class="text-base font-semibold mb-2">Требования</h3>
                            <ul class="list-disc list-inside text-sm text-muted-foreground space-y-1">
                                <li v-for="(req, index) in vacancy.requirements" :key="index">
                                    {{ req }}
                                </li>
                            </ul>
                        </div>

                        <div v-if="vacancy.responsibilities?.length">
                            <h3 class="text-base font-semibold mb-2">Обязанности</h3>
                            <ul class="list-disc list-inside text-sm text-muted-foreground space-y-1">
                                <li v-for="(task, index) in vacancy.responsibilities" :key="index">
                                    {{ task }}
                                </li>
                            </ul>
                        </div>

                        <div class="pt-6">
                            <Button size="lg" class="w-full sm:w-auto">Откликнуться на вакансию</Button>
                        </div>
                    </div>
                </CardContent>
            </Card>

            <!-- Информация о компании -->
            <Card class="p-6 bg-muted/40 shadow-sm">
                <div class="flex items-center gap-3 mb-4">
                    <div
                        class="w-12 h-12 bg-primary/10 text-primary flex items-center justify-center rounded-full font-semibold text-lg">
                        {{ vacancy.company[0] }}
                    </div>
                    <div>
                        <h3 class="text-lg font-semibold">{{ vacancy.company }}</h3>
                        <p class="text-sm text-muted-foreground">{{ companyInfo.industry }}</p>
                    </div>
                </div>

                <p class="text-sm text-muted-foreground mb-4">
                    {{ companyInfo.about }}
                </p>

                <div class="text-sm space-y-1">
                    <p><span class="font-medium">Сайт:</span>
                        <a :href="companyInfo.website" target="_blank" class="text-primary hover:underline">
                            {{ companyInfo.website }}
                        </a>
                    </p>
                    <p><span class="font-medium">Город:</span> {{ vacancy.city }}</p>
                </div>
            </Card>
        </div>

        <div v-else class="text-center py-16 text-muted-foreground">
            Вакансия не найдена
        </div>
    </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { ArrowLeft } from 'lucide-vue-next'

type Vacancy = {
    id: number
    title: string
    company: string
    city: string
    description: string
    salary: number
    date: string
    requirements?: string[]
    responsibilities?: string[]
}

type CompanyInfo = {
    about: string
    website: string
    industry: string
}

const route = useRoute()
const router = useRouter()
const vacancy = ref<Vacancy | null>(null)

const mockVacancies: Vacancy[] = [
    {
        id: 1,
        title: 'Frontend-разработчик (Vue 3)',
        company: 'Технополис Москва',
        city: 'Москва',
        description:
            'Разработка клиентской части внутренних сервисов и интерфейсов на Vue 3, TypeScript и Tailwind.',
        salary: 180000,
        date: '2025-10-10',
        requirements: [
            'Опыт работы с Vue 3 и Composition API',
            'Уверенное владение TypeScript',
            'Понимание принципов адаптивной верстки',
        ],
        responsibilities: [
            'Разработка и поддержка UI-компонентов',
            'Интеграция с REST API',
            'Участие в code review и планировании спринтов',
        ],
    },
    {
        id: 2,
        title: 'Backend-разработчик (Go)',
        company: 'CyberFlow',
        city: 'Санкт-Петербург',
        description:
            'Разработка микросервисов и API на Go, интеграции с ML-системами и мониторингом данных.',
        salary: 230000,
        date: '2025-09-30',
        requirements: ['Go, PostgreSQL, Docker', 'Понимание REST и gRPC'],
        responsibilities: ['Создание API', 'Тестирование и CI/CD'],
    },
]

const companyInfo = ref<CompanyInfo>({
    about:
        'Компания занимается разработкой цифровых решений для промышленности и автоматизации процессов.',
    website: 'https://example.com',
    industry: 'Информационные технологии',
})

function formatDate(date: string) {
    return new Date(date).toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: 'long',
        year: 'numeric',
    })
}


</script>
