import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useState, createContext } from "react";
import SignUp from "./pages/SignUp";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";

export const AuthCtx = createContext(null);

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  return (
    <AuthCtx.Provider value={{ token, setToken }}>
      <BrowserRouter>
        <Routes>
          <Route path="/signup" element={<SignUp />} />
          <Route path="/login" element={<Login />} />
          <Route
            path="/"
            element={token ? <Dashboard /> : <Navigate to="/login" replace />}
          />
        </Routes>
      </BrowserRouter>
    </AuthCtx.Provider>
  );
}
