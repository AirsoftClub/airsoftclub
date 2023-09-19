import { GoogleLoginRequest } from "@/interfaces/auth/google-login";
import { LoginRequest } from "@/interfaces/auth/login";
import { TokenFamilyResponse } from "@/interfaces/auth/token-family";
import axios from "axios";

const login = async (request: LoginRequest) => {
  const { data } = await axios.post<TokenFamilyResponse>(
    "/api/auth/login",
    request
  );

  localStorage.setItem("access_token", data.token);

  return data;
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
  const { data } = await axios.post<TokenFamilyResponse>(
    "/api/auth/refresh",
    {}
  );

  return data;
};

const getToken = async () => {
  const { data } = await axios.get("/api/auth/token");

  return data;
};

const logout = async () => {
  localStorage.clear();
  await axios.post("/api/auth/logout");
};

export const authService = {
  login,
  googleLogin,
  refresh,
  getToken,
  logout,
};
