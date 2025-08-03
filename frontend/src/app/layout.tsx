import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "@/components/providers";
import Navbar from "@/components/navbar";
import { Toaster } from "@/components/ui/sonner"; // For toast notifications
import { ThemeSwitcher } from "@/components/theme-switcher"; // Optional standalone switcher

const inter = Inter({
  subsets: ["latin"],
  display: "swap", // Better font loading
  variable: "--font-inter", // CSS variable for font
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={inter.variable} // Apply font variable
    >
      <head>
        {/* Preconnect to Google Fonts for better performance */}
        <link
          rel="preconnect"
          href="https://fonts.googleapis.com"
        />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
      </head>
      <body className={`font-sans antialiased min-h-screen flex flex-col`}>
        <Providers
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
          storageKey="ai-recruiter-theme" // Unique key for localStorage
        >
          <Navbar />
          {/* Optional: Standalone theme switcher for mobile */}
          <div className="fixed bottom-4 right-4 z-50 md:hidden">
            <ThemeSwitcher />
          </div>
          
          <main className="flex-1 container mx-auto px-4 py-8">
            {children}
          </main>
          
          {/* Toast notifications positioned at top-center */}
          <Toaster position="top-center" richColors />
          
          {/* Optional: Footer component can be added here */}
        </Providers>
      </body>
    </html>
  );
}
