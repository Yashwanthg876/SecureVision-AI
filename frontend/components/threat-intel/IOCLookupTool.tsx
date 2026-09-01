'use client';

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, ShieldAlert, CheckCircle2, AlertTriangle, Info, Copy, Check, Loader2, ArrowRight } from "lucide-react";
import { IOCLookupResult } from "@/types/threat-intel";
import { threatIntelService } from "@/lib/services/threat-intel.service";

interface IOCLookupToolProps {
  onLookupComplete?: (result: IOCLookupResult) => void;
}

export function IOCLookupTool({ onLookupComplete }: IOCLookupToolProps) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<IOCLookupResult | null>(null);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sampleQueries = [
    { label: "IP: 185.220.101.5", value: "185.220.101.5" },
    { label: "CVE: cve-2024-3094", value: "cve-2024-3094" },
    { label: "Domain: auth-verify.com", value: "auth-verify-security-login.com" },
    { label: "Clean IP: 8.8.8.8", value: "8.8.8.8" },
  ];

  const handleSearch = async (searchQuery?: string) => {
    const q = searchQuery || query;
    if (!q.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const res = await threatIntelService.lookupIOC(q.trim());
      setResult(res);
      if (onLookupComplete) {
        onLookupComplete(res);
      }
    } catch (err: any) {
      setError(err.message || "Failed to complete threat lookup.");
    } finally {
      setLoading(false);
    }
  };

  const copyToAction = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getSeverityBadge = (severity: string) => {
    switch (severity.toUpperCase()) {
      case "CRITICAL":
        return <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-bold bg-[#EF4444]/20 text-[#EF4444] border border-[#EF4444]/40"><ShieldAlert className="w-3.5 h-3.5" /> CRITICAL</span>;
      case "HIGH":
        return <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-bold bg-[#F97316]/20 text-[#F97316] border border-[#F97316]/40"><AlertTriangle className="w-3.5 h-3.5" /> HIGH</span>;
      case "MEDIUM":
        return <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-bold bg-[#EAB308]/20 text-[#EAB308] border border-[#EAB308]/40"><Info className="w-3.5 h-3.5" /> MEDIUM</span>;
      default:
        return <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-bold bg-[#10B981]/20 text-[#10B981] border border-[#10B981]/40"><CheckCircle2 className="w-3.5 h-3.5" /> CLEAN / LOW</span>;
    }
  };

  return (
    <div className="rounded-xl border border-[#334155] bg-[#111827]/80 p-6 backdrop-blur-md space-y-6 shadow-xl">
      <div className="space-y-1">
        <h3 className="text-lg font-bold text-[#F8FAFC] flex items-center gap-2">
          <Search className="w-5 h-5 text-[#8B5CF6]" />
          Instant Threat IOC Lookup
        </h3>
        <p className="text-xs text-muted-foreground">
          Query IP addresses, domains, file hashes, URLs, or CVE IDs against live threat telemetry.
        </p>
      </div>

      {/* Input Bar */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSearch();
        }}
        className="flex flex-col sm:flex-row gap-3"
      >
        <div className="relative flex-1">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g. 185.220.101.5, cve-2024-3094, auth-verify.com"
            className="w-full h-11 px-4 pl-10 text-sm bg-[#0F172A] border border-[#334155] rounded-lg text-[#F8FAFC] placeholder:text-[#64748B] focus:outline-none focus:border-[#8B5CF6] focus:ring-1 focus:ring-[#8B5CF6] transition-all"
          />
          <Search className="absolute left-3 top-3 w-5 h-5 text-[#64748B]" />
        </div>
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="h-11 px-6 text-sm font-semibold rounded-lg bg-gradient-to-r from-[#8B5CF6] to-[#6D28D9] text-white hover:from-[#7C3AED] hover:to-[#5B21B6] transition-all disabled:opacity-50 flex items-center justify-center gap-2 shadow-lg shadow-purple-900/30"
        >
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" /> Analyzing...
            </>
          ) : (
            <>
              Analyze IOC <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>
      </form>

      {/* Preset Quick Buttons */}
      <div className="flex flex-wrap items-center gap-2 text-xs">
        <span className="text-muted-foreground font-medium">Quick Test:</span>
        {sampleQueries.map((sample) => (
          <button
            key={sample.value}
            type="button"
            onClick={() => {
              setQuery(sample.value);
              handleSearch(sample.value);
            }}
            className="px-2.5 py-1 rounded-md bg-[#1E293B] hover:bg-[#334155] text-[#94A3B8] hover:text-[#F8FAFC] border border-[#334155] transition-colors"
          >
            {sample.label}
          </button>
        ))}
      </div>

      {error && (
        <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 text-xs">
          ⚠️ {error}
        </div>
      )}

      {/* Results Display */}
      <AnimatePresence>
        {result && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="rounded-lg border border-[#334155] bg-[#0F172A] p-5 space-y-4"
          >
            {/* Header Result */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-[#1E293B]">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-mono font-bold text-[#F8FAFC]">{result.query}</span>
                  {getSeverityBadge(result.risk_level)}
                </div>
                <p className="text-xs font-semibold text-purple-400">{result.verdict}</p>
              </div>

              {/* Reputation Gauge */}
              <div className="flex items-center gap-3 bg-[#1E293B] px-3.5 py-2 rounded-lg border border-[#334155]">
                <div className="text-right">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground block">
                    Reputation Score
                  </span>
                  <span className={`text-base font-bold ${result.reputation_score < 50 ? 'text-red-400' : 'text-emerald-400'}`}>
                    {result.reputation_score}/100
                  </span>
                </div>
              </div>
            </div>

            {/* Analysis Details */}
            <div className="space-y-2 text-xs">
              <h4 className="font-semibold text-[#94A3B8] uppercase tracking-wider text-[11px]">
                Threat Intelligence Summary
              </h4>
              <p className="text-[#E2E8F0] leading-relaxed bg-[#1E293B]/50 p-3 rounded border border-[#334155]/60">
                {result.analysis_details}
              </p>
            </div>

            {/* Recommended Action */}
            <div className="space-y-2 text-xs">
              <div className="flex items-center justify-between">
                <h4 className="font-semibold text-emerald-400 uppercase tracking-wider text-[11px] flex items-center gap-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5" /> Recommended Remediation Protocol
                </h4>
                <button
                  type="button"
                  onClick={() => copyToAction(result.recommended_action)}
                  className="flex items-center gap-1 text-[11px] text-muted-foreground hover:text-white transition-colors"
                >
                  {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                  {copied ? "Copied" : "Copy Protocol"}
                </button>
              </div>
              <p className="text-[#CBD5E1] bg-emerald-950/20 border border-emerald-500/20 p-3 rounded leading-relaxed">
                {result.recommended_action}
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
