import { useState } from "react";
import { api } from "../api/client";
import { PageHeader, Panel } from "../components/ui";
import { useResource } from "../hooks/useResource";

type Member = { id: string; user: { email: string; display_name: string }; role: { name: string }; title: string; is_active: boolean };
type Role = { id: string; name: string; slug: string; permissions: string[] };
type Invite = { id: string; email: string; role: { name: string }; expires_at: string; accepted_at?: string | null };

export function TeamPage() {
  const { data: members } = useResource<Member>("/api/v1/members/");
  const { data: roles } = useResource<Role>("/api/v1/roles/");
  const { data: invites, reload } = useResource<Invite>("/api/v1/invitations/");
  const [email, setEmail] = useState("");
  const [roleId, setRoleId] = useState("");

  return (
    <>
      <PageHeader title="Team" subtitle="Members, roles, invitations, and API access for this organization." />
      <div className="grid-2">
        <Panel title="Members">
          <table>
            <tbody>
              {members.map((m) => (
                <tr key={m.id}>
                  <td>{m.user.display_name || m.user.email}</td>
                  <td>{m.role.name}</td>
                  <td>{m.title}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>
        <Panel title="Invite">
          <label>Email</label>
          <input value={email} onChange={(e) => setEmail(e.target.value)} />
          <label>Role</label>
          <select value={roleId} onChange={(e) => setRoleId(e.target.value)}>
            <option value="">Select role</option>
            {roles.map((r) => (
              <option key={r.id} value={r.id}>
                {r.name}
              </option>
            ))}
          </select>
          <button
            className="btn"
            style={{ marginTop: 12 }}
            onClick={async () => {
              await api.post("/api/v1/invitations/", { email, role_id: roleId });
              setEmail("");
              reload();
            }}
          >
            Send invitation
          </button>
          <table>
            <tbody>
              {invites.map((i) => (
                <tr key={i.id}>
                  <td>{i.email}</td>
                  <td>{i.role.name}</td>
                  <td>{i.accepted_at ? "accepted" : "open"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>
      </div>
    </>
  );
}
