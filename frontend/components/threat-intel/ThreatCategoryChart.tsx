'use client';

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell
} from 'recharts';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { PieChart } from "lucide-react";
import { ThreatIntelStats } from "@/types/threat-intel";

interface ThreatCategoryChartProps {
  stats: ThreatIntelStats | null;
}

const CATEGORY_COLORS = [
  "#EF4444", // Red
  "#F97316", // Orange
  "#8B5CF6", // Purple
  "#3B82F6", // Blue
  "#10B981", // Emerald
  "#EC4899", // Pink
  "#EAB308", // Yellow
];

export function ThreatCategoryChart({ stats }: ThreatCategoryChartProps) {
  if (!stats || !stats.category_distribution) {
    return (
      <Card className="bg-[#111827] border-[#334155] h-full">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-[#F8FAFC]">Threat Categories</CardTitle>
        </CardHeader>
        <CardContent className="h-64 flex items-center justify-center text-xs text-muted-foreground">
          Loading threat distribution...
        </CardContent>
      </Card>
    );
  }

  const chartData = Object.entries(stats.category_distribution).map(([name, count]) => ({
    name: name.length > 18 ? `${name.substring(0, 16)}...` : name,
    fullName: name,
    count,
  }));

  return (
    <Card className="bg-[#111827] border-[#334155] shadow-lg flex flex-col justify-between">
      <CardHeader className="pb-2 border-b border-[#334155]/50">
        <CardTitle className="text-sm font-medium text-[#F8FAFC] flex items-center gap-2">
          <PieChart className="h-4 w-4 text-[#8B5CF6]" />
          Threat Vectors & Categories
        </CardTitle>
        <CardDescription className="text-xs">
          Distribution of active threat vectors detected globally
        </CardDescription>
      </CardHeader>
      <CardContent className="pt-4">
        <div className="w-full h-[250px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 10, right: 10, left: -15, bottom: 25 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
              <XAxis
                dataKey="name"
                stroke="#94A3B8"
                fontSize={11}
                tickLine={false}
                axisLine={false}
                angle={-20}
                textAnchor="end"
              />
              <YAxis
                stroke="#94A3B8"
                fontSize={11}
                tickLine={false}
                axisLine={false}
                allowDecimals={false}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#020817',
                  border: '1px solid #334155',
                  borderRadius: '8px',
                  boxShadow: '0 10px 40px -10px rgba(0,0,0,0.5)',
                }}
                formatter={(value: any) => [`${value} Indicators`, 'Count']}
                labelFormatter={(label: any, items: any) => {
                  if (items && items[0]) {
                    return items[0].payload.fullName;
                  }
                  return label;
                }}
              />
              <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={CATEGORY_COLORS[index % CATEGORY_COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
