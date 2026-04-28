"use client";

import { useEffect, useState } from "react";
import { authService } from "@/services/auth-service";
import type { User } from "@/types/user";

export function Header() {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    authService.getMe().then(setUser).catch(() => {});
  }, []);

  return (
    <header className="h-16 bg-gray-800 border-b border-gray-700 flex items-center justify-between px-6">
      <div />
      <div className="flex items-center gap-4">
        {user && (
          <div className="text-right">
            <p className="text-sm font-medium">{user.email}</p>
            <p className="text-xs text-gray-400">
              {user.is_kyc_verified ? "Verified" : "Unverified"}
            </p>
          </div>
        )}
        <div className="w-9 h-9 rounded-full bg-primary-600 flex items-center justify-center text-sm font-bold">
          {user?.email?.charAt(0).toUpperCase() || "U"}
        </div>
      </div>
    </header>
  );
}
