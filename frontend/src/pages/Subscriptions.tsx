import { useState } from "react";
import { Link } from "react-router-dom";
import { api, money } from "../api/client";
import type { Company, Plan, Subscription } from "../api/types";
import { PageHeader, Panel, StatusPill } from "../components/ui";
import { useResource } from "../hooks/useResource";

export function SubscriptionsPage() {
  const { data, reload } = useResource<Subscription>("/api/v1/subscriptions/");
  const { data: companies } = useResource<Company>("/api/v1/customers/");
  const { data: plans } = useResource<Plan>("/api/v1/plans/");
  const [form, setForm] = useState({ company_id: "", plan_id: "", quantity: "1" });

  return (
    <>
      <PageHeader title="Subscriptions" subtitle="Activation, amendments, scheduled changes, and lifecycle." />
      <Panel title="Activate">
        <div className="grid-3">
          <select value={form.company_id} onChange={(e) => setForm({ ...form, company_id: e.target.value })}>
            <option value="">Customer</option>
            {companies.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
          <select value={form.plan_id} onChange={(e) => setForm({ ...form, plan_id: e.target.value })}>
            <option value="">Plan</option>
            {plans.map((p) => <option key={p.id} value={p.id}>{p.name}</option>)}
          </select>
          <input value={form.quantity} onChange={(e) => setForm({ ...form, quantity: e.target.value })} />
        </div>
        <button className="btn" style={{ marginTop: 12 }} onClick={async () => { await api.post("/api/v1/subscriptions/", { ...form, quantity: Number(form.quantity) }); reload(); }}>
          Activate subscription
        </button>
      </Panel>
      <Panel>
        <table>
          <thead><tr><th>Account</th><th>Plan</th><th>Status</th><th>Qty</th><th>MRR</th><th>Period</th></tr></thead>
          <tbody>
            {data.map((sub) => (
              <tr key={sub.id}>
                <td><Link to={`/subscriptions/${sub.id}`}>{sub.company_name}</Link></td>
                <td>{sub.plan_name}</td>
                <td><StatusPill value={sub.status} /></td>
                <td>{sub.quantity}</td>
                <td>{money(sub.mrr, sub.currency)}</td>
                <td>{sub.current_period_start} → {sub.current_period_end}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Panel>
    </>
  );
}
