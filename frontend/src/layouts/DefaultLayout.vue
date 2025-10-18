<template>
    <div class="main-layout" :class="{ 'sidebar-collapsed': !appStore.isSidebarOpen && !appStore.isMobile }">
        <Sidebar />
        <div class="content-wrapper">
            <MainHeader>
                <template #header-actions>
                    <slot name="header-actions"></slot>
                </template>
            </MainHeader>
            <main class="content-main">
                <RouterView />
            </main>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useAppStore } from '@/stores/appStore';
import Sidebar from '@/components/sidebar/Sidebar.vue';
import MainHeader from '@/components/header/MainHeader.vue';

const appStore = useAppStore();
</script>

<style scoped lang="css">
.main-layout {
    display: grid;
    grid-template:
        'sidebar header' auto
        'sidebar content' 1fr
        / clamp(0px, var(--sidebar-width, 270px), 270px) 1fr;
    height: 100vh;
    width: 100vw;
    overflow: hidden;
    transition: grid-template-columns 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@media (min-width: 769px) {
    .main-layout.sidebar-collapsed {
        --sidebar-width: 0px;
    }
}

@media (max-width: 768px) {
    .main-layout {
        grid-template:
            'header' auto
            'content' 1fr
            / 1fr;
    }
}

.content-wrapper {
    grid-area: content;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.content-main {
    flex: 1;
    background-color: var(--background);
    overflow-y: scroll;
    scrollbar-width: thin;
    scrollbar-color: var(--color-border) var(--color-background);
}
</style>