"use client";

import { useState } from "react";
import LoginForm from "./LoginForm";
import RegisterForm from "./RegisterForm";

const Auth = () => {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <div className="p-6 bg-secondary rounded-lg shadow-lg w-96">
        {isLogin ? (
          <LoginForm toggle={() => setIsLogin(false)} />
        ) : (
          <RegisterForm toggle={() => setIsLogin(true)} />
        )}
      </div>
    </div>
  );
};

export default Auth;
