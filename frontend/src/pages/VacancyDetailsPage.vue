<template>
  <section class="max-w-6xl mx-auto px-6 py-8">
    <div v-if="pending" class="text-muted-foreground">Загрузка данных...</div>
    <div v-else-if="error" class="text-destructive">{{ error }}</div>

    <div v-else class="grid grid-cols-1 md:grid-cols-[1fr_250px] gap-10">
      <!-- Левая колонка — форма -->
      <div>
        <h1 class="text-2xl font-semibold mb-2">Модерация вакансии</h1>
        <p class="text-sm text-muted-foreground mb-6">
          Проверьте данные вакансии, при необходимости внесите правки и выберите действие.
        </p>

        <form @submit.prevent="onSubmit" class="space-y-8">
          <FormField name="title" v-slot="{ componentField }">
            <FormItem>
              <FormLabel>Название вакансии</FormLabel>
              <FormControl>
                <Input v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField name="company" v-slot="{ componentField }">
            <FormItem>
              <FormLabel>Компания</FormLabel>
              <FormControl>
                <Input v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField name="platform" v-slot="{ componentField }">
            <FormItem>
              <FormLabel>Площадка</FormLabel>
              <Select v-bind="componentField">
                <FormControl>
                  <SelectTrigger class="w-full">
                    <SelectValue placeholder="Выберите площадку" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  <SelectItem
                    v-for="opt in platformOptions"
                    :key="opt.value"
                    :value="opt.value"
                  >
                    {{ opt.label }}
                  </SelectItem>
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField name="specialty" v-slot="{ componentField }">
            <FormItem>
              <FormLabel>Специальность</FormLabel>
              <Select v-bind="componentField">
                <FormControl>
                  <SelectTrigger class="w-full">
                    <SelectValue placeholder="Выберите специальность" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  <SelectItem
                    v-for="opt in specialtyOptions"
                    :key="opt.value"
                    :value="opt.value"
                  >
                    {{ opt.label }}
                  </SelectItem>
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField name="description" v-slot="{ componentField }">
            <FormItem>
              <FormLabel>Описание</FormLabel>
              <FormControl>
                <Textarea v-bind="componentField" rows="6" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <Button variant="outline" type="button" @click="router.back()">Назад</Button>
        </form>
      </div>

      <!-- Правая колонка — кнопки -->
      <div class="flex flex-col space-y-3 mt-1">
        <Button
          type="submit"
          :disabled="isLoading"
          @click="onSubmit"
          class="w-full"
        >
          {{ isLoading ? "Сохраняем..." : " Одобрить" }}
        </Button>

        <Button
          variant="outline"
          type="button"
          :disabled="isLoading"
          class="w-full"
          @click="sendToRevision"
        >
          На доработку
        </Button>

        <Button
          variant="outline"
          type="button"
          :disabled="isLoading"
          class="w-full text-destructive border-destructive hover:bg-destructive/10"
          @click="rejectVacancy"
        >
          Отклонить
        </Button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useForm } from "vee-validate"
import { toTypedSchema } from "@vee-validate/zod"
import * as z from "zod"
import axios from "axios"

import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import {
  Select,
  SelectTrigger,
  SelectContent,
  SelectItem,
  SelectValue,
} from "@/components/ui/select"

const router = useRouter()
const route = useRoute()

const isLoading = ref(false)
const pending = ref(false)
const error = ref<string | null>(null)

const platformOptions = [
  "АЛАБУШЕВО",
  "АНГСТРЕМ",
  "МИКРОН",
  "МИЭТ",
  "ПЕЧАТНИКИ",
  "РУДНЕВО",
].map((v) => ({ label: v, value: v }))

const specialtyOptions = [
  "HR",
  "Производство",
  "Микроэлектроника",
  "Финансы",
  "IT",
  "Административная работа",
  "Юриспруденция",
  "Другое",
  "Логистика",
  "Маркетинг",
  "Медицина",
  "Продажи",
].map((v) => ({ label: v, value: v }))

const schema = toTypedSchema(
  z.object({
    title: z.string().min(3, "Введите название вакансии"),
    company: z.string().min(2, "Введите название компании"),
    platform: z.string().min(1, "Выберите площадку"),
    specialty: z.string().min(1, "Выберите специальность"),
    description: z.string().min(5, "Введите описание"),
  })
)

const { handleSubmit, setValues, values } = useForm({
  validationSchema: schema,
  initialValues: {
    title: "",
    company: "",
    platform: "",
    specialty: "",
    description: "",
  },
})

async function fetchVacancy() {
  pending.value = true
  try {
    const { data } = await axios.get(`/api/vacancy/${route.params.id}`)
    setValues({
      title: data.title || "",
      company: data.company || "",
      platform: data.city || "",
      specialty: data.direction || "",
      description: data.description || "",
    })
  } catch (e) {
    console.error("Ошибка при загрузке:", e)
    error.value = "Не удалось загрузить данные"
  } finally {
    pending.value = false
  }
}

const patchVacancy = async (body: Record<string, any>) => {
  isLoading.value = true
  try {
    await axios.patch(`/api/vacancy/${route.params.id}`, body)
    router.push("/moderator")
  } catch (e) {
    console.error("Ошибка при PATCH:", e)
    error.value = "Не удалось обновить вакансию"
  } finally {
    isLoading.value = false
  }
}

const onSubmit = handleSubmit(async (formData) => {
  await patchVacancy({
    title: formData.title,
    company: formData.company,
    city: formData.platform,
    direction: formData.specialty,
    description: formData.description,
    active: true,
    status: "approved",
  })
})

async function sendToRevision() {
  await patchVacancy({ status: "revision", active: false })
}

async function rejectVacancy() {
  await patchVacancy({ status: "rejected", active: false })
}

onMounted(fetchVacancy)
</script>
