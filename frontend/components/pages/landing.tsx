"use client";

import { GoogleLogin } from "@/components/auth/google/GoogleLogin";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/hooks/auth/use-auth";
import { useMe } from "@/hooks/users/use-me";
import { authService } from "@/services/auth/auth-service";
import { googleLogout } from "@react-oauth/google";
import { useQueryClient } from "@tanstack/react-query";

export const LandingPage = () => {
  const { token, setToken } = useAuth();
  const { data: me } = useMe();
  const queryClient = useQueryClient();

  const handleRefresh = () => {
    authService.refresh().then((res) => {
      setToken(res.token);
    });
  };

  const handleLogin = () => {
    authService
      .login({
        email: "test",
        password: "test",
      })
      .then((res) => {
        setToken(res.token);
      });
  };

  const handleLogout = () => {
    authService.logout().then((res) => {
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
