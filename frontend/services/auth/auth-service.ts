import { getTokenAction } from "@/actions/get-token-action";
import { googleLoginAction } from "@/actions/google-login-action";
import { loginAction } from "@/actions/login-action";
import { logoutAction } from "@/actions/logout-action";
import { refreshTokenAction } from "@/actions/refresh-token-action";
import { GoogleLoginRequest } from "@/interfaces/auth/google-login";
import { LoginRequest } from "@/interfaces/auth/login";

const login = async (request: LoginRequest) => {
  const response = await loginAction(request);

  return response;
};

const googleLogin = async (request: GoogleLoginRequest) => {
  const data = await googleLoginAction(request);

  return data;
};

const refresh = async () => {
  const response = await refreshTokenAction();

  return response;
};

const getToken = async () => {
  return await getTokenAction();
};

const logout = async () => {
  global.token = null;
  global.queryClient.clear();
  await logoutAction();
};

export const authService = {
  login,
  googleLogin,
  refresh,
  getToken,
  logout,
};
