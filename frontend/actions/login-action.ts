"use server";

import { setAuthCookies } from "@/hooks/auth/use-cookies";
import { LoginRequest, LoginResponse } from "@/interfaces/auth/login";
import axios from "axios";

export const loginAction = async (loginRequest: LoginRequest) => {
  const response = await axios.post<LoginResponse>(
    `${process.env.INTERNAL_API_URL}/auth/login`,
    loginRequest
  );

  if (response.status === 200) {
    setAuthCookies(response.data);
  }

  return response.data;
};
