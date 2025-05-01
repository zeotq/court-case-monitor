'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Button } from '@/app/home/components/Button';

type Party = {
  name: string | null;
  inn: string | null;
};

type CaseData = {
  date: string | null;
  case_number: string;
  case_link: string;
  judge: string | null;
  court: string | null;
  plaintiff: Party;
  respondent: Party;
};

const sampleData: CaseData[] = [
  {
    date: '30.04.2025 0:00:00',
    case_number: 'СИП-377/2025',
    case_link: 'https://kad.arbitr.ru/Card/2ca2d01e-bd04-4587-865f-f16210b04d5a',
    judge: null,
    court: null,
    plaintiff: {
      name: 'ООО Группа компаний "ФЕНИКС"',
      inn: '6165231191',
    },
    respondent: {
      name: 'ООО "КББ"',
      inn: '7806286171',
    },
  },
  {
    date: null,
    case_number: 'СИП-376/2025',
    case_link: 'https://kad.arbitr.ru/Card/c15d8ff5-c015-431b-8182-9cb8045dae80',
    judge: null,
    court: null,
    plaintiff: {
      name: 'ООО "Яндекс"',
      inn: '7736207543',
    },
    respondent: {
      name: null,
      inn: null,
    },
  },
];

export default function CasesTablePage() {
  const [cases, setCases] = useState<CaseData[]>([]);

  useEffect(() => {
    // Здесь вы можете заменить sampleData на результат fetch
    setCases(sampleData);
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Список дел</h1>
      <div className="overflow-x-auto">
        <table className="min-w-full border border-red-500 color-foreground">
          <thead className="bg-foreground text-background">
            <tr>
              <th className="border px-4 py-2">Дата</th>
              <th className="border px-4 py-2">Номер дела</th>
              <th className="border px-4 py-2">Истец</th>
              <th className="border px-4 py-2">Ответчик</th>
              <th className="border px-4 py-2">Судья</th>
              <th className="border px-4 py-2">Суд</th>
            </tr>
          </thead>
          <tbody>
            {cases.map((c, i) => (
              <tr key={i} className="">
                <td className="border px-4 py-2">{c.date ?? '—'}</td>
                <td className="border px-4 py-2">
                  <Link href={c.case_link} target="_blank" className="text-blue-600 underline">
                    {c.case_number}
                  </Link>
                </td>
                <td className="border px-4 py-2">
                  {c.plaintiff.name ?? '—'}<br />
                  <small className="text-gray-500">{c.plaintiff.inn ?? ''}</small>
                </td>
                <td className="border px-4 py-2">
                  {c.respondent.name ?? '—'}<br />
                  <small className="text-gray-500">{c.respondent.inn ?? ''}</small>
                </td>
                <td className="border px-4 py-2">{c.judge ?? '—'}</td>
                <td className="border px-4 py-2">{c.court ?? '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
