import { ref, computed } from "vue"

type UserRole = "resident" | "curator" | null

export function useRoles() {
  const role = ref<UserRole>(null)

  function setRole(newRole: UserRole) {
    role.value = newRole
  }

  function hasRole(required: UserRole | UserRole[]): boolean {
    if (!role.value) return false
    return Array.isArray(required)
      ? required.includes(role.value)
      : role.value === required
  }

  const isResident = computed(() => role.value === "resident")
  const isCurator = computed(() => role.value === "curator")

  return {
    role,
    setRole,
    hasRole,
    isResident,
    isCurator,
  }
}
