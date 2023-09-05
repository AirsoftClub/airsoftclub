"use client"

import { Button } from "@/components/ui/button";
import { login } from "@/services/authService";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <Button onClick={() => login("n.kasevich@gmail.com", "1234")}>Click me</Button>
    </main>
  )
}
