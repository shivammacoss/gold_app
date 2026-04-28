"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuthStore } from "@/stores/auth-store";

const navItems = [
  { label: "Dashboard", href: "/dashboard", icon: "📊" },
  { label: "Wallets", href: "/dashboard/wallets", icon: "💰" },
  { label: "Deposits", href: "/dashboard/deposits", icon: "📥" },
  { label: "Withdrawals", href: "/dashboard/withdrawals", icon: "📤" },
  { label: "Investments", href: "/dashboard/investments", icon: "📈" },
  { label: "Transactions", href: "/dashboard/transactions", icon: "📋" },
];

export function Sidebar() {
  const pathname = usePathname();
  const { logout } = useAuthStore();

  return (
    <aside className="w-64 bg-gray-800 border-r border-gray-700 flex flex-col">
      <div className="p-6">
        <h1 className="text-xl font-bold">
          Setup<span className="text-primary-400">FX</span>
        </h1>
      </div>
      <nav className="flex-1 px-4 space-y-1">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition ${
                isActive
                  ? "bg-primary-600 text-white"
                  : "text-gray-300 hover:bg-gray-700"
              }`}
            >
              <span>{item.icon}</span>
              {item.label}
            </Link>
          );
        })}
      </nav>
      <div className="p-4 border-t border-gray-700">
        <button
          onClick={() => {
            logout();
            window.location.href = "/login";
          }}
          className="w-full px-4 py-2 text-sm text-red-400 hover:bg-gray-700 rounded-lg transition"
        >
          Logout
        </button>
      </div>
    </aside>
  );
}
