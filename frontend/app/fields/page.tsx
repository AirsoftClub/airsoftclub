import { Fields } from "@/components/fields/Fields";
import { getQueryClient } from "@/providers/react-query/client";
import { Hydrate } from "@/providers/react-query/hydrate";
import { dehydrate } from "@tanstack/react-query";

export default async function () {
  const queryClient = getQueryClient();
  await queryClient.prefetchQuery(["posts"], async () => {
    const response = await fetch("https://jsonplaceholder.typicode.com/todos/");
    return response.json();
  });
  const dehydratedState = dehydrate(queryClient);

  return (
    <Hydrate state={dehydratedState}>
      <Fields />
    </Hydrate>
  );
}
