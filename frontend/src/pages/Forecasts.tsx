import { api, money } from "../api/client";
import { Metric, PageHeader, Panel } from "../components/ui";
import { useResource } from "../hooks/useResource";

type Outlook = {
  id: string;
  name: string;
  committed: string;
  pipeline: string;
  best_case: string;
  period_start: string;
  period_end: string;
  scenarios: { id: string; name: string; probability: number; uplift_percent: string }[];
  lines: { id: string; month: string; new_mrr: string; expansion_mrr: string; churn_mrr: string; ending_mrr: string }[];
  assumptions: { id: string; name: string; value: string; unit: string }[];
};

export function ForecastsPage() {
  const { data: outlooks, reload } = useResource<Outlook>("/api/v1/forecasts/");
  const current = outlooks[0];

  return (
    <>
      <PageHeader
        title="Forecasts"
        subtitle="Renewal outlooks, scenarios, monthly bridges, and capacity assumptions."
        actions={
          <button className="btn" onClick={() => api.post("/api/v1/forecasts/refresh/", {}).then(reload)}>
            Refresh outlook
          </button>
        }
      />
      <div className="metrics">
        <Metric label="Committed" value={money(current?.committed)} />
        <Metric label="Pipeline" value={money(current?.pipeline)} />
        <Metric label="Best case" value={money(current?.best_case)} />
        <Metric label="Window" value={current ? `${current.period_start} → ${current.period_end}` : "—"} />
      </div>
      <div className="grid-2">
        <Panel title="Monthly bridge">
          <table>
            <thead>
              <tr>
                <th>Month</th>
                <th>New</th>
                <th>Expansion</th>
                <th>Churn</th>
                <th>Ending</th>
              </tr>
            </thead>
            <tbody>
              {(current?.lines ?? []).map((line) => (
                <tr key={line.id}>
                  <td>{line.month}</td>
                  <td>{money(line.new_mrr)}</td>
                  <td>{money(line.expansion_mrr)}</td>
                  <td>{money(line.churn_mrr)}</td>
                  <td>{money(line.ending_mrr)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>
        <Panel title="Scenarios">
          <table>
            <tbody>
              {(current?.scenarios ?? []).map((s) => (
                <tr key={s.id}>
                  <td>{s.name}</td>
                  <td>{s.probability}%</td>
                  <td>{s.uplift_percent}%</td>
                </tr>
              ))}
            </tbody>
          </table>
          <h3>Assumptions</h3>
          <table>
            <tbody>
              {(current?.assumptions ?? []).map((a) => (
                <tr key={a.id}>
                  <td>{a.name}</td>
                  <td>
                    {a.value} {a.unit}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>
      </div>
    </>
  );
}
