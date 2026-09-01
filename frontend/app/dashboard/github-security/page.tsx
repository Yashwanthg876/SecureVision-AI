'use client';

import { useState } from "react";
import { PageTitle } from "@/components/layout/PageTitle";
import { RepoScanForm } from "@/components/github-security/RepoScanForm";
import { RepoScanProgress } from "@/components/github-security/RepoScanProgress";
import { RepoScanResultsViewer } from "@/components/github-security/RepoScanResultsViewer";
import { RepoScanPlaceholder } from "@/components/github-security/RepoScanPlaceholder";
import { RepoScanHistoryTable } from "@/components/github-security/RepoScanHistoryTable";
import { motion } from "framer-motion";

export default function GitHubSecurityPage() {
  const [isScanning, setIsScanning] = useState(false);
  const [scanResults, setScanResults] = useState<any>(null);
  const [scanError, setScanError] = useState<string | null>(null);
  const [historyRefreshKey, setHistoryRefreshKey] = useState(0);

  const handleScanStart = () => {
    setIsScanning(true);
    setScanError(null);
    setScanResults(null);
  };

  const handleScanSuccess = (data: any) => {
    setIsScanning(false);
    setScanResults(data);
    setHistoryRefreshKey((k) => k + 1);
  };

  const handleScanError = (msg: string) => {
    setIsScanning(false);
    setScanError(msg);
  };

  return (
    <div className="relative space-y-10 pb-12">
      {/* Ambient glow */}
      <div className="pointer-events-none absolute -top-20 -left-20 w-96 h-96 bg-[#2563EB]/5 rounded-full blur-[100px]" aria-hidden="true" />

      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
        <PageTitle
          title="GitHub Security Scanner"
          subtitle="Scan public repositories for exposed secrets, risky configuration files, and dependency manifests — no token required."
        />
      </motion.div>

      {/* Main Grid: Form + Results */}
      <div className="grid gap-10 xl:grid-cols-3">
        {/* Left: form + progress */}
        <div className="xl:col-span-1 space-y-4">
          <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.5, delay: 0.1 }}>
            <RepoScanForm
              onScanStart={handleScanStart}
              onScanSuccess={handleScanSuccess}
              onScanError={handleScanError}
              isScanning={isScanning}
            />
          </motion.div>
          <RepoScanProgress isVisible={isScanning} />
        </div>

        {/* Right: results */}
        <div className="xl:col-span-2">
          {scanError && (
            <div className="p-4 mb-4 rounded-lg bg-red-500/10 border border-red-500/50 text-red-400 text-sm">
              ⚠️ {scanError}
            </div>
          )}
          {scanResults ? (
            <RepoScanResultsViewer data={scanResults} />
          ) : (
            <RepoScanPlaceholder />
          )}
        </div>
      </div>

      {/* History Table */}
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5, delay: 0.3 }}>
        <RepoScanHistoryTable refreshKey={historyRefreshKey} />
      </motion.div>
    </div>
  );
}
