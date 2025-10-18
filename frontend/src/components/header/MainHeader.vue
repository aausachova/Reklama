<template>
    <header v-if="showHeader" class="header">
        <slot name="header">
            <div class="header-content">
                <Transition name="bounce">
                    <Button v-if="!appStore.isSidebarOpen" variant="ghost" class="p-0 w-[32px] h-[32px]"
                        @click="appStore.openSidebar">
                        <PanelLeft />
                    </Button>
                </Transition>
                <div class="header-actions">
                    <slot name="header-actions"></slot>
                </div>

                <div class="flex h-5 items-center space-x-4 text-sm">
                    <ThemeChanger />
                    <HeaderNotification />
                    <Separator orientation="vertical" />
                    <Button @click="authStore.logout">
                        Выйти
                    </Button>
                </div>
            </div>
        </slot>
    </header>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router';
import { computed } from 'vue';
import { PanelLeft } from 'lucide-vue-next';
import { Button } from '@/components/ui/button';
import { useAppStore } from '@/stores/appStore';
import { Separator } from '@/components/ui/separator'
import HeaderNotification from '@/components/header/HeaderNotification.vue';
import ThemeChanger from '@/components/header/ThemeChanger.vue';
import { useAuthStore } from '@/stores/authStore';

const appStore = useAppStore();
const route = useRoute();
const showHeader = computed(() => route.meta.showHeader ?? true);
const authStore = useAuthStore()

</script>

<style scoped>
.header {
    display: flex;
    width: 100%;
    height: 56px;
    flex-shrink: 0;
    padding: 0 16px;
}

.header-content {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.header-actions {
    display: flex;
    flex: 1 auto 1;
}

.bounce-enter-active {
    animation: bounce-in 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.bounce-leave-active {
    animation: collapse 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes bounce-in {
    0% {
        transform: scale(0) rotate(-20deg);
        opacity: 0;
    }

    60% {
        transform: scale(1.2) rotate(25deg);
        opacity: 0.7;
    }

    100% {
        transform: scale(1) rotate(0deg);
        opacity: 1;
    }
}

@keyframes collapse {
    0% {
        transform: scale(1) rotate(0deg);
        opacity: 1;
    }

    60% {
        transform: scale(1.2) rotate(-25deg);
        opacity: 0.7;
    }

    100% {
        transform: scale(0) rotate(-30deg);
        opacity: 0;
    }
}
</style>
