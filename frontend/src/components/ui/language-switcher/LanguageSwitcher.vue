<template>
    <DropdownMenu>
        <DropdownMenuTrigger as-child>
            <Button :variant="variant" :size="size" :class="buttonClass">
                <Languages class="size-4" :class="{ 'mr-2': showText }" />
                <span v-if="showText">{{ $t(`language.${currentLocale}`) }}</span>
                <span v-else class="sr-only">Toggle language</span>
            </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end">
            <DropdownMenuLabel>{{ $t('language.select') }}</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuRadioGroup v-model="currentLocale">
                <DropdownMenuRadioItem v-for="locale in supportedLocales" :key="locale" :value="locale">
                    {{ $t(`language.${locale}`) }}
                </DropdownMenuRadioItem>
            </DropdownMenuRadioGroup>
        </DropdownMenuContent>
    </DropdownMenu>
</template>

<script setup lang="ts">
import { Languages } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuLabel,
    DropdownMenuRadioGroup,
    DropdownMenuRadioItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { useLanguage } from '@/composables/useLanguage'

interface Props {
    variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link'
    size?: 'default' | 'sm' | 'lg' | 'icon'
    showText?: boolean
    buttonClass?: string
}

withDefaults(defineProps<Props>(), {
    variant: 'ghost',
    size: 'icon',
    showText: false,
    buttonClass: ''
})

const { currentLocale, supportedLocales } = useLanguage()
</script>
