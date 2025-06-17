import { useContext, useState } from "react";
import axios from "axios";
import { AuthCtx } from "../App";

export default function Dashboard() {
  const { token, setToken } = useContext(AuthCtx);
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const process = async () => {
    if (!file) return;
    setStatus("Processando…");
    const form = new FormData();
    form.append("file", file);
    const r = await axios.post("http://localhost:5000/process", form, {
      headers: { Authorization: `Bearer ${token}` },
      responseType: "blob",
    });
    const url = URL.createObjectURL(r.data);
    const a = document.createElement("a");
    a.href = url;
    a.download = "corrigido.kmz";
    a.click();
    URL.revokeObjectURL(url);
    setStatus("Arquivo pronto! 🎉");
  };

  return (
    <div className="min-h-screen flex flex-col items-center pt-20 bg-gray-50 space-y-6">
      <h1 className="text-3xl font-bold">Editor de KMZ – 1 s</h1>

      <input
        type="file"
        accept=".kmz"
        onChange={(e) => setFile(e.target.files[0])}
        className="p-2 border rounded"
      />

      <button
        onClick={process}
        className="bg-green-600 text-white py-2 px-4 rounded shadow"
      >
        Iniciar Edição Automática
      </button>

      {status && <p>{status}</p>}

      <button
        onClick={() => {
          localStorage.clear();
          setToken(null);
        }}
        className="absolute top-4 right-4 text-sm text-red-600"
      >
        Sair
      </button>
    </div>
  );
}
