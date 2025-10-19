<template>
  <section class="px-4 pb-10">
    <div class="my-5 flex flex-wrap justify-between items-center gap-3">
      <h1 class="text-2xl font-semibold">Стажировки</h1>

      <Button
      
        @click="goToCreate"
     
      >
      
  {{ isCurator ? 'Связаться с резидентом' : 'Связаться с куратором' }}      </Button>
    </div>

    <!-- 🔽 Фильтры -->
    <div class="flex flex-wrap gap-3 items-center mb-6">
      <!-- Поиск по программе -->
      <div class="flex items-center flex-grow min-w-[250px] relative">
        <Search class="absolute left-3 text-muted-foreground w-4 h-4" />
        <Input
          v-model="search"
          placeholder="Поиск по программе"
          class="pl-9 w-full"
        />
      </div>

      <Select v-model="selectedDirection">
        <SelectTrigger class="w-[180px]">
          <SelectValue placeholder="Направление" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">Все направления</SelectItem>
          <SelectItem
            v-for="d in filters.direction"
            :key="d"
            :value="d"
          >
            {{ d }}
          </SelectItem>
        </SelectContent>
      </Select>

      <Select v-model="selectedCourse">
        <SelectTrigger class="w-[180px]">
          <SelectValue placeholder="Курс" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">Все курсы</SelectItem>
          <SelectItem
            v-for="c in filters.course"
            :key="c"
            :value="c"
          >
            {{ c }}
          </SelectItem>
        </SelectContent>
      </Select>

      <Select v-model="selectedPeriod">
        <SelectTrigger class="w-[180px]">
          <SelectValue placeholder="Период" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">Все периоды</SelectItem>
          <SelectItem
            v-for="p in filters.period"
            :key="p"
            :value="p"
          >
            {{ p }}
          </SelectItem>
        </SelectContent>
      </Select>

      <div class="flex items-center space-x-2">
        <Checkbox id="reserved" v-model:checked="isReserved" />
        <label
          for="reserved"
          class="text-sm font-medium leading-none cursor-pointer select-none"
        >
          Бронь от компании
        </label>
      </div>
    </div>

    <div v-if="pending" class="text-muted-foreground text-sm">Загрузка...</div>
    <div v-else-if="error" class="text-destructive text-sm">{{ error }}</div>

    <div v-else class="overflow-x-auto rounded-2xl border">
      <table class="min-w-full text-sm border-collapse">
        <thead class="bg-muted/50 text-left">
          <tr>
            <th class="px-4 py-3 font-semibold text-foreground">Программа обучения</th>
            <th class="px-4 py-3 font-semibold text-foreground whitespace-nowrap">Дата начала</th>
            <th class="px-4 py-3 font-semibold text-foreground whitespace-nowrap">Дата окончания</th>
            <th class="px-4 py-3 font-semibold text-foreground whitespace-nowrap text-center">Кол-во студентов</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="intern in filteredInterns"
            :key="intern.study_program"
            class="border-t hover:bg-muted/30 transition"
          >
            <td class="px-4 py-3">{{ intern.study_program }}</td>
            <td class="px-4 py-3 whitespace-nowrap">{{ formatDate(intern.start_date) }}</td>
            <td class="px-4 py-3 whitespace-nowrap">{{ formatDate(intern.end_date) }}</td>
            <td class="px-4 py-3 text-center">{{ intern.students_count }}</td>
           
          </tr>
        </tbody>
      </table>

      <div v-if="!filteredInterns.length" class="text-center py-8 text-muted-foreground">
        Нет данных для отображения
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from "vue"
import { useRouter, useRoute } from "vue-router"
import { Input } from "@/components/ui/input"
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import { Search } from "lucide-vue-next"
import Button from "@/components/ui/button/Button.vue"
import { useRoles } from "@/composables/usePermissions"

import axios from "axios"

const { isCurator } = useRoles()
const route = useRoute()
const router = useRouter()

const filters = ref({
  direction: ["IT", "Медицина", "Финансы"],
  course: ["1 курс", "2 курс", "3 курс", "4 курс"],
  period: ["Весна", "Лето", "Осень", "Зима"],
})

const search = ref(route.query.search?.toString() || "")
const selectedDirection = ref(route.query.direction?.toString() || "all")
const selectedCourse = ref(route.query.course?.toString() || "all")
const selectedPeriod = ref(route.query.period?.toString() || "all")
const isReserved = ref(route.query.reserved === "true")

const pending = ref(false)
const error = ref<string | null>(null)
const interns = ref<any[]>([])

onMounted(async () => {
  try {
    pending.value = true
    const res = await axios.get("/api/intern")
    interns.value = res.data
  } catch (err: any) {
    error.value = "Ошибка при загрузке данных"
  } finally {
    pending.value = false
  }
})

const filteredInterns = computed(() => {
  return interns.value.filter((i) => {
    const matchesSearch = search.value
      ? i.study_program.toLowerCase().includes(search.value.toLowerCase())
      : true
    const matchesReserved = isReserved.value ? i.company_reserved : true
    return matchesSearch && matchesReserved
  })
})

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  })
}

watch([search, selectedDirection, selectedCourse, selectedPeriod, isReserved], () => {
  router.replace({
    query: {
      search: search.value || undefined,
      direction: selectedDirection.value !== "all" ? selectedDirection.value : undefined,
      course: selectedCourse.value !== "all" ? selectedCourse.value : undefined,
      period: selectedPeriod.value !== "all" ? selectedPeriod.value : undefined,
      reserved: isReserved.value ? "true" : undefined,
    },
  })
})

const goToCreate = () => {
    router.push("/chat")
}
</script>
