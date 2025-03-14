"use client";

import { redirect } from "next/navigation";
import Button from "@/components/Button";

const ButtonsPanel = () => {
  return (
    <div className="relative flex items-center justify-center w-full h-80">
      <div className="relative z-10 flex flex-col gap-4">
        Welcome to Court Case Monitor
        <Button onClick={() => redirect(`/auth`)}>Authorization</Button>
      </div>
    </div>
  );
}

export default ButtonsPanel;
