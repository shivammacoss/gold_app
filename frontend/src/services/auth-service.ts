import apiClient from "@/lib/api-client";
import type { LoginResponse, RegisterPayload, User } from "@/types/user";

export const authService = {
  async login(email: string, password: string): Promise<LoginResponse> {
    const { data } = await apiClient.post("/auth/login/", { email, password });
    return data;
  },

  async register(payload: RegisterPayload) {
    const { data } = await apiClient.post("/auth/register/", payload);
    return data;
  },

  async getMe(): Promise<User> {
    const { data } = await apiClient.get("/auth/me/");
    return data;
  },

  async changePassword(oldPassword: string, newPassword: string) {
    const { data } = await apiClient.post("/auth/change-password/", {
      old_password: oldPassword,
      new_password: newPassword,
    });
    return data;
  },
};
