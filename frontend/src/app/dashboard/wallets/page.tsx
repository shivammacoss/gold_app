"use client";

import { useEffect, useState } from "react";
import { walletService } from "@/services/wallet-service";
import { shortenAddress } from "@/lib/utils";
import type { Wallet } from "@/types/wallet";
import { NETWORKS } from "@/lib/constants";

export default function WalletsPage() {
  const [wallets, setWallets] = useState<Wallet[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    walletService
      .getWallets()
      .then(setWallets)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p className="text-gray-400 p-8">Loading wallets...</p>;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">My Wallets</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {wallets.map((w) => (
          <div key={w.id} className="bg-gray-800 rounded-xl p-6 space-y-3">
            <div className="flex items-center justify-between">
              <span className={`text-sm font-semibold ${NETWORKS[w.network]?.color}`}>
                {NETWORKS[w.network]?.label}
              </span>
              <span className={`text-xs px-2 py-1 rounded ${w.is_active ? "bg-green-900 text-green-300" : "bg-red-900 text-red-300"}`}>
                {w.is_active ? "Active" : "Inactive"}
              </span>
            </div>
            <p className="text-3xl font-bold">{w.balance} <span className="text-sm text-gray-400">USDT</span></p>
            <p className="text-xs text-gray-500 font-mono">{shortenAddress(w.address, 10)}</p>
          </div>
        ))}
        {wallets.length === 0 && (
          <p className="text-gray-500 col-span-full text-center py-12">No wallets yet.</p>
        )}
      </div>
    </div>
  );
}
