'use client';

import { useState } from "react";
import { PageTitle } from "@/components/layout/PageTitle";
import { AIDetectionForm } from "@/components/ai-detection/AIDetectionForm";
import { AIDetectionResults } from "@/components/ai-detection/AIDetectionResults";
import { AIDetectionHistory } from "@/components/ai-detection/AIDetectionHistory";
import { motion } from "framer-motion";
import { Bot } from "lucide-react";

export default function AIDetectionPage() {
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
      <div className="pointer-events-none absolute -top-20 -left-20 w-96 h-96 bg-[#8B5CF6]/5 rounded-full blur-[100px]" aria-hidden="true" />

      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
        <PageTitle
          title="AI Detection"
          subtitle="Detect and analyze AI-generated content, anomalous patterns, and emerging threats."
        />
      </motion.div>

      {/* Main Grid: Form + Results */}
      <div className="grid gap-10 xl:grid-cols-2">
        {/* Left: form */}
        <div className="space-y-4">
          <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.5, delay: 0.1 }}>
            <AIDetectionForm
              onScanStart={handleScanStart}
              onScanSuccess={handleScanSuccess}
              onScanError={handleScanError}
              isScanning={isScanning}
            />
          </motion.div>
        </div>

        {/* Right: results */}
        <div>
          {scanError && (
            <div className="p-4 mb-4 rounded-lg bg-red-500/10 border border-red-500/50 text-red-400 text-sm">
              ⚠️ {scanError}
            </div>
          )}
          {scanResults ? (
            <AIDetectionResults data={scanResults} />
          ) : (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
              className="h-full min-h-[420px] rounded-xl border border-dashed border-[#334155] bg-[#111827]/50 flex flex-col items-center justify-center p-10 text-center gap-5"
            >
              <div className="relative">
                <div className="absolute inset-0 rounded-full bg-[#8B5CF6]/10 blur-xl scale-150" />
                <div className="relative flex h-16 w-16 items-center justify-center rounded-full bg-[#111827] border border-[#334155]">
                  <Bot className="h-8 w-8 text-[#8B5CF6]" />
                </div>
              </div>
              <div className="space-y-2">
                <h3 className="text-lg font-semibold text-[#F8FAFC]">Content Analyzer</h3>
                <p className="text-sm text-muted-foreground max-w-sm">
                  Paste content on the left and click <span className="text-[#F8FAFC] font-medium">Analyze</span> to evaluate it for AI signatures.
                </p>
              </div>
            </motion.div>
          )}
        </div>
      </div>

      {/* History Table */}
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5, delay: 0.3 }}>
        <AIDetectionHistory refreshKey={historyRefreshKey} />
      </motion.div>
    </div>
  );
}
