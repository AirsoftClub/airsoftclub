"use client";

import { authService } from "@/services/auth/auth-service";
import { createContext, useEffect } from "react";

type AuthContextType = {
  token: string | null;
  setToken: (token: string) => void;
};

type AuthContextProps = {
  children: React.ReactNode;
};

export const AuthContext = createContext({} as AuthContextType);

export const AuthContextProvider = ({ children }: AuthContextProps) => {
  const token = global.token;

  const setToken = (token: string) => {
    global.token = token;
  };

  useEffect(() => {
    if (!token) {
      authService.getToken().then((newToken) => {
        setToken(newToken);
      });
    }
  }, []);

  return (
    <AuthContext.Provider value={{ token, setToken }}>
      {children}
    </AuthContext.Provider>
  );
};
