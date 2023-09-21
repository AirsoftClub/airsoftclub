import { useIsServer } from "@/hooks/utils/use-is-server";
import axios, { AxiosInstance } from "axios";
import { authService } from "./auth/auth-service";

export const createAxiosInstance = (): AxiosInstance => {
  const isServer = useIsServer();

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
      const store = await import("@/store/store").then((m) => m.store);
      token = store.getState().auth.token;
    }

    if (isServer) {
      token = await authService.getToken();
    }

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  });

  instance.interceptors.response.use(
    (response) => response,
    async (error) => {
      const prevRequest = error.config;

      if (error.response.status === 401 && !prevRequest.sent) {
        prevRequest.sent = true;

        const data = await authService.refresh();

        prevRequest.headers["Authorization"] = `Bearer ${data.token}`;

        return instance(prevRequest);
      }

      return Promise.reject(error);
    }
  );

  return instance;
};

export const axiosInstance = createAxiosInstance();
