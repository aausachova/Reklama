<template>
    <DropdownMenu>
        <DropdownMenuTrigger as-child>
            <Button variant="ghost" class="w-full h-auto p-2">
                <Avatar class="  size-[52px] ">
                    <AvatarImage src="/" :alt="authStore.user?.username" />
                    <AvatarFallback class="dark:bg-muted font-bold bg-primary !text-white">
                        {{ authStore.userInitials }}
                    </AvatarFallback>
                </Avatar>
                <div class="grid flex-1 text-left text-sm leading-tight">
                    <span class="truncate font-semibold text-lg">{{ authStore.user?.username }}</span>
                    <span class="truncate text-xs font-medium  text-muted-foreground/70 ">{{ authStore.user?.role
                        }}</span>
                </div>
            </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent class="w-[--reka-dropdown-menu-trigger-width] min-w-[230px] rounded-lg" side="bottom"
            align="center">
            <DropdownMenuLabel class="p-0 font-normal">
                <div class="flex flex-col gap-1 px-1 py-1 text-left text-sm">
                    <div class="flex gap-2   items-center ">
                        <Avatar class="h-8 w-8">
                            <AvatarImage src="/" :alt="authStore.user?.username" />
                            <AvatarFallback class="dark:bg-muted font-bold bg-primary !text-white">
                                {{ authStore.userInitials }}
                            </AvatarFallback>
                        </Avatar>
                        <div class="grid flex-1 text-left text-sm leading-tight">
                            <span class="truncate font-semibold">{{ authStore.user?.username }}</span>
                            <span class="truncate text-xs">{{ authStore.user?.username }}</span>
                        </div>
                    </div>

                </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />



            <DropdownMenuGroup>
                <DropdownMenuItem @click="authStore.logout">
                    <LogOut />
                    {{ $t('common.logout') }}
                </DropdownMenuItem>
            </DropdownMenuGroup>
        </DropdownMenuContent>
    </DropdownMenu>
</template>

<script lang="ts" setup>
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
    LogOut,
} from 'lucide-vue-next';
import { DropdownMenu, DropdownMenuContent, DropdownMenuTrigger, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuGroup, DropdownMenuItem } from '@/components/ui/dropdown-menu';
import { useAuthStore } from '@/stores/authStore';

const authStore = useAuthStore();

</script>
