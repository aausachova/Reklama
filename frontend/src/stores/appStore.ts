import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useWindowSize, useColorMode } from "@vueuse/core";

export const useAppStore = defineStore(
  "app",
  () => {
    const { width } = useWindowSize();
    const isMobile = computed(() => width.value <= 768);
    const isSidebarOpen = ref(true);

    const openSidebar = () => {
      isSidebarOpen.value = true;
    };

    const closeSidebar = () => {
      isSidebarOpen.value = false;
    };

    const toggleSidebar = () => {
      isSidebarOpen.value = !isSidebarOpen.value;
    };

    const mode = useColorMode({
      attribute: "class",
      modes: {
        auto: "auto",
        light: "light",
        dark: "dark",
      },
    });

    return {
      isMobile,
      isSidebarOpen,
      openSidebar,
      closeSidebar,
      toggleSidebar,
      mode,
    };
  },
  {
    persist: true,
  }
);
