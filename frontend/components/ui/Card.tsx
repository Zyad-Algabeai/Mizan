import { ReactNode } from "react";
import clsx from "clsx";

interface CardProps {
  children: ReactNode;
  className?: string;
  title?: ReactNode;
  subtitle?: ReactNode;
  chip?: ReactNode;
  action?: ReactNode;
}

export default function Card({
  children,
  className,
  title,
  subtitle,
  chip,
  action,
}: CardProps) {
  return (
    <section className={clsx("mz-card p-5 sm:p-6 mz-fade", className)}>
      {(title || chip || action) && (
        <header className="flex items-start justify-between gap-4 mb-4">
          <div>
            <div className="flex items-center gap-2">
              {title && (
                <h2 className="text-[15px] font-semibold text-fg tracking-tight">
                  {title}
                </h2>
              )}
              {chip && <span className="mz-chip">{chip}</span>}
            </div>
            {subtitle && (
              <p className="text-xs text-fg-muted mt-1 font-mono tracking-[0.08em]">
                {subtitle}
              </p>
            )}
          </div>
          {action && <div className="shrink-0">{action}</div>}
        </header>
      )}
      {children}
    </section>
  );
}
