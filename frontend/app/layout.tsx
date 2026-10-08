import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import WebThreads from "@/components/ui/WebThreads";
import "./globals.css";
import { UserProvider } from "@/context/UserContext";
import { ThemeProvider } from "@/context/ThemeContext";

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

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased dark`}
    >
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `(function(){try{var t=localStorage.getItem('securevision-theme');if(t==='light'){document.documentElement.classList.remove('dark');document.documentElement.classList.add('light');document.documentElement.setAttribute('data-theme','light');}else{document.documentElement.classList.add('dark');document.documentElement.classList.remove('light');document.documentElement.setAttribute('data-theme','dark');}}catch(e){}})();`,
          }}
        />
      </head>
      <body className="min-h-full flex flex-col bg-background text-foreground selection:bg-primary/30 selection:text-primary-foreground relative transition-colors duration-200">
        {/* Global Animated WebThreads Background */}
        <div className="fixed inset-0 z-0 pointer-events-none opacity-25 dark:opacity-70 overflow-hidden">
          <WebThreads
            color1="#3B82F6"
            color2="#10B981"
            color3="#8B5CF6"
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

        {/* Global Providers */}
        <ThemeProvider>
          <UserProvider>
            <div className="relative z-10 flex-1 flex flex-col">
              {children}
            </div>
          </UserProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
