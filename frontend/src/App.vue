<template>
  <div class="min-h-screen">
    <RouterView class="h-full min-h-screen" v-slot="{ Component }">
      <component :is="Component" />
    </RouterView>
  </div>
  <Toaster class="pointer-events-auto" />
</template>

<script setup lang="ts">
import { Toaster } from '@/components/ui/sonner'
import { useAuthStore } from './stores/authStore'
import { useColorMode } from '@vueuse/core'
import { onMounted } from 'vue'
import router from './router'

useColorMode()
const authStore = useAuthStore()
onMounted(async () => {
  await router.isReady() 

  if (router.currentRoute.value.path === '/main') return

  try {
    await authStore.initializeAuth()
    router.push('/')
  } catch (e) {
    console.error(e)
  }
})
</script>
