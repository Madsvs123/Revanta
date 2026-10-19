import { useParams } from "react-router-dom";
import { api, money } from "../api/client";
import type { Invoice } from "../api/types";
import { Panel, StatusPill } from "../components/ui";
import { useOne } from "../hooks/useResource";

export function InvoiceDetailPage() {
  const { id } = useParams();
  const { data: invoice, reload } = useOne<Invoice>(id ? `/api/v1/invoices/${id}/` : null);
  if (!invoice) return <p>Loading invoice…</p>;

  return (
    <>
      <div className="page-head">
        <div>
          <h1>{invoice.number}</h1>
          <p>{invoice.company_name} · due {invoice.due_date}</p>
        </div>
        <StatusPill value={invoice.status} />
      </div>
      <div className="row">
        <button className="btn" onClick={() => window.open(`/api/v1/invoices/${invoice.id}/pdf/`, "_blank")}>Download PDF</button>
        <button className="btn ghost" onClick={async () => { await api.post("/api/v1/credit-notes/", { invoice: invoice.id, amount: 50, reason: "Service credit" }); reload(); }}>
          Issue credit note
        </button>
      </div>
      <Panel title="Line items">
        <table>
          <thead><tr><th>Description</th><th>Qty</th><th>Amount</th></tr></thead>
          <tbody>
            {(invoice.lines ?? []).map((line) => (
              <tr key={line.id}>
                <td>{line.description}</td>
                <td>{line.quantity}</td>
                <td>{money(line.amount, invoice.currency)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Panel>
    </>
  );
}
