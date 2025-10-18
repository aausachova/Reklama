import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { User, LoginCredentials, RegisterCredentials } from "@/types/auth";
import { AuthService } from "@/services/auth.service";
import router from "@/router";

export const useAuthStore = defineStore("auth", () => {
  const user = ref<User | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const authChecked = ref(false);
  const redirectPath = ref<string | null>(null);

  const isAuthenticated = computed(() => !!user.value);

  // Загрузка данных пользователя
  const setUserData = async () => {
    try {
      const userData = await AuthService.getUserData();
      console.log("User data from server:", userData); // Логируем данные

      if (!userData || !userData.id) {
        throw new Error("Invalid user data received from server");
      }

      user.value = {
        user_id: userData.id,
        username: userData.username,
        email: userData.email,
        created_at: userData.created_at,
      };
    } catch (e) {
      console.error("Ошибка загрузки данных пользователя:", e);
      user.value = null;
    }
  };

  // Инициализация аутентификации
  async function initializeAuth() {
    if (authChecked.value) return;

    try {
      loading.value = true;
      await setUserData();
    } catch (e) {
      console.error("Ошибка инициализации аутентификации:", e);
      user.value = null;
    } finally {
      loading.value = false;
      authChecked.value = true;
    }
  }

  // Авторизация пользователя
  async function login(credentials: LoginCredentials) {
    try {
      loading.value = true;
      error.value = null;
      await AuthService.login(credentials);
      await setUserData();

      router.push(redirectPath.value || "/");
      redirectPath.value = null;
    } catch (e) {
      const message = e instanceof Error ? e.message : "Неизвестная ошибка";
      error.value = message;
      throw new Error(message);
    } finally {
      loading.value = false;
    }
  }

  // Регистрация пользователя
  async function register(credentials: RegisterCredentials) {
    try {
      loading.value = true;
      error.value = null;
      await AuthService.register(credentials);
      await AuthService.login({
        username: credentials.username,
        password: credentials.password,
      });
      await setUserData();
      router.push("/");
    } catch (e) {
      const message = e instanceof Error ? e.message : "Неизвестная ошибка";
      error.value = message;
      throw new Error(message);
    } finally {
      loading.value = false;
    }
  }

  // Выход из системы
  async function logout() {
    try {
      await AuthService.logout();
    } catch (e) {
      error.value = "Ошибка выхода";
    } finally {
      user.value = null;
      authChecked.value = true;
      router.push("/auth/login");
    }
  }

  // Смена пароля
  async function changePassword(oldPassword: string, newPassword: string) {
    try {
      loading.value = true;
      error.value = null;
      await AuthService.changePassword(oldPassword, newPassword);
    } catch (e) {
      const message = e instanceof Error ? e.message : "Неизвестная ошибка";
      error.value = message;
      throw new Error(message);
    } finally {
      loading.value = false;
    }
  }

  // Генерация инициалов пользователя
  const userInitials = computed(() => {
    if (!user.value?.username) {
      return "U";
    }
    const username = user.value.username.trim();
    if (!username) {
      return "U";
    }
    const names = username.split(/\s+/);
    let initials = "";
    if (names.length >= 2) {
      initials = names[0][0] + names[names.length - 1][0];
    } else {
      initials = names[0].slice(0, 2);
    }
    return initials.toUpperCase().padEnd(2, "").slice(0, 2);
  });

  return {
    user,
    loading,
    error,
    authChecked,
    isAuthenticated,
    register,
    login,
    logout,
    initializeAuth,
    setRedirectPath: (path: string) => (redirectPath.value = path),
    redirectPath: computed(() => redirectPath.value),
    userInitials,
    changePassword,
  };
});
