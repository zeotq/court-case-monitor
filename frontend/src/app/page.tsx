import InfoPanel from "@/components/InfoPanel";

export default function Home() {
  return (
    <main className="flex h-screen items-center justify-center">
      <div className="p-6 bg-secondary rounded-lg shadow-lg w-96">
        <InfoPanel />
      </div>
    </main>
  );
}
