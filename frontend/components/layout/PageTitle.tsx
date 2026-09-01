import { ReactNode } from "react";

interface PageTitleProps {
  title: string;
  subtitle?: string;
  children?: ReactNode;
}

export function PageTitle({ title, subtitle, children }: PageTitleProps) {
  return (
    <div className="mb-8 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-[#F8FAFC]">{title}</h1>
        {subtitle && (
          <p className="mt-1 text-sm text-muted-foreground">
            {subtitle}
          </p>
        )}
      </div>
      {children && (
        <div className="flex items-center gap-3">
          {children}
        </div>
      )}
    </div>
  );
}
