"use client";

import { AuthContextProvider } from "@/contexts/auth-context";
import { ReactQueryProvider } from "@/providers/react-query/provider";
import { GoogleOAuthProvider } from "@react-oauth/google";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthContextProvider>
          <GoogleOAuthProvider
            clientId={process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID}
          >
            <ReactQueryProvider>{children}</ReactQueryProvider>
          </GoogleOAuthProvider>
        </AuthContextProvider>
      </body>
    </html>
  );
}
