"use server";

import { LoginRequest } from "@/interfaces/auth/login";
import { setAuthCookies } from "@/services/auth/cookies";
import axios from "axios";

export const loginAction = async (loginRequest: LoginRequest) => {
  const response = await axios.post(
    `${process.env.INTERNAL_API_URL}/auth/login`,
    loginRequest
  );

  if (response.status === 200) {
    setAuthCookies(response.data);
  }

  return response.data;
};