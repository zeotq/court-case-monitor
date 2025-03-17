'use client'

import { useState, ChangeEvent } from "react";
import { useRouter } from "next/navigation";

import { Button } from  "@/app/home/components/button";
import { Input } from "@/app/home/components/input";
import { fetchWithAuth } from "@/app/auth/services/fetchWithAuth";
import { useAuth } from "@/app/auth/components/AuthContext";
import { logout } from "@/app/services/logout";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default function PostRequestPage() {
  const [url, setUrl] = useState(`${API_URL}/external/search`);
  const [response, setResponse] = useState<string | null>(null);
  const { accessToken, setAccessToken } = useAuth();
  const router = useRouter();

  const sendPostRequest = async () => {
    try {
      const res = await fetchWithAuth(url, accessToken, setAccessToken, router, {
        method: "POST",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: "Hello, server!" }),
        credentials: "include",
      });
      const data = await res.json();
      setResponse(JSON.stringify(data, null, 2));
    } catch (error) {
      setResponse(`Error: ${error}`);
    }
  };

  return (
    <div className="grow flex-col items-center p-4 space-y-4 gap-4">
      <div className="flex flex-row gap-4">
        {/* Поле ввода для URL */}
        <Input
          type="text"
          placeholder="Enter URL"
          value={url}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setUrl(e.target.value)}
        />
        
        {/* Кнопка для отправки POST-запроса */}
        <Button onClick={sendPostRequest}>Send POST Request</Button>
        <Button onClick={() => router.push("/auth")}>Login</Button>
        <Button onClick={() => logout(setAccessToken)}>Logout</Button>
      </div>
      <div>
        {/* Блок для отображения ответа */}
        {response && (
          <pre className="mt-4 p-2 bg-background border rounded overflow-auto">
            {response}
          </pre>
        )}
      </div>
    </div>
  );
}
