import { useState } from "react";
import { api } from "../api/client";
import { PageHeader, Panel } from "../components/ui";
import { useResource } from "../hooks/useResource";

type Saved = { id: string; name: string; report_type: string };
type ExportJob = { id: string; name: string; resource: string; status: string };

export function ReportsPage() {
  const { data: reports, reload } = useResource<Saved>("/api/v1/reports/");
  const { data: exports, reload: reloadExports } = useResource<ExportJob>("/api/v1/exports/");
  const [rows, setRows] = useState<Record<string, string>[]>([]);

  return (
    <>
      <PageHeader
        title="Reports"
        subtitle="Saved views, ad-hoc collections, and CSV exports."
        actions={
          <button className="btn" onClick={async () => { await api.post("/api/v1/reports/", { name: "Collections aging", report_type: "collections", definition: {} }); reload(); }}>
            Save collections report
          </button>
        }
      />
      <div className="grid-2">
        <Panel title="Saved reports">
          <table>
            <tbody>
              {reports.map((r) => (
                <tr key={r.id}>
                  <td>{r.name}</td>
                  <td>{r.report_type}</td>
                  <td>
                    <button className="btn ghost" onClick={async () => {
                      const data = await api.get<{ rows: Record<string, string>[] }>(`/api/v1/reports/${r.id}/run/`);
                      setRows(data.rows);
                    }}>Run</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>
        <Panel title="Exports" actions={
          <button className="btn ghost" onClick={async () => { await api.post("/api/v1/exports/", { name: "Customers", resource: "customers" }); reloadExports(); }}>
            Export customers
          </button>
        }>
          <table>
            <tbody>
              {exports.map((job) => (
                <tr key={job.id}>
                  <td>{job.name}</td>
                  <td>{job.status}</td>
                  <td>{job.status === "ready" && <a href={`/api/v1/exports/${job.id}/download/`} target="_blank" rel="noreferrer">Download</a>}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>
      </div>
      {rows.length > 0 && (
        <Panel title="Result">
          <table>
            <thead><tr>{Object.keys(rows[0]).map((key) => <th key={key}>{key}</th>)}</tr></thead>
            <tbody>
              {rows.map((row, i) => (
                <tr key={i}>{Object.values(row).map((value, j) => <td key={j}>{value}</td>)}</tr>
              ))}
            </tbody>
          </table>
        </Panel>
      )}
    </>
  );
}
