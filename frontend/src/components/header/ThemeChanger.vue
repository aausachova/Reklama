<template>
    <DropdownMenu>
        <DropdownMenuTrigger as-child>
            <Button variant="outline" class="size-8 bg-card p-0">
                <component :is="themeIcons[appStore.mode]" class="size-4" />
            </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" class="w-[130px]">
            <DropdownMenuItem @click="appStore.mode = 'light'" class="gap-2">
                <Sun class="size-4" /> {{ $t('settings.app.theme.light') }}
            </DropdownMenuItem>
            <DropdownMenuItem @click="appStore.mode = 'dark'" class="gap-2">
                <Moon class="size-4" /> {{ $t('settings.app.theme.dark') }}
            </DropdownMenuItem>
            <DropdownMenuItem @click="appStore.mode = 'auto'" class="gap-2">
                <Laptop class="size-4" /> {{ $t('settings.app.theme.system') }}
            </DropdownMenuItem>
        </DropdownMenuContent>
    </DropdownMenu>
</template>

<script setup lang="ts">
import { Moon, Sun, Laptop } from 'lucide-vue-next'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu'
import { Button } from '@/components/ui/button'
import { useAppStore } from '@/stores/appStore'

const appStore = useAppStore()

const themeIcons = {
    'light': Sun,
    'dark': Moon,
    'auto': Laptop
}

</script>
