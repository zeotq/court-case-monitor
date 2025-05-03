"use client";

import React, { HTMLAttributes, PropsWithChildren } from "react";
import { useAuth } from "@/app/auth/components/AuthContext";
import { logout } from "@/app/services/logout";
import AuthButton from "@/components/AuthButton";
import { Button } from "@/components/Button";


interface TopBarProps extends HTMLAttributes<HTMLDivElement> {}

const TopBar: React.FC<PropsWithChildren<TopBarProps>> = ({ children, className = "", ...props }) => {
  const { isAuthenticated, setAccessToken, accessToken } = useAuth();

  return (
    <div className="w-full flex justify-end items-center p-4 bg-background shadow-md border-2 border-b-5 border-foreground rounded-lg">
      <div className="w-full flex flex-row gap-5">
        <div className="flex-col gap-2">
          <h1 className="text-xl font-bold text-foreground">Система мониторинга</h1>
          <h1 className="text-l text-foreground">by zeotq</h1>
        </div>
        <div className="flex flex-row gap-5">
          {children ? ('-') : ''}
          {children}
        </div>
      </div>
      <div className="flex justify-end">
        {!isAuthenticated ? (
          <AuthButton>Login</AuthButton>
        ) : (
          <Button onClick={() => logout(setAccessToken)}>Logout</Button>
        )}
      </div>
    </div>
  );
};

export default TopBar;