"use server";

import { LoginResponse } from "@/interfaces/auth/login";
import { setAuthCookies } from "@/services/auth/cookies";
import axios from "axios";
import { cookies } from "next/headers";

export const refreshTokenAction = async () => {
  const refreshToken = cookies().get("refresh_token");

  if (!refreshToken) {
    throw new Error("No refresh refresh token found");
  }

  const payloadString = Buffer.from(
    refreshToken.value.split(".")[1],
    "base64"
  ).toString();

  const payload = JSON.parse(payloadString);

  if (payload.exp * 1000 < Date.now()) {
    cookies().delete("refresh_token");
    throw new Error("Refresh token expired");
  }

  const response = await axios.post<LoginResponse>(
    `${process.env.INTERNAL_API_URL}/auth/refresh`,
    {
      refresh_token: refreshToken.value,
    }
  );

  setAuthCookies(response.data);

  return response.data;
};
