"use client";

import { AuthContext } from "@/contexts/auth-context";
import { useContext } from "react";

export const useAuth = () => {
  const { token, setToken } = useContext(AuthContext);

  return { token, setToken };
};
