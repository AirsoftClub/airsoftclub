import { refreskTokenAction as refreshTokenAction } from "@/actions/refresh-token-action";
import axios, { AxiosInstance } from "axios";

const createAxiosInstace = (): AxiosInstance => {
  const instance = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL,
    headers: {
      "Content-Type": "application/json",
    },
    withCredentials: true,
  });

  instance.interceptors.request.use(async (config) => {
    let token: string | null = null;

    if (typeof window !== "undefined") {
      token = localStorage.getItem("access_token");
    }

    if (typeof window === "undefined") {
      const { cookies } = await import("next/headers");
      const tokenCookie = cookies().get("access_token");
      if (tokenCookie) {
        token = tokenCookie.value;
      }
    }

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  });

  instance.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error.config;

      if (error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;

        if (typeof window !== "undefined") {
          const data = await refreshTokenAction();
          localStorage.setItem("access_token", data.token);
          return axios(originalRequest);
        }
      }

      return Promise.reject(error);
    }
  );

  return instance;
};

export const axiosInstance = createAxiosInstace();
