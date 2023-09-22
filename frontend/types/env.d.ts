import { QueryClient } from "@tanstack/react-query";

declare global {
  namespace NodeJS {
    interface ProcessEnv {
      NEXT_PUBLIC_APP_URL: string;
      NEXT_PUBLIC_API_URL: string;
      NEXT_PUBLIC_GOOGLE_CLIENT_ID: string;
      INTERNAL_API_URL: string;
    }
  }

  interface Window {
    queryClient: QueryClient;
  }
}

export {};
