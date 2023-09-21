import { getTokenAction } from "@/actions/get-token-action";
import { loginAction } from "@/actions/login-action";
import { logoutAction } from "@/actions/logout-action";
import { refreshTokenAction } from "@/actions/refresh-token-action";
import { GoogleLoginRequest } from "@/interfaces/auth/google-login";
import { LoginRequest } from "@/interfaces/auth/login";
import { TokenFamilyResponse } from "@/interfaces/auth/token-family";
import axios from "axios";

const login = async (request: LoginRequest) => {
  const response = await loginAction(request);

  localStorage.setItem("access_token", response.token);

  return response;
};

const googleLogin = async (request: GoogleLoginRequest) => {
  const { data } = await axios.post<TokenFamilyResponse>(
    "/api/auth/google/login",
    request
  );

  localStorage.setItem("access_token", data.token);

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
  await logoutAction();
  localStorage.clear();
};

export const authService = {
  login,
  googleLogin,
  refresh,
  getToken,
  logout,
};
