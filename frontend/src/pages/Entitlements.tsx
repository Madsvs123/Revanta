import { useState } from "react";
import { api } from "../api/client";
import { PageHeader, Panel, StatusPill } from "../components/ui";
import { useResource } from "../hooks/useResource";

type Feature = { id: string; name: string; code: string; value_type: string; unit_label: string; is_active: boolean };
type Grant = { id: string; plan_name: string; feature_name: string; enabled: boolean; quantity: string };
type Entitlement = {
  id: string;
  company_name: string;
  feature_name: string;
  feature_code: string;
  granted: string;
  consumed: string;
  remaining: string;
  enabled: boolean;
  source: string;
};

export function EntitlementsPage() {
  const { data: features, reload: reloadFeatures } = useResource<Feature>("/api/v1/entitlements/features/");
  const { data: grants } = useResource<Grant>("/api/v1/entitlements/grants/");
  const { data: items, reload } = useResource<Entitlement>("/api/v1/entitlements/");
  const [name, setName] = useState("");
  const [code, setCode] = useState("");

  return (
    <>
      <PageHeader title="Entitlements" subtitle="Feature grants, quantity caps, plan catalogs, and access checks." />
      <div className="grid-2">
        <Panel
          title="Feature catalog"
          actions={
            <div className="row">
              <input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
              <input placeholder="Code" value={code} onChange={(e) => setCode(e.target.value)} />
              <button
                className="btn"
                onClick={async () => {
                  await api.post("/api/v1/entitlements/features/", { name, code, value_type: "boolean" });
                  setName("");
                  setCode("");
                  reloadFeatures();
                }}
              >
                Add
              </button>
            </div>
          }
        >
          <table>
            <thead>
              <tr>
                <th>Feature</th>
                <th>Type</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {features.map((f) => (
                <tr key={f.id}>
                  <td>
                    {f.name}
                    <div className="muted">{f.code}</div>
                  </td>
                  <td>{f.value_type}</td>
                  <td>
                    <StatusPill value={f.is_active ? "active" : "archived"} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>
        <Panel title="Plan grants">
          <table>
            <thead>
              <tr>
                <th>Plan</th>
                <th>Feature</th>
                <th>Qty</th>
              </tr>
            </thead>
            <tbody>
              {grants.map((g) => (
                <tr key={g.id}>
                  <td>{g.plan_name}</td>
                  <td>{g.feature_name}</td>
                  <td>{g.enabled ? g.quantity : "off"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>
      </div>
      <Panel title="Live entitlements">
        <table>
          <thead>
            <tr>
              <th>Account</th>
              <th>Feature</th>
              <th>Granted</th>
              <th>Used</th>
              <th>Left</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id}>
                <td>{item.company_name}</td>
                <td>{item.feature_name}</td>
                <td>{item.granted}</td>
                <td>{item.consumed}</td>
                <td>{item.remaining}</td>
                <td>
                  <button className="btn ghost" onClick={() => api.post(`/api/v1/entitlements/${item.id}/check/`, { requested: 1 }).then(reload)}>
                    Check
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Panel>
    </>
  );
}
