'use client';

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FileText, X, Download, FileCode, FileSpreadsheet, Check, Loader2 } from "lucide-react";
import { ReportItem } from "@/types/reports";
import { reportsService } from "@/lib/services/reports.service";

interface ReportGeneratorModalProps {
  isOpen: boolean;
  onClose: () => void;
  reportsList: ReportItem[];
  onReportGenerated?: () => void;
}

export function ReportGeneratorModal({ isOpen, onClose, reportsList, onReportGenerated }: ReportGeneratorModalProps) {
  const [selectedAssessmentId, setSelectedAssessmentId] = useState<string>(reportsList[0]?.id || "demo-assessment-01");
  const [reportType, setReportType] = useState<string>("Executive Summary");
  const [formatType, setFormatType] = useState<"pdf" | "csv" | "json">("pdf");
  const [loading, setLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleGenerate = async () => {
    setLoading(true);
    setSuccessMsg(null);
    try {
      const selectedReport = reportsList.find(r => r.id === selectedAssessmentId);
      const res = await reportsService.generateReport({
        assessment_id: selectedAssessmentId,
        target_domain: selectedReport?.target_domain || "api.securevision.ai",
        report_type: reportType,
        format_type: formatType,
      });

      // Trigger file download
      reportsService.downloadReportFile(selectedAssessmentId, formatType);
      setSuccessMsg(`Report generated successfully! Exporting ${formatType.toUpperCase()} file...`);

      if (onReportGenerated) {
        onReportGenerated();
      }

      setTimeout(() => {
        setSuccessMsg(null);
        onClose();
      }, 1500);
    } catch (err: any) {
      console.error("Failed to generate report", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="relative w-full max-w-lg rounded-xl border border-[#334155] bg-[#0F172A] p-6 space-y-6 shadow-2xl"
        >
          {/* Header */}
          <div className="flex items-center justify-between border-b border-[#1E293B] pb-4">
            <div className="flex items-center gap-2.5">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#8B5CF6]/10 border border-[#8B5CF6]/30 text-[#8B5CF6]">
                <FileText className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-[#F8FAFC]">Export Security Report</h3>
                <p className="text-xs text-muted-foreground">Customize parameters and download report files</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-1 rounded-lg hover:bg-[#1E293B] text-muted-foreground hover:text-white transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Form */}
          <div className="space-y-4 text-xs">
            {/* Target Assessment */}
            <div className="space-y-1.5">
              <label className="font-semibold text-[#94A3B8] uppercase tracking-wider text-[11px]">
                Target Assessment Domain
              </label>
              <select
                value={selectedAssessmentId}
                onChange={(e) => setSelectedAssessmentId(e.target.value)}
                className="w-full h-10 px-3 text-xs bg-[#1E293B] border border-[#334155] rounded-lg text-[#F8FAFC] focus:outline-none focus:border-[#8B5CF6]"
              >
                {reportsList.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.target_domain} (Score: {r.overall_score}/100 - {r.risk_level})
                  </option>
                ))}
              </select>
            </div>

            {/* Report Type */}
            <div className="space-y-1.5">
              <label className="font-semibold text-[#94A3B8] uppercase tracking-wider text-[11px]">
                Report Classification
              </label>
              <div className="grid grid-cols-3 gap-2">
                {[
                  { label: "Executive Summary", desc: "High-level overview" },
                  { label: "Technical Audit", desc: "Detailed findings" },
                  { label: "OWASP Top 10", desc: "Compliance Framework" },
                ].map((type) => (
                  <button
                    key={type.label}
                    type="button"
                    onClick={() => setReportType(type.label)}
                    className={`p-2.5 rounded-lg border text-left transition-all ${
                      reportType === type.label
                        ? "bg-[#8B5CF6]/15 border-[#8B5CF6] text-white"
                        : "bg-[#1E293B]/60 border-[#334155] text-muted-foreground hover:text-white hover:bg-[#1E293B]"
                    }`}
                  >
                    <div className="font-semibold text-[11px]">{type.label}</div>
                    <div className="text-[10px] opacity-70 mt-0.5">{type.desc}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Export Format */}
            <div className="space-y-1.5">
              <label className="font-semibold text-[#94A3B8] uppercase tracking-wider text-[11px]">
                Export File Format
              </label>
              <div className="grid grid-cols-3 gap-2">
                {[
                  { id: "pdf", label: "PDF Document", icon: Download, color: "text-red-400" },
                  { id: "csv", label: "CSV Spreadsheet", icon: FileSpreadsheet, color: "text-emerald-400" },
                  { id: "json", label: "JSON Raw Data", icon: FileCode, color: "text-blue-400" },
                ].map((fmt) => {
                  const Icon = fmt.icon;
                  const isSelected = formatType === fmt.id;
                  return (
                    <button
                      key={fmt.id}
                      type="button"
                      onClick={() => setFormatType(fmt.id as any)}
                      className={`flex flex-col items-center justify-center p-3 rounded-lg border text-center transition-all ${
                        isSelected
                          ? "bg-[#8B5CF6]/20 border-[#8B5CF6] text-white"
                          : "bg-[#1E293B]/60 border-[#334155] text-muted-foreground hover:text-white hover:bg-[#1E293B]"
                      }`}
                    >
                      <Icon className={`w-5 h-5 mb-1 ${fmt.color}`} />
                      <span className="font-semibold text-[11px]">{fmt.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          </div>

          {successMsg && (
            <div className="p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs flex items-center gap-2">
              <Check className="w-4 h-4" /> {successMsg}
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex items-center justify-end gap-3 pt-2 border-t border-[#1E293B]">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-semibold rounded-lg bg-[#1E293B] hover:bg-[#334155] text-white transition-colors"
            >
              Cancel
            </button>
            <button
              type="button"
              onClick={handleGenerate}
              disabled={loading}
              className="px-5 py-2 text-xs font-semibold rounded-lg bg-gradient-to-r from-[#8B5CF6] to-[#6D28D9] text-white hover:from-[#7C3AED] hover:to-[#5B21B6] transition-all disabled:opacity-50 flex items-center gap-2 shadow-lg shadow-purple-900/30"
            >
              {loading ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin" /> Generating...
                </>
              ) : (
                <>
                  <Download className="w-3.5 h-3.5" /> Export Report ({formatType.toUpperCase()})
                </>
              )}
            </button>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
