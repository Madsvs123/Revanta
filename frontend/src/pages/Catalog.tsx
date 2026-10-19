import { useState } from "react";
import { api, money } from "../api/client";
import type { Coupon, Plan, Product } from "../api/types";
import { PageHeader, Panel, StatusPill } from "../components/ui";
import { useResource } from "../hooks/useResource";

export function CatalogPage() {
  const { data: products, reload } = useResource<Product>("/api/v1/products/");
  const { data: plans } = useResource<Plan>("/api/v1/plans/");
  const { data: coupons } = useResource<Coupon>("/api/v1/coupons/");
  const [tab, setTab] = useState("products");
  const [name, setName] = useState("");
  const [sku, setSku] = useState("");

  return (
    <>
      <PageHeader title="Catalog" subtitle="Products, plans, tiers, add-ons, bundles, and regional pricing." />
      <div className="tabs">
        {["products", "plans", "coupons"].map((key) => (
          <button key={key} className={`tab ${tab === key ? "on" : ""}`} onClick={() => setTab(key)}>{key}</button>
        ))}
      </div>
      {tab === "products" && (
        <Panel
          title="Products"
          actions={
            <div className="row">
              <input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
              <input placeholder="SKU" value={sku} onChange={(e) => setSku(e.target.value)} />
              <button className="btn" onClick={async () => { await api.post("/api/v1/products/", { name, sku }); setName(""); setSku(""); reload(); }}>Add</button>
            </div>
          }
        >
          <table>
            <thead><tr><th>Product</th><th>SKU</th><th>Type</th><th>Active</th></tr></thead>
            <tbody>
              {products.map((p) => (
                <tr key={p.id}>
                  <td>{p.name}</td>
                  <td>{p.sku}</td>
                  <td>{p.product_type}</td>
                  <td><StatusPill value={p.is_active ? "active" : "archived"} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>
      )}
      {tab === "plans" && (
        <Panel title="Plans">
          <table>
            <thead><tr><th>Plan</th><th>Interval</th><th>Model</th><th>Trial</th><th>Starting price</th></tr></thead>
            <tbody>
              {plans.map((plan) => (
                <tr key={plan.id}>
                  <td>{plan.name}</td>
                  <td>{plan.interval}</td>
                  <td>{plan.billing_model}</td>
                  <td>{plan.trial_days}d</td>
                  <td>{money(plan.tiers?.[0]?.unit_amount)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>
      )}
      {tab === "coupons" && (
        <Panel title="Coupons">
          <table>
            <thead><tr><th>Name</th><th>Code</th><th>Off</th><th>Duration</th></tr></thead>
            <tbody>
              {coupons.map((c) => (
                <tr key={c.id}>
                  <td>{c.name}</td>
                  <td>{c.code}</td>
                  <td>{c.percent_off ? `${c.percent_off}%` : money(c.amount_off)}</td>
                  <td>{c.duration}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>
      )}
    </>
  );
}
