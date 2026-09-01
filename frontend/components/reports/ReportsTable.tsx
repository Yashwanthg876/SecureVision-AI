'use client';

import { useState } from "react";
import { Search, FileText, Download, FileCode, FileSpreadsheet, ShieldAlert, CheckCircle2, AlertTriangle, Info } from "lucide-react";
import { ReportItem } from "@/types/reports";
import { reportsService } from "@/lib/services/reports.service";

interface ReportsTableProps {
  reports: ReportItem[];
  loading?: boolean;
}

export function ReportsTable({ reports, loading }: ReportsTableProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedRisk, setSelectedRisk] = useState("ALL");

  const filteredReports = reports.filter((report) => {
    if (selectedRisk !== "ALL" && report.risk_level.toUpperCase() !== selectedRisk.toUpperCase()) {
      return false;
    }
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const matchTitle = report.title.toLowerCase().includes(q);
      const matchDomain = report.target_domain.toLowerCase().includes(q);
      const matchType = report.report_type.toLowerCase().includes(q);
      if (!matchTitle && !matchDomain && !matchType) return false;
    }
    return true;
  });

  const getRiskBadge = (risk: string) => {
    const r = risk.toUpperCase();
    if (r === "HEALTHY" || r === "LOW") {
      return <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-[11px] font-bold bg-[#10B981]/20 text-[#10B981] border border-[#10B981]/40"><CheckCircle2 className="w-3 h-3" /> Healthy</span>;
    }
    if (r === "MEDIUM") {
      return <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-[11px] font-bold bg-[#EAB308]/20 text-[#EAB308] border border-[#EAB308]/40"><Info className="w-3 h-3" /> Medium</span>;
    }
    if (r === "HIGH") {
      return <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-[11px] font-bold bg-[#F97316]/20 text-[#F97316] border border-[#F97316]/40"><AlertTriangle className="w-3 h-3" /> High Risk</span>;
    }
    return <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-[11px] font-bold bg-[#EF4444]/20 text-[#EF4444] border border-[#EF4444]/40"><ShieldAlert className="w-3 h-3" /> Critical</span>;
  };

  return (
    <div className="rounded-xl border border-[#334155] bg-[#111827]/80 p-6 backdrop-blur-md space-y-6 shadow-xl">
      {/* Header Controls */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h3 className="text-lg font-bold text-[#F8FAFC] flex items-center gap-2">
            <FileText className="w-5 h-5 text-[#8B5CF6]" />
            Generated Security Assessment Reports
          </h3>
          <p className="text-xs text-muted-foreground">
            View completed security scans and download executive, technical, or raw JSON reports.
          </p>
        </div>

        {/* Search & Filter */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search domain or type..."
              className="h-9 w-44 sm:w-56 px-3 pl-8 text-xs bg-[#0F172A] border border-[#334155] rounded-lg text-[#F8FAFC] placeholder:text-[#64748B] focus:outline-none focus:border-[#8B5CF6]"
            />
            <Search className="absolute left-2.5 top-2.5 w-3.5 h-3.5 text-[#64748B]" />
          </div>

          <select
            value={selectedRisk}
            onChange={(e) => setSelectedRisk(e.target.value)}
            className="h-9 px-3 text-xs bg-[#0F172A] border border-[#334155] rounded-lg text-[#F8FAFC] focus:outline-none focus:border-[#8B5CF6]"
          >
            <option value="ALL">All Risk Levels</option>
            <option value="HEALTHY">Healthy / Low</option>
            <option value="MEDIUM">Medium</option>
            <option value="HIGH">High</option>
            <option value="CRITICAL">Critical</option>
          </select>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto rounded-lg border border-[#334155]">
        <table className="w-full text-left text-xs">
          <thead className="bg-[#0F172A] text-[#94A3B8] uppercase font-bold text-[11px] tracking-wider border-b border-[#334155]">
            <tr>
              <th className="py-3 px-4">Report & Target Domain</th>
              <th className="py-3 px-4">Audit Type</th>
              <th className="py-3 px-4">Overall Score</th>
              <th className="py-3 px-4">Risk Level</th>
              <th className="py-3 px-4">Findings</th>
              <th className="py-3 px-4">Generated Date</th>
              <th className="py-3 px-4 text-right">Quick Export</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#1E293B]">
            {loading ? (
              <tr>
                <td colSpan={7} className="py-8 text-center text-muted-foreground">
                  Loading security reports...
                </td>
              </tr>
            ) : filteredReports.length === 0 ? (
              <tr>
                <td colSpan={7} className="py-8 text-center text-muted-foreground">
                  No reports matching filter criteria.
                </td>
              </tr>
            ) : (
              filteredReports.map((report) => (
                <tr key={report.id} className="hover:bg-[#1E293B]/40 transition-colors group">
                  <td className="py-3.5 px-4 font-semibold text-[#F8FAFC]">
                    <div className="space-y-0.5">
                      <div className="text-sm font-bold text-[#F8FAFC] group-hover:text-purple-300 transition-colors">
                        {report.target_domain}
                      </div>
                      <div className="text-[11px] font-normal text-muted-foreground">
                        {report.title}
                      </div>
                    </div>
                  </td>
                  <td className="py-3.5 px-4 text-[#E2E8F0] font-medium">
                    <span className="px-2 py-0.5 rounded bg-[#1E293B] text-[#94A3B8] border border-[#334155] text-[11px]">
                      {report.report_type}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 font-bold">
                    <span className={report.overall_score >= 80 ? 'text-emerald-400' : report.overall_score >= 60 ? 'text-yellow-400' : 'text-red-400'}>
                      {report.overall_score} / 100
                    </span>
                  </td>
                  <td className="py-3.5 px-4">
                    {getRiskBadge(report.risk_level)}
                  </td>
                  <td className="py-3.5 px-4 font-medium text-[#F8FAFC]">
                    {report.total_findings} vulnerabilities
                  </td>
                  <td className="py-3.5 px-4 text-muted-foreground text-[11px]">
                    {new Date(report.created_at).toLocaleDateString()}
                  </td>
                  <td className="py-3.5 px-4 text-right">
                    <div className="flex items-center justify-end gap-1.5">
                      <button
                        type="button"
                        onClick={() => reportsService.downloadReportFile(report.id, "pdf")}
                        title="Download PDF Executive Report"
                        className="flex items-center gap-1 px-2.5 py-1 rounded bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/30 text-[11px] font-semibold transition-colors"
                      >
                        <Download className="w-3 h-3" /> PDF
                      </button>
                      <button
                        type="button"
                        onClick={() => reportsService.downloadReportFile(report.id, "csv")}
                        title="Export CSV Data"
                        className="flex items-center gap-1 px-2.5 py-1 rounded bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-[11px] font-semibold transition-colors"
                      >
                        <FileSpreadsheet className="w-3 h-3" /> CSV
                      </button>
                      <button
                        type="button"
                        onClick={() => reportsService.downloadReportFile(report.id, "json")}
                        title="Export JSON Payload"
                        className="flex items-center gap-1 px-2.5 py-1 rounded bg-blue-500/10 hover:bg-blue-500/20 text-blue-400 border border-blue-500/30 text-[11px] font-semibold transition-colors"
                      >
                        <FileCode className="w-3 h-3" /> JSON
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
