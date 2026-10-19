import { useParams } from "react-router-dom";
import { api, money } from "../api/client";
import type { Company, Subscription } from "../api/types";
import { Metric, Panel, StatusPill } from "../components/ui";
import { useOne, useResource } from "../hooks/useResource";

export function CustomerDetailPage() {
  const { id } = useParams();
  const { data: company, reload } = useOne<Company>(id ? `/api/v1/customers/${id}/` : null);
  const { data: subscriptions } = useResource<Subscription>(id ? `/api/v1/subscriptions/?company=${id}` : null);
  if (!company) return <p>Loading account…</p>;

  return (
    <>
      <div className="page-head">
        <div>
          <h1>{company.name}</h1>
          <p>{company.domain} · {company.country}</p>
        </div>
        <StatusPill value={company.stage} />
      </div>
      <div className="metrics">
        <Metric label="MRR" value={money(company.mrr)} />
        <Metric label="Balance" value={money(company.balance)} />
        <Metric label="Credits" value={money(company.credit_balance)} />
        <Metric label="Health" value={String(company.health_score)} />
      </div>
      <div className="detail-grid">
        <Panel title="Contacts">
          <table>
            <tbody>
              {(company.contacts ?? []).map((c) => (
                <tr key={c.id}>
                  <td>{c.first_name} {c.last_name}</td>
                  <td>{c.email}</td>
                  <td>{c.title}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>
        <Panel title="Issue credit">
          <button
            className="btn"
            onClick={async () => {
              await api.post(`/api/v1/customers/${company.id}/credit/`, { amount: 250, reason: "Goodwill" });
              reload();
            }}
          >
            Add $250 credit
          </button>
        </Panel>
      </div>
      <Panel title="Subscriptions">
        <table>
          <thead>
            <tr><th>Plan</th><th>Status</th><th>MRR</th></tr>
          </thead>
          <tbody>
            {subscriptions.map((sub) => (
              <tr key={sub.id}>
                <td>{sub.plan_name}</td>
                <td><StatusPill value={sub.status} /></td>
                <td>{money(sub.mrr, sub.currency)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Panel>
    </>
  );
}
