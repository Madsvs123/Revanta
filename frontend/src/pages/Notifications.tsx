import { api } from "../api/client";
import type { Notification } from "../api/types";
import { PageHeader, Panel } from "../components/ui";
import { useResource } from "../hooks/useResource";

export function NotificationsPage() {
  const { data, reload } = useResource<Notification>("/api/v1/notifications/");

  return (
    <>
      <PageHeader
        title="Notifications"
        subtitle="Workspace alerts from billing, dunning, usage, and integrations."
        actions={<button className="btn ghost" onClick={() => api.post("/api/v1/notifications/read_all/", {}).then(reload)}>Mark all read</button>}
      />
      <Panel>
        <table>
          <thead>
            <tr>
              <th>When</th>
              <th>Category</th>
              <th>Message</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {data.map((n) => (
              <tr key={n.id}>
                <td>{n.created_at.slice(0, 16)}</td>
                <td>{n.category}</td>
                <td>{n.title}</td>
                <td>
                  {n.read_at ? (
                    "Read"
                  ) : (
                    <button className="btn ghost" onClick={() => api.post(`/api/v1/notifications/${n.id}/read/`).then(reload)}>
                      Read
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
