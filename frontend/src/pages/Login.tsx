import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../state/auth";

export function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("ava@revanta.io");
  const [password, setPassword] = useState("revanta-demo");
  const [error, setError] = useState("");

  return (
    <div className="auth-screen">
      <section className="auth-panel">
        <div className="mark">
          <i /> Revanta
        </div>
        <h1>The ledger for modern revenue teams.</h1>
        <p>
          Subscriptions, metered usage, collections, and forecasts in one operating system — built for finance, sales
          operations, and customer success.
        </p>
      </section>
      <section className="auth-form">
        <form
          className="form-card"
          onSubmit={async (e) => {
            e.preventDefault();
            try {
              await login(email, password);
              navigate("/");
            } catch (err) {
              setError(err instanceof Error ? err.message : "Unable to sign in");
            }
          }}
        >
          <h2>Welcome back</h2>
          <p>Sign in to your billing workspace.</p>
          <label>Work email</label>
          <input value={email} onChange={(e) => setEmail(e.target.value)} />
          <label>Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          {error ? <p className="error">{error}</p> : null}
          <div className="row" style={{ marginTop: 18 }}>
            <button className="btn" type="submit">
              Enter workspace
            </button>
            <Link to="/register" className="btn ghost">
              Create organization
            </Link>
          </div>
        </form>
      </section>
    </div>
  );
}
