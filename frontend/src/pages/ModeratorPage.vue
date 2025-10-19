<template>
  <section class="px-6 py-4">
    <div class="flex mb-4 items-center justify-between flex-wrap gap-3">
      <div>
        <h1 class="text-2xl font-semibold mb-1">
          {{ pageTitle }}
        </h1>
       
      </div>

   
    </div>

    <div class="grid gap-4 lg:grid-cols-4 rounded-[32px]">
      <!-- Левая часть -->
      <Card class="lg:col-span-3">
        <CardHeader class="flex justify-between items-center flex-wrap gap-3">
          <div>
            <CardTitle class="text-xl font-semibold">Вакансии на модерации</CardTitle>
          </div>
        </CardHeader>

        <CardContent class="h-full">
          <div v-if="pending" class="text-muted-foreground text-sm">Загрузка...</div>
          <div v-else-if="error" class="text-destructive text-sm">{{ error }}</div>

          <div v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-2">
            <Card
              v-for="vacancy in inactiveVacancies"
              :key="vacancy.id"
              class="border rounded-xl p-4 flex flex-col justify-between"
            >
              <div>
                <div class="flex justify-between items-start mb-2">
                  <CardTitle class="text-base font-semibold">
                    {{ vacancy.title }}
                  </CardTitle>
                  <p class="text-xs text-muted-foreground">{{ vacancy.city }}</p>
                </div>

                <p class="text-sm text-muted-foreground mb-3">
                  {{ vacancy.company }} — {{ vacancy.direction }}
                </p>
              </div>

              <div class="mt-3 grid grid-cols-2 gap-2">
                <Button @click="openVacancy(vacancy.id)" class="w-full">Открыть</Button>
                <Button
                  variant="outline"
                  class="w-full"
                  @click="deleteVacancy(vacancy.id)"
                >
                  Удалить
                </Button>
              </div>
            </Card>

            <p
              v-if="inactiveVacancies.length === 0 && !pending"
              class="text-center text-muted-foreground col-span-full py-6"
            >
              Нет вакансий на модерации
            </p>
          </div>
        </CardContent>
      </Card>

      <!-- Правая часть -->
      <div class="flex flex-col gap-4">
        <Card>
          <CardHeader>
            <CardTitle>Активные вакансии</CardTitle>
            <CardDescription>Количество открытых позиций</CardDescription>
          </CardHeader>
          <CardContent>
            <p class="text-3xl font-bold">{{ activeCount }}</p>
            <p class="text-xs text-muted-foreground">+14% за последний месяц</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Кандидаты</CardTitle>
            <CardDescription>Новые отклики</CardDescription>
          </CardHeader>
          <CardContent>
            <p class="text-3xl font-bold">312</p>
            <p class="text-xs text-muted-foreground">-5% по сравнению с прошлым месяцем</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Стажировки</CardTitle>
            <CardDescription>Активные предложения от вузов</CardDescription>
          </CardHeader>
          <CardContent>
            <p class="text-3xl font-bold">42</p>
            <p class="text-xs text-muted-foreground">6 новых за неделю</p>
          </CardContent>
        </Card>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { Button } from '@/components/ui/button'
import { Card, CardDescription, CardHeader, CardTitle, CardContent } from '@/components/ui/card'

const pageTitle = 'Модерация'

const router = useRouter()
const route = useRoute()

const vacancies = ref<any[]>([])
const pending = ref(false)
const error = ref<string | null>(null)

async function fetchVacancies() {
  pending.value = true
  error.value = null
  try {
    const { data } = await axios.get('/api/vacancy/')
    vacancies.value = Array.isArray(data) ? data : []
  } catch (e) {
    console.error('Ошибка при загрузке вакансий:', e)
    error.value = 'Не удалось загрузить вакансии'
  } finally {
    pending.value = false
  }
}

const inactiveVacancies = computed(() => vacancies.value.filter(v => v.active === false))
const activeCount = computed(() => vacancies.value.filter(v => v.active === true).length)

async function deleteVacancy(id: string) {
  if (!confirm('Вы уверены, что хотите удалить эту вакансию?')) return
  try {
    await axios.delete(`/api/vacancy/${id}`)
    vacancies.value = vacancies.value.filter(v => v.id !== id)
  } catch (e) {
    console.error('Ошибка при удалении вакансии:', e)
    alert('Не удалось удалить вакансию')
  }
}

function openVacancy(id: string) {
  router.push(`/vacancies/${id}`)
}

onMounted(() => {
  fetchVacancies()
})
</script>
