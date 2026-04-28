"use client";

import { useEffect, useState } from "react";
import { investmentService } from "@/services/investment-service";
import { formatDate } from "@/lib/utils";
import type { InvestmentPlan, UserInvestment } from "@/types/investment";

export default function InvestmentsPage() {
  const [plans, setPlans] = useState<InvestmentPlan[]>([]);
  const [investments, setInvestments] = useState<UserInvestment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      investmentService.getPlans(),
      investmentService.getUserInvestments(),
    ])
      .then(([p, i]) => {
        setPlans(p);
        setInvestments(i);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p className="text-gray-400 p-8">Loading investments...</p>;
  }

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold">Investments</h1>

      {/* Available Plans */}
      <section>
        <h2 className="text-lg font-semibold mb-4">Available Plans</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {plans.map((plan) => (
            <div key={plan.id} className="bg-gray-800 rounded-xl p-6 space-y-3 border border-gray-700">
              <h3 className="text-lg font-bold">{plan.name}</h3>
              <p className="text-sm text-gray-400">{plan.description}</p>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Daily ROI</span>
                <span className="text-green-400 font-semibold">{plan.daily_roi_percent}%</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Duration</span>
                <span>{plan.duration_days} days</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Range</span>
                <span>{plan.min_amount} — {plan.max_amount} USDT</span>
              </div>
              <button className="w-full mt-2 py-2 bg-primary-600 hover:bg-primary-700 rounded-lg font-semibold text-sm transition">
                Invest Now
              </button>
            </div>
          ))}
        </div>
      </section>

      {/* My Investments */}
      <section>
        <h2 className="text-lg font-semibold mb-4">My Investments</h2>
        <div className="bg-gray-800 rounded-xl overflow-hidden">
          <table className="w-full text-left text-sm">
            <thead className="bg-gray-700 text-gray-300">
              <tr>
                <th className="px-4 py-3">Plan</th>
                <th className="px-4 py-3">Amount</th>
                <th className="px-4 py-3">Earned</th>
                <th className="px-4 py-3">Days</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Expires</th>
              </tr>
            </thead>
            <tbody>
              {investments.map((inv) => (
                <tr key={inv.id} className="border-t border-gray-700">
                  <td className="px-4 py-3 font-medium">{inv.plan_name}</td>
                  <td className="px-4 py-3">{inv.amount} USDT</td>
                  <td className="px-4 py-3 text-green-400">{inv.total_earned} USDT</td>
                  <td className="px-4 py-3">{inv.days_completed}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      inv.status === "ACTIVE" ? "bg-green-900 text-green-300" :
                      inv.status === "COMPLETED" ? "bg-blue-900 text-blue-300" :
                      "bg-red-900 text-red-300"
                    }`}>
                      {inv.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-gray-400">{formatDate(inv.expires_at)}</td>
                </tr>
              ))}
              {investments.length === 0 && (
                <tr>
                  <td colSpan={6} className="px-4 py-8 text-center text-gray-500">
                    No investments yet.
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
