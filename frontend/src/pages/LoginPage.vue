<template>
    <section class="w-full flex flex-col  items-center pt-24 bg-background px-4">
        <div class="w-full max-w-[400px] flex flex-col items-center gap-4">
            <img width="165" height="400" class=" max-w-full mb-25 size-96 h-auto" src="/img/Logo.svg" />
            <div class="text-center  space-y-2 mb-6">
                <h1 class="text-2xl font-bold">{{ $t('auth.login.title') }}</h1>
                <p class="text-sm text-muted-foreground">{{ $t('auth.login.subtitle') }}</p>
            </div>
            <!-- <div class="flex flex-col w-full gap-4">
                <Button size="lg" variant="outline">
                    <Icon icon="mingcute:google-fill" />
                    {{ $t('auth.login.googleLogin') }}
                </Button>

                <div
                    class="relative text-center text-sm after:absolute after:inset-0 after:top-1/2 after:z-0 after:flex after:items-center after:border-t after:border-border">
                    <span class="relative z-10 bg-background px-2 text-muted-foreground">
                        {{ $t('auth.login.or') }}
                    </span>
                </div>
            </div> -->

            <form @submit="onSubmit" class="w-full space-y-4">
                <FormField v-slot="{ componentField }" name="username" :validate-on-blur="!isFieldDirty">
                    <FormItem class=" relative ">
                        <FormLabel class=" px-1 text-sm  bg-background">
                            {{ $t('auth.login.form.username') }}
                        </FormLabel>
                        <FormControl>
                            <Input autocomplete="username" class="h-10 !bg-card" v-bind="componentField"
                                :placeholder="$t('auth.login.form.username')" />
                        </FormControl>
                        <FormMessage class="text-xs text-destructive" />
                    </FormItem>
                </FormField>

                <FormField v-slot="{ componentField }" name="password" :validate-on-blur="!isFieldDirty">
                    <FormItem class="relative">
                        <FormLabel class=" px-1 text-sm bg-background z-[1]">
                            {{ $t('auth.login.form.password') }}
                        </FormLabel>
                        <div class="relative">
                            <FormControl>
                                <Input autocomplete="current-password" class="h-10 !bg-card pr-10"
                                    v-bind="componentField" :type="showPassword ? 'text' : 'password'"
                                    :placeholder="$t('auth.login.form.password')" />
                            </FormControl>
                            <button type="button" @click="showPassword = !showPassword"
                                class="absolute right-0 top-1/2 h-full -translate-y-1/2 px-3 flex items-center  text-muted-foreground hover:text-foreground">
                                <EyeIcon v-if="showPassword" class="h-4 w-4" />
                                <EyeOffIcon v-else class="h-4 w-4" />
                            </button>
                        </div>
                        <FormMessage class="text-xs text-destructive" />
                    </FormItem>
                </FormField>

                <Button :disabled="isLoading" size="lg" type="submit" class="w-full ">
                    {{ isLoading ? $t('common.loading') : $t('auth.login.form.submit') }}
                </Button>
            </form>

            <div class="w-full text-center text-sm">
                <span class="text-muted-foreground">{{ $t('auth.login.noAccount') }}</span> <router-link
                    to="/auth/register" class="text-primary hover:underline">{{ $t('auth.login.createAccount')
                    }}</router-link>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { Icon } from "@iconify/vue";
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { FormControl, FormField, FormItem, FormMessage, FormLabel } from '@/components/ui/form'
import LottieAnimation from '@/components/animations/LottieAnimation.vue'
import { ref } from 'vue'
import { EyeIcon, EyeOffIcon } from 'lucide-vue-next'
import { toast } from 'vue-sonner'
import { useAuthStore } from "@/stores/authStore";
import { REGEX_PATTERNS } from '@/utils/validation'

const isLoading = ref(false)
const authStore = useAuthStore()
const { t } = useI18n()

const formSchema = toTypedSchema(z.object({
    username: z.string()
        .min(1, t('validation.username.required'))
        .min(3, t('validation.username.min'))
        .max(20, t('validation.username.max'))
        .regex(REGEX_PATTERNS.USERNAME, t('validation.username.pattern')),
    password: z.string()
        .min(1, t('validation.password.required'))
        .min(6, t('validation.password.min'))
        .max(50, t('validation.password.max'))
        .regex(REGEX_PATTERNS.PASSWORD, t('validation.password.pattern')),
}))

const { handleSubmit, isFieldDirty } = useForm({
    validationSchema: formSchema,
    initialValues: {
        username: '',
        password: ''
    },
})

const showPassword = ref(false)
const onSubmit = handleSubmit(async (values) => {
    if (isLoading.value) return;

    try {
        isLoading.value = true;
        await authStore.login(values);
    } catch (error) {
        toast.error('Ошибка входа', {
            description: error instanceof Error ? error.message : 'Произошла ошибка при входе',
            duration: 3000,
        });
    } finally {
        isLoading.value = false;
    }
});
</script>
