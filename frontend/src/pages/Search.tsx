import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";
import { PageHeader, Panel } from "../components/ui";

type Hit = { type: string; id: string; label: string; hint: string };

export function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Hit[]>([]);
  const navigate = useNavigate();

  const routes: Record<string, string> = {
    customer: "/customers/",
    subscription: "/subscriptions/",
    invoice: "/invoices/",
    product: "/catalog",
    contract: "/contracts",
    entitlement: "/entitlements",
    integration: "/integrations",
  };

  return (
    <>
      <PageHeader title="Search" subtitle="Find customers, subscriptions, invoices, contracts, features, and connectors." />
      <Panel>
        <div className="row">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search the workspace…"
            onKeyDown={async (e) => {
              if (e.key === "Enter") {
                const data = await api.get<{ results: Hit[] }>(`/api/v1/search/?q=${encodeURIComponent(query)}`);
                setResults(data.results);
              }
            }}
          />
          <button
            className="btn"
            onClick={async () => {
              const data = await api.get<{ results: Hit[] }>(`/api/v1/search/?q=${encodeURIComponent(query)}`);
              setResults(data.results);
            }}
          >
            Search
          </button>
        </div>
        <table>
          <thead>
            <tr>
              <th>Type</th>
              <th>Result</th>
              <th>Hint</th>
            </tr>
          </thead>
          <tbody>
            {results.map((item) => (
              <tr key={`${item.type}-${item.id}`} style={{ cursor: "pointer" }} onClick={() => navigate((routes[item.type] || "/") + (["customer", "subscription", "invoice"].includes(item.type) ? item.id : ""))}>
                <td>{item.type}</td>
                <td>{item.label}</td>
                <td>{item.hint}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Panel>
    </>
  );
}
