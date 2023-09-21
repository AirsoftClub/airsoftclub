"use server";

import { GoogleLoginRequest } from "@/interfaces/auth/google-login";
import { LoginResponse } from "@/interfaces/auth/login";
import { setAuthCookies } from "@/services/auth/cookies";
import axios from "axios";

export const googleLoginAction = async (
  googleLoginRequest: GoogleLoginRequest
) => {
  const response = await axios.post<LoginResponse>(
    `${process.env.INTERNAL_API_URL}/auth/google/login`,
    googleLoginRequest
  );

  if (response.status !== 200) {
    throw new Error("Google login failed");
  }

  setAuthCookies({
    refresh_token: response.data.refresh_token,
    access_token: response.data.token,
  });

  return response.data;
};
