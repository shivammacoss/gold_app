import apiClient from "@/lib/api-client";
import type { Wallet } from "@/types/wallet";

export const walletService = {
  async getWallets(): Promise<Wallet[]> {
    const { data } = await apiClient.get("/wallets/");
    return data.results ?? data;
  },

  async getWallet(id: string): Promise<Wallet> {
    const { data } = await apiClient.get(`/wallets/${id}/`);
    return data;
  },
};
