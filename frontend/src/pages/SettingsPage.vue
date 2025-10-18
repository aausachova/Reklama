<template>
  <section class="p-4 space-y-8 max-w-[1024px] mx-auto">

    <div class="space-y-0.5">
      <div class="flex items-center gap-4">
        <h1 class="text-2xl font-bold">{{ $t('settings.title') }} </h1>
        <LottieAnimation :src="'/Gamepad.tgs'" :height="40" :width="40" renderer="svg" />
      </div>
      <p class="text-muted-foreground">
        {{ $t('settings.subtitle') }}
      </p>
    </div>


    <div class="space-y-6">
      <div>
        <h2 class="text-lg font-medium mb-1">{{ $t('settings.app.title') }}</h2>
        <p class="text-sm text-muted-foreground mb-4">
          {{ $t('settings.app.subtitle') }}
        </p>
        <Separator class="mb-4" />

        <div class="flex items-center justify-between py-4">
          <div>
            <h3 class="font-medium mb-1">{{ $t('settings.app.theme.title') }}</h3>
            <p class="text-sm text-muted-foreground">
              {{ $t('settings.app.theme.subtitle') }}
            </p>
          </div>
          <ThemeChanger />
        </div>

        <Separator />

        <div class="flex items-center justify-between py-4">
          <div>
            <h3 class="font-medium mb-1">{{ $t('settings.app.language.title') }}</h3>
            <p class="text-sm text-muted-foreground">
              {{ $t('settings.app.language.subtitle') }}
            </p>
          </div>
          <LanguageSwitcher variant="outline" />
        </div>
      </div>

      <div>
        <h2 class="text-lg font-medium mb-1">{{ $t('settings.account.title') }}</h2>
        <p class="text-sm text-muted-foreground mb-4">
          {{ $t('settings.account.subtitle') }}
        </p>
        <Separator class="mb-4" />

        <div class="flex items-center justify-between py-4">
          <div>
            <h3 class="font-medium mb-1">{{ $t('settings.account.logoutTitle') }}</h3>
            <p class="text-sm text-muted-foreground">{{ $t('settings.account.logoutDescription') }}</p>
          </div>
          <Button variant="destructive" size="sm" class="gap-2 w-[130px]" @click="authStore.logout">
            <LogOut class="size-4" />
            {{ $t('settings.account.logout') }}
          </Button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { useAuthStore } from '@/stores/authStore'
import { LogOut } from 'lucide-vue-next'
import { Separator } from '@/components/ui/separator'
import LanguageSwitcher from '@/components/ui/language-switcher/LanguageSwitcher.vue'
import LottieAnimation from '@/components/animations/LottieAnimation.vue'
import ThemeChanger from '@/components/header/ThemeChanger.vue'

const authStore = useAuthStore()


</script>