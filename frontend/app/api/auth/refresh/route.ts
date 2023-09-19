import { setAuthCookies } from "@/services/auth/cookies";
import axios from "axios";
import { cookies } from "next/headers";
import { NextResponse } from "next/server";

export async function POST() {
  const token = cookies().get("refresh_token");

  if (!token) {
    return new Response(null, { status: 401 });
  }

  const payloadString = Buffer.from(
    token.value.split(".")[1],
    "base64"
  ).toString();

  const payload = JSON.parse(payloadString);

  if (payload.exp * 1000 < Date.now()) {
    cookies().delete("refresh_token");
    return new Response(null, { status: 401 });
  }

  const response = await axios.post(
    `${process.env.NEXT_PUBLIC_API_URL}/auth/refresh`,
    { refresh_token: token.value }
  );

  setAuthCookies({
    refresh_token: response.data.refresh_token,
    access_token: response.data.token,
  });

  return NextResponse.json(response.data, { status: 200 });
}
