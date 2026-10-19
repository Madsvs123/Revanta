import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../state/auth";

export function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    organization_name: "",
    default_currency: "USD",
  });
  const [error, setError] = useState("");
  const set = (key: string, value: string) => setForm((f) => ({ ...f, [key]: value }));

  return (
    <div className="auth-screen">
      <section className="auth-panel">
        <div className="mark">
          <i /> Revanta
        </div>
        <h1>Open a new revenue workspace.</h1>
        <p>Multi-entity billing, tax regions, roles, and financial controls are provisioned with the organization.</p>
      </section>
      <section className="auth-form">
        <form
          className="form-card"
          onSubmit={async (e) => {
            e.preventDefault();
            try {
              await register(form);
              navigate("/");
            } catch (err) {
              setError(err instanceof Error ? err.message : "Unable to create workspace");
            }
          }}
        >
          <h2>Create Revanta</h2>
          <p>Owner access is granted automatically.</p>
          <div className="row">
            <div style={{ flex: 1 }}>
              <label>First name</label>
              <input value={form.first_name} onChange={(e) => set("first_name", e.target.value)} />
            </div>
            <div style={{ flex: 1 }}>
              <label>Last name</label>
              <input value={form.last_name} onChange={(e) => set("last_name", e.target.value)} />
            </div>
          </div>
          <label>Email</label>
          <input value={form.email} onChange={(e) => set("email", e.target.value)} />
          <label>Password</label>
          <input type="password" value={form.password} onChange={(e) => set("password", e.target.value)} />
          <label>Organization</label>
          <input value={form.organization_name} onChange={(e) => set("organization_name", e.target.value)} />
          {error ? <p className="error">{error}</p> : null}
          <div className="row" style={{ marginTop: 18 }}>
            <button className="btn copper" type="submit">
              Provision workspace
            </button>
            <Link to="/login" className="btn ghost">
              I already have access
            </Link>
          </div>
        </form>
      </section>
    </div>
  );
}
