'use client'

import { useState, ChangeEvent } from "react";
import { Button } from  "@/app/test/components/button";
import { Input } from "@/app/test/components/input";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default function PostRequestPage() {
  const [url, setUrl] = useState(`${API_URL}/auth/login`);
  const [response, setResponse] = useState<string | null>(null);

  const sendPostRequest = async () => {
    try {
      const res = await fetch(url, {
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
    <div className="flex flex-col items-center p-4 space-y-4">
      {/* Поле ввода для URL */}
      <Input
        type="text"
        placeholder="Enter URL"
        value={url}
        onChange={(e: ChangeEvent<HTMLInputElement>) => setUrl(e.target.value)}
        className="w-96"
      />
      
      {/* Кнопка для отправки POST-запроса */}
      <Button onClick={sendPostRequest}>Send POST Request</Button>
      
      {/* Блок для отображения ответа */}
      {response && (
        <pre className="mt-4 p-2 bg-background border rounded w-96 overflow-auto">
          {response}
        </pre>
      )}
    </div>
  );
}
