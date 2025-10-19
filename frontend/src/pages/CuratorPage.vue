<template>
  <div class="p-6 bg-[#0f0f10] text-white min-h-screen">
<div class="my-5 flex flex-wrap justify-between items-center gap-3">
    <h1 class="text-2xl font-bold mb-6">Панель управления</h1>

   
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
      <Card
        v-for="item in stats.slice(0, 3)"
        :key="item.label"
        class="bg-[#1a1a1c] border-0 px-6 py-4 flex flex-col justify-between"
      >
        <div>
          <CardTitle class="text-sm text-primary mb-1">{{ item.label }}</CardTitle>
          <p class="text-4xl font-semibold text-white">{{ item.value }}</p>
        </div>
      </Card>

      <Card
        class="bg-[#1a1a1c] border-0 px-6 py-4 flex flex-col justify-center items-center gap-3"
      >
        <Button   variant="outline" class="w-full bg-primary text-white hover:bg-primary/80">
          <PlusIcon class="w-4 h-4 mr-2" /> Подать заявку
        </Button>
        <Button
         variant="outline"
          class="w-full bg-[#2a2a2d] hover:bg-[#333] text-white"
        >
          <DownloadIcon class="w-4 h-4 mr-2" /> Загрузить Excel
        </Button>
        <Button
          variant="outline"
          class="w-full border-[#444] text-white hover:bg-[#222]"
        >
          <UploadIcon class="w-4 h-4 mr-2" /> Экспортировать Excel
        </Button>
      </Card>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-6 items-start">
      <Card class="bg-[#1a1a1c] border-0 p-4 flex flex-col lg:col-span-3">
        <CardTitle class="text-lg mb-3 text-white">Требуют действий</CardTitle>
        <div class="flex flex-col gap-3">
          <div
            v-for="task in actions"
            :key="task.label"
            class="flex justify-between items-center bg-card rounded-xl px-4 py-3 text-sm"
          >
            <p>{{ task.label }}</p>
            <Button variant="ghost" class="text-primary hover:text-white">
              {{ task.action }}
            </Button>
          </div>
        </div>
      </Card>

      <Card
        class="bg-[#1a1a1c] border-0 p-4 flex flex-col justify-between lg:col-span-1"
      >
        <CardTitle class="text-lg mb-4 text-white text-center">
          Календарь окон практик
        </CardTitle>
        <div class="flex justify-center items-center flex-1">
          <RangeCalendar    v-model="value"
            class="rounded-lg bg-[#252527] text-white border border-[#333] p-2 w-full max-w-[280px]"
          />
        </div>
      </Card>
    </div>

    <Card class="bg-[#1a1a1c] border-0 p-5">
      <div class="flex justify-between items-center mb-4">
        <CardTitle class="text-lg text-white">Кадровый резерв</CardTitle>
        <p class="text-sm text-muted-foreground">6 месяцев</p>
      </div>

      <div class="flex flex-col gap-3">
        <div v-for="(bar, index) in reserveBars" :key="index" class="w-full">
          <p class="text-sm mb-1">{{ bar.label }}</p>
          <div class="w-full bg-[#2d2d30] rounded-xs  h-4">
            <div
              class="h-4  rounded-xs "
              :class="bar.color"
              :style="{ width: bar.value + '%' }"
            />
          </div>
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { Card, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { RangeCalendar } from "@/components/ui/range-calendar"
import type { Ref } from "vue"
import { getLocalTimeZone, today } from "@internationalized/date"

import { DownloadIcon, PlusIcon, UploadIcon } from "lucide-vue-next"
import type { DateRange } from "reka-ui"

// вычисляем дату 5 дней назад
const start = today(getLocalTimeZone())
const end = start.add({ days: 7 })

const value = ref({
  start,
  end,
}) as Ref<DateRange>
// Статистика
const stats = [
  { label: "Активных стажировок", value: 4 },
  { label: "Поступило заявок от резидентов", value: 35 },
  { label: "Открыто запросов от кандидатов", value: 68 },
  { label: "", value: "" },
]

// Действия
const actions = [
  { label: "Черновики с ошибками", action: "Перейти к редактированию" },
  { label: "На модерации у ОЭЗ Технополис Москва", action: "Ожидаем решения" },
  { label: "Есть входящие сообщения", action: "Перейти в чат" },
]

// Бар-чарт кадрового резерва
const reserveBars = [
  { label: "Производство", value: 90, color: "bg-blue-500" },
  { label: "Медицина", value: 70, color: "bg-pink-500" },
  { label: "Финансы", value: 60, color: "bg-yellow-400" },
  { label: "Data Science", value: 85, color: "bg-green-500" },
]
</script>
