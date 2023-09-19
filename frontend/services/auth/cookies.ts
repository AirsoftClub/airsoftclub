import { cookies } from "next/headers";

type SetCookiesAuth = {
  refresh_token: string;
  access_token: string;
};

export const setAuthCookies = ({
  refresh_token,
  access_token,
}: SetCookiesAuth) => {
  const cookiesStore = cookies();

  cookiesStore.set("refresh_token", refresh_token, {
    httpOnly: true,
    sameSite: "none",
    secure: true,
  });

  cookiesStore.set("access_token", access_token, {
    httpOnly: true,
    sameSite: "none",
    secure: true,
  });
};
