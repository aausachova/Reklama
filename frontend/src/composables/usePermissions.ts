import { useAuthStore } from "@/stores/authStore";
import type { Roles } from "@/types/auth";
import { computed, type ComputedRef } from "vue";

type PermissionKey = "read" | "write" | "delete" | "update";

type PermissionsMap = Record<Roles, PermissionKey[]>;

export const usePermissions = () => {
  const { user } = useAuthStore();


  const hasRole = (role: Roles): boolean => {
    return user?.role === role;
  };
  const hasAnyRole = (roles: Roles[]): boolean => {
    if (!user) {
      return false;
    }
    return roles.includes(user.role as Roles);
  };

  return {
    hasRole,
    hasAnyRole,
  };
};
