import { LoginResponse } from "@/interfaces/auth/login";
import { cookies } from "next/headers";

export const setAuthCookies = ({ token, refresh_token }: LoginResponse) => {
  const cookiesStore = cookies();

  cookiesStore.set("refresh_token", refresh_token, {
    httpOnly: true,
    sameSite: "none",
    secure: true,
  });

  cookiesStore.set("access_token", token, {
    httpOnly: true,
    sameSite: "none",
    secure: true,
  });
};
