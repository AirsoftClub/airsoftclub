import { LandingPage } from "@/components/pages/landing";
import { GET_ME_QUERY_KEY, getMe } from "@/hooks/users/use-me";
import { getQueryClient } from "@/providers/react-query/client";
import { Hydrate } from "@/providers/react-query/hydrate";
import { dehydrate } from "@tanstack/react-query";

export default async function Home() {
  const queryClient = getQueryClient();
  await queryClient.prefetchQuery(GET_ME_QUERY_KEY, getMe);
  const dehydratedState = dehydrate(queryClient);

  return (
    <Hydrate state={dehydratedState}>
      <LandingPage />
    </Hydrate>
  );
}
