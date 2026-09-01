'use client';

import { useState } from "react";
import { Sliders, Shield, Database, Check, Save } from "lucide-react";

export function ScanPreferencesSettings() {
  const [scanDepth, setScanDepth] = useState("deep");
  const [autoExportPdf, setAutoExportPdf] = useState(true);
  const [retentionDays, setRetentionDays] = useState("90");
  const [savedMsg, setSavedMsg] = useState<string | null>(null);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSavedMsg("Scan execution preferences saved successfully!");
    setTimeout(() => setSavedMsg(null), 3000);
  };

  return (
    <div className="rounded-xl border border-[#334155] bg-[#111827]/80 p-6 backdrop-blur-md space-y-5 shadow-xl">
      <div className="space-y-1">
        <h4 className="text-base font-bold text-[#F8FAFC] flex items-center gap-2">
          <Sliders className="w-4 h-4 text-[#8B5CF6]" />
          Platform Execution & Retention Settings
        </h4>
        <p className="text-xs text-muted-foreground">Adjust assessment engine behavior, report automation, and database retention policies.</p>
      </div>

      <form onSubmit={handleSave} className="space-y-4 text-xs">
        <div className="grid gap-4 sm:grid-cols-2">
          {/* Scan Depth */}
          <div className="space-y-1.5">
            <label className="font-semibold text-[#94A3B8] uppercase tracking-wider text-[11px] flex items-center gap-1.5">
              <Shield className="w-3.5 h-3.5 text-[#8B5CF6]" /> Assessment Depth Mode
            </label>
            <select
              value={scanDepth}
              onChange={(e) => setScanDepth(e.target.value)}
              className="w-full h-10 px-3 text-xs bg-[#0F172A] border border-[#334155] rounded-lg text-[#F8FAFC] focus:outline-none focus:border-[#8B5CF6]"
            >
              <option value="quick">Quick Heuristic Scan (SSL + Headers)</option>
              <option value="deep">Deep Comprehensive Audit (SSL + DNS + SHAP + AI)</option>
              <option value="paranoid">Strict Compliance Scan (Full Penetration Heuristics)</option>
            </select>
          </div>

          {/* Retention Period */}
          <div className="space-y-1.5">
            <label className="font-semibold text-[#94A3B8] uppercase tracking-wider text-[11px] flex items-center gap-1.5">
              <Database className="w-3.5 h-3.5 text-[#8B5CF6]" /> Audit Log Retention Policy
            </label>
            <select
              value={retentionDays}
              onChange={(e) => setRetentionDays(e.target.value)}
              className="w-full h-10 px-3 text-xs bg-[#0F172A] border border-[#334155] rounded-lg text-[#F8FAFC] focus:outline-none focus:border-[#8B5CF6]"
            >
              <option value="30">30 Days Retention</option>
              <option value="60">60 Days Retention</option>
              <option value="90">90 Days Retention (Recommended)</option>
              <option value="365">1 Year Retention (Compliance Default)</option>
            </select>
          </div>
        </div>

        {/* Auto Export Toggle */}
        <div className="flex items-center justify-between p-3.5 rounded-lg bg-[#0F172A] border border-[#334155]">
          <div className="space-y-0.5">
            <div className="font-semibold text-[#F8FAFC]">Auto-Generate PDF Executive Summary</div>
            <div className="text-[11px] text-muted-foreground">Automatically construct downloadable PDF report upon completion of any assessment scan.</div>
          </div>
          <input
            type="checkbox"
            checked={autoExportPdf}
            onChange={(e) => setAutoExportPdf(e.target.checked)}
            className="w-4 h-4 accent-[#8B5CF6] cursor-pointer"
          />
        </div>

        {savedMsg && (
          <div className="p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs flex items-center gap-2">
            <Check className="w-4 h-4" /> {savedMsg}
          </div>
        )}

        <div className="flex justify-end pt-2">
          <button
            type="submit"
            className="px-5 py-2 text-xs font-semibold rounded-lg bg-[#1E293B] hover:bg-[#334155] text-white transition-colors flex items-center gap-2"
          >
            <Save className="w-3.5 h-3.5" /> Save Preferences
          </button>
        </div>
      </form>
    </div>
  );
}
