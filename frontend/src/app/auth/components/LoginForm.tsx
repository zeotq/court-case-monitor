"use client";

import { useState, useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/app/auth/components/AuthContext";
import getBaseURL from "@/utils/getBaseURL";
import { generatePKCE } from "@/utils/pkce";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

interface LoginFormProps {
  toggle: () => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ toggle }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const searchParams = useSearchParams();
  const router = useRouter()
  const { setAccessToken } = useAuth();

  const callbackUri = searchParams.get("callback_uri") || getBaseURL();

  useEffect(() => {
    const setupPKCE = async () => {
      const { codeVerifier, codeChallenge } = await generatePKCE();
      sessionStorage.setItem("code_verifier", codeVerifier);
      sessionStorage.setItem("code_challenge", codeChallenge);
    };

    setupPKCE();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    const codeVerifier = sessionStorage.getItem("code_verifier");
    const codeChallenge = sessionStorage.getItem("code_challenge");
    if (!codeChallenge) {
      setError("Ошибка генерации PKCE");
      return;
    }

    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);
    params.append("code_challenge", codeChallenge);
    params.append("callback_uri", callbackUri);

    const auth_response = await fetch(`${API_URL}/auth/authorize`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: params.toString(),
      credentials: "include"
    });

    const data = await auth_response.json();
    const authCode = data.code;
    
    if (auth_response.ok) {
      const token_response = await fetch(`${API_URL}/auth/token?code=${authCode}&code_verifier=${codeVerifier}&callback_uri=${callbackUri}`, {credentials: "include"});
      if (token_response.ok) {
        const data = await token_response.json();
        setAccessToken(data.access_token);
        router.replace(callbackUri);
      } else {
        const data = await token_response.json();
        setError(data.detail || "Ошибка авторизации");
      }
    } else {
      setError(data.detail || "Ошибка авторизации");
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

export default function LoginFormWrapper({ toggle }: LoginFormProps) {
  return (
    <Suspense fallback={<div>Загрузка...</div>}>
      <LoginForm toggle={toggle} />
    </Suspense>
  );
}