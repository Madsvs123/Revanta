import type { ReactNode } from "react";

export function PageHeader({
  title,
  subtitle,
  actions,
}: {
  title: string;
  subtitle?: string;
  actions?: ReactNode;
}) {
  return (
    <div className="page-head">
      <div>
        <h1>{title}</h1>
        {subtitle ? <p>{subtitle}</p> : null}
      </div>
      <div className="row">{actions}</div>
    </div>
  );
}

export function Metric({ label, value, delta, down }: { label: string; value: string; delta?: string; down?: boolean }) {
  return (
    <div className="metric">
      <div className="k">{label}</div>
      <div className="v">{value}</div>
      {delta ? <div className={`d ${down ? "down" : ""}`}>{delta}</div> : null}
    </div>
  );
}

export function Panel({ title, children, actions }: { title?: string; children: ReactNode; actions?: ReactNode }) {
  return (
    <section className="panel">
      {(title || actions) && (
        <div className="row" style={{ marginBottom: 12 }}>
          {title ? <h3 style={{ margin: 0 }}>{title}</h3> : null}
          <div className="right">{actions}</div>
        </div>
      )}
      {children}
    </section>
  );
}

export function StatusPill({ value }: { value?: string }) {
  const key = (value || "unknown").toLowerCase();
  return <span className={`pill ${key}`}>{value?.replaceAll("_", " ")}</span>;
}
