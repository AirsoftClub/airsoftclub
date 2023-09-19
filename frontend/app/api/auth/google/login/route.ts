import { setAuthCookies } from "@/services/auth/cookies";
import axios from "axios";
import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const response = await axios.post(
    `${process.env.NEXT_PUBLIC_API_URL}/auth/google/login`,
    await request.json()
  );

  if (response.status === 200) {
    setAuthCookies({
      refresh_token: response.data.refresh_token,
      access_token: response.data.token,
    });

    return NextResponse.json(response.data);
  }

  return Response.json({ message: "Not Authenticated" }, { status: 400 });
}
