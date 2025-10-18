<template>
  <section class="max-w-3xl mx-auto px-4 py-8">
    <!-- Экран подтверждения -->
    <div v-if="isSuccess" class="text-center space-y-4 mt-10">
      <LottieAnimation
        class="mx-auto"
        :src="animationSrc"
        :height="250"
        :width="250"
        renderer="svg"
      />
      <h2 class="text-2xl font-semibold">Вакансия отправлена на модерацию</h2>
      <p class="text-muted-foreground max-w-md mx-auto">
        Мы передали вашу заявку координатору. Обычно модерация занимает до 3 рабочих дней.
      </p>
      <Button class="mt-4" @click="goHome">Вернуться на главную</Button>
    </div>

    <!-- Форма создания вакансии -->
    <div v-else>
      <h1 class="text-2xl font-semibold mb-2">Анкета для работодателей</h1>
      <p class="text-sm text-muted-foreground mb-6">
        Заполните поля, чтобы создать вакансию
      </p>

      <form @submit.prevent="onSubmit" class="space-y-10">
        <FormField name="title" v-slot="{ componentField }">
          <FormItem>
            <FormLabel>Название вакансии</FormLabel>
            <FormControl>
              <Input
                v-bind="componentField"
                placeholder="Например: Инженер по тестированию"
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <FormField name="company" v-slot="{ componentField }">
          <FormItem>
            <FormLabel>Название компании</FormLabel>
            <FormControl>
              <Input v-bind="componentField" placeholder="Например: Нейротех" />
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
                  v-for="opt in platformOptions "
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
                  v-for="opt in specialtyOptions "
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
            <FormLabel>Описание вакансии</FormLabel>
            <FormControl>
              <Textarea
                v-bind="componentField"
                placeholder="Краткое описание обязанностей, требований и условий"
                rows="6"
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>
         <FormField name="description" v-slot="{ componentField }">
 <FormLabel class="mb-2">Автоснятие с публикации</FormLabel>
   <FormControl>
 <Input type="date"  />

   </FormControl>          

         </FormField>

        <div class="flex items-center justify-end space-x-3">
          <Button variant="ghost" type="button" @click="onCancel">Отмена</Button>
          <Button type="submit" :disabled="isLoading">
            {{ isLoading ? "Сохранение..." : "Отправить" }}
          </Button>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useForm } from "vee-validate"
import { toTypedSchema } from "@vee-validate/zod"
import * as z from "zod"

import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import {
  Select,
  SelectTrigger,
  SelectContent,
  SelectItem,
  SelectValue,
} from "@/components/ui/select"
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import LottieAnimation from '@/components/animations/LottieAnimation.vue';
import apiClient from "@/lib/axios"

const platformOptions = [
  "АЛАБУШЕВО",
  "АНГСТРЕМ",
  "МИКРОН",
  "МИЭТ",
  "ПЕЧАТНИКИ",
  "РУДНЕВО",
].map((v) => ({ label: v, value: v }))
// --- список для дропдаунов ---
const specialtyOptions  = [
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

// --- схема формы ---
const formSchema = toTypedSchema(
  z.object({
    title: z.string().min(3, "Введите название вакансии (мин. 3 символа)"),
    company: z.string().min(2, "Введите название компании"),
    platform: z.string().min(1, "Выберите площадку"),
    specialty: z.string().min(1, "Выберите специальность"),
    description: z
      .string()
      .min(10, "Описание должно быть не короче 10 символов"),
  })
)

type FormValues = z.infer<typeof formSchema>

const { handleSubmit, resetForm } = useForm<FormValues>({
  validationSchema: formSchema,
  initialValues: {
    title: "",
    company: "",
    platform: "",
    specialty: "",
    description: "",
  },
})

const isLoading = ref(false)
const isSuccess = ref(false)
const router = useRouter()

const animationSrc = "/DuckNothingFound.tgs" 

async function createVacancy(payload: FormValues) {
  const body = {
    title: payload.title,
    city: payload.platform, // можно уточнить, если city отдельное поле
    company: payload.company,
    type: "full", // можно добавить дропдаун "тип занятости" позже
    direction: payload.specialty,
    experience: false, // добавить чекбокс "требуется опыт"
  }

  const { data } = await apiClient.post("/api/vacancy/", body)
  return data
}
const onSubmit = handleSubmit(async (values) => {
  isLoading.value = true
  try {
    await createVacancy(values)
    resetForm()
    isSuccess.value = true
  } catch (e) {
    console.error("Ошибка при создании вакансии:", e)
  } finally {
    isLoading.value = false
  }
})
const goHome = () => router.push("/")
const onCancel = () => router.back()
</script>
