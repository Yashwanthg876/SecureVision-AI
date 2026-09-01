'use client';

import { useState } from "react";
import { PageTitle } from "@/components/layout/PageTitle";
import { AssessmentForm } from "@/components/website-security/AssessmentForm";
import { QuickChecks } from "@/components/website-security/QuickChecks";
import { AssessmentHistoryTable } from "@/components/website-security/AssessmentHistoryTable";
import { AssessmentResultsPlaceholder } from "@/components/website-security/AssessmentResultsPlaceholder";
import { AssessmentResultsViewer } from "@/components/website-security/AssessmentResultsViewer";
import { AssessmentProgress } from "@/components/website-security/AssessmentProgress";
import { motion } from "framer-motion";

export default function WebsiteSecurityPage() {
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
    setHistoryRefreshKey((key) => key + 1);
  };

  const handleScanError = (errorMsg: string) => {
    setIsScanning(false);
    setScanError(errorMsg);
  };

  return (
    <div className="relative space-y-10 pb-12">
      {/* Subtle Glow */}
      <div className="pointer-events-none absolute -top-20 -left-20 w-96 h-96 bg-[#2563EB]/5 rounded-full blur-[100px]" aria-hidden="true" />

      {/* Hero Section */}
      <motion.div 
        initial={{ opacity: 0, y: -10 }} 
        animate={{ opacity: 1, y: 0 }} 
        transition={{ duration: 0.4 }}
      >
        <PageTitle 
          title="Website Security Assessment" 
          subtitle="Passively analyze domains to discover misconfigurations, expired certificates, and open vulnerabilities without triggering alerts." 
        />
      </motion.div>

      {/* Top Row: Form & Results */}
      <div className="grid gap-10 xl:grid-cols-3">
        <div className="xl:col-span-1 space-y-8">
          <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.5, delay: 0.1 }}>
            <AssessmentForm 
              onScanStart={handleScanStart}
              onScanSuccess={handleScanSuccess}
              onScanError={handleScanError}
              isScanning={isScanning}
            />
          </motion.div>
          <AssessmentProgress isVisible={isScanning} />
        </div>

        <div className="xl:col-span-2">
          {scanError && (
            <div className="p-4 mb-4 rounded-lg bg-red-500/10 border border-red-500/50 text-red-400 text-sm">
              Failed to run assessment: {scanError}
            </div>
          )}
          {scanResults ? (
            <AssessmentResultsViewer data={scanResults} />
          ) : (
            <AssessmentResultsPlaceholder />
          )}
        </div>
      </div>

      {/* Middle Row: Full Width Quick Checks */}
      <div className="pt-2">
        <QuickChecks />
      </div>

      {/* Bottom Row: History */}
      <div className="pt-2">
        <AssessmentHistoryTable refreshKey={historyRefreshKey} />
      </div>
    </div>
  );
}
