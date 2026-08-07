import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Modern Curve Number Hydrology · 2026 workshop",
  description:
    "A workshop on curve-number theory, spatial estimation, and Earth Observation applications.",
  metadataBase: new URL("https://skp703.github.io/cn-workshop-2026/"),
  openGraph: {
    title: "Modern Curve Number Hydrology",
    description: "From lookup tables to a watershed you can measure.",
    type: "website",
    images: [
      {
        url: "/og.png",
        width: 1731,
        height: 909,
        alt: "Modern Curve Number Hydrology workshop",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Modern Curve Number Hydrology",
    description: "From lookup tables to a watershed you can measure.",
    images: ["/og.png"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" data-path="core">
      <head>
        {/* The same stylesheet is used by the app preview and static Pages export. */}
        {/* eslint-disable-next-line @next/next/no-css-tags */}
        <link rel="stylesheet" href="/workshop.css" />
        <script src="/workshop.js" defer />
      </head>
      <body>{children}</body>
    </html>
  );
}
