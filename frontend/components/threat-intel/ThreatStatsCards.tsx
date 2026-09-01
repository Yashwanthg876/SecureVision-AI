'use client';

import { motion } from "framer-motion";
import { ShieldAlert, AlertTriangle, Activity, Zap } from "lucide-react";
import { ThreatIntelStats } from "@/types/threat-intel";

interface ThreatStatsCardsProps {
  stats: ThreatIntelStats | null;
  loading?: boolean;
}

export function ThreatStatsCards({ stats, loading }: ThreatStatsCardsProps) {
  if (loading || !stats) {
    return (
      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-32 rounded-xl border border-[#334155] bg-[#111827]/40 animate-pulse" />
        ))}
      </div>
    );
  }

  const cardData = [
    {
      title: "Active Threat IOCs",
      value: stats.total_active_iocs.toLocaleString(),
      subtitle: `${stats.critical_threats} Critical, ${stats.high_threats} High`,
      icon: ShieldAlert,
      iconColor: "text-[#EF4444]",
      bgColor: "bg-[#EF4444]/10",
      borderColor: "border-[#EF4444]/30",
    },
    {
      title: "Critical Vulnerabilities",
      value: stats.critical_threats.toString(),
      subtitle: "Requires Immediate Remediation",
      icon: AlertTriangle,
      iconColor: "text-[#F97316]",
      bgColor: "bg-[#F97316]/10",
      borderColor: "border-[#F97316]/30",
    },
    {
      title: "Top Threat Vector",
      value: stats.top_threat_vector,
      subtitle: "Primary Attack Pattern",
      icon: Zap,
      iconColor: "text-[#8B5CF6]",
      bgColor: "bg-[#8B5CF6]/10",
      borderColor: "border-[#8B5CF6]/30",
      isSmallText: true,
    },
    {
      title: "Confidence Score",
      value: `${stats.avg_confidence_score}%`,
      subtitle: "Verified Telemetry Accuracy",
      icon: Activity,
      iconColor: "text-[#10B981]",
      bgColor: "bg-[#10B981]/10",
      borderColor: "border-[#10B981]/30",
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
            className="group relative overflow-hidden rounded-xl border border-[#334155] bg-[#111827]/70 p-5 backdrop-blur-md transition-all duration-300 hover:border-[#475569] hover:shadow-lg hover:shadow-purple-950/20"
          >
            {/* Top row */}
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                {card.title}
              </span>
              <div className={`flex h-9 w-9 items-center justify-center rounded-lg border ${card.borderColor} ${card.bgColor}`}>
                <Icon className={`h-5 w-5 ${card.iconColor}`} />
              </div>
            </div>

            {/* Value */}
            <div className="mt-3">
              <span className={`font-bold tracking-tight text-[#F8FAFC] ${card.isSmallText ? 'text-lg line-clamp-1' : 'text-3xl'}`}>
                {card.value}
              </span>
            </div>

            {/* Subtitle */}
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
