import { Inbox } from "lucide-react";

interface EmptyStateProps {
  title?: string;
  description?: string;
}

export function EmptyState({ 
  title = "No data available", 
  description = "There is currently no data to display for this widget." 
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center p-8 h-full min-h-[200px] border border-border border-dashed rounded-xl bg-card/30 text-center">
      <div className="h-12 w-12 rounded-full bg-muted flex items-center justify-center mb-4">
        <Inbox className="h-6 w-6 text-muted-foreground" />
      </div>
      <h3 className="text-sm font-medium text-foreground mb-1">{title}</h3>
      <p className="text-xs text-muted-foreground max-w-sm">
        {description}
      </p>
    </div>
  );
}
