import { money } from "../api/client";
import type { Contract, Renewal } from "../api/types";
import { PageHeader, Panel, StatusPill } from "../components/ui";
import { useResource } from "../hooks/useResource";

export function ContractsPage() {
  const { data: contracts } = useResource<Contract>("/api/v1/contracts/");
  const { data: renewals } = useResource<Renewal>("/api/v1/renewals/");

  return (
    <>
      <PageHeader title="Contracts" subtitle="Renewals, sales handoffs, ownership, and customer-success health." />
      <div className="grid-2">
        <Panel title="Agreements">
          <table>
            <thead><tr><th>Contract</th><th>Account</th><th>ACV</th><th>Ends</th></tr></thead>
            <tbody>
              {contracts.map((c) => (
                <tr key={c.id}>
                  <td>{c.name}<div className="muted">{c.number}</div></td>
                  <td>{c.company_name}</td>
                  <td>{money(c.acv)}</td>
                  <td><StatusPill value={c.status} /> {c.end_date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>
        <Panel title="Renewal pipeline">
          <table>
            <thead><tr><th>Account</th><th>Stage</th><th>Weighted</th></tr></thead>
            <tbody>
              {renewals.map((r) => (
                <tr key={r.id}>
                  <td>{r.company_name}</td>
                  <td><StatusPill value={r.stage} /></td>
                  <td>{money(r.weighted)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>
      </div>
    </>
  );
}
