import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "LinkedIn AgentOS — Autonomous AI Operations Command Center",
  description: "Enterprise autonomous multi-agent content research, creation, and publishing platform for LinkedIn",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#090909] text-white min-h-screen antialiased selection:bg-[#E53935] selection:text-white">
        {children}
      </body>
    </html>
  );
}
