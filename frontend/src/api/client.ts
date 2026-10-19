const TOKEN_KEY = "revanta.access";
const REFRESH_KEY = "revanta.refresh";
const ORG_KEY = "revanta.org";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}
export function getRefresh() {
  return localStorage.getItem(REFRESH_KEY);
}
export function getOrgId() {
  return localStorage.getItem(ORG_KEY);
}
export function setSession(access: string, refresh: string, orgId?: string) {
  localStorage.setItem(TOKEN_KEY, access);
  localStorage.setItem(REFRESH_KEY, refresh);
  if (orgId) localStorage.setItem(ORG_KEY, orgId);
}
export function clearSession() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REFRESH_KEY);
  localStorage.removeItem(ORG_KEY);
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set("Content-Type", "application/json");
  const token = getToken();
  const org = getOrgId();
  if (token) headers.set("Authorization", `Bearer ${token}`);
  if (org) headers.set("X-Organization-Id", org);
  const response = await fetch(path, { ...init, headers });
  if (response.status === 401 && getRefresh()) {
    const refreshed = await fetch("/api/v1/auth/refresh/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh: getRefresh() }),
    });
    if (refreshed.ok) {
      const data = await refreshed.json();
      localStorage.setItem(TOKEN_KEY, data.access);
      if (data.refresh) localStorage.setItem(REFRESH_KEY, data.refresh);
      headers.set("Authorization", `Bearer ${data.access}`);
      const retry = await fetch(path, { ...init, headers });
      if (!retry.ok) throw new Error(await retry.text());
      return retry.status === 204 ? (undefined as T) : retry.json();
    }
    clearSession();
  }
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || response.statusText);
  }
  if (response.status === 204) return undefined as T;
  return response.json();
}

export const api = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, body?: unknown) => request<T>(path, { method: "POST", body: JSON.stringify(body ?? {}) }),
  patch: <T>(path: string, body?: unknown) => request<T>(path, { method: "PATCH", body: JSON.stringify(body ?? {}) }),
  delete: <T>(path: string) => request<T>(path, { method: "DELETE" }),
};

export function money(value?: string | number, currency = "USD") {
  const amount = Number(value || 0);
  return new Intl.NumberFormat("en-US", { style: "currency", currency, maximumFractionDigits: 0 }).format(amount);
}

export function list<T>(payload: { results?: T[] } | T[] | undefined): T[] {
  if (!payload) return [];
  if (Array.isArray(payload)) return payload;
  return payload.results ?? [];
}
