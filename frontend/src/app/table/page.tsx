'use client';

import { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { useRouter } from "next/navigation";
import { useAuth } from "@/app/auth/components/AuthContext";
import { fetchWithAuth } from "@/app/auth/services/fetchWithAuth";
import Filter, { Filters } from "@/app/table/components/Filter";
import { Button } from "@/components/Button";
import TopBar from "@/components/TopBar";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

type Party = {
  name: string | null;
  inn: string | null;
};

type CaseData = {
  date: string | null;
  case_type: string | null;
  case_number: string;
  case_link: string;
  judge: string | null;
  court: string | null;
  plaintiff: Party;
  respondent: Party;
};

export default function CasesTablePage() {
  const [cases, setCases] = useState<CaseData[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<Filters>({});

  const { accessToken, setAccessToken } = useAuth();
  const router = useRouter();

  const fetchCases = useCallback(async (address: string) => {
    setLoading(true);
    setError(null);

    try {
      const res = await fetchWithAuth(
        address,
        { accessToken, setAccessToken },
        router.push,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            ...filters,
            CaseType: filters.CaseType || undefined,
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
      setCases(data.cases || []);
    } catch (err) {
      console.error("Error fetching cases:", err);
      setError((err instanceof Error ? err.message : "Unknown error"));
    } finally {
      setLoading(false);
    }
  }, [accessToken, setAccessToken, router, filters]);

  useEffect(() => {
    if (accessToken) {
      fetchCases(`${API_URL}/case/search`);
    }
  }, [accessToken, fetchCases]);
  
  return (
    <div className="p-4 space-y-4">

    <TopBar>
      <div>
        <h1 className="text-xl font-bold">Список дел</h1>
      </div>
    </TopBar>
    
    
    <Filter filters={filters} setFilters={setFilters} />
    
    <div className="flex justify-end gap-3">
      <Button onClick={() => fetchCases(`${API_URL}/case/search`)}>Внутренний поиск (БД)</Button>
      <Button onClick={() => fetchCases(`${API_URL}/external/search`)}>Внешний поиск (Target)</Button>
      <Button onClick={() => router.push('external/search')}>JSON представление</Button>
    </div>

      {loading && <p>Загрузка...</p>}
      {error && <p className="text-red-600">Ошибка: {error}</p>}

      {!loading && !error && (
        <div className="overflow-x-auto">
          <table className="min-w-full border border-red-500 color-foreground">
            <thead className="bg-foreground text-background">
              <tr>
                <th className="border px-4 py-2">Дата</th>
                <th className="border px-4 py-2">Номер дела</th>
                <th className="border px-4 py-2">Тип дела</th>
                <th className="border px-4 py-2">Истец</th>
                <th className="border px-4 py-2">Ответчик</th>
                <th className="border px-4 py-2">Судья</th>
                <th className="border px-4 py-2">Суд</th>
              </tr>
            </thead>
            <tbody>
              {cases.map((c, i) => (
                <tr key={i}>
                  <td className="border px-4 py-2">{c.date ?? '—'}</td>
                  <td className="border px-4 py-2">
                    <Link href={c.case_link} target="_blank" className="text-blue-600 underline">
                      {c.case_number}
                    </Link>
                  </td>
                  <td className="border px-4 py-2">{c.case_type ?? '—'}</td>
                  <td className="border px-4 py-2">
                    {c.plaintiff?.name ?? '—'}<br />
                    <small className="text-gray-500">{c.plaintiff?.inn ?? ''}</small>
                  </td>
                  <td className="border px-4 py-2">
                    {c.respondent?.name ?? '—'}<br />
                    <small className="text-gray-500">{c.respondent?.inn ?? ''}</small>
                  </td>
                  <td className="border px-4 py-2">{c.judge ?? '—'}</td>
                  <td className="border px-4 py-2">{c.court ?? '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}