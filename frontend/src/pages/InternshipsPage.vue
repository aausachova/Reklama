<template>
  <section class="px-4 pb-10">
    <div class="my-5 flex flex-wrap justify-between items-center gap-3">
      <h1 class="text-2xl font-semibold">Стажировки</h1>

      <Button
        v-if="!isCurator"
        @click="goToCreate"
        class="bg-accent text-white hover:opacity-90"
      >
       Связаться с куратором
      </Button>
    </div>

    <!-- 🔽 Фильтры -->
    <div class="flex flex-wrap gap-3 items-center mb-6">
      <!-- Поиск по ВУЗу -->
      <div class="flex items-center flex-grow min-w-[250px] relative">
        <Search class="absolute left-3 text-muted-foreground w-4 h-4" />
        <Input
          v-model="search"
          placeholder="Поиск по ВУЗу"
          class="pl-9 w-full"
        />
      </div>

      <!-- Направление -->
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

      <!-- Курс -->
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

      <!-- 🗓 Период -->
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

      <!-- Бронь от компании -->
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

    <!-- 🧭 Таблица стажировок -->
    <div v-if="pending" class="text-muted-foreground text-sm">Загрузка...</div>
    <div v-else-if="error" class="text-destructive text-sm">{{ error }}</div>

    <div v-else class="overflow-x-auto rounded-2xl border">
      <table class="min-w-full text-sm border-collapse">
        <thead class="bg-muted/50 text-left">
          <tr>
            <th class="px-4 py-3 font-semibold text-foreground whitespace-nowrap">ВУЗ</th>
            <th class="px-4 py-3 font-semibold text-foreground w-[35%]">Направление обучения, курс</th>
            <th class="px-4 py-3 font-semibold text-foreground whitespace-nowrap">Дата прохождения практики</th>
            <th class="px-4 py-3 font-semibold text-foreground whitespace-nowrap">Количество человек</th>
            <th class="px-4 py-3 font-semibold text-foreground whitespace-nowrap">Бронь компании</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="intern in filteredInterns"
            :key="intern.id"
            class="border-t hover:bg-muted/30 transition"
          >
            <td class="px-4 py-3">{{ intern.university }}</td>
            <td class="px-4 py-3">
              <span class="font-medium">{{ intern.direction }}</span>,
              <span class="text-muted-foreground">{{ intern.course }}</span>
            </td>
            <td class="px-4 py-3">{{ intern.period }}</td>
            <td class="px-4 py-3 text-center">{{ intern.count }}</td>
            <td class="px-4 py-3">
              <span
                v-if="intern.reserved"
                class="bg-green-600 text-white text-xs px-3 py-1 rounded-full"
              >
                Да
              </span>
              <span
                v-else
                class="bg-muted text-foreground text-xs px-3 py-1 rounded-full"
              >
                Нет
              </span>
            </td>
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
import { ref, computed, watch } from "vue"
import { useRouter, useRoute } from "vue-router"
import { Input } from "@/components/ui/input"
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import { Search } from "lucide-vue-next"
import Button from "@/components/ui/button/Button.vue"
import { useRoles } from "@/composables/usePermissions"

const { isCurator } = useRoles()

const route = useRoute()
const router = useRouter()

// --- 🔧 Моковые фильтры ---
const filters = ref({
  direction: ["IT", "Медицина", "Финансы", "Маркетинг", "Юриспруденция"],
  course: ["1 курс", "2 курс", "3 курс", "4 курс", "5 курс"],
  period: ["Весна 2024", "Лето 2024", "Осень 2024", "Зима 2025"],
})

// --- ⚙️ Параметры фильтрации ---
const search = ref(route.query.search?.toString() || "")
const selectedDirection = ref(route.query.direction?.toString() || "all")
const selectedCourse = ref(route.query.course?.toString() || "all")
const selectedPeriod = ref(route.query.period?.toString() || "all")
const isReserved = ref(route.query.reserved === "true")

const pending = ref(false)
const error = ref<string | null>(null)

// --- 🧑‍🎓 Моковые данные стажировок ---
const interns = ref([
  {
    id: 1,
    university: "МИЭТ",
    direction: "IT",
    course: "3 курс",
    period: "Лето 2024",
    count: 12,
    reserved: true,
  },
  {
    id: 2,
    university: "МГУ",
    direction: "Финансы",
    course: "4 курс",
    period: "Осень 2024",
    count: 8,
    reserved: false,
  },
  {
    id: 3,
    university: "МГТУ",
    direction: "Медицина",
    course: "2 курс",
    period: "Весна 2024",
    count: 5,
    reserved: true,
  },
])

// --- 🧮 Фильтрация ---
const filteredInterns = computed(() => {
  return interns.value.filter((i) => {
    const matchesSearch = search.value
      ? i.university.toLowerCase().includes(search.value.toLowerCase())
      : true
    const matchesDirection =
      selectedDirection.value === "all" || i.direction === selectedDirection.value
    const matchesCourse =
      selectedCourse.value === "all" || i.course === selectedCourse.value
    const matchesPeriod =
      selectedPeriod.value === "all" || i.period === selectedPeriod.value
    const matchesReserved = isReserved.value ? i.reserved : true
    return (
      matchesSearch &&
      matchesDirection &&
      matchesCourse &&
      matchesPeriod &&
      matchesReserved
    )
  })
})

// --- Обновление query параметров ---
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

// --- Навигация ---
const goToCreate = () => router.push("/chat")
</script>
