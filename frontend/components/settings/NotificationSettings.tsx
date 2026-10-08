'use client';

import { useState, useEffect } from "react";
import { Bell, Mail, Webhook, Check, Save } from "lucide-react";

export function NotificationSettings() {
  const [criticalAlerts, setCriticalAlerts] = useState(true);
  const [weeklyDigest, setWeeklyDigest] = useState(true);
  const [webhookUrl, setWebhookUrl] = useState("https://hooks.slack.com/services/SecureVision/AlertsChannel");
  const [savedMsg, setSavedMsg] = useState<string | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const storedCritical = localStorage.getItem("sv_critical_alerts");
      const storedWeekly = localStorage.getItem("sv_weekly_digest");
      const storedWebhook = localStorage.getItem("sv_webhook_url");
      if (storedCritical !== null) setCriticalAlerts(storedCritical === "true");
      if (storedWeekly !== null) setWeeklyDigest(storedWeekly === "true");
      if (storedWebhook !== null) setWebhookUrl(storedWebhook);
    }
  }, []);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    if (typeof window !== "undefined") {
      localStorage.setItem("sv_critical_alerts", String(criticalAlerts));
      localStorage.setItem("sv_weekly_digest", String(weeklyDigest));
      localStorage.setItem("sv_webhook_url", webhookUrl);
    }
    setSavedMsg("Notification preferences updated successfully!");
    setTimeout(() => setSavedMsg(null), 3000);
  };

  return (
    <div className="rounded-xl border border-[#334155] bg-[#111827]/80 p-6 backdrop-blur-md space-y-5 shadow-xl">
      <div className="space-y-1">
        <h4 className="text-base font-bold text-[#F8FAFC] flex items-center gap-2">
          <Bell className="w-4 h-4 text-[#8B5CF6]" />
          Security Notifications & Webhooks
        </h4>
        <p className="text-xs text-muted-foreground">Configure automated email digests and real-time webhook incident alerts.</p>
      </div>

      <form onSubmit={handleSave} className="space-y-4 text-xs">
        {/* Critical Alerts Toggle */}
        <div className="flex items-center justify-between p-3.5 rounded-lg bg-[#0F172A] border border-[#334155]">
          <div className="space-y-0.5">
            <div className="font-semibold text-[#F8FAFC] flex items-center gap-1.5">
              <Mail className="w-3.5 h-3.5 text-red-400" /> Critical Incident Email Alerts
            </div>
            <div className="text-[11px] text-muted-foreground">Receive instant email alerts whenever a Critical zero-day or secret is detected.</div>
          </div>
          <input
            type="checkbox"
            checked={criticalAlerts}
            onChange={(e) => setCriticalAlerts(e.target.checked)}
            className="w-4 h-4 accent-[#8B5CF6] cursor-pointer"
          />
        </div>

        {/* Weekly Digest Toggle */}
        <div className="flex items-center justify-between p-3.5 rounded-lg bg-[#0F172A] border border-[#334155]">
          <div className="space-y-0.5">
            <div className="font-semibold text-[#F8FAFC] flex items-center gap-1.5">
              <Mail className="w-3.5 h-3.5 text-purple-400" /> Weekly Executive Summary Digest
            </div>
            <div className="text-[11px] text-muted-foreground">Receive a weekly PDF audit digest detailing overall security posture trends.</div>
          </div>
          <input
            type="checkbox"
            checked={weeklyDigest}
            onChange={(e) => setWeeklyDigest(e.target.checked)}
            className="w-4 h-4 accent-[#8B5CF6] cursor-pointer"
          />
        </div>

        {/* Webhook URL */}
        <div className="space-y-1.5">
          <label className="font-semibold text-[#94A3B8] uppercase tracking-wider text-[11px] flex items-center gap-1.5">
            <Webhook className="w-3.5 h-3.5 text-[#8B5CF6]" /> Webhook Endpoint (Slack / Microsoft Teams / SIEM)
          </label>
          <input
            type="url"
            value={webhookUrl}
            onChange={(e) => setWebhookUrl(e.target.value)}
            placeholder="https://your-webhook-endpoint.com/alerts"
            className="w-full h-10 px-3 text-xs bg-[#0F172A] border border-[#334155] rounded-lg text-[#F8FAFC] focus:outline-none focus:border-[#8B5CF6]"
          />
          <p className="text-[11px] text-muted-foreground">HTTP POST JSON payloads will be dispatched when high severity findings trigger.</p>
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
