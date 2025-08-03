"use client";

import { useTheme } from "next-themes";
import { Toaster as Sonner, toast as sonnerToast } from "sonner";

type ToasterProps = React.ComponentProps<typeof Sonner>;

const Toaster = ({ ...props }: ToasterProps) => {
  const { theme = "system" } = useTheme();

  return (
    <Sonner
      theme={theme as ToasterProps["theme"]}
      className="toaster group"
      toastOptions={{
        classNames: {
          toast:
            "group toast group-[.toaster]:bg-background group-[.toaster]:text-foreground group-[.toaster]:border-border group-[.toaster]:shadow-lg",
          description: "group-[.toast]:text-muted-foreground",
          actionButton:
            "group-[.toast]:bg-primary group-[.toast]:text-primary-foreground",
          cancelButton:
            "group-[.toast]:bg-muted group-[.toast]:text-muted-foreground",
          error: "group-[.toaster]:bg-destructive group-[.toaster]:text-destructive-foreground group-[.toaster]:border-destructive",
          success: "group-[.toaster]:bg-success group-[.toaster]:text-success-foreground group-[.toaster]:border-success",
          warning: "group-[.toaster]:bg-warning group-[.toaster]:text-warning-foreground group-[.toaster]:border-warning",
          info: "group-[.toaster]:bg-info group-[.toaster]:text-info-foreground group-[.toaster]:border-info",
        },
      }}
      style={{
        "--normal-bg": "hsl(var(--popover))",
        "--normal-text": "hsl(var(--popover-foreground))",
        "--normal-border": "hsl(var(--border))",
        "--success-bg": "hsl(var(--success))",
        "--success-text": "hsl(var(--success-foreground))",
        "--success-border": "hsl(var(--success))",
        "--error-bg": "hsl(var(--destructive))",
        "--error-text": "hsl(var(--destructive-foreground))",
        "--error-border": "hsl(var(--destructive))",
        "--warning-bg": "hsl(var(--warning))",
        "--warning-text": "hsl(var(--warning-foreground))",
        "--warning-border": "hsl(var(--warning))",
        "--info-bg": "hsl(var(--info))",
        "--info-text": "hsl(var(--info-foreground))",
        "--info-border": "hsl(var(--info))",
      }}
      {...props}
    />
  );
};

// Export toast function for easy use
const toast = sonnerToast;

export { Toaster, toast };
