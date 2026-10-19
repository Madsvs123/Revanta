import { api, money } from "../api/client";
import { Metric, PageHeader, Panel, StatusPill } from "../components/ui";
import { useResource } from "../hooks/useResource";

type Plan = { id: string; name: string; source: string; default_rate: string; is_active: boolean };
type Accrual = { id: string; owner_name: string; company_name: string; amount: string; rate: string; source: string; status: string; period: string };
type Payout = { id: string; owner_name: string; period: string; amount: string; status: string };

export function CommissionsPage() {
  const { data: plans } = useResource<Plan>("/api/v1/commission-plans/");
  const { data: accruals, reload } = useResource<Accrual>("/api/v1/commissions/");
  const { data: payouts, reload: reloadPayouts } = useResource<Payout>("/api/v1/commission-payouts/");

  return (
    <>
      <PageHeader
        title="Commissions"
        subtitle="Plans, tiered rates, accruals, and payouts for sales operations."
        actions={
          <button
            className="btn"
            onClick={async () => {
              await api.post("/api/v1/commission-payouts/generate/", { period: new Date().toISOString().slice(0, 7) });
              reloadPayouts();
            }}
          >
            Generate payout
          </button>
        }
      />
      <div className="metrics">
        <Metric label="Accrued" value={money(accruals.filter((a) => a.status === "accrued").reduce((s, a) => s + Number(a.amount), 0))} />
        <Metric label="Paid" value={money(accruals.filter((a) => a.status === "paid").reduce((s, a) => s + Number(a.amount), 0))} />
        <Metric label="Plans" value={String(plans.length)} />
        <Metric label="Open payouts" value={String(payouts.filter((p) => p.status !== "paid").length)} />
      </div>
      <div className="grid-2">
        <Panel title="Plans">
          <table>
            <tbody>
              {plans.map((p) => (
                <tr key={p.id}>
                  <td>{p.name}</td>
                  <td>{p.source}</td>
                  <td>{p.default_rate}%</td>
                  <td>
                    <StatusPill value={p.is_active ? "active" : "archived"} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>
        <Panel title="Payouts">
          <table>
            <tbody>
              {payouts.map((p) => (
                <tr key={p.id}>
                  <td>{p.owner_name}</td>
                  <td>{p.period}</td>
                  <td>{money(p.amount)}</td>
                  <td>
                    <StatusPill value={p.status} />
                    {p.status !== "paid" && (
                      <button className="btn ghost" onClick={() => api.post(`/api/v1/commission-payouts/${p.id}/pay/`).then(() => { reload(); reloadPayouts(); })}>
                        Mark paid
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>
      </div>
      <Panel title="Accruals">
        <table>
          <thead>
            <tr>
              <th>Owner</th>
              <th>Account</th>
              <th>Source</th>
              <th>Rate</th>
              <th>Amount</th>
            </tr>
          </thead>
          <tbody>
            {accruals.map((a) => (
              <tr key={a.id}>
                <td>{a.owner_name}</td>
                <td>{a.company_name}</td>
                <td>{a.source}</td>
                <td>{a.rate}%</td>
                <td>{money(a.amount)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Panel>
    </>
  );
}
