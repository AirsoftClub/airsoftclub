import { QueryClient } from "@tanstack/react-query";

declare global {
  var queryClient: QueryClient;
  var token: string | null;
}

export {};
