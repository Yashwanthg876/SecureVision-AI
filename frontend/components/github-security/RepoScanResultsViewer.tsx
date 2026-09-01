'use client';

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  ShieldCheck, AlertTriangle, XCircle, CheckCircle2,
  FileWarning, Package, Key, Star, GitFork, Bug
} from "lucide-react";
import { motion } from "framer-motion";

function GithubIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
    </svg>
  );
}

type Tab = "overview" | "secrets" | "risky-files" | "dependencies";

const SEVERITY_CLASSES: Record<string, string> = {
  Critical: "bg-red-500/10 text-red-400 border-red-500/20",
  High:     "bg-orange-500/10 text-orange-400 border-orange-500/20",
  Medium:   "bg-yellow-500/10 text-yellow-400 border-yellow-500/20",
  Low:      "bg-blue-500/10 text-blue-400 border-blue-500/20",
};

const SCORE_COLOR = (score: number) =>
  score >= 85 ? "text-green-400" :
  score >= 65 ? "text-yellow-400" :
  score >= 40 ? "text-orange-400" : "text-red-400";

const RISK_CLASS = (risk: string) =>
  risk === "Low" ? "bg-green-500/10 text-green-400" :
  risk === "Medium" ? "bg-yellow-500/10 text-yellow-400" :
  risk === "High" ? "bg-orange-500/10 text-orange-400" :
  "bg-red-500/10 text-red-400";

