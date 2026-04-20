"use client";
import { ButtonHTMLAttributes, ReactNode } from "react";
import clsx from "clsx";

type Variant = "primary" | "ghost" | "outline";
type Size = "sm" | "md";

interface Props extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: Size;
  icon?: ReactNode;
  loading?: boolean;
}

export default function Button({
  children,
  className,
  variant = "primary",
  size = "md",
  icon,
  loading,
  disabled,
  ...rest
}: Props) {
  const base =
    "inline-flex items-center justify-center gap-2 rounded-xl font-medium tracking-tight transition-all active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed";
  const sizes = {
    sm: "text-xs px-3 py-1.5",
    md: "text-sm px-4 py-2.5",
  };
  const variants = {
    primary:
      "accent-bg text-black hover:brightness-110 shadow-[0_6px_20px_var(--accent-glow)]",
    ghost:
      "bg-bg-elev text-fg hover:bg-bg-card border border-bg-border",
    outline:
      "bg-transparent text-fg border border-bg-border hover:border-[color:var(--accent)] hover:text-[color:var(--accent)]",
  };
  return (
    <button
      className={clsx(base, sizes[size], variants[variant], className)}
      disabled={disabled || loading}
      {...rest}
    >
      {loading ? (
        <span className="w-3.5 h-3.5 border-2 border-current border-t-transparent rounded-full animate-spin" />
      ) : (
        icon
      )}
      {children}
    </button>
  );
}
