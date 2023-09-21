"use server";

import { cookies } from "next/headers";

export const getTokenAction = async () => {
  const accessTokenCookie = cookies().get("access_token");

  if (!accessTokenCookie) {
    throw new Error("No access token found");
  }

  return accessTokenCookie.value;
};
