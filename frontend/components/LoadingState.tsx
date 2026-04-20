import clsx from "clsx";

export function Skeleton({ className }: { className?: string }) {
  return (
    <div
      className={clsx(
        "animate-pulse rounded-lg bg-bg-elev border border-bg-border/50",
        className,
      )}
    />
  );
}

export function ErrorBanner({ message }: { message: string }) {
  return (
    <div className="mz-card p-4 border-danger/40 bg-danger/5 text-sm text-fg">
      <span className="font-mono text-xs uppercase tracking-wider text-danger mr-2">
        Error
      </span>
      {message}
    </div>
  );
}
