<template>
  <section class="px-4 pb-10">
    <div class="my-5 flex flex-wrap justify-between items-center gap-3">
      <h1 class="text-2xl font-semibold">Витрина вакансий</h1>

      <Button v-if="!isCurator" @click="goToCreate" class="bg-accent text-white hover:opacity-90">
        + Создать вакансию
      </Button>
    </div>

    <div class="flex flex-wrap gap-3 items-center mb-6">
      <div class="flex items-center flex-grow min-w-[250px] relative">
        <Search class="absolute left-3 text-muted-foreground w-4 h-4" />
        <Input
          v-model="search"
          placeholder="Поиск вакансий"
          class="pl-9 w-full"
        />
      </div>

      <Select v-model="selectedCompany">
        <SelectTrigger class="w-[180px]">
          <SelectValue placeholder="Компания" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">Все компании</SelectItem>
          <SelectItem value="biocad">БИОКАД</SelectItem>
          <SelectItem value="cnk">НЦК</SelectItem>
          <SelectItem value="ao">АО</SelectItem>
        </SelectContent>
      </Select>

      <!-- Направление -->
      <Select v-model="selectedDirection">
        <SelectTrigger class="w-[180px]">
          <SelectValue placeholder="Направление" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">Все направления</SelectItem>
          <SelectItem value="fabric">Производство</SelectItem>
          <SelectItem value="medicine">Медицина</SelectItem>
          <SelectItem value="it">IT</SelectItem>
        </SelectContent>
      </Select>

      <!-- Тип занятости -->
      <Select v-model="selectedType">
        <SelectTrigger class="w-[180px]">
          <SelectValue placeholder="Тип занятости" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">Все типы</SelectItem>
          <SelectItem value="full">Полная</SelectItem>
          <SelectItem value="part">Частичная</SelectItem>
          <SelectItem value="internship">Стажировка</SelectItem>
        </SelectContent>
      </Select>

      <!-- Без опыта -->
      <div class="flex items-center space-x-2">
        <Checkbox id="no-exp" v-model:checked="noExperience" />
        <label
          for="no-exp"
          class="text-sm font-medium leading-none cursor-pointer select-none"
        >
          Без опыта
        </label>
      </div>
    </div>

    <!-- Список вакансий -->
    <div v-if="pending" class="text-muted-foreground text-sm">Загрузка...</div>

    <div v-else class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <Card
        v-for="vacancy in filteredVacancies"
        :key="vacancy.id"
        class="hover:shadow-md transition-shadow border rounded-2xl p-4 flex flex-col justify-between"
      >
        <div>
          <div class="flex justify-between items-start mb-2">
            <CardTitle class="text-lg font-semibold">
              {{ vacancy.company }}
            </CardTitle>
            <p class="text-sm text-muted-foreground">{{ vacancy.city }}</p>
          </div>

          <p class="text-primary font-semibold mb-4">
            {{ vacancy.title }}
          </p>
        </div>

        <div class="mt-4 gap-2 flex justify-start flex-wrap">
          <span
            class="bg-accent text-sm text-primary px-3 py-1 rounded-full font-medium"
          >
            {{ vacancy.direction }}
          </span>
          <span
            class="bg-black text-sm text-white px-3 py-1 rounded-full font-medium"
          >
            {{ vacancy.experience ? "С опытом" : "Без опыта" }}
          </span>
        </div>
      </Card>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, watch, computed, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { Input } from "@/components/ui/input"
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import { Card, CardTitle } from "@/components/ui/card"
import { Search } from "lucide-vue-next"
import Button from "@/components/ui/button/Button.vue"
import axios from "axios"
import { useRoles } from "@/composables/usePermissions"
const {isCurator } = useRoles()

const route = useRoute()
const router = useRouter()

const search = ref(route.query.search?.toString() || "")
const selectedCompany = ref(route.query.company?.toString() || "all")
const selectedDirection = ref(route.query.direction?.toString() || "all")
const selectedType = ref(route.query.type?.toString() || "all")
const noExperience = ref(route.query.noExperience === "true")

const vacancies = ref<any[]>([])
const pending = ref(false)
const error = ref<string | null>(null)

async function fetchVacancies() {
  pending.value = true
  error.value = null

  try {
    const params: Record<string, string> = {}
    if (selectedCompany.value !== "all") params.company = selectedCompany.value
    if (selectedDirection.value !== "all") params.direction = selectedDirection.value
    if (selectedType.value !== "all") params.type = selectedType.value

    const { data } = await axios.get("/api/vacancy/", { params })
    vacancies.value = Array.isArray(data) ? data : []
  } catch (e) {
    console.error("Ошибка при загрузке вакансий:", e)
    error.value = "Не удалось загрузить вакансии"
  } finally {
    pending.value = false
  }
}

onMounted(fetchVacancies)

const filteredVacancies = computed(() => {
  return vacancies.value.filter((v) => {
    const matchesSearch = search.value
      ? v.title.toLowerCase().includes(search.value.toLowerCase())
      : true
    const matchesExperience = noExperience.value ? !v.experience : true
    return matchesSearch && matchesExperience
  })
})

watch(
  [selectedCompany, selectedDirection, selectedType],
  () => {
    router.replace({
      query: {
        search: search.value || undefined,
        company: selectedCompany.value !== "all" ? selectedCompany.value : undefined,
        direction: selectedDirection.value !== "all" ? selectedDirection.value : undefined,
        type: selectedType.value !== "all" ? selectedType.value : undefined,
      },
    })
    fetchVacancies()
  },
  { deep: true }
)

const goToCreate = () => router.push("/vacancies/create")
</script>
