import type { UsagePeriod } from "../api/types";
import { PageHeader, Panel } from "../components/ui";
import { useResource } from "../hooks/useResource";

type Metric = { id: string; name: string; code: string; aggregation: string; unit_label: string };

export function UsagePage() {
  const { data: metrics } = useResource<Metric>("/api/v1/usage/metrics/");
  const { data: periods } = useResource<UsagePeriod>("/api/v1/usage/periods/");

  return (
    <>
      <PageHeader title="Usage" subtitle="Event ingestion, idempotency, aggregation windows, and billable counters." />
      <div className="grid-2">
        <Panel title="Meters">
          <table>
            <thead><tr><th>Metric</th><th>Code</th><th>Aggregation</th></tr></thead>
            <tbody>
              {metrics.map((m) => (
                <tr key={m.id}><td>{m.name}</td><td>{m.code}</td><td>{m.aggregation}</td></tr>
              ))}
            </tbody>
          </table>
        </Panel>
        <Panel title="Open periods">
          <table>
            <thead><tr><th>Account</th><th>Metric</th><th>Qty</th></tr></thead>
            <tbody>
              {periods.map((p) => (
                <tr key={p.id}><td>{p.company_name}</td><td>{p.metric_name}</td><td>{p.billable_quantity}</td></tr>
              ))}
            </tbody>
          </table>
        </Panel>
      </div>
    </>
  );
}
