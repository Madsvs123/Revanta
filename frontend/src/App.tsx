import { Navigate, Route, Routes } from "react-router-dom";
import { AppShell } from "./layout/AppShell";
import { AuditPage } from "./pages/Audit";
import { CatalogPage } from "./pages/Catalog";
import { CommissionsPage } from "./pages/Commissions";
import { ContractsPage } from "./pages/Contracts";
import { CustomerDetailPage } from "./pages/CustomerDetail";
import { CustomersPage } from "./pages/Customers";
import { DashboardPage } from "./pages/Dashboard";
import { DunningPage } from "./pages/Dunning";
import { EntitlementsPage } from "./pages/Entitlements";
import { ForecastsPage } from "./pages/Forecasts";
import { IntegrationsPage } from "./pages/Integrations";
import { InvoiceDetailPage } from "./pages/InvoiceDetail";
import { InvoicesPage } from "./pages/Invoices";
import { LoginPage } from "./pages/Login";
import { NotificationsPage } from "./pages/Notifications";
import { PaymentsPage } from "./pages/Payments";
import { RegisterPage } from "./pages/Register";
import { ReportsPage } from "./pages/Reports";
import { SearchPage } from "./pages/Search";
import { SettingsPage } from "./pages/Settings";
import { SubscriptionDetailPage } from "./pages/SubscriptionDetail";
import { SubscriptionsPage } from "./pages/Subscriptions";
import { TeamPage } from "./pages/Team";
import { UsagePage } from "./pages/Usage";
import { useAuth } from "./state/auth";

function Guard({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  if (loading) return <p style={{ padding: 40 }}>Opening workspace…</p>;
  if (!user) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route
        element={
          <Guard>
            <AppShell />
          </Guard>
        }
      >
        <Route path="/" element={<DashboardPage />} />
        <Route path="/forecasts" element={<ForecastsPage />} />
        <Route path="/commissions" element={<CommissionsPage />} />
        <Route path="/customers" element={<CustomersPage />} />
        <Route path="/customers/:id" element={<CustomerDetailPage />} />
        <Route path="/catalog" element={<CatalogPage />} />
        <Route path="/subscriptions" element={<SubscriptionsPage />} />
        <Route path="/subscriptions/:id" element={<SubscriptionDetailPage />} />
        <Route path="/entitlements" element={<EntitlementsPage />} />
        <Route path="/contracts" element={<ContractsPage />} />
        <Route path="/invoices" element={<InvoicesPage />} />
        <Route path="/invoices/:id" element={<InvoiceDetailPage />} />
        <Route path="/payments" element={<PaymentsPage />} />
        <Route path="/usage" element={<UsagePage />} />
        <Route path="/dunning" element={<DunningPage />} />
        <Route path="/integrations" element={<IntegrationsPage />} />
        <Route path="/reports" element={<ReportsPage />} />
        <Route path="/notifications" element={<NotificationsPage />} />
        <Route path="/audit" element={<AuditPage />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/team" element={<TeamPage />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Route>
    </Routes>
  );
}
