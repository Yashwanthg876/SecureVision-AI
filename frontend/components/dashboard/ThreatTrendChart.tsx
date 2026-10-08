'use client';

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { ThreatTrend } from "@/types/dashboard";
import { EmptyState } from "@/components/common/EmptyState";
import { CHART_CONFIG, SEVERITY_COLORS } from "@/constants/dashboard";
import { motion } from "framer-motion";
import { LineChart as LineChartIcon } from "lucide-react";

interface ThreatTrendChartProps {
  data: ThreatTrend[];
}

export function ThreatTrendChart({ data }: ThreatTrendChartProps) {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5, delay: 0.1 }}>
      <Card className="bg-card border-border h-full shadow-sm">
        <CardHeader className="pb-4 border-b border-border">
          <CardTitle className="text-sm font-medium text-foreground flex items-center gap-2">
            <LineChartIcon className="h-4 w-4 text-primary" />
            Threat Trend
          </CardTitle>
          <CardDescription>7-day history of detected threats across all modules</CardDescription>
        </CardHeader>
        <CardContent className="pt-6">
          {data.length === 0 ? (
            <EmptyState title="No Threat Data" description="There is currently no threat trend data to display." />
          ) : (
            <div className="w-full" style={{ height: CHART_CONFIG.height }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data} margin={CHART_CONFIG.margins}>
                  <XAxis 
                    dataKey="date" 
                    stroke="var(--muted-foreground)" 
                    fontSize={12} 
                    tickLine={false} 
                    axisLine={false}
                    dy={10}
                  />
                  <YAxis 
                    stroke="var(--muted-foreground)" 
                    fontSize={12} 
                    tickLine={false} 
                    axisLine={false}
                    dx={-10}
                  />
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'var(--card)', 
                      borderColor: 'var(--border)', 
                      borderRadius: '8px', 
                      color: 'var(--foreground)',
                      boxShadow: '0 10px 40px -10px rgba(0,0,0,0.15)' 
                    }}
                    itemStyle={{ color: 'var(--foreground)' }}
                    labelStyle={{ color: 'var(--foreground)', fontWeight: 600 }}
                  />
                  <Legend verticalAlign="top" height={36} iconType="circle" />
                  <Line type="monotone" dataKey="critical" stroke={SEVERITY_COLORS.Critical} strokeWidth={CHART_CONFIG.strokeWidth} dot={false} activeDot={{ r: 6 }} />
                  <Line type="monotone" dataKey="high" stroke={SEVERITY_COLORS.High} strokeWidth={CHART_CONFIG.strokeWidth} dot={false} activeDot={{ r: 6 }} />
                  <Line type="monotone" dataKey="medium" stroke={SEVERITY_COLORS.Medium} strokeWidth={CHART_CONFIG.strokeWidth} dot={false} activeDot={{ r: 6 }} />
                  <Line type="monotone" dataKey="low" stroke={SEVERITY_COLORS.Low} strokeWidth={CHART_CONFIG.strokeWidth} dot={false} activeDot={{ r: 6 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}
