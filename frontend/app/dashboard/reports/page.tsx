'use client';

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { PageTitle } from "@/components/layout/PageTitle";
import { ReportStatsCards } from "@/components/reports/ReportStatsCards";
import { ReportsTable } from "@/components/reports/ReportsTable";
import { ReportGeneratorModal } from "@/components/reports/ReportGeneratorModal";
import { reportsService } from "@/lib/services/reports.service";
import { ReportItem, ReportStats } from "@/types/reports";
import { FileText, Plus, UserCheck, Building, Mail, ShieldCheck } from "lucide-react";
import { useUser } from "@/context/UserContext";

export default function ReportsPage() {
  const { user } = useUser();
  const [reports, setReports] = useState<ReportItem[]>([]);
  const [stats, setStats] = useState<ReportStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const fetchReportsData = async () => {
    setLoading(true);
    try {
      const reportsData = await reportsService.getReports();
      setReports(reportsData);
      const computedStats = reportsService.getStats(reportsData);
      setStats(computedStats);
    } catch (err) {
      console.error("Failed to load reports page data", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReportsData();
  }, []);

  return (
    <div className="relative space-y-8 pb-12">
      {/* Ambient blue/purple glow */}
      <div
        className="pointer-events-none absolute -top-20 -left-20 w-96 h-96 bg-[#3B82F6]/5 rounded-full blur-[100px]"
        aria-hidden="true"
      />

      {/* Header with Export Button */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
          <PageTitle
            title="Reports & Compliance"
            subtitle="Generate, view, and export executive security assessment reports in PDF, CSV, or JSON."
          />
        </motion.div>

        <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.4, delay: 0.1 }}>
          <button
            type="button"
            onClick={() => setIsModalOpen(true)}
            className="h-10 px-5 text-xs font-semibold rounded-lg bg-gradient-to-r from-[#8B5CF6] to-[#6D28D9] text-white hover:from-[#7C3AED] hover:to-[#5B21B6] transition-all flex items-center gap-2 shadow-lg shadow-purple-900/30"
          >
            <Plus className="w-4 h-4" /> Export Custom Report
          </button>
        </motion.div>
      </div>

      {/* Logged-in User Information Card for Reports */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.1 }}
        className="p-4 rounded-xl border border-[#334155] bg-gradient-to-r from-[#111827] via-[#0F172A] to-[#1E1B4B]/40 backdrop-blur-md flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-md"
      >
        <div className="flex items-center gap-3.5">
          <div className="h-10 w-10 rounded-xl bg-[#8B5CF6]/20 border border-[#8B5CF6]/40 flex items-center justify-center text-[#A78BFA] shrink-0">
            <UserCheck className="h-5 w-5" />
          </div>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <h4 className="text-sm font-bold text-[#F8FAFC]">
                {user.full_name || "PRAKASH"}
              </h4>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#8B5CF6]/20 text-[#A78BFA] border border-[#8B5CF6]/30">
                {user.role || "Lead Security Analyst"}
              </span>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center gap-1">
                <ShieldCheck className="w-3 h-3" /> Active Auditor
              </span>
            </div>
            <div className="flex items-center gap-4 text-xs text-muted-foreground mt-1 flex-wrap">
              <span className="flex items-center gap-1">
                <Mail className="w-3.5 h-3.5 text-slate-400" />
                {user.email || "9924008052@klu.ac.in"}
              </span>
              <span className="flex items-center gap-1">
                <Building className="w-3.5 h-3.5 text-slate-400" />
                {user.organization || "KLU Cyber Security"}
              </span>
            </div>
          </div>
        </div>

        <div className="text-xs text-slate-400 border-t md:border-t-0 md:border-l border-[#334155]/60 pt-2 md:pt-0 md:pl-4">
          <span className="text-[11px] text-muted-foreground uppercase tracking-wider block">Audited Reports</span>
          <span className="text-base font-bold text-[#F8FAFC]">{reports.length} Records</span>
        </div>
      </motion.div>

      {/* Metric KPI Cards */}
      <ReportStatsCards stats={stats} loading={loading} />

      {/* Reports Table */}
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5, delay: 0.2 }}>
        <ReportsTable reports={reports} loading={loading} />
      </motion.div>

      {/* Report Generator Modal */}
      <ReportGeneratorModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        reportsList={reports}
        onReportGenerated={fetchReportsData}
      />
    </div>
  );
}
