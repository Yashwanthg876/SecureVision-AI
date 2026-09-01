'use client';

import { PageTitle } from "@/components/layout/PageTitle";
import { KPICards } from "@/components/dashboard/KPICards";
import { QuickActions } from "@/components/dashboard/QuickActions";
import { ThreatTrendChart } from "@/components/dashboard/ThreatTrendChart";
import { RiskDistributionChart } from "@/components/dashboard/RiskDistributionChart";
import { RecentActivityTable } from "@/components/dashboard/RecentActivityTable";
import { CriticalFindings } from "@/components/dashboard/CriticalFindings";

import { useDashboard } from "@/hooks/useDashboard";
import { ErrorState } from "@/components/common/ErrorState";
import { SkeletonKPICard } from "@/components/dashboard/skeletons/SkeletonKPICard";
import { SkeletonChart } from "@/components/dashboard/skeletons/SkeletonChart";
import { SkeletonTable } from "@/components/dashboard/skeletons/SkeletonTable";
import { SkeletonActivity } from "@/components/dashboard/skeletons/SkeletonActivity";

import { format } from "date-fns";
import { motion } from "framer-motion";
import { Calendar, Hand } from "lucide-react";
import { useUser } from "@/context/UserContext";

export default function DashboardPage() {
  const { user } = useUser();
  const {
    summary,
    threatTrend,
    riskDistribution,
    recentActivity,
    criticalFindings,
    loading,
    error,
  } = useDashboard();

  const currentDate = format(new Date(), 'EEEE, MMMM do, yyyy');

  return (
    <div className="relative space-y-10">
      {/* Subtle Radial Glow */}
      <div className="pointer-events-none absolute -top-20 -right-20 w-96 h-96 bg-[#2563EB]/5 rounded-full blur-[100px]" aria-hidden="true" />

      {/* Welcome Section */}
      <motion.div 
        initial={{ opacity: 0, y: -10 }} 
        animate={{ opacity: 1, y: 0 }} 
        transition={{ duration: 0.4 }}
      >
        <div className="mb-2 flex items-center gap-2">
          <Hand className="h-4 w-4 text-yellow-400" />
          <p className="text-sm font-medium text-muted-foreground">Welcome back,</p>
        </div>
        <div className="mb-1">
          <h2 className="text-xl font-semibold text-[#F8FAFC]">{user.full_name || "Administrator"}</h2>
        </div>
        
        <PageTitle 
          title="SecureVision AI Executive Dashboard" 
          subtitle="Monitor your organization's cybersecurity posture from a centralized dashboard." 
        >
          <div className="flex items-center gap-2 text-sm font-medium text-muted-foreground bg-[#111827] border border-[#334155]/60 px-4 py-2 rounded-lg shadow-sm">
            <Calendar className="h-4 w-4 text-[#2563EB]" />
            {currentDate}
          </div>
        </PageTitle>
      </motion.div>

      {/* Quick Actions Row */}
      <QuickActions />

      {/* Main Dashboard Content */}
      {error ? (
        <ErrorState message={error} />
      ) : loading ? (
        <div className="space-y-10">
          <div className="grid gap-4 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-4">
            <SkeletonKPICard />
            <SkeletonKPICard />
            <SkeletonKPICard />
            <SkeletonKPICard />
          </div>
          <div className="grid gap-6 lg:grid-cols-4">
            <div className="col-span-1 lg:col-span-2">
              <SkeletonChart />
            </div>
            <div className="col-span-1 lg:col-span-2">
              <SkeletonChart />
            </div>
          </div>
          <div className="grid gap-6 lg:grid-cols-4 pb-8">
            <div className="col-span-1 lg:col-span-2 xl:col-span-2">
              <SkeletonTable />
            </div>
            <div className="col-span-1 lg:col-span-2 xl:col-span-2">
              <SkeletonActivity />
            </div>
          </div>
        </div>
      ) : (
        <div className="space-y-10">
          {/* KPI Cards Section */}
          <KPICards data={summary} />

          {/* Analytics Charts Section */}
          <div className="grid gap-6 lg:grid-cols-2">
            <ThreatTrendChart data={threatTrend} />
            <RiskDistributionChart data={riskDistribution} />
          </div>

          {/* Activity and Findings Section */}
          <div className="grid gap-6 grid-cols-1 pb-8">
            <RecentActivityTable data={recentActivity} />
            <CriticalFindings data={criticalFindings} />
          </div>
        </div>
      )}
    </div>
  );
}
