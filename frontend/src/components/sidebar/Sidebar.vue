<template>
    <aside ref="sidebarRef" class="sidebar dark:!bg-background" :inert="!appStore.isSidebarOpen" :class="{
        'sidebar-open': appStore.isSidebarOpen,
        'sidebar-mobile': appStore.isMobile,
        'sidebar-closed': !appStore.isSidebarOpen
    }">
        <div class="flex flex-col justify-center items-start h-[56px] gap-2 px-5">
            <Button variant="ghost" class="p-0 w-[32px] h-[32px]" @click="appStore.closeSidebar">
                <PanelLeft />
            </Button>
        </div>
        <div class="flex flex-col gap-2 p-2">
            <SidebarUserMenu v-if="authStore.user"  />
            <div v-else class="flex flex-col h-[49.5px] gap-1.5">
                <Skeleton class="h-4 w-full" />
                <Skeleton class="h-4 w-[80%]" />
            </div>
        </div>
        <ScrollArea class="flex flex-1 flex-col gap-2 overflow-x-hidden min-h-0  ">
            <SidebarNav :links="USER_LINKS" />
        </ScrollArea>

        <div class="flex flex-col gap-2 p-2" v-if="usePermissions().hasRole('Administrator')">
            <SidebarNav :label="'Admin'" :links="ADMIN_LINKS" />

        </div>
    </aside>
    <div v-if="appStore.isSidebarOpen && appStore.isMobile" class="sidebar-overlay" @click="appStore.closeSidebar" />
</template>

<script setup lang="ts">
import SidebarUserMenu from './SidebarUserMenu.vue';
import SidebarNav from './SidebarNav.vue';
import { HouseIcon, type LucideIcon, BookIcon, SettingsIcon, PanelLeft, ChartColumn, PanelsTopLeft, Calendar, NotepadText, MessageCircle, UserIcon } from 'lucide-vue-next';
import Button from '@/components/ui/button/Button.vue';
import { onClickOutside, useEventListener } from '@vueuse/core';
import { useAppStore } from '@/stores/appStore';
import { ref } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { Skeleton } from '@/components/ui/skeleton';
import ScrollArea from '../ui/scroll-area/ScrollArea.vue';
import { usePermissions } from '@/composables/usePermissions';
export interface Links {
    label: string;
    url: string;
    icon: LucideIcon;
}
const authStore = useAuthStore();
const appStore = useAppStore();
const sidebarRef = ref<HTMLElement | null>(null);

onClickOutside(sidebarRef, () => {
    if (appStore.isMobile && appStore.isSidebarOpen) {
        appStore.closeSidebar();
    }
});



const USER_LINKS: Links[] = [
    { label: 'sidebar.home', url: '/', icon: HouseIcon },
    { label: 'Создание вакансии', url: '/projects', icon: BookIcon },
    // { label: 'Мероприятия', url: '/events', icon: Calendar },
    { label: 'Чаты', url: '/chat', icon: MessageCircle },
    //{ label: 'sidebar.settings', url: '/settings', icon: SettingsIcon },
    { label: 'Карьера', url: '/career', icon: NotepadText },
      { label: 'Помощь', url: '/help', icon: UserIcon },
];
const ADMIN_LINKS: Links[] = [
    { label: 'Панель управления', url: '/users', icon: PanelsTopLeft },
    { label: 'Аналитика данных', url: '/dashboard', icon: ChartColumn },
];

</script>

<style scoped>
.sidebar {
    background-color: #FFFFFF;
    grid-area: sidebar;
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: 270px;
    min-width: 0;
    border-radius: 0 40px 40px 0;
    box-shadow: 1px 0 0 0 var(--border);
    overflow: hidden;
    z-index: 50;
    will-change: transform;
}

@media (max-width: 768px) {
    .sidebar {
        position: fixed;
        top: 0;
        left: 0;
        bottom: 0;
        width: min(100%, 270px);
        transform: translateX(-100%);
        transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: none;
    }

    .sidebar.sidebar-open {
        transform: translateX(0);
        box-shadow: 1px 0 0 0 var(--border);
    }
}

.sidebar-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.3);
    z-index: 40;
}
</style>