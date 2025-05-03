'use client';

import { useEffect } from 'react';
import { useRouter } from "next/navigation";
import Loading from "@/components/Loading";
import getBaseURL from "@/utils/getBaseURL";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    router.push(getBaseURL() + '/table');  
  });
  return (
    <div className="grow flex-col items-center p-4 space-y-4 gap-4">
      <main className="flex h-screen items-center justify-center">
        <div className="p-6 bg-secondary rounded-lg shadow-lg w-96">
          <Loading />
        </div>
      </main>
    </div>
  );
}