export function RepoScanResultsViewer({ data }: { data: any }) {
  const [activeTab, setActiveTab] = useState<Tab>("overview");
  if (!data) return null;

  const tabs: { id: Tab; label: string; count?: number }[] = [
    { id: "overview",     label: "Overview" },
    { id: "secrets",      label: "Secrets",       count: data.secrets_count },
    { id: "risky-files",  label: "Risky Files",   count: data.risky_files_count },
    { id: "dependencies", label: "Dependencies",  count: data.dependency_files_count },
  ];

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
      <Card className="bg-[#111827] border-[#334155] shadow-sm overflow-hidden">
        {/* ── Header ── */}
        <CardHeader className="pb-4 border-b border-[#334155]/50 flex flex-row items-start justify-between">
          <div>
            <CardTitle className="text-lg font-semibold text-[#F8FAFC] flex items-center gap-2">
              <GithubIcon className="h-5 w-5 text-[#2563EB]" />
              {data.owner}/{data.repo_name}
            </CardTitle>
            <CardDescription>
              Scanned {data.total_files_scanned} files · {(data.scan_duration_ms / 1000).toFixed(1)}s ·{" "}
              {new Date(data.created_at).toLocaleString()}
            </CardDescription>
          </div>
          <Badge className={`border-0 font-semibold ${RISK_CLASS(data.risk_level)}`}>
            {data.risk_level} Risk
          </Badge>
        </CardHeader>

        {/* ── Tabs ── */}
        <div className="flex border-b border-[#334155]/50 px-6">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`relative py-3 px-4 text-sm font-medium transition-colors flex items-center gap-2 ${
                activeTab === tab.id
                  ? "text-[#F8FAFC] border-b-2 border-[#2563EB]"
                  : "text-muted-foreground hover:text-[#F8FAFC]"
              }`}
            >
              {tab.label}
              {tab.count !== undefined && tab.count > 0 && (
                <span className={`text-xs rounded-full px-1.5 py-0.5 font-bold ${
                  tab.count > 0 && tab.id === "secrets" ? "bg-red-500/20 text-red-400" : "bg-[#334155] text-muted-foreground"
                }`}>
                  {tab.count}
                </span>
              )}
            </button>
          ))}
        </div>

        <CardContent className="pt-6 space-y-6">
          {/* ── Overview Tab ── */}
          {activeTab === "overview" && (
            <div className="space-y-6">
              {/* Score + Severity counts */}
              <div className="flex flex-wrap gap-6 items-center">
                <div>
                  <p className="text-xs text-muted-foreground mb-1">Security Score</p>
                  <span className={`text-5xl font-bold ${SCORE_COLOR(data.security_score)}`}>
                    {data.security_score}
                    <span className="text-2xl text-muted-foreground">/100</span>
                  </span>
                </div>
                <div className="flex flex-wrap gap-2">
                  <Badge className="bg-red-500/15 text-red-400 border-0 font-semibold">{data.critical_count} Critical</Badge>
                  <Badge className="bg-orange-500/15 text-orange-400 border-0 font-semibold">{data.high_count} High</Badge>
                  <Badge className="bg-yellow-500/15 text-yellow-400 border-0 font-semibold">{data.medium_count} Medium</Badge>
                  <Badge className="bg-blue-500/15 text-blue-400 border-0 font-semibold">{data.low_count} Low</Badge>
                </div>
              </div>

              {/* Stat grid */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                  { label: "Files Scanned", value: data.total_files_scanned, icon: ShieldCheck, color: "text-[#2563EB]" },
                  { label: "Secrets Found", value: data.secrets_count, icon: Key, color: data.secrets_count > 0 ? "text-red-400" : "text-green-400" },
                  { label: "Risky Files", value: data.risky_files_count, icon: FileWarning, color: data.risky_files_count > 0 ? "text-orange-400" : "text-green-400" },
                  { label: "Dep. Manifests", value: data.dependency_files_count, icon: Package, color: "text-purple-400" },
                ].map((stat) => (
                  <div key={stat.label} className="bg-[#020817] border border-[#334155] rounded-lg p-4 space-y-2">
                    <stat.icon className={`h-5 w-5 ${stat.color}`} />
                    <p className="text-2xl font-bold text-[#F8FAFC]">{stat.value}</p>
                    <p className="text-xs text-muted-foreground">{stat.label}</p>
                  </div>
                ))}
              </div>

              {/* Repo Info */}
              {data.repo_info && (
                <div className="bg-[#020817] border border-[#334155] rounded-lg p-4 space-y-3">
                  <h4 className="text-sm font-semibold text-[#F8FAFC] flex items-center gap-2">
                    <GithubIcon className="h-4 w-4 text-[#2563EB]" />
                    Repository Info
                  </h4>
                  {data.repo_info.description && (
                    <p className="text-sm text-muted-foreground">{data.repo_info.description}</p>
                  )}
                  <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                    <span className="flex items-center gap-1"><Star className="h-4 w-4 text-yellow-400" />{data.repo_info.stars.toLocaleString()} stars</span>
                    <span className="flex items-center gap-1"><GitFork className="h-4 w-4" />{data.repo_info.forks.toLocaleString()} forks</span>
                    <span className="flex items-center gap-1"><Bug className="h-4 w-4" />{data.repo_info.open_issues} issues</span>
                    {data.repo_info.language && <Badge className="bg-[#334155] text-[#F8FAFC] border-0">{data.repo_info.language}</Badge>}
                    {data.repo_info.license && <Badge className="bg-[#334155]/50 text-muted-foreground border-0">{data.repo_info.license}</Badge>}
                  </div>
                  {data.repo_info.topics?.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      {data.repo_info.topics.map((t: string) => (
                        <Badge key={t} className="bg-[#2563EB]/10 text-[#2563EB] border-[#2563EB]/20 text-xs">{t}</Badge>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {/* ── Secrets Tab ── */}
          {activeTab === "secrets" && (
            <div className="space-y-3">
              {data.secret_findings?.length === 0 ? (
                <div className="flex flex-col items-center justify-center py-12 text-center gap-3">
                  <CheckCircle2 className="h-10 w-10 text-green-500" />
                  <p className="font-semibold text-[#F8FAFC]">No secrets detected</p>
                  <p className="text-sm text-muted-foreground">No credential patterns were found in scanned files.</p>
                </div>
              ) : (
                data.secret_findings.map((finding: any, i: number) => (
                  <div key={i} className="p-4 border border-[#334155] bg-[#020817] rounded-lg space-y-2">
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex items-center gap-2 font-medium text-[#F8FAFC] text-sm">
                        <XCircle className="h-4 w-4 text-red-400 shrink-0" />
                        {finding.pattern_name}
                      </div>
                      <Badge className={`border text-xs shrink-0 ${SEVERITY_CLASSES[finding.severity] ?? SEVERITY_CLASSES.Low}`}>
                        {finding.severity}
                      </Badge>
                    </div>
                    <p className="text-xs text-muted-foreground font-mono bg-[#111827] px-2 py-1 rounded">
                      📄 {finding.file_path}
                    </p>
                    <p className="text-xs text-muted-foreground">{finding.description}</p>
                    <div className="bg-[#111827] border border-blue-900/30 p-3 rounded text-xs text-blue-200">
                      <span className="font-semibold text-blue-400">Remediation: </span>
                      {finding.recommendation}
                    </div>
                  </div>
                ))
              )}
            </div>
          )}

          {/* ── Risky Files Tab ── */}
          {activeTab === "risky-files" && (
            <div className="space-y-3">
              {data.risky_files?.length === 0 ? (
                <div className="flex flex-col items-center justify-center py-12 text-center gap-3">
                  <CheckCircle2 className="h-10 w-10 text-green-500" />
                  <p className="font-semibold text-[#F8FAFC]">No risky filenames found</p>
                  <p className="text-sm text-muted-foreground">No sensitive file patterns detected in the repository.</p>
                </div>
              ) : (
                data.risky_files.map((file: any, i: number) => (
                  <div key={i} className="p-4 border border-[#334155] bg-[#020817] rounded-lg space-y-2">
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex items-center gap-2 font-medium text-[#F8FAFC] text-sm">
                        <AlertTriangle className="h-4 w-4 text-orange-400 shrink-0" />
                        {file.file_path.split("/").pop()}
                      </div>
                      <Badge className={`border text-xs shrink-0 ${SEVERITY_CLASSES[file.severity] ?? SEVERITY_CLASSES.Low}`}>
                        {file.severity}
                      </Badge>
                    </div>
                    <p className="text-xs text-muted-foreground font-mono bg-[#111827] px-2 py-1 rounded">
                      📄 {file.file_path}
                    </p>
                    <p className="text-xs text-muted-foreground">{file.risk_reason}</p>
                  </div>
                ))
              )}
            </div>
          )}

          {/* ── Dependencies Tab ── */}
          {activeTab === "dependencies" && (
            <div className="space-y-3">
              {data.dependency_findings?.length === 0 ? (
                <div className="flex flex-col items-center justify-center py-12 text-center gap-3">
                  <Package className="h-10 w-10 text-muted-foreground" />
                  <p className="font-semibold text-[#F8FAFC]">No dependency files detected</p>
                  <p className="text-sm text-muted-foreground">No known dependency manifests were found.</p>
                </div>
              ) : (
                data.dependency_findings.map((dep: any, i: number) => (
                  <div key={i} className="p-4 border border-[#334155] bg-[#020817] rounded-lg space-y-2">
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex items-center gap-2 font-medium text-[#F8FAFC] text-sm">
                        <Package className="h-4 w-4 text-purple-400 shrink-0" />
                        {dep.dependency_type.toUpperCase()} — {dep.file_path.split("/").pop()}
                      </div>
                      <Badge className="bg-purple-500/10 text-purple-400 border-purple-500/20 border text-xs">
                        {dep.dependency_type}
                      </Badge>
                    </div>
                    <p className="text-xs text-muted-foreground font-mono bg-[#111827] px-2 py-1 rounded">
                      📄 {dep.file_path}
                    </p>
                    <p className="text-xs text-muted-foreground">{dep.description}</p>
                    <div className="bg-[#111827] border border-blue-900/30 p-3 rounded text-xs text-blue-200">
                      <span className="font-semibold text-blue-400">Recommendation: </span>
                      {dep.recommendation}
                    </div>
                  </div>
                ))
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}
