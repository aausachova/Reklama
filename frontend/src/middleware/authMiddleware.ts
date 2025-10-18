import type { NavigationGuardNext, RouteLocationNormalized } from "vue-router";
import { useAuthStore } from "@/stores/authStore";

export async function authMiddleware(
  to: RouteLocationNormalized,
  _: RouteLocationNormalized,
  next: NavigationGuardNext
) {
  const authStore = useAuthStore();

  if (authStore.isAuthenticated && to.meta.requiresGuest) {
    return next("/");
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({
      path: "/auth/login",
      query: { redirect: to.fullPath },
    });
  }
  next();
}
