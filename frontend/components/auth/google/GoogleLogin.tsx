"use client";

import { googleLoginAction } from "@/actions/google-login-action";
import { useAuth } from "@/hooks/auth/use-auth";
import {
  CredentialResponse,
  GoogleLogin as GoogleLoginButton,
} from "@react-oauth/google";

export const GoogleLogin = () => {
  const { token, setToken } = useAuth();

  const authenticateAgainstBackend = async (
    credentialsResponse: CredentialResponse
  ) => {
    if (!credentialsResponse.credential) {
      return;
    }

    const res = await googleLoginAction({
      token: credentialsResponse.credential,
    });

    setToken(res.token);
  };

  return (
    <>
      {!token && (
        <GoogleLoginButton
          onSuccess={authenticateAgainstBackend}
          useOneTap
          auto_select
        />
      )}
    </>
  );
};
