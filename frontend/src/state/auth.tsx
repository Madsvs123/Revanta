import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { api, clearSession, getToken, setSession } from "../api/client";
import type { Organization, User } from "../api/types";

type AuthState = {
  user: User | null;
  organization: Organization | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (payload: Record<string, string>) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [organization, setOrganization] = useState<Organization | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!getToken()) {
      setLoading(false);
      return;
    }
    api
      .get<{ user: User; organization: Organization }>("/api/v1/auth/me/")
      .then((data) => {
        setUser(data.user);
        setOrganization(data.organization);
      })
      .catch(() => clearSession())
      .finally(() => setLoading(false));
  }, []);

  const value = useMemo<AuthState>(
    () => ({
      user,
      organization,
      loading,
      async login(email, password) {
        const data = await api.post<{
          user: User;
          organization: Organization;
          access: string;
          refresh: string;
        }>("/api/v1/auth/login/", { email, password });
        setSession(data.access, data.refresh, data.organization.id);
        setUser(data.user);
        setOrganization(data.organization);
      },
      async register(payload) {
        const data = await api.post<{
          user: User;
          organization: Organization;
          access: string;
          refresh: string;
        }>("/api/v1/auth/register/", payload);
        setSession(data.access, data.refresh, data.organization.id);
        setUser(data.user);
        setOrganization(data.organization);
      },
      logout() {
        clearSession();
        setUser(null);
        setOrganization(null);
      },
    }),
    [user, organization, loading],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("AuthProvider missing");
  return ctx;
}
