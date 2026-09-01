import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

export function SkeletonChart() {
  const heights = [40, 75, 55, 90, 65, 35, 80];
  
  return (
    <Card className="bg-[#111827] border-[#334155] h-full shadow-sm">
      <CardHeader>
        <Skeleton className="h-5 w-[150px] mb-2" />
        <Skeleton className="h-4 w-[250px]" />
      </CardHeader>
      <CardContent>
        <div className="flex items-end space-x-2 h-[250px] pt-4">
          {heights.map((height, i) => (
            <Skeleton key={i} className="w-full flex-1 rounded-t-sm" style={{ height: `${height}%` }} />
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
