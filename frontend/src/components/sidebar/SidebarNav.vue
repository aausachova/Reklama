<template>
    <div class="flex flex-col gap-1 p-2">
        <span v-if="label" class="px-3 mb-0.5 text-xs text-muted-foreground cursor-default">
            {{ label }}
        </span>
        <Button v-for="item in links" :key="item.label" variant="ghost" :class="[
            'h-8 justify-start w-full text-sm font-normal text-muted-foreground',
            { 'bg-accent text-accent-foreground': isActiveRoute(item.url) }
        ]" asChild>
            <RouterLink :to="item.url" class="flex items-center gap-2 truncate">
                <component :is="item.icon" class="flex-shrink-0" />
                <span class="truncate">{{ $t(item.label) }}</span>
            </RouterLink>
        </Button>
    </div>
</template>

<script lang="ts" setup>
import { Button } from '@/components/ui/button';
import type { Links } from './Sidebar.vue';
import { useRoute } from 'vue-router';

interface Props {
    label?: string;
    links: Links[]
}

defineProps<Props>();
const route = useRoute();

const isActiveRoute = (url: string) => {
    if (url === '/') {
        return route.path === '/database' || route.path === '/achievements';
    }
    if (url === '/events') {
        return route.path.startsWith('/events');
    }
    return route.path === url;
};
</script>
