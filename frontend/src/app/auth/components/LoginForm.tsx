"use client";

import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

interface LoginFormProps {
  toggle: () => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ toggle }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    const response = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      mode: "cors",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: params.toString(),
      credentials: "include",
    });

    const data = await response.json();
    if (!response.ok) {
      setError(data.message || "Ошибка авторизации");
    } else {
      alert("Успешный вход!");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <h2 className="text-xl font-bold">Авторизация</h2>
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
        type="password"
        placeholder="Пароль"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="p-2 bg-midground border border-gray-600 rounded"
        required
      />

      <button type="submit" className="p-2 bg-blue-600 hover:bg-blue-700 rounded text-white">
        Войти
      </button>

      {/* Кликабельный текст */}
      <p className="text-sm text-right text-gray-400 cursor-pointer hover:text-gray-200" onClick={toggle}>
        Нет аккаунта?
      </p>
    </form>
  );
};

export default LoginForm;
