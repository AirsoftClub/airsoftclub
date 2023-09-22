"use client";

import { login } from "@/lib/rtk/reducers/auth-reducer";
import { RootState } from "@/lib/rtk/store";
import { authService } from "@/services/auth/auth-service";
import { createContext, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";

type AuthContextType = {
  token: string | null;
  setToken: (token: string) => void;
};

type AuthContextProps = {
  children: React.ReactNode;
};

export const AuthContext = createContext({} as AuthContextType);

export const AuthContextProvider = ({ children }: AuthContextProps) => {
  const token = useSelector((state: RootState) => state.auth.token);
  const dispatch = useDispatch();

  const setToken = (token: string) => {
    dispatch(login(token));
  };

  useEffect(() => {
    if (!token) {
      authService.getToken().then((newToken) => {
        dispatch(login(newToken));
      });
    }
  }, []);

  return (
    <AuthContext.Provider value={{ token, setToken }}>
      {children}
    </AuthContext.Provider>
  );
};
