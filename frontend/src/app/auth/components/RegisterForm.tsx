"use client";

import { useState } from "react";
import { useAuth } from "@/app/auth/components/AuthContext";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

interface RegisterFormProps {
  toggle: () => void;
}

const RegisterForm: React.FC<RegisterFormProps> = ({ toggle }) => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { setAccessToken } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    const response = await fetch(`${API_URL}/auth/registration`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, email, password }),
      credentials: "include",
    });

    const data = await response.json();
    if (!response.ok) {
      setError(data.message || "Ошибка регистрации");
    } else {
      alert("Ты молодец, ты зарегистрировался!");
      toggle();
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <h2 className="text-xl font-bold">Регистрация</h2>
      {error && <p className="text-red-400">{error}</p>}

      <input
        type="text"
        placeholder="Логин"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        className="p-2 bg-midground border border-gray-600 rounded"
        required
      />

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="p-2 bg-midground border border-gray-600 rounded"
        required
      />

      <input
        type="password"
        placeholder="Пароль"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="p-2 bg-midground border border-gray-600 rounded"
        required
      />

      <button type="submit" className="p-2 bg-green-600 hover:bg-green-700 rounded text-white">
        Зарегистрироваться
      </button>

      {/* Кликабельный текст */}
      <p className="text-sm text-right text-gray-400 cursor-pointer hover:text-gray-200" onClick={toggle}>
        Уже есть аккаунт?
      </p>
    </form>
  );
};

export default RegisterForm;
