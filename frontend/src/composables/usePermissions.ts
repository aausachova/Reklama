import { computed } from "vue"
import { useAuthStore } from "@/stores/authStore"

export function useRoles() {
  const authStore = useAuthStore()

  const role = computed(() => authStore.user?.role ?? null)

  const isResident = computed(() => role.value?.toLowerCase() === "resident")
  const isCurator = computed(() => role.value?.toLowerCase() === "curator")

  function hasRole(required: string | string[]): boolean {
    if (!role.value) return false
    return Array.isArray(required)
      ? required.includes(role.value.toLowerCase())
      : role.value.toLowerCase() === required.toLowerCase()
  }

  return {
    role,
    isResident,
    isCurator,
    hasRole,
  }
}
