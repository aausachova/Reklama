import type {
  LoginCredentials,
  RegisterCredentials,
  AuthResponse,
} from "@/types/auth";
import apiClient from "@/lib/axios";

export class AuthService {
  private static handleError(error: any, defaultMessage: string): never {
    const message =
      error.response?.data?.message ||
      error.response?.data?.error ||
      error.message ||
      defaultMessage;
    throw new Error(message);
  }

  // Авторизация пользователя
  static async login(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      const response = await apiClient.post<AuthResponse>(
        "/api/login",
        credentials
      );
      return response.data;
    } catch (error: any) {
      this.handleError(error, "Ошибка авторизации");
    }
  }

  // Регистрация пользователя
  static async register(credentials: RegisterCredentials): Promise<void> {
    try {
      await apiClient.post("/api/register", credentials);
    } catch (error: any) {
      throw new Error(error.response?.data?.error || "Ошибка регистрации");
    }
  }

  static async logout(): Promise<void> {
    try {
      await apiClient.post("/api/logout");
    } catch (error: any) {
      throw new Error(error.response?.data?.error || "Ошибка выхода");
    }
  }

  // Получение данных пользователя
  static async getUserData(): Promise<any> {
    try {
      const response = await apiClient.get("/api/user");
      return response.data;
    } catch (error: any) {
      throw new Error(
        error.response?.data?.error || "Ошибка получения данных пользователя"
      );
    }
  }

  // Смена пароля
  static async changePassword(
    oldPassword: string,
    newPassword: string
  ): Promise<void> {
    try {
      await apiClient.put("/api/change-password", { oldPassword, newPassword });
    } catch (error: any) {
      throw new Error(error.response?.data?.error || "Ошибка смены пароля");
    }
  }
}
