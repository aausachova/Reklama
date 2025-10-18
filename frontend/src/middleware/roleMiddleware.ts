import { useAuthStore } from "@/stores/authStore";
import type { Roles } from "@/types/auth";
import type { NavigationGuardNext, RouteLocationNormalized } from "vue-router";

export const roleMiddleware = (
  to: RouteLocationNormalized,
  _: RouteLocationNormalized,
  next: NavigationGuardNext
) => {
  // const { user } = useAuthStore();
  // const roles = to.meta.roles as Roles[] | undefined; 
  // if (!roles) {
  //   return next();
  // }
  // if (!user || !roles.includes(user.role)) {
  //   return next({ name: "403" });
  // }
  next();
};
