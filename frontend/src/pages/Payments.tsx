import { api, money } from "../api/client";
import type { Invoice, Payment } from "../api/types";
import { PageHeader, Panel, StatusPill } from "../components/ui";
import { useResource } from "../hooks/useResource";

export function PaymentsPage() {
  const { data, reload } = useResource<Payment>("/api/v1/payments/");
  const { data: invoices } = useResource<Invoice>("/api/v1/invoices/");
  const open = invoices.find((i) => Number(i.amount_due) > 0);

  return (
    <>
      <PageHeader
        title="Payments"
        subtitle="Provider adapters, retries, refunds, webhooks, and reconciliation."
        actions={
          open ? (
            <button className="btn" onClick={async () => { await api.post("/api/v1/payments/", { invoice_id: open.id, provider: "simulated" }); reload(); }}>
              Collect open invoice
            </button>
          ) : null
        }
      />
      <Panel>
        <table>
          <thead><tr><th>Customer</th><th>Invoice</th><th>Amount</th><th>Status</th><th>Provider</th><th></th></tr></thead>
          <tbody>
            {data.map((payment) => (
              <tr key={payment.id}>
                <td>{payment.company_name}</td>
                <td>{payment.invoice_number}</td>
                <td>{money(payment.amount, payment.currency)}</td>
                <td><StatusPill value={payment.status} /></td>
                <td>{payment.provider} · {payment.attempt_count} attempts</td>
                <td>
                  {payment.status === "failed" && (
                    <button className="btn ghost" onClick={() => api.post(`/api/v1/payments/${payment.id}/retry/`).then(reload)}>Retry</button>
                  )}
                  {payment.status === "succeeded" && (
                    <button className="btn ghost" onClick={() => api.post(`/api/v1/payments/${payment.id}/refund/`, { amount: payment.amount, reason: "Customer request" }).then(reload)}>Refund</button>
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
