'use client';

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { RiskDistribution } from "@/types/dashboard";
import { EmptyState } from "@/components/common/EmptyState";
import { CHART_CONFIG } from "@/constants/dashboard";
import { motion } from "framer-motion";
import { PieChart as PieChartIcon } from "lucide-react";

interface RiskDistributionProps {
  data: RiskDistribution[];
}

export function RiskDistributionChart({ data }: RiskDistributionProps) {
  const totalFindings = data.reduce((acc, curr) => acc + curr.value, 0);

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5, delay: 0.2 }}>
      <Card className="bg-[#111827] border-[#334155] h-full shadow-sm">
        <CardHeader className="pb-4 border-b border-[#334155]/50">
          <CardTitle className="text-sm font-medium text-[#F8FAFC] flex items-center gap-2">
            <PieChartIcon className="h-4 w-4 text-[#2563EB]" />
            Risk Distribution
          </CardTitle>
          <CardDescription>Breakdown of active findings by severity</CardDescription>
        </CardHeader>
        <CardContent className="pt-6">
          {data.length === 0 ? (
            <EmptyState title="No Risk Data" description="There is currently no risk distribution data to display." />
          ) : (
            <div className="w-full relative" style={{ height: CHART_CONFIG.height }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart margin={CHART_CONFIG.margins}>
                  <Pie
                    data={data}
                    cx="50%"
                    cy="50%"
                    innerRadius={70}
                    outerRadius={100}
                    paddingAngle={3}
                    dataKey="value"
                    stroke="none"
                  >
                    {data.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#020817', border: '1px solid #334155', borderRadius: '8px', boxShadow: '0 10px 40px -10px rgba(0,0,0,0.5)' }}
                    itemStyle={{ color: '#F8FAFC' }}
                  />
                  <Legend verticalAlign="bottom" height={36} iconType="circle" />
                </PieChart>
              </ResponsiveContainer>
              {/* Centered Total Count */}
              <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none pb-8">
                <span className="text-3xl font-bold text-[#F8FAFC]">{totalFindings}</span>
                <span className="text-xs text-muted-foreground uppercase tracking-wider font-medium">Total</span>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}
