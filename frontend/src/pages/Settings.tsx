import { useEffect, useState } from "react";
import { api } from "../api/client";
import { PageHeader, Panel } from "../components/ui";
import { useResource } from "../hooks/useResource";

type SettingsPayload = {
  organization: { name: string; default_currency: string; industry: string };
  controls: { require_invoice_approval: boolean; max_discount_percent: string; collection_grace_days: number; dunning_enabled: boolean };
  settings: { billing_email: string; support_email: string; invoice_footer: string };
  tax_regions: { id: string; name: string; country: string; rate: string }[];
};
type Member = { id: string; user: { email: string; display_name: string }; role: { name: string }; title: string };
type Audit = { id: string; action: string; summary: string; actor_email: string; created_at: string };
type ApiKey = { id: string; name: string; prefix: string; revoked_at?: string | null; secret?: string };

export function SettingsPage() {
  const [payload, setPayload] = useState<SettingsPayload | null>(null);
  const { data: members } = useResource<Member>("/api/v1/members/");
  const { data: audits } = useResource<Audit>("/api/v1/audit-logs/");
  const { data: keys, reload: reloadKeys } = useResource<ApiKey>("/api/v1/api-keys/");
  const [secret, setSecret] = useState("");

  useEffect(() => {
    api.get<SettingsPayload>("/api/v1/settings/").then(setPayload);
  }, []);

  if (!payload) return <p>Loading settings…</p>;

  return (
    <>
      <PageHeader title="Settings" subtitle="Entities, tax, financial controls, roles, API access, and audit." />
      <div className="grid-2">
        <Panel title="Organization">
          <label>Name</label>
          <input value={payload.organization.name} onChange={(e) => setPayload({ ...payload, organization: { ...payload.organization, name: e.target.value } })} />
          <label>Billing email</label>
          <input value={payload.settings.billing_email} onChange={(e) => setPayload({ ...payload, settings: { ...payload.settings, billing_email: e.target.value } })} />
          <button className="btn" style={{ marginTop: 12 }} onClick={() => api.patch("/api/v1/settings/", { organization: payload.organization, settings: payload.settings, controls: payload.controls })}>
            Save workspace
          </button>
        </Panel>
        <Panel title="Financial controls">
          <label>
            <input type="checkbox" checked={payload.controls.dunning_enabled} onChange={(e) => setPayload({ ...payload, controls: { ...payload.controls, dunning_enabled: e.target.checked } })} /> Dunning enabled
          </label>
          <label>Grace days</label>
          <input value={payload.controls.collection_grace_days} onChange={(e) => setPayload({ ...payload, controls: { ...payload.controls, collection_grace_days: Number(e.target.value) } })} />
          <label>Max discount %</label>
          <input value={payload.controls.max_discount_percent} onChange={(e) => setPayload({ ...payload, controls: { ...payload.controls, max_discount_percent: e.target.value } })} />
        </Panel>
      </div>
      <Panel title="Tax regions">
        <table>
          <tbody>
            {payload.tax_regions.map((t) => (
              <tr key={t.id}><td>{t.name}</td><td>{t.country}</td><td>{Number(t.rate) * 100}%</td></tr>
            ))}
          </tbody>
        </table>
      </Panel>
      <div className="grid-2">
        <Panel title="Members">
          <table>
            <tbody>
              {members.map((m) => (
                <tr key={m.id}><td>{m.user.display_name || m.user.email}</td><td>{m.role.name}</td><td>{m.title}</td></tr>
              ))}
            </tbody>
          </table>
        </Panel>
        <Panel title="API keys" actions={
          <button className="btn ghost" onClick={async () => {
            const key = await api.post<ApiKey>("/api/v1/api-keys/", { name: "Workspace key" });
            setSecret(key.secret || "");
            reloadKeys();
          }}>Issue key</button>
        }>
          {secret ? <p>Secret (copy now): {secret}</p> : null}
          <table>
            <tbody>
              {keys.map((k) => (
                <tr key={k.id}><td>{k.name}</td><td>{k.prefix}</td><td>{k.revoked_at ? "revoked" : "active"}</td></tr>
              ))}
            </tbody>
          </table>
        </Panel>
      </div>
      <Panel title="Audit log">
        <table>
          <tbody>
            {audits.slice(0, 12).map((a) => (
              <tr key={a.id}><td>{a.created_at.slice(0, 16)}</td><td>{a.action}</td><td>{a.summary}</td><td>{a.actor_email}</td></tr>
            ))}
          </tbody>
        </table>
      </Panel>
    </>
  );
}
