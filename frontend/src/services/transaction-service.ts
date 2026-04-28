import apiClient from "@/lib/api-client";
import type { Transaction, TransactionType } from "@/types/transaction";

export const transactionService = {
  async getTransactions(txType?: TransactionType): Promise<Transaction[]> {
    const params = txType ? { tx_type: txType } : {};
    const { data } = await apiClient.get("/transactions/", { params });
    return data.results ?? data;
  },
};
