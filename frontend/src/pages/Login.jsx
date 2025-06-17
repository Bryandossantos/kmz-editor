import { useState, useContext } from "react";
import axios from "axios";
import { AuthCtx } from "../App";
import { useNavigate, Link } from "react-router-dom";

export default function Login() {
  const nav = useNavigate();
  const { setToken } = useContext(AuthCtx);
  const [form, setForm] = useState({ email: "", password: "" });
  const handle = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    const r = await axios.post("http://localhost:5000/login", form);
    setToken(r.data.access_token);
    localStorage.setItem("token", r.data.access_token);
    nav("/");
  };

  return (
    <div className="h-screen flex items-center justify-center bg-gray-100">
      <form onSubmit={submit} className="bg-white p-8 rounded-xl shadow w-80 space-y-4">
        <h1 className="text-2xl font-semibold text-center">Login</h1>
        <input
          className="w-full border p-2 rounded"
          placeholder="E-mail"
          name="email"
          value={form.email}
          onChange={handle}
        />
        <input
          className="w-full border p-2 rounded"
          type="password"
          placeholder="Senha"
          name="password"
          value={form.password}
          onChange={handle}
        />
        <button className="w-full bg-blue-600 text-white p-2 rounded shadow">
          Entrar
        </button>
        <Link className="block text-center text-sm text-blue-600" to="/signup">
          Criar conta
        </Link>
      </form>
    </div>
  );
}
