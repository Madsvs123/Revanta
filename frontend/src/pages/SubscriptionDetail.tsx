import { useParams } from "react-router-dom";
import { api, money } from "../api/client";
import type { Plan, Subscription } from "../api/types";
import { Panel, StatusPill } from "../components/ui";
import { useOne, useResource } from "../hooks/useResource";

export function SubscriptionDetailPage() {
  const { id } = useParams();
  const { data: sub, reload } = useOne<Subscription>(id ? `/api/v1/subscriptions/${id}/` : null);
  const { data: plans } = useResource<Plan>("/api/v1/plans/");
  if (!sub) return <p>Loading subscription…</p>;

  const act = async (path: string, body: Record<string, unknown> = {}) => {
    await api.post(`/api/v1/subscriptions/${sub.id}/${path}/`, body);
    reload();
  };

  return (
    <>
      <div className="page-head">
        <div>
          <h1>{sub.company_name}</h1>
          <p>{sub.plan_name} · {money(sub.mrr, sub.currency)} MRR</p>
        </div>
        <StatusPill value={sub.status} />
      </div>
      <div className="row">
        <button className="btn ghost" onClick={() => act("pause")}>Pause</button>
        <button className="btn ghost" onClick={() => act("resume")}>Resume</button>
        <button className="btn danger" onClick={() => act("cancel", { at_period_end: true })}>Cancel at period end</button>
      </div>
      <Panel title="Change plan">
        <div className="row">
          {plans.map((plan) => (
            <button key={plan.id} className="btn ghost" onClick={() => act("change_plan", { plan_id: plan.id })}>
              Move to {plan.name}
            </button>
          ))}
        </div>
      </Panel>
      <div className="detail-grid">
        <Panel title="Items">
          <table>
            <tbody>
              {(sub.items ?? []).map((item) => (
                <tr key={item.id}>
                  <td>{item.description}</td>
                  <td>{item.quantity}</td>
                  <td>{money(item.unit_amount, sub.currency)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>
        <Panel title="Amendments">
          <table>
            <tbody>
              {(sub.amendments ?? []).map((a) => (
                <tr key={a.id}>
                  <td>{a.amendment_type}</td>
                  <td>{a.summary}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>
      </div>
    </>
  );
}
