'use client';

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { PageTitle } from "@/components/layout/PageTitle";
import { ThreatStatsCards } from "@/components/threat-intel/ThreatStatsCards";
import { IOCLookupTool } from "@/components/threat-intel/IOCLookupTool";
import { ThreatCategoryChart } from "@/components/threat-intel/ThreatCategoryChart";
import { ThreatFeedTable } from "@/components/threat-intel/ThreatFeedTable";
import { threatIntelService } from "@/lib/services/threat-intel.service";
import { ThreatIOC, ThreatIntelStats } from "@/types/threat-intel";

export default function ThreatIntelligencePage() {
  const [stats, setStats] = useState<ThreatIntelStats | null>(null);
  const [feedItems, setFeedItems] = useState<ThreatIOC[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [statsData, feedData] = await Promise.all([
        threatIntelService.getStats(),
        threatIntelService.getFeed({ limit: 50 }),
      ]);
      setStats(statsData);
      setFeedItems(feedData);
    } catch (err) {
      console.error("Failed to load threat intelligence dashboard data", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="relative space-y-10 pb-12">
      {/* Ambient purple glowing backdrop */}
      <div
        className="pointer-events-none absolute -top-20 -left-20 w-96 h-96 bg-[#8B5CF6]/5 rounded-full blur-[100px]"
        aria-hidden="true"
      />

      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
        <PageTitle
          title="Threat Intelligence"
          subtitle="Stay ahead of emerging zero-days, ransomware vectors, and global Indicators of Compromise (IOCs)."
        />
      </motion.div>

      {/* Metric KPI Cards */}
      <ThreatStatsCards stats={stats} loading={loading} />

      {/* Lookup Tool + Threat Category Analytics */}
      <div className="grid gap-8 lg:grid-cols-12">
        <div className="lg:col-span-7">
          <IOCLookupTool onLookupComplete={() => fetchData()} />
        </div>
        <div className="lg:col-span-5">
          <ThreatCategoryChart stats={stats} />
        </div>
      </div>

      {/* Live Threat Feed Table */}
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5, delay: 0.2 }}>
        <ThreatFeedTable items={feedItems} loading={loading} onRefresh={fetchData} />
      </motion.div>
    </div>
  );
}
