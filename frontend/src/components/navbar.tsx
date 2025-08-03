"use client";
import Link from "next/link";
import { ThemeToggle } from "./theme-toggle";
import { Button } from "./ui/button";

export default function Navbar() {
  return (
    <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-16 items-center px-4">
        <Link href="/" className="flex items-center space-x-2 mr-8">
          <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center text-white font-bold">
            AR
          </div>
          <span className="font-bold text-lg hidden sm:inline-block">
            AI Recruiter
          </span>
        </Link>

        <div className="flex items-center space-x-6">
          <Link href="/dashboard" className="text-sm font-medium transition-colors hover:text-primary">
            Dashboard
          </Link>
          <Link href="/jobs" className="text-sm font-medium transition-colors hover:text-primary text-muted-foreground">
            Jobs
          </Link>
          <Link href="/candidates" className="text-sm font-medium transition-colors hover:text-primary text-muted-foreground">
            Candidates
          </Link>
        </div>

        <div className="ml-auto flex items-center space-x-4">
          <ThemeToggle />
          <Button>Sign In</Button>
        </div>
      </div>
    </nav>
  );
}
