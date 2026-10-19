import { api } from "../api/client";
import type { DunningCase } from "../api/types";
import { PageHeader, Panel, StatusPill } from "../components/ui";
import { useResource } from "../hooks/useResource";

export function DunningPage() {
  const { data, reload } = useResource<DunningCase>("/api/v1/dunning/cases/");

  return (
    <>
      <PageHeader title="Dunning" subtitle="Retry schedules, reminders, grace, restrictions, and recovery." />
      <Panel>
        <table>
          <thead><tr><th>Customer</th><th>Invoice</th><th>Status</th><th>Step</th><th>Next</th><th></th></tr></thead>
          <tbody>
            {data.map((item) => (
              <tr key={item.id}>
                <td>{item.company_name}</td>
                <td>{item.invoice_number}</td>
                <td><StatusPill value={item.status} /></td>
                <td>{item.current_step}</td>
                <td>{item.next_action_at?.slice(0, 10)}</td>
                <td className="row">
                  <button className="btn ghost" onClick={() => api.post(`/api/v1/dunning/cases/${item.id}/advance/`).then(reload)}>Advance</button>
                  <button className="btn" onClick={() => api.post(`/api/v1/dunning/cases/${item.id}/recover/`).then(reload)}>Recover</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Panel>
    </>
  );
}
