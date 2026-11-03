import type { Metadata } from "next";
import { Fraunces, IBM_Plex_Mono, Manrope } from "next/font/google";
import type { ReactNode } from "react";

import "./globals.css";

// Visual Design Direction (docs/features/phase1/slice-3-map-experience.md):
// display (Fraunces, used sparingly) / UI (Manrope — the Fontshare "General
// Sans" register, self-hostable via next/font) / utility-mono (IBM Plex Mono,
// for anything that reads like a measured value: distances, coordinates).
const displayFont = Fraunces({
  subsets: ["latin"],
  variable: "--font-display",
  weight: ["400", "500", "600"],
});

const uiFont = Manrope({
  subsets: ["latin"],
  variable: "--font-ui",
  weight: ["400", "500", "600", "700"],
});

const monoFont = IBM_Plex_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  weight: ["400", "500"],
});

export const metadata: Metadata = {
  title: "NorthStar",
  description: "Your career has a location. Discover opportunities around you.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html
      lang="en"
      className={`theme-brand dark ${displayFont.variable} ${uiFont.variable} ${monoFont.variable}`}
    >
      <body className="min-h-screen bg-background font-ui text-foreground antialiased">
        {children}
      </body>
    </html>
  );
}
