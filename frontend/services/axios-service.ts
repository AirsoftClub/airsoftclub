import { useIsServer } from "@/hooks/utils/use-is-server";
import axios, { AxiosInstance } from "axios";
import { authService } from "./auth/auth-service";

const isServer = useIsServer();

const createAxiosInstace = (): AxiosInstance => {
  const instance = axios.create({
    baseURL: isServer
      ? process.env.INTERNAL_API_URL
      : process.env.NEXT_PUBLIC_API_URL,
    headers: {
      "Content-Type": "application/json",
    },
    withCredentials: true,
  });

  instance.interceptors.request.use(async (config) => {
    let token: string | null = null;

    if (!isServer) {
      token = localStorage.getItem("access_token");
    }

    if (isServer) {
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
      console.log("hola", error);

      const prevRequest = error.config;

      if (error.response.status === 401 && !prevRequest.sent) {
        prevRequest.sent = true;

        const data = await authService.refresh();

        prevRequest.headers["Authorization"] = `Bearer ${data.token}`;

        if (!isServer) {
          localStorage.setItem("access_token", data.token);
        }

        return instance(prevRequest);
      }

      return Promise.reject(error);
    }
  );

  return instance;
};

export const axiosInstance = createAxiosInstace();
