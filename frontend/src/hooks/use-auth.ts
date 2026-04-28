import { useEffect, useState } from "react";
import { useAuthStore } from "@/stores/auth-store";
import { authService } from "@/services/auth-service";
import type { User } from "@/types/user";

export function useAuth() {
  const { isAuthenticated, logout } = useAuthStore();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated) {
      setLoading(false);
      return;
    }
    authService
      .getMe()
      .then(setUser)
      .catch(() => logout())
      .finally(() => setLoading(false));
  }, [isAuthenticated, logout]);

  return { user, loading, isAuthenticated };
}
