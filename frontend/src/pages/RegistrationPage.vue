<template>
  <section class="w-full flex flex-col items-center pt-24 bg-background p-4 space-y-6">
    <div class="w-full max-w-[400px] flex flex-col items-center space-y-4">
      <img width="165" height="400" class="max-w-full mb-17 size-70 h-auto" src="/img/Logo.svg" />

      <div class="text-center  ">
        <h1 class="text-2xl font-bold">{{ $t('auth.register.title') }}</h1>
      </div>

      <Tabs v-model="selectedRole" class="max-w-sm mx-auto mb-5">
        <TabsList class="grid w-full h-12 p-0 grid-cols-2">
          <TabsTrigger class="px-5" value="resident">Резидент</TabsTrigger>
          <TabsTrigger value="curator">Куратор</TabsTrigger>
        </TabsList>

      
      </Tabs>

      <form @submit="onSubmit" class="w-full space-y-4">
        <FormField v-slot="{ componentField }" name="username" :validate-on-blur="!isFieldDirty">
          <FormItem class="relative">
            <FormLabel class="px-1 text-nowrap text-sm">{{ $t('auth.register.form.username') }}</FormLabel>
            <FormControl>
              <Input autocomplete="username" class="h-10 !bg-card" v-bind="componentField" type="text"
                :placeholder="$t('auth.register.form.username')" />
            </FormControl>
            <FormMessage class="text-xs text-destructive" />
          </FormItem>
        </FormField>

        <FormField v-slot="{ componentField }" name="password" :validate-on-blur="!isFieldDirty">
          <FormItem class="relative">
            <FormLabel class="px-1 text-sm">{{ $t('auth.register.form.password') }}</FormLabel>
            <div class="relative">
              <FormControl>
                <Input autocomplete="new-password" class="h-10 pr-10 !bg-card" v-bind="componentField"
                  :type="showPassword ? 'text' : 'password'"
                  :placeholder="$t('auth.register.form.password')" />
              </FormControl>
              <button type="button" @click="showPassword = !showPassword"
                class="absolute right-0 top-1/2 h-full -translate-y-1/2 px-3 flex items-center text-muted-foreground hover:text-foreground">
                <EyeIcon v-if="showPassword" class="h-4 w-4" />
                <EyeOffIcon v-else class="h-4 w-4" />
              </button>
            </div>
            <FormMessage class="text-xs text-destructive" />
          </FormItem>
        </FormField>

        <FormField v-slot="{ componentField }" name="repeatPassword" :validate-on-blur="!isFieldDirty">
          <FormItem class="relative">
            <FormLabel class="px-1 text-sm">{{ $t('auth.register.form.repeatPassword') }}</FormLabel>
            <div class="relative">
              <FormControl>
                <Input autocomplete="new-password" class="h-10 pr-10 !bg-card" v-bind="componentField"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  :placeholder="$t('auth.register.form.repeatPassword')" />
              </FormControl>
              <button type="button" @click="showConfirmPassword = !showConfirmPassword"
                class="absolute right-0 top-1/2 h-full -translate-y-1/2 px-3 flex items-center text-muted-foreground hover:text-foreground">
                <EyeIcon v-if="showConfirmPassword" class="h-4 w-4" />
                <EyeOffIcon v-else class="h-4 w-4" />
              </button>
            </div>
            <FormMessage class="text-xs text-destructive" />
          </FormItem>
        </FormField>

        <Button size="lg" type="submit" class="w-full" :disabled="isLoading">
          {{ isLoading ? $t('common.loading') : $t('auth.register.form.submit') }}
        </Button>
      </form>

      <div class="text-center text-sm">
        <span class="text-muted-foreground">{{ $t('auth.register.hasAccount') }}   <router-link to="/auth/login" class="text-primary hover:underline">
          {{ $t('auth.register.login') }}
        </router-link></span> 
       
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, h } from 'vue'
import { useI18n } from 'vue-i18n'
import { toast } from 'vue-sonner'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'
import { EyeIcon, EyeOffIcon } from 'lucide-vue-next'
import ToastWithAnimation from '@/components/toast/ToastWithAnimation.vue'
import { useAuthStore } from '@/stores/authStore'
import { REGEX_PATTERNS } from '@/utils/validation'

const { t } = useI18n()

const selectedRole = ref<'resident' | 'curator'>('resident')

const formSchema = toTypedSchema(
  z.object({
    username: z.string()
      .min(3, t('validation.username.min'))
      .max(20, t('validation.username.max'))
      .regex(REGEX_PATTERNS.USERNAME, t('validation.username.pattern')),
    password: z.string()
      .min(6, t('validation.password.min'))
      .max(50, t('validation.password.max'))
      .regex(REGEX_PATTERNS.PASSWORD, t('validation.password.pattern')),
    repeatPassword: z.string()
  }).refine(data => data.password === data.repeatPassword, {
    message: t('validation.repeatPassword.mismatch'),
    path: ['repeatPassword']
  })
)

const { isFieldDirty, handleSubmit } = useForm({
  validationSchema: formSchema,
  initialValues: {
    username: '',
    password: '',
    repeatPassword: ''
  }
})

const isLoading = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const authStore = useAuthStore()

const onSubmit = handleSubmit(async (values) => {
  if (isLoading.value) return
  try {
    isLoading.value = true
    await authStore.register({
      username: values.username,
      password: values.password,
      repeat_password: values.repeatPassword,
      role: selectedRole.value, 
    })

    toast(h(ToastWithAnimation, {
      message: t('auth.register.success.title'),
      description: t('auth.register.success.message'),
      animationSrc: '/PartyPopper.tgs',
    }))
  } catch (error) {
    toast.error(t('auth.register.error.title'), {
      description: error instanceof Error ? error.message : t('auth.register.error.message'),
      duration: 3000,
    })
  } finally {
    isLoading.value = false
  }
})
</script>
