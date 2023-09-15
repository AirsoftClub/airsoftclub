import { ReactNode, useState } from "react"
import { Hydrate, QueryClient, QueryClientProvider } from "react-query"
import { useDehydratedState } from "use-dehydrated-state"

export default function Providers({ children }: { children: ReactNode }) {
    const [queryClient] = useState(() => new QueryClient())
    const dehydratedState = useDehydratedState()

    return (
        <QueryClientProvider client={queryClient}>
            <Hydrate state={dehydratedState}>
                {children}
            </Hydrate>
        </QueryClientProvider>
    )
}