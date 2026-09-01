'use client';

import { Card, CardContent } from "@/components/ui/card";
import { Shield, Globe, GitBranch, Brain, TrendingUp, TrendingDown, Minus } from "lucide-react";
import { DashboardSummary } from "@/types/dashboard";
import { EmptyState } from "@/components/common/EmptyState";
import { motion } from "framer-motion";

interface KPICardsProps {
  data: DashboardSummary | null;
}

export function KPICards({ data }: KPICardsProps) {
  if (!data) {
    return <EmptyState title="No KPIs available" description="The dashboard summary data is currently empty." />;
  }

  const cardVariants = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    hover: { 
      y: -4,
      boxShadow: "0 10px 40px -10px rgba(37, 99, 235, 0.15)",
      borderColor: "rgba(37, 99, 235, 0.4)",
      transition: { duration: 0.2 } 
    }
  };

  const getTrendIcon = (trendText: string) => {
    if (trendText.includes('+')) return <TrendingUp className="h-3 w-3 mr-1 text-green-500" />;
    if (trendText.includes('-')) return <TrendingDown className="h-3 w-3 mr-1 text-red-500" />;
    return <Minus className="h-3 w-3 mr-1 text-muted-foreground" />;
  };

  return (
    <div className="grid gap-4 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-4">
      {/* Security Score */}
      <motion.div variants={cardVariants} initial="initial" animate="animate" whileHover="hover" transition={{ duration: 0.3, delay: 0.1 }}>
        <Card className="h-full bg-[#111827] border-[#334155] relative overflow-hidden group shadow-sm transition-colors duration-300">
          <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-[#2563EB]/50 to-transparent opacity-50 group-hover:opacity-100 transition-opacity" />
          <CardContent className="p-6">
            <div className="flex justify-between items-start mb-4">
              <p className="text-xs font-medium text-muted-foreground tracking-wide uppercase">Overall Security Score</p>
              <div className="p-2 bg-[#2563EB]/10 rounded-lg">
                <Shield className="h-4 w-4 text-[#2563EB]" />
              </div>
            </div>
            <div className="flex flex-col">
              <span className="text-4xl font-bold text-[#F8FAFC] tracking-tight">{data.score}</span>
              <div className="flex items-center justify-between mt-3">
                <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                  data.score_status === 'Healthy' ? 'bg-green-500/10 text-green-500' : 
                  data.score_status === 'Fair' ? 'bg-yellow-500/10 text-yellow-500' : 
                  data.score_status === 'Warning' || data.score_status === 'Critical' ? 'bg-red-500/10 text-red-400' :
                  'bg-slate-500/10 text-slate-400'
                }`}>
                  {data.score_status}
                </span>
                <span className="text-xs text-muted-foreground flex items-center">
                  {getTrendIcon(data.score_trend)}
                  {data.score_trend}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
      
      {/* Websites Monitored */}
      <motion.div variants={cardVariants} initial="initial" animate="animate" whileHover="hover" transition={{ duration: 0.3, delay: 0.2 }}>
        <Card className="h-full bg-[#111827] border-[#334155] relative overflow-hidden group shadow-sm transition-colors duration-300">
          <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-[#2563EB]/50 to-transparent opacity-50 group-hover:opacity-100 transition-opacity" />
          <CardContent className="p-6">
            <div className="flex justify-between items-start mb-4">
              <p className="text-xs font-medium text-muted-foreground tracking-wide uppercase">Websites Monitored</p>
              <div className="p-2 bg-[#2563EB]/10 rounded-lg">
                <Globe className="h-4 w-4 text-[#2563EB]" />
              </div>
            </div>
            <div className="flex flex-col">
              <span className="text-4xl font-bold text-[#F8FAFC] tracking-tight">{data.websites_total}</span>
              <div className="flex items-center justify-between mt-3">
                <span className="text-xs text-muted-foreground font-medium">Assessments Saved</span>
                <span className="text-xs text-muted-foreground flex items-center bg-[#334155]/40 px-2 py-0.5 rounded-full">
                  <TrendingUp className="h-3 w-3 mr-1 text-green-500" />
                  {data.websites_scanned_today} Scanned today
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* GitHub Repositories */}
      <motion.div variants={cardVariants} initial="initial" animate="animate" whileHover="hover" transition={{ duration: 0.3, delay: 0.3 }}>
        <Card className="h-full bg-[#111827] border-[#334155] relative overflow-hidden group shadow-sm transition-colors duration-300">
          <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-[#2563EB]/50 to-transparent opacity-50 group-hover:opacity-100 transition-opacity" />
          <CardContent className="p-6">
            <div className="flex justify-between items-start mb-4">
              <p className="text-xs font-medium text-muted-foreground tracking-wide uppercase">GitHub Repositories</p>
              <div className="p-2 bg-[#2563EB]/10 rounded-lg">
                <GitBranch className="h-4 w-4 text-[#2563EB]" />
              </div>
            </div>
            <div className="flex flex-col">
              <span className="text-4xl font-bold text-[#F8FAFC] tracking-tight">{data.repos_total}</span>
              <div className="flex items-center justify-between mt-3">
                <span className="text-xs text-muted-foreground font-medium">Repository Scans</span>
                <span className="text-xs flex items-center bg-red-500/10 text-red-400 px-2 py-0.5 rounded-full">
                  {data.repos_high_risk} High Risk
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* AI Threat Scans */}
      <motion.div variants={cardVariants} initial="initial" animate="animate" whileHover="hover" transition={{ duration: 0.3, delay: 0.4 }}>
        <Card className="h-full bg-[#111827] border-[#334155] relative overflow-hidden group shadow-sm transition-colors duration-300">
          <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-[#2563EB]/50 to-transparent opacity-50 group-hover:opacity-100 transition-opacity" />
          <CardContent className="p-6">
            <div className="flex justify-between items-start mb-4">
              <p className="text-xs font-medium text-muted-foreground tracking-wide uppercase">AI Scans</p>
              <div className="p-2 bg-[#2563EB]/10 rounded-lg">
                <Brain className="h-4 w-4 text-[#2563EB]" />
              </div>
            </div>
            <div className="flex flex-col">
              <span className="text-4xl font-bold text-[#F8FAFC] tracking-tight">{data.ai_threats_total}</span>
              <div className="flex items-center justify-between mt-3">
                <span className="text-xs text-muted-foreground font-medium">Total AI Scans</span>
                <span className="text-xs flex items-center bg-red-500/10 text-red-400 px-2 py-0.5 rounded-full">
                  {data.ai_threats_critical} Critical
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
