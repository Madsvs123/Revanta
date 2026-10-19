import { useEffect, useState } from "react";
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { api, money } from "../api/client";
import type { Snapshot } from "../api/types";
import { Metric, Panel } from "../components/ui";

type Overview = {
  snapshot: Snapshot;
  history: Snapshot[];
  cohorts: { cohort_month: string; months_later: number; retention_rate: string }[];
  forecast: { committed: string; pipeline: string; best_case: string };
};

export function DashboardPage() {
  const [data, setData] = useState<Overview | null>(null);

  useEffect(() => {
    api.get<Overview>("/api/v1/analytics/overview/").then(setData);
  }, []);

  const snap = data?.snapshot;
  return (
    <>
      <div className="page-head">
        <div>
          <h1>Revenue operations</h1>
          <p>MRR movement, retention, collections, and the quarter ahead.</p>
        </div>
      </div>
      <div className="metrics">
        <Metric label="MRR" value={money(snap?.mrr)} delta={`${money(snap?.net_new_mrr)} net new`} down={Number(snap?.net_new_mrr) < 0} />
        <Metric label="ARR" value={money(snap?.arr)} delta={`${snap?.active_customers ?? 0} customers`} />
        <Metric label="NRR" value={`${snap?.nrr ?? 0}%`} delta={`LTV ${money(snap?.ltv)}`} />
        <Metric label="Collections" value={money(snap?.collections_balance)} delta={`${snap?.failed_payments ?? 0} failed payments`} down />
      </div>
      <div className="grid-2">
        <Panel title="Recurring revenue">
          <div className="chart">
            <ResponsiveContainer>
              <AreaChart data={data?.history ?? []}>
                <XAxis dataKey="as_of" hide />
                <YAxis hide />
                <Tooltip />
                <Area type="monotone" dataKey="mrr" stroke="#1c3d3a" fill="#c45c26" fillOpacity={0.18} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>
        <Panel title="Movement this period">
          <table>
            <tbody>
              <tr><td>New</td><td>{money(snap?.new_mrr)}</td></tr>
              <tr><td>Expansion</td><td>{money(snap?.expansion_mrr)}</td></tr>
              <tr><td>Contraction</td><td>{money(snap?.contraction_mrr)}</td></tr>
              <tr><td>Churned</td><td>{money(snap?.churned_mrr)}</td></tr>
            </tbody>
          </table>
        </Panel>
      </div>
      <div className="grid-2">
        <Panel title="Cohort retention">
          <table>
            <thead>
              <tr>
                <th>Cohort</th>
                <th>Month</th>
                <th>Retained</th>
              </tr>
            </thead>
            <tbody>
              {(data?.cohorts ?? []).slice(0, 8).map((row, i) => (
                <tr key={i}>
                  <td>{row.cohort_month}</td>
                  <td>+{row.months_later}</td>
                  <td>{row.retention_rate}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>
        <Panel title="Quarterly forecast">
          <div className="stack">
            <div>Committed {money(data?.forecast.committed)}</div>
            <div>Pipeline {money(data?.forecast.pipeline)}</div>
            <div>Best case {money(data?.forecast.best_case)}</div>
          </div>
        </Panel>
      </div>
    </>
  );
}
