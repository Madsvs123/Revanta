import { api } from "../api/client";
import { PageHeader, Panel, StatusPill } from "../components/ui";
import { useResource } from "../hooks/useResource";

type Connector = { id: string; name: string; provider: string; status: string; last_synced_at?: string };
type Delivery = { id: string; endpoint_name: string; event_type: string; status: string; attempt_count: number; created_at: string };
type Job = { id: string; connector_name: string; job_type: string; status: string; records: number };

export function IntegrationsPage() {
  const { data: connectors, reload } = useResource<Connector>("/api/v1/integrations/connectors/");
  const { data: deliveries, reload: reloadDeliveries } = useResource<Delivery>("/api/v1/integrations/deliveries/");
  const { data: jobs } = useResource<Job>("/api/v1/integrations/jobs/");

  return (
    <>
      <PageHeader
        title="Integrations"
        subtitle="Replaceable connectors, outbound webhooks, delivery retries, and sync jobs."
        actions={
          <button
            className="btn"
            onClick={async () => {
              await api.post("/api/v1/integrations/deliveries/emit/", { event_type: "manual.test", payload: { source: "ui" } });
              reloadDeliveries();
            }}
          >
            Emit test event
          </button>
        }
      />
      <div className="grid-2">
        <Panel title="Connectors">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Provider</th>
                <th>Status</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {connectors.map((c) => (
                <tr key={c.id}>
                  <td>{c.name}</td>
                  <td>{c.provider}</td>
                  <td>
                    <StatusPill value={c.status} />
                  </td>
                  <td>
                    <button className="btn ghost" onClick={() => api.post(`/api/v1/integrations/connectors/${c.id}/sync/`, { job_type: "customers" }).then(reload)}>
                      Sync
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>
        <Panel title="Sync jobs">
          <table>
            <tbody>
              {jobs.map((j) => (
                <tr key={j.id}>
                  <td>{j.connector_name}</td>
                  <td>{j.job_type}</td>
                  <td>{j.records} records</td>
                  <td>
                    <StatusPill value={j.status} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>
      </div>
      <Panel title="Deliveries">
        <table>
          <thead>
            <tr>
              <th>Endpoint</th>
              <th>Event</th>
              <th>Status</th>
              <th>Attempts</th>
            </tr>
          </thead>
          <tbody>
            {deliveries.map((d) => (
              <tr key={d.id}>
                <td>{d.endpoint_name}</td>
                <td>{d.event_type}</td>
                <td>
                  <StatusPill value={d.status} />
                </td>
                <td>
                  {d.attempt_count}{" "}
                  {d.status === "failed" && (
                    <button className="btn ghost" onClick={() => api.post(`/api/v1/integrations/deliveries/${d.id}/retry/`).then(reloadDeliveries)}>
                      Retry
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Panel>
    </>
  );
}
