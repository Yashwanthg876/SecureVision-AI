'use client';

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { CriticalFinding } from "@/types/dashboard";
import { EmptyState } from "@/components/common/EmptyState";
import { AlertOctagon, Clock, Target, ArrowRight } from "lucide-react";
import { SEVERITY_COLORS } from "@/constants/dashboard";
import { motion } from "framer-motion";

interface CriticalFindingsProps {
  data: CriticalFinding[];
}

export function CriticalFindings({ data }: CriticalFindingsProps) {
  const displayData = data.slice(0, 5);

  const getSeverityStyles = (severity: string) => {
    switch (severity) {
      case 'Critical':
        return { color: SEVERITY_COLORS.Critical, bg: 'bg-red-500/10 text-red-600 dark:text-red-400' };
      case 'High':
        return { color: SEVERITY_COLORS.High, bg: 'bg-orange-500/10 text-orange-600 dark:text-orange-400' };
      case 'Medium':
        return { color: SEVERITY_COLORS.Medium, bg: 'bg-yellow-500/10 text-yellow-600 dark:text-yellow-400' };
      default:
        return { color: SEVERITY_COLORS.Low, bg: 'bg-blue-500/10 text-blue-600 dark:text-blue-400' };
    }
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5, delay: 0.4 }}>
      <Card className="bg-card border-border shadow-sm flex flex-col h-full">
        <CardHeader className="pb-4 border-b border-border shrink-0">
          <CardTitle className="text-sm font-medium text-foreground flex items-center gap-2">
            <AlertOctagon className="h-4 w-4 text-red-500" />
            Critical Findings
          </CardTitle>
          <CardDescription>Top priority vulnerabilities requiring immediate attention</CardDescription>
        </CardHeader>
        <CardContent className="pt-6 flex-1">
          {displayData.length === 0 ? (
            <EmptyState title="No Critical Findings" description="Your environment is secure." />
          ) : (
            <div className="space-y-4">
              {displayData.map((finding) => {
                const styles = getSeverityStyles(finding.severity);
                return (
                  <div 
                    key={finding.id} 
                    className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-lg bg-muted/40 border border-border transition-colors hover:bg-muted relative overflow-hidden group"
                  >
                    {/* Subtle Left Border Glow for Severity */}
                    <div 
                      className="absolute left-0 top-0 bottom-0 w-1 transition-opacity" 
                      style={{ backgroundColor: styles.color }}
                    />
                    
                    <div className="flex-1 min-w-0 pl-2">
                      <div className="flex items-center gap-2 mb-1.5">
                        <Badge 
                          variant="outline" 
                          className={`font-medium border-0 shadow-none ${styles.bg}`}
                        >
                          {finding.severity}
                        </Badge>
                        <h4 className="font-semibold text-sm text-foreground truncate">
                          {finding.title}
                        </h4>
                      </div>
                      <div className="flex items-center gap-4 text-xs text-muted-foreground mt-2">
                        <span className="flex items-center gap-1.5 truncate">
                          <Target className="h-3.5 w-3.5" />
                          {finding.target}
                        </span>
                        <span className="flex items-center gap-1.5">
                          <Clock className="h-3.5 w-3.5" />
                          {finding.timestamp}
                        </span>
                      </div>
                    </div>
                    
                    <div className="shrink-0 pl-2 sm:pl-0">
                      <Button className="bg-transparent hover:bg-primary/10 h-8 px-3 text-xs text-muted-foreground hover:text-primary group-hover:text-primary">
                        View Details
                        <ArrowRight className="ml-1.5 h-3.5 w-3.5" />
                      </Button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}
