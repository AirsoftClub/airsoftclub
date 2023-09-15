"use client";

import { Hydrate as HydrationBoundary } from "@tanstack/react-query";

export const Hydrate = (props: any) => {
  return <HydrationBoundary {...props} />;
};
