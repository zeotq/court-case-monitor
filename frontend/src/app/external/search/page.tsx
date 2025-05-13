'use client'

import { useState, ChangeEvent } from "react";
import { useRouter } from "next/navigation";

import { Input } from "@/app/table/components/Input";
import { fetchWithAuth } from "@/app/auth/services/fetchWithAuth";
import { useAuth } from "@/app/auth/components/AuthContext";
import TopBar from "@/components/TopBar";
import { Button } from "@/components/Button";
import Filter, { Filters } from "@/app/table/components/Filter";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default function PostRequestPage() {
  const [url, setUrl] = useState(`${API_URL}/external/search`);
  const [response, setResponse] = useState<string | null>(null);
  const { accessToken, setAccessToken } = useAuth();
  const [filters, setFilters] = useState<Filters>({});
  const router = useRouter();

  const sendPostRequest = async () => {
    try {
          const res = await fetchWithAuth(
            `${API_URL}/external/search`,
            { accessToken, setAccessToken },
            router.push,
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                ...filters,
                CaseNumbers: filters.CaseNumbers || undefined,
                Courts: filters.Courts || undefined,
                Judges: filters.Judges?.map(judge => ({ JudgeId: judge })) || undefined,
                Sides: filters.Sides?.map(side => ({
                  Name: side.Name,
                  Inn: side.Inn,
                  ExactMatch: side.ExactMatch
                })) || undefined,
                DateFrom: filters.DateFrom,
                DateTo: filters.DateTo,
                WithVKSInstances: filters.WithVKSInstances
              }),
            }
          );
          if (!res.ok) {
            const text = await res.text();
            throw new Error(`Ошибка ${res.status}: ${text}`);
          }
    
          const data = await res.json();
          setResponse(JSON.stringify(data, null, 2));
        } catch (err: any) {
          console.error("Error fetching cases:", err);
          setResponse(`Error: ${err}`);
        } finally {
          
        }
    };

  return (
    <div className="grow flex-col items-center p-4 space-y-4 gap-4">
      <TopBar>
        <div>
          <h1 className="text-xl font-bold">Внешний поиск</h1>
        </div>
      </TopBar>
      <Filter filters={filters} setFilters={setFilters} />
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
        <Button onClick={() => router.push('/table')}>Поиск по БД</Button>
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
