"use client";

import { useEffect, useState } from "react";
import { transactionService } from "@/services/transaction-service";
import { formatDate } from "@/lib/utils";
import { TRANSACTION_LABELS } from "@/lib/constants";
import type { Transaction } from "@/types/transaction";

export default function TransactionsPage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    transactionService
      .getTransactions()
      .then(setTransactions)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p className="text-gray-400 p-8">Loading transactions...</p>;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Transaction History</h1>
      <div className="bg-gray-800 rounded-xl overflow-hidden">
        <table className="w-full text-left text-sm">
          <thead className="bg-gray-700 text-gray-300">
            <tr>
              <th className="px-4 py-3">Type</th>
              <th className="px-4 py-3">Amount</th>
              <th className="px-4 py-3">Description</th>
              <th className="px-4 py-3">Date</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((tx) => {
              const label = TRANSACTION_LABELS[tx.tx_type] || {
                label: tx.tx_type,
                color: "text-gray-400",
              };
              return (
                <tr key={tx.id} className="border-t border-gray-700">
                  <td className="px-4 py-3">
                    <span className={`font-medium ${label.color}`}>
                      {label.label}
                    </span>
                  </td>
                  <td className="px-4 py-3 font-semibold">{tx.amount} USDT</td>
                  <td className="px-4 py-3 text-gray-400 truncate max-w-xs">
                    {tx.description}
                  </td>
                  <td className="px-4 py-3 text-gray-400">
                    {formatDate(tx.created_at)}
                  </td>
                </tr>
              );
            })}
            {transactions.length === 0 && (
              <tr>
                <td colSpan={4} className="px-4 py-8 text-center text-gray-500">
                  No transactions yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
