"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactNode, useState } from "react";

export const ReactQueryProvider = ({ children }: { children: ReactNode }) => {
  const [queryClient] = useState(() => new QueryClient());

  global.queryClient = queryClient;

  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
};
