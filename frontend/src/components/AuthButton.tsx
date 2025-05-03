"use client";

import React from "react";
import { useRouter } from "next/navigation";
import fullURL from "@/utils/getFullURL"
import { Button } from "./Button";

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
    <Button
      onClick={handleRedirect}
    >
      {children}
    </Button>
  );
};

export default AuthButton;
