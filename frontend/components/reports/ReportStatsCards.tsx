'use client';

import { motion } from "framer-motion";
import { FileText, Download, ShieldCheck, Award } from "lucide-react";
import { ReportStats } from "@/types/reports";

interface ReportStatsCardsProps {
  stats: ReportStats | null;
  loading?: boolean;
}

export function ReportStatsCards({ stats, loading }: ReportStatsCardsProps) {
  if (loading || !stats) {
    return (
      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-32 rounded-xl border border-border bg-card/60 animate-pulse" />
        ))}
      </div>
    );
  }

  const cardData = [
    {
      title: "Total Security Reports",
      value: stats.total_reports.toString(),
      subtitle: "Generated Security Audits",
      icon: FileText,
      iconColor: "text-[#3B82F6]",
      bgColor: "bg-[#3B82F6]/10",
      borderColor: "border-[#3B82F6]/30",
    },
    {
      title: "Executive PDF Exports",
      value: stats.pdf_downloads.toString(),
      subtitle: "Downloaded Compliance Files",
      icon: Download,
      iconColor: "text-[#8B5CF6]",
      bgColor: "bg-[#8B5CF6]/10",
      borderColor: "border-[#8B5CF6]/30",
    },
    {
      title: "Latest Audit Score",
      value: `${stats.latest_score} / 100`,
      subtitle: stats.latest_score >= 80 ? "Healthy Security Posture" : "Review Recommended",
      icon: ShieldCheck,
      iconColor: stats.latest_score >= 80 ? "text-[#10B981]" : "text-[#F97316]",
      bgColor: stats.latest_score >= 80 ? "bg-[#10B981]/10" : "bg-[#F97316]/10",
      borderColor: stats.latest_score >= 80 ? "border-[#10B981]/30" : "border-[#F97316]/30",
    },
    {
      title: "Framework Status",
      value: "NIST & OWASP",
      subtitle: stats.compliance_status,
      icon: Award,
      iconColor: "text-[#EC4899]",
      bgColor: "bg-[#EC4899]/10",
      borderColor: "border-[#EC4899]/30",
      isSmallText: true,
    },
  ];

  return (
    <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
      {cardData.map((card, index) => {
        const Icon = card.icon;
        return (
          <motion.div
            key={card.title}
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: index * 0.08 }}
            className="group relative overflow-hidden rounded-xl border border-border bg-card p-5 backdrop-blur-md shadow-sm transition-all duration-300 hover:border-primary/50 hover:shadow-md"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                {card.title}
              </span>
              <div className={`flex h-9 w-9 items-center justify-center rounded-lg border ${card.borderColor} ${card.bgColor}`}>
                <Icon className={`h-5 w-5 ${card.iconColor}`} />
              </div>
            </div>

            <div className="mt-3">
              <span className={`font-bold tracking-tight text-foreground ${card.isSmallText ? 'text-xl' : 'text-3xl'}`}>
                {card.value}
              </span>
            </div>

            <p className="mt-2 text-xs font-medium text-muted-foreground flex items-center gap-1.5">
              <span className={`inline-block h-1.5 w-1.5 rounded-full ${card.iconColor.replace('text-', 'bg-')}`} />
              {card.subtitle}
            </p>
          </motion.div>
        );
      })}
    </div>
  );
}
