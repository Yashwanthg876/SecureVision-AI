import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { RecentActivity } from "@/types/dashboard";
import { EmptyState } from "@/components/common/EmptyState";
import { STATUS_COLORS } from "@/constants/dashboard";
import { motion } from "framer-motion";
import { Activity } from "lucide-react";

interface RecentActivityTableProps {
  data: RecentActivity[];
}

export function RecentActivityTable({ data }: RecentActivityTableProps) {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5, delay: 0.3 }}>
      <Card className="bg-[#111827] border-[#334155] shadow-sm">
        <CardHeader className="pb-4 border-b border-[#334155]/50">
          <CardTitle className="text-sm font-medium text-[#F8FAFC] flex items-center gap-2">
            <Activity className="h-4 w-4 text-[#2563EB]" />
            Recent Activity
          </CardTitle>
          <CardDescription>Live activity stream and system events</CardDescription>
        </CardHeader>
        <CardContent className="pt-6">
          {data.length === 0 ? (
            <EmptyState title="No Recent Activity" description="No activity logs have been recorded yet." />
          ) : (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow className="border-[#334155] hover:bg-transparent">
                    <TableHead className="text-muted-foreground font-medium">Timestamp</TableHead>
                    <TableHead className="text-muted-foreground font-medium">Module</TableHead>
                    <TableHead className="text-muted-foreground font-medium">Target</TableHead>
                    <TableHead className="text-muted-foreground font-medium">Action</TableHead>
                    <TableHead className="text-muted-foreground font-medium">Status</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {data.map((activity) => (
                    <TableRow key={activity.id} className="border-[#334155]/50 hover:bg-white/5 transition-colors">
                      <TableCell className="text-muted-foreground whitespace-nowrap text-sm">
                        {activity.timestamp}
                      </TableCell>
                      <TableCell className="font-medium text-[#F8FAFC] whitespace-nowrap text-sm">
                        {activity.module}
                      </TableCell>
                      <TableCell className="text-muted-foreground text-sm">
                        {activity.target}
                      </TableCell>
                      <TableCell className="text-sm text-[#F8FAFC]">
                        {activity.action}
                      </TableCell>
                      <TableCell>
                        <Badge
                          variant={
                            activity.status === 'Success' ? 'default' :
                            activity.status === 'Failed' ? 'destructive' : 'secondary'
                          }
                          style={{ 
                            backgroundColor: (activity.status === 'Success' || activity.status === 'Warning' || activity.status === 'Pending') 
                              ? STATUS_COLORS[activity.status] 
                              : undefined 
                          }}
                          className="font-medium shadow-none border-0"
                        >
                          {activity.status}
                        </Badge>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}
