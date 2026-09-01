'use client';

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ShieldAlert, AlertTriangle, Info, CheckCircle2, Copy, Check, ExternalLink, Filter, Search, X, Globe, Eye } from "lucide-react";
import { ThreatIOC } from "@/types/threat-intel";

interface ThreatFeedTableProps {
  items: ThreatIOC[];
  loading?: boolean;
  onRefresh?: () => void;
}

export function ThreatFeedTable({ items, loading }: ThreatFeedTableProps) {
  const [selectedSeverity, setSelectedSeverity] = useState<string>("ALL");
  const [selectedType, setSelectedType] = useState<string>("ALL");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [activeItem, setActiveItem] = useState<ThreatIOC | null>(null);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  // Filtering
  const filteredItems = items.filter((item) => {
    if (selectedSeverity !== "ALL" && item.severity.toUpperCase() !== selectedSeverity) {
      return false;
    }
    if (selectedType !== "ALL" && item.ioc_type.toLowerCase() !== selectedType.toLowerCase()) {
      return false;
    }
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const matchesValue = item.ioc_value.toLowerCase().includes(q);
      const matchesType = item.threat_type.toLowerCase().includes(q);
      const matchesSource = item.source.toLowerCase().includes(q);
      const matchesSector = item.target_sector.toLowerCase().includes(q);
      if (!matchesValue && !matchesType && !matchesSource && !matchesSector) {
        return false;
      }
    }
    return true;
  });

  const handleCopy = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const getSeverityBadge = (severity: string) => {
    switch (severity.toUpperCase()) {
      case "CRITICAL":
        return <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-bold bg-[#EF4444]/20 text-[#EF4444] border border-[#EF4444]/40"><ShieldAlert className="w-3 h-3" /> CRITICAL</span>;
      case "HIGH":
        return <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-bold bg-[#F97316]/20 text-[#F97316] border border-[#F97316]/40"><AlertTriangle className="w-3 h-3" /> HIGH</span>;
      case "MEDIUM":
        return <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-bold bg-[#EAB308]/20 text-[#EAB308] border border-[#EAB308]/40"><Info className="w-3 h-3" /> MEDIUM</span>;
      default:
        return <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-bold bg-[#3B82F6]/20 text-[#3B82F6] border border-[#3B82F6]/40"><CheckCircle2 className="w-3 h-3" /> LOW</span>;
    }
  };

  const getTypeBadge = (type: string) => {
    return (
      <span className="uppercase text-[10px] font-extrabold tracking-wider px-2 py-0.5 rounded bg-[#1E293B] text-[#94A3B8] border border-[#334155]">
        {type}
      </span>
    );
  };

  return (
    <div className="rounded-xl border border-[#334155] bg-[#111827]/80 p-6 backdrop-blur-md space-y-6 shadow-xl">
      {/* Header & Controls */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h3 className="text-lg font-bold text-[#F8FAFC] flex items-center gap-2">
            <Globe className="w-5 h-5 text-[#8B5CF6]" />
            Live Global Threat IOC Feed
          </h3>
          <p className="text-xs text-muted-foreground">
            Real-time feed of active Indicators of Compromise detected by SecureVision AI sensors & intelligence feeds.
          </p>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-3">
          {/* Search */}
          <div className="relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search feed..."
              className="h-9 w-44 sm:w-56 px-3 pl-8 text-xs bg-[#0F172A] border border-[#334155] rounded-lg text-[#F8FAFC] placeholder:text-[#64748B] focus:outline-none focus:border-[#8B5CF6]"
            />
            <Search className="absolute left-2.5 top-2.5 w-3.5 h-3.5 text-[#64748B]" />
          </div>

          {/* Severity filter */}
          <select
            value={selectedSeverity}
            onChange={(e) => setSelectedSeverity(e.target.value)}
            className="h-9 px-3 text-xs bg-[#0F172A] border border-[#334155] rounded-lg text-[#F8FAFC] focus:outline-none focus:border-[#8B5CF6]"
          >
            <option value="ALL">All Severities</option>
            <option value="CRITICAL">Critical</option>
            <option value="HIGH">High</option>
            <option value="MEDIUM">Medium</option>
            <option value="LOW">Low</option>
          </select>

          {/* Type filter */}
          <select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            className="h-9 px-3 text-xs bg-[#0F172A] border border-[#334155] rounded-lg text-[#F8FAFC] focus:outline-none focus:border-[#8B5CF6]"
          >
            <option value="ALL">All IOC Types</option>
            <option value="IP">IP Address</option>
            <option value="DOMAIN">Domain</option>
            <option value="HASH">Hash</option>
            <option value="URL">URL</option>
            <option value="CVE">CVE ID</option>
          </select>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto rounded-lg border border-[#334155]">
        <table className="w-full text-left text-xs">
          <thead className="bg-[#0F172A] text-[#94A3B8] uppercase font-bold text-[11px] tracking-wider border-b border-[#334155]">
            <tr>
              <th className="py-3 px-4">Indicator (IOC)</th>
              <th className="py-3 px-4">Threat Classification</th>
              <th className="py-3 px-4">Severity</th>
              <th className="py-3 px-4">Target Sector</th>
              <th className="py-3 px-4">Confidence</th>
              <th className="py-3 px-4">Source Feed</th>
              <th className="py-3 px-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#1E293B]">
            {loading ? (
              <tr>
                <td colSpan={7} className="py-8 text-center text-muted-foreground">
                  Loading live threat feed...
                </td>
              </tr>
            ) : filteredItems.length === 0 ? (
              <tr>
                <td colSpan={7} className="py-8 text-center text-muted-foreground">
                  No threat indicators matching your filter criteria.
                </td>
              </tr>
            ) : (
              filteredItems.map((item) => (
                <tr key={item.id} className="hover:bg-[#1E293B]/40 transition-colors group">
                  <td className="py-3 px-4 font-mono font-semibold text-[#F8FAFC]">
                    <div className="flex items-center gap-2">
                      {getTypeBadge(item.ioc_type)}
                      <span className="truncate max-w-[200px]" title={item.ioc_value}>
                        {item.ioc_value}
                      </span>
                    </div>
                  </td>
                  <td className="py-3 px-4 text-[#E2E8F0] font-medium">
                    {item.threat_type}
                  </td>
                  <td className="py-3 px-4">
                    {getSeverityBadge(item.severity)}
                  </td>
                  <td className="py-3 px-4 text-muted-foreground">
                    {item.target_sector}
                  </td>
                  <td className="py-3 px-4 font-semibold text-[#F8FAFC]">
                    {item.confidence_score}%
                  </td>
                  <td className="py-3 px-4 text-muted-foreground text-[11px]">
                    {item.source}
                  </td>
                  <td className="py-3 px-4 text-right space-x-1">
                    <button
                      type="button"
                      onClick={() => handleCopy(item.id, item.ioc_value)}
                      title="Copy IOC Value"
                      className="p-1.5 rounded hover:bg-[#334155] text-muted-foreground hover:text-white transition-colors"
                    >
                      {copiedId === item.id ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                    </button>
                    <button
                      type="button"
                      onClick={() => setActiveItem(item)}
                      title="Inspect Threat Details"
                      className="p-1.5 rounded hover:bg-[#334155] text-purple-400 hover:text-purple-300 transition-colors"
                    >
                      <Eye className="w-3.5 h-3.5" />
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Detail Modal */}
      <AnimatePresence>
        {activeItem && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="relative w-full max-w-2xl rounded-xl border border-[#334155] bg-[#0F172A] p-6 space-y-5 shadow-2xl"
            >
              <div className="flex items-center justify-between border-b border-[#1E293B] pb-4">
                <div className="flex items-center gap-3">
                  {getTypeBadge(activeItem.ioc_type)}
                  <h3 className="text-lg font-bold font-mono text-[#F8FAFC]">{activeItem.ioc_value}</h3>
                  {getSeverityBadge(activeItem.severity)}
                </div>
                <button
                  onClick={() => setActiveItem(null)}
                  className="p-1 rounded-lg hover:bg-[#1E293B] text-muted-foreground hover:text-white transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="grid grid-cols-2 gap-4 text-xs bg-[#1E293B]/40 p-4 rounded-lg border border-[#334155]">
                <div>
                  <span className="text-muted-foreground uppercase text-[10px] font-bold tracking-wider block">Threat Classification</span>
                  <span className="text-[#F8FAFC] font-semibold text-sm">{activeItem.threat_type}</span>
                </div>
                <div>
                  <span className="text-muted-foreground uppercase text-[10px] font-bold tracking-wider block">Target Sector</span>
                  <span className="text-[#F8FAFC] font-semibold text-sm">{activeItem.target_sector}</span>
                </div>
                <div>
                  <span className="text-muted-foreground uppercase text-[10px] font-bold tracking-wider block">Telemetry Source</span>
                  <span className="text-[#F8FAFC] font-semibold">{activeItem.source}</span>
                </div>
                <div>
                  <span className="text-muted-foreground uppercase text-[10px] font-bold tracking-wider block">Confidence Rating</span>
                  <span className="text-emerald-400 font-bold">{activeItem.confidence_score}%</span>
                </div>
              </div>

              <div className="space-y-2 text-xs">
                <h4 className="font-semibold text-[#94A3B8] uppercase tracking-wider text-[11px]">Description & Attack Vector</h4>
                <p className="text-[#E2E8F0] leading-relaxed bg-[#1E293B] p-3.5 rounded border border-[#334155]">
                  {activeItem.description || "No description provided."}
                </p>
              </div>

              <div className="space-y-2 text-xs">
                <h4 className="font-semibold text-emerald-400 uppercase tracking-wider text-[11px]">Remediation Protocol</h4>
                <p className="text-[#CBD5E1] bg-emerald-950/20 border border-emerald-500/20 p-3.5 rounded leading-relaxed">
                  {activeItem.recommended_action || "Block traffic at perimeter."}
                </p>
              </div>

              <div className="flex justify-end pt-2">
                <button
                  type="button"
                  onClick={() => setActiveItem(null)}
                  className="px-4 py-2 text-xs font-semibold rounded-lg bg-[#1E293B] hover:bg-[#334155] text-white transition-colors"
                >
                  Close Detail
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}
