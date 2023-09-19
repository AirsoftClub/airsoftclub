import { cookies } from "next/headers";

export async function GET() {
  const token = cookies().get("access_token");

  if (!token) {
    return new Response(null, { status: 401 });
  }

  return Response.json({ token: token.value }, { status: 200 });
}
