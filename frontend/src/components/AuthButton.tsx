"use client";

import React from "react";
import { useRouter } from "next/navigation";
import fullURL from "@/utils/getFullURL"

export interface AuthButtonProps {
  children: React.ReactNode;
  redirectUri?: string;
}

const AuthButton: React.FC<AuthButtonProps> = ({ children, redirectUri: callbackUri }) => {
  const router = useRouter();
  const pathname = fullURL();

  const handleRedirect = () => {
    const returnTo = callbackUri || pathname;
    router.push(`/auth?callback_uri=${encodeURIComponent(returnTo)}`);
  };

  return (
    <button
      className="px-6 py-3 text-lg font-medium text-white bg-blue-600 rounded-lg shadow-md hover:bg-blue-700 transition"
      onClick={handleRedirect}
    >
      {children}
    </button>
  );
};

export default AuthButton;
