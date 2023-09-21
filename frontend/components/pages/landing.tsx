"use client";

import { loginAction } from "@/actions/login-action";
import { logoutAction } from "@/actions/logout-action";
import { refreskTokenAction } from "@/actions/refresh-token-action";
import { GoogleLogin } from "@/components/auth/google/GoogleLogin";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/hooks/auth/use-auth";
import { useMe } from "@/hooks/users/use-me";
import { googleLogout } from "@react-oauth/google";
import { useQueryClient } from "@tanstack/react-query";

export const LandingPage = () => {
  const { token, setToken } = useAuth();
  const { data: me } = useMe();
  const queryClient = useQueryClient();

  const handleRefresh = () => {
    refreskTokenAction().then((res) => {
      setToken(res.token);
    });
  };

  const handleLogin = () => {
    loginAction({
      email: "test",
      password: "test",
    }).then((res) => {
      setToken(res.token);
    });
  };

  const handleLogout = () => {
    logoutAction().then((res) => {
      googleLogout();
      localStorage.clear();
      queryClient.clear();
      setToken(null);
    });
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      {token ? (
        <>
          <Button onClick={handleLogout}>logout</Button>
          <Button onClick={handleRefresh}>Refresh</Button>
        </>
      ) : (
        <>
          <Button onClick={handleLogin}>login</Button>
          <GoogleLogin />
        </>
      )}

      {me && <pre>{JSON.stringify(me, null, 2)}</pre>}
    </main>
  );
};
