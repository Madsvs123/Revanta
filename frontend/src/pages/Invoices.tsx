import { Link } from "react-router-dom";
import { api, money } from "../api/client";
import type { Invoice, Subscription } from "../api/types";
import { PageHeader, Panel, StatusPill } from "../components/ui";
import { useResource } from "../hooks/useResource";

export function InvoicesPage() {
  const { data, reload } = useResource<Invoice>("/api/v1/invoices/");
  const { data: subscriptions } = useResource<Subscription>("/api/v1/subscriptions/");

  return (
    <>
      <PageHeader
        title="Invoices"
        subtitle="Recurring generation, taxes, credits, adjustments, and PDF delivery."
        actions={
          subscriptions[0] ? (
            <button className="btn" onClick={async () => { await api.post("/api/v1/invoices/generate/", { subscription_id: subscriptions[0].id }); reload(); }}>
              Generate from first subscription
            </button>
          ) : null
        }
      />
      <Panel>
        <table>
          <thead><tr><th>Number</th><th>Customer</th><th>Status</th><th>Total</th><th>Due</th><th>Issued</th></tr></thead>
          <tbody>
            {data.map((invoice) => (
              <tr key={invoice.id}>
                <td><Link to={`/invoices/${invoice.id}`}>{invoice.number}</Link></td>
                <td>{invoice.company_name}</td>
                <td><StatusPill value={invoice.status} /></td>
                <td>{money(invoice.total, invoice.currency)}</td>
                <td>{money(invoice.amount_due, invoice.currency)}</td>
                <td>{invoice.issue_date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Panel>
    </>
  );
}
