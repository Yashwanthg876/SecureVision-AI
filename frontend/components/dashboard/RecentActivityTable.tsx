'use client';

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { RecentActivity } from "@/types/dashboard";
import { EmptyState } from "@/components/common/EmptyState";
import { motion } from "framer-motion";
import { Activity } from "lucide-react";

interface RecentActivityTableProps {
  data: RecentActivity[];
}

export function RecentActivityTable({ data }: RecentActivityTableProps) {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5, delay: 0.3 }}>
      <Card className="bg-card border-border shadow-sm">
        <CardHeader className="pb-4 border-b border-border">
          <CardTitle className="text-sm font-medium text-foreground flex items-center gap-2">
            <Activity className="h-4 w-4 text-primary" />
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
                  <TableRow className="border-border hover:bg-transparent">
                    <TableHead className="text-muted-foreground font-medium">Timestamp</TableHead>
                    <TableHead className="text-muted-foreground font-medium">Module</TableHead>
                    <TableHead className="text-muted-foreground font-medium">Target</TableHead>
                    <TableHead className="text-muted-foreground font-medium">Action</TableHead>
                    <TableHead className="text-muted-foreground font-medium">Status</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {data.map((activity) => (
                    <TableRow key={activity.id} className="border-border hover:bg-muted/50 transition-colors">
                      <TableCell className="text-muted-foreground whitespace-nowrap text-sm">
                        {activity.timestamp}
                      </TableCell>
                      <TableCell className="font-medium text-foreground whitespace-nowrap text-sm">
                        {activity.module}
                      </TableCell>
                      <TableCell className="text-muted-foreground text-sm">
                        {activity.target}
                      </TableCell>
                      <TableCell className="text-sm text-foreground">
                        {activity.action}
                      </TableCell>
                      <TableCell>
                        <Badge
                          variant={
                            activity.status === 'Success' ? 'default' :
                            activity.status === 'Failed' ? 'destructive' : 'secondary'
                          }
                          className="capitalize text-xs font-semibold"
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
