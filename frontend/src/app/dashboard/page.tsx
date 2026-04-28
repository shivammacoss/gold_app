"use client";

import { useEffect, useState } from "react";
import { walletService } from "@/services/wallet-service";
import { investmentService } from "@/services/investment-service";
import type { Wallet } from "@/types/wallet";
import type { UserInvestment } from "@/types/investment";

export default function DashboardPage() {
  const [wallets, setWallets] = useState<Wallet[]>([]);
  const [investments, setInvestments] = useState<UserInvestment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [walletsData, investmentsData] = await Promise.all([
          walletService.getWallets(),
          investmentService.getUserInvestments(),
        ]);
        setWallets(walletsData);
        setInvestments(investmentsData);
      } catch {
        console.error("Failed to load dashboard data");
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  const totalBalance = wallets.reduce(
    (sum, w) => sum + parseFloat(w.balance),
    0
  );
  const totalInvested = investments
    .filter((i) => i.status === "ACTIVE")
    .reduce((sum, i) => sum + parseFloat(i.amount), 0);
  const totalEarned = investments.reduce(
    (sum, i) => sum + parseFloat(i.total_earned),
    0
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-gray-400">Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold">Dashboard</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gray-800 rounded-xl p-6">
          <p className="text-sm text-gray-400">Total Balance</p>
          <p className="text-3xl font-bold text-green-400 mt-1">
            {totalBalance.toFixed(2)} USDT
          </p>
        </div>
        <div className="bg-gray-800 rounded-xl p-6">
          <p className="text-sm text-gray-400">Active Investments</p>
          <p className="text-3xl font-bold text-primary-400 mt-1">
            {totalInvested.toFixed(2)} USDT
          </p>
        </div>
        <div className="bg-gray-800 rounded-xl p-6">
          <p className="text-sm text-gray-400">Total Earnings</p>
          <p className="text-3xl font-bold text-yellow-400 mt-1">
            {totalEarned.toFixed(2)} USDT
          </p>
        </div>
      </div>

      {/* Wallets */}
      <section>
        <h2 className="text-xl font-semibold mb-4">Wallets</h2>
        <div className="bg-gray-800 rounded-xl overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-gray-700 text-gray-300 text-sm">
              <tr>
                <th className="px-6 py-3">Network</th>
                <th className="px-6 py-3">Address</th>
                <th className="px-6 py-3 text-right">Balance</th>
              </tr>
            </thead>
            <tbody>
              {wallets.map((w) => (
                <tr key={w.id} className="border-t border-gray-700">
                  <td className="px-6 py-4 font-medium">{w.network}</td>
                  <td className="px-6 py-4 text-gray-400 text-sm font-mono">
                    {w.address}
                  </td>
                  <td className="px-6 py-4 text-right font-semibold">
                    {w.balance} USDT
                  </td>
                </tr>
              ))}
              {wallets.length === 0 && (
                <tr>
                  <td colSpan={3} className="px-6 py-8 text-center text-gray-500">
                    No wallets found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
