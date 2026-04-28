import apiClient from "@/lib/api-client";
import type { InvestmentPlan, UserInvestment } from "@/types/investment";

export const investmentService = {
  async getPlans(): Promise<InvestmentPlan[]> {
    const { data } = await apiClient.get("/investments/plans/");
    return data.results ?? data;
  },

  async getUserInvestments(): Promise<UserInvestment[]> {
    const { data } = await apiClient.get("/investments/");
    return data.results ?? data;
  },

  async createInvestment(planId: string, walletId: string, amount: number) {
    const { data } = await apiClient.post("/investments/create/", {
      plan_id: planId,
      wallet_id: walletId,
      amount,
    });
    return data;
  },
};
