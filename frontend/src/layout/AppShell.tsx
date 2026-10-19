import { useEffect, useMemo, useState } from "react";
import { NavLink, Outlet, useNavigate } from "react-router-dom";
import {
  Activity,
  BarChart3,
  Bell,
  BookOpen,
  Building2,
  FileText,
  KeyRound,
  Landmark,
  Plug,
  Receipt,
  ScrollText,
  Search,
  Settings,
  ShieldAlert,
  Sparkles,
  Users,
  UserPlus,
  Wallet,
} from "lucide-react";
import { api, getOrgId, getToken } from "../api/client";
import type { Notification } from "../api/types";
import { useAuth } from "../state/auth";

const NAV = [
  {
    label: "Workspace",
    items: [
      { to: "/", icon: BarChart3, label: "Revenue" },
      { to: "/forecasts", icon: Sparkles, label: "Forecasts" },
      { to: "/commissions", icon: Receipt, label: "Commissions" },
    ],
  },
  {
    label: "Commercial",
    items: [
      { to: "/customers", icon: Users, label: "Customers" },
      { to: "/catalog", icon: BookOpen, label: "Catalog" },
      { to: "/subscriptions", icon: Building2, label: "Subscriptions" },
      { to: "/entitlements", icon: KeyRound, label: "Entitlements" },
      { to: "/contracts", icon: Landmark, label: "Contracts" },
    ],
  },
  {
    label: "Billing",
    items: [
      { to: "/invoices", icon: FileText, label: "Invoices" },
      { to: "/payments", icon: Wallet, label: "Payments" },
      { to: "/usage", icon: Activity, label: "Usage" },
      { to: "/dunning", icon: ShieldAlert, label: "Dunning" },
    ],
  },
  {
    label: "Operations",
    items: [
      { to: "/integrations", icon: Plug, label: "Integrations" },
      { to: "/reports", icon: Receipt, label: "Reports" },
      { to: "/notifications", icon: Bell, label: "Notifications" },
      { to: "/audit", icon: ScrollText, label: "Audit" },
      { to: "/search", icon: Search, label: "Search" },
      { to: "/team", icon: UserPlus, label: "Team" },
      { to: "/settings", icon: Settings, label: "Settings" },
    ],
  },
];

export function AppShell() {
  const { user, organization, logout } = useAuth();
  const navigate = useNavigate();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<{ type: string; id: string; label: string; hint: string }[]>([]);
  const [notes, setNotes] = useState<Notification[]>([]);

  useEffect(() => {
    api.get<{ results: Notification[] }>("/api/v1/notifications/").then((d) => setNotes(d.results ?? [])).catch(() => undefined);
    const token = getToken();
    const org = getOrgId();
    if (!token) return;
    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    const socket = new WebSocket(`${protocol}://${window.location.host}/ws/notifications/?token=${token}&organization_id=${org}`);
    socket.onmessage = (event) => {
      const payload = JSON.parse(event.data);
      setNotes((current) => [payload, ...current].slice(0, 20));
    };
    return () => socket.close();
  }, []);

  useEffect(() => {
    if (!query) {
      setResults([]);
      return;
    }
    const handle = setTimeout(() => {
      api.get<{ results: typeof results }>(`/api/v1/search/?q=${encodeURIComponent(query)}`).then((d) => setResults(d.results));
    }, 180);
    return () => clearTimeout(handle);
  }, [query]);

  const unread = useMemo(() => notes.filter((n) => !n.read_at).length, [notes]);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="mark">
          <i /> Revanta
        </div>
        {NAV.map((group) => (
          <div className="nav-group" key={group.label}>
            <div className="nav-label">{group.label}</div>
            {group.items.map((item) => (
              <NavLink key={item.to} to={item.to} end={item.to === "/"} className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
                <item.icon size={16} />
                {item.label}
              </NavLink>
            ))}
          </div>
        ))}
        <div className="workspace">
          <strong>{organization?.name}</strong>
          <div className="muted">{user?.display_name || user?.email}</div>
        </div>
      </aside>
      <div className="main">
        <header className="topbar">
          <div className="search">
            <Search className="search-icon" size={16} />
            <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search customers, invoices, contracts…" />
            {results.length > 0 && (
              <div className="search-results">
                {results.map((item) => (
                  <a
                    key={`${item.type}-${item.id}`}
                    href="#"
                    onClick={(e) => {
                      e.preventDefault();
                      const routes: Record<string, string> = {
                        customer: `/customers/${item.id}`,
                        subscription: `/subscriptions/${item.id}`,
                        invoice: `/invoices/${item.id}`,
                        product: "/catalog",
                        contract: "/contracts",
                        entitlement: "/entitlements",
                        integration: "/integrations",
                      };
                      setQuery("");
                      navigate(routes[item.type] || "/");
                    }}
                  >
                    <strong>{item.label}</strong>
                    <div className="muted">
                      {item.type} · {item.hint}
                    </div>
                  </a>
                ))}
              </div>
            )}
          </div>
          <button className="btn ghost" title="Notifications">
            <Bell size={16} /> {unread || ""}
          </button>
          <button className="btn ghost" onClick={logout}>
            Sign out
          </button>
        </header>
        <div className="content">
          <Outlet />
        </div>
      </div>
    </div>
  );
}
