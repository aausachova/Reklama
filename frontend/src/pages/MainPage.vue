<template>
  <div class="flex flex-col items-center gap-6 p-6 bg-white">
    <img src="/img/svg/header.svg" alt="Header" />
    <img src="/img/svg/section.svg" alt="Section" />
    <div class="w-full max-w-2xl border-[20px] border-primary rounded-[16px] p-[2px] overflow-hidden">
  <div class="rounded-[14px] p-6 flex flex-col gap-6 bg-white">

        <img width="165" height="400" class="max-w-full size-70 mx-auto h-auto" src="/img/Logo.svg" />

       <div class="w-full max-w-2xl flex flex-col gap-6 mt-6 ">

      <div v-if="responseData.length" class="flex justify-end  ">
        <div class="flex items-center gap-3 bg-[#F5F7FB] border border-gray-200 rounded-2xl p-4 max-w-xs">
          <div class="flex flex-col items-center justify-center bg-blue-100 rounded-xl p-3">
            
               <FileTextIcon class="w-6 h-6 text-blue-500"/>
          </div>
          <div class="flex flex-col text-sm">
            <p class="text-blue-600 font-medium truncate max-w-[180px]">
              {{ selectedFile?.name }}
            </p>
            <span class="text-gray-500 text-xs">
              {{ (selectedFile?.size / 1024 / 1024).toFixed(2) }} МБ
            </span>
          </div>
        </div>
      </div>

      <p v-if="responseData.length" class="text-gray-700 text-center">
        Проанализировал резюме и подобрал лучшую вакансию для тебя
      </p>

      <div
        v-if="bestVacancy"
        class="relative border border-gray-200 rounded-[32px] p-6 bg-transparent flex flex-col justify-between min-h-[220px] "
       
      >
        <div>
          <div class="flex justify-between items-start mb-2">
            <h3 class="text-lg text-black font-bold">{{ bestVacancy.company }}</h3>
            <p class="text-sm text-gray-400">{{ bestVacancy.city }}</p>
          </div>

          <p class="text-[#df3053] font-semibold border-b-2 border-[#df3053] inline-block pb-1 mb-4">
            {{ bestVacancy.title }}
          </p>
        </div>

        <div class="flex gap-2">
          <span
            class="bg-pink-100 text-sm text-[#df3053] px-3 py-1 rounded-full font-medium"
          >
            {{ bestVacancy.direction }}
          </span>
          <span
            class="bg-black text-sm text-white px-3 py-1 rounded-full font-medium"
          >
            {{ bestVacancy.experience ? "С опытом" : "Без опыта" }}
          </span>
        </div>

        <div class="absolute right-2 bottom-3 text-[#df3053]">
         
          <ChevronRight  class="w-6 h-6"/>
        </div>
      </div>
    </div>

    <div
      class="flex items-center justify-between w-full max-w-2xl border border-[#E6E6E6] rounded-[12px] px-6 py-3 mt-10"
    >
      <label
        for="fileUpload"
        class="text-black text-base cursor-pointer flex-1"
      >
        {{ selectedFile ? selectedFile.name : "Прикрепи резюме со своими навыками и опытом работы" }}
      </label>

      <button
        type="button"
        class="mr-3 text-gray-500 hover:text-black transition-colors"
        @click="triggerFileSelect"
      >
        <Paperclip class="w-5 h-5" />
      </button>

      <button
        type="button"
        :disabled="loading || !selectedFile"
        class="flex items-center justify-center w-10 h-10 rounded-full bg-[#df3053] hover:opacity-90 transition disabled:opacity-50"
        @click="uploadResume"
      >
        <ArrowRight class="w-5 h-5 text-white" />
      </button>

      <input
        ref="fileInput"
        id="fileUpload"
        type="file"
        accept="application/pdf"
        class="hidden"
        @change="handleFileSelect"
      />
    </div>

    <p v-if="error" class="text-red-500 text-sm mt-2">{{ error }}</p>
      </div>
    </div>
    <img src="/img/svg/main.svg" alt="Main" />

  
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue"
import axios from "axios"
import { Paperclip, ArrowRight, FileTextIcon, ChevronRight } from "lucide-vue-next"

interface ResumeResponse {
  id: string
  title: string
  city: string
  company: string
  type: string
  direction: string
  experience: boolean
  score: number
}

const selectedFile = ref<File | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const responseData = ref<ResumeResponse[]>([])
const error = ref<string | null>(null)
const loading = ref(false)

const bestVacancy = computed(() => {
  if (!responseData.value.length) return null
  return [...responseData.value].sort((a, b) => b.score - a.score)[0]
})

function triggerFileSelect() {
  fileInput.value?.click()
}

function handleFileSelect(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return
  if (file.type !== "application/pdf") {
    error.value = "Можно загружать только PDF-файлы."
    selectedFile.value = null
    return
  }
  error.value = null
  selectedFile.value = file
}

async function uploadResume() {
  if (!selectedFile.value) {
    error.value = "Выберите PDF-файл."
    return
  }

  const formData = new FormData()
  formData.append("resume_pdf", selectedFile.value)

  loading.value = true
  error.value = null
  responseData.value = []

  try {
    const { data } = await axios.post<ResumeResponse[]>(
      "/api/resume/candidates",
      formData,
      { headers: { "Content-Type": "multipart/form-data" } }
    )
    responseData.value = data
  } catch (e: any) {
    console.error("Ошибка при отправке резюме:", e)
    error.value =
      e.response?.status === 422
        ? "Ошибка 422: сервер не принял файл. Проверьте формат и ключ поля."
        : "Не удалось отправить файл. Попробуйте снова."
  } finally {
    loading.value = false
  }
}
</script>
