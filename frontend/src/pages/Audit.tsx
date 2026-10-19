import { PageHeader, Panel } from "../components/ui";
import { useResource } from "../hooks/useResource";

type Audit = { id: string; action: string; summary: string; actor_email: string; object_type: string; created_at: string };

export function AuditPage() {
  const { data } = useResource<Audit>("/api/v1/audit-logs/");

  return (
    <>
      <PageHeader title="Audit" subtitle="Immutable tenant-scoped change history for finance and security reviews." />
      <Panel>
        <table>
          <thead>
            <tr>
              <th>Time</th>
              <th>Actor</th>
              <th>Action</th>
              <th>Object</th>
              <th>Summary</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row) => (
              <tr key={row.id}>
                <td>{row.created_at.slice(0, 16)}</td>
                <td>{row.actor_email}</td>
                <td>{row.action}</td>
                <td>{row.object_type}</td>
                <td>{row.summary}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Panel>
    </>
  );
}
