import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import WebThreads from "@/components/ui/WebThreads";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "SecureVision AI | Autonomous Cybersecurity & AI Threat Intelligence Platform",
  description: "Next-generation vulnerability scanner, ML decision engine, SHAP explainability, and AI Copilot for continuous infrastructure security.",
};

import { UserProvider } from "@/context/UserContext";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased dark`}
    >
      <body className="min-h-full flex flex-col bg-[#020817] text-foreground selection:bg-primary/30 selection:text-primary-foreground relative">
        {/* Global Animated WebThreads Background */}
        <div className="fixed inset-0 z-0 pointer-events-none opacity-70 overflow-hidden">
          <WebThreads
            color1="#3B82F6"
            color2="#10B981"
            color3="#FFFFFF"
            speed={0.2}
            threadCount={7}
            frequency={4.5}
            spread={0.22}
            taper={1.0}
            position={0.5}
            fanMode="center"
            glow={0.03}
            falloff={0.55}
            thickness={1.2}
            brightness={0.7}
            opacity={0.85}
            mirror={true}
            shimmer={true}
            grain={true}
            grainIntensity={0.04}
            mouseInteraction={true}
            mouseStrength={0.35}
          />
        </div>

        {/* Global Page Content Container with UserContext */}
        <UserProvider>
          <div className="relative z-10 flex-1 flex flex-col">
            {children}
          </div>
        </UserProvider>
      </body>
    </html>
  );
}
