"use server";

import { cookies } from "next/headers";

export const logoutAction = async () => {
  const cookieStore = cookies();

  cookieStore.getAll().forEach((cookie) => {
    cookieStore.delete(cookie.name);
  });

  return {
    redirect: {
      destination: "/",
      permanent: false,
    },
  };
};
