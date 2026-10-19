import { useState } from "react";
import { Link } from "react-router-dom";
import { api, money } from "../api/client";
import type { Company } from "../api/types";
import { PageHeader, Panel, StatusPill } from "../components/ui";
import { useResource } from "../hooks/useResource";

export function CustomersPage() {
  const { data, reload } = useResource<Company>("/api/v1/customers/");
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({ name: "", domain: "", country: "US", industry: "SaaS" });

  return (
    <>
      <PageHeader
        title="Customers"
        subtitle="Companies, billing profiles, health, and account ownership."
        actions={<button className="btn" onClick={() => setOpen((v) => !v)}>New account</button>}
      />
      {open && (
        <Panel title="Create company">
          <div className="grid-3">
            <div>
              <label>Name</label>
              <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
            </div>
            <div>
              <label>Domain</label>
              <input value={form.domain} onChange={(e) => setForm({ ...form, domain: e.target.value })} />
            </div>
            <div>
              <label>Country</label>
              <input value={form.country} onChange={(e) => setForm({ ...form, country: e.target.value })} />
            </div>
          </div>
          <div className="row" style={{ marginTop: 12 }}>
            <button
              className="btn copper"
              onClick={async () => {
                await api.post("/api/v1/customers/", form);
                setOpen(false);
                reload();
              }}
            >
              Save account
            </button>
          </div>
        </Panel>
      )}
      <Panel>
        <table>
          <thead>
            <tr>
              <th>Company</th>
              <th>Stage</th>
              <th>MRR</th>
              <th>Balance</th>
              <th>Health</th>
            </tr>
          </thead>
          <tbody>
            {data.map((company) => (
              <tr key={company.id}>
                <td>
                  <Link to={`/customers/${company.id}`}>
                    <strong>{company.name}</strong>
                    <div className="muted">{company.domain}</div>
                  </Link>
                </td>
                <td><StatusPill value={company.stage} /></td>
                <td>{money(company.mrr)}</td>
                <td>{money(company.balance)}</td>
                <td>{company.health_score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Panel>
    </>
  );
}
