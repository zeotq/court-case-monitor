"use client";

import AuthButton from "@/components/AuthButton";
import getBaseURL from "@/utils/getBaseURL";
import { useEffect, useState } from "react";

const InfoPanel = () => {
  const [redirectUri, setRedirectUri] = useState("");

  useEffect(() => {
    const baseURL = getBaseURL();
    if (baseURL) {
      setRedirectUri(`${baseURL}/home`);
    }
  }, []);

  return (
    <div className="relative flex items-center justify-center">
      <div className="relative z-10 flex flex-col gap-4">
        Welcome to Court Case Monitor
        <AuthButton  redirectUri={redirectUri}>Auth</AuthButton>
      </div>
    </div>
  );
}

export default InfoPanel;
