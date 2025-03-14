"use client";

import React from "react";

export interface ButtonProps {
  children: React.ReactNode;
  onClick: () => void;
}

const Button: React.FC<ButtonProps> = ({ children, onClick }) => {
  return (
    <button
      className="px-6 py-3 text-lg font-medium text-white bg-blue-600 rounded-lg shadow-md hover:bg-blue-700 transition"
      onClick={onClick}
    >
      {children}
    </button>
  );
};

export default Button;
