'use client';

import { useState } from "react";
import { Lock, Key, ShieldCheck, Check, Loader2 } from "lucide-react";

export function SecuritySettingsForm() {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setSuccessMsg(null);

    if (newPassword.length < 8) {
      setErrorMsg("New password must be at least 8 characters long.");
      return;
    }

    if (newPassword !== confirmPassword) {
      setErrorMsg("New password and confirm password do not match.");
      return;
    }

    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setSuccessMsg("Security credentials updated successfully!");
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
      setTimeout(() => setSuccessMsg(null), 3000);
    }, 600);
  };

  return (
    <div className="rounded-xl border border-[#334155] bg-[#111827]/80 p-6 backdrop-blur-md space-y-5 shadow-xl">
      <div className="space-y-1">
        <h4 className="text-base font-bold text-[#F8FAFC] flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-[#8B5CF6]" />
          Account Security & Password
        </h4>
        <p className="text-xs text-muted-foreground">Change your password and manage login authentication preferences.</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4 text-xs">
        {/* Current Password */}
        <div className="space-y-1.5">
          <label className="font-semibold text-[#94A3B8] uppercase tracking-wider text-[11px] flex items-center gap-1.5">
            <Key className="w-3.5 h-3.5 text-[#8B5CF6]" /> Current Password
          </label>
          <input
            type="password"
            value={currentPassword}
            onChange={(e) => setCurrentPassword(e.target.value)}
            required
            placeholder="••••••••••••"
            className="w-full h-10 px-3 text-xs bg-[#0F172A] border border-[#334155] rounded-lg text-[#F8FAFC] focus:outline-none focus:border-[#8B5CF6]"
          />
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          {/* New Password */}
          <div className="space-y-1.5">
            <label className="font-semibold text-[#94A3B8] uppercase tracking-wider text-[11px] flex items-center gap-1.5">
              <Lock className="w-3.5 h-3.5 text-[#8B5CF6]" /> New Password
            </label>
            <input
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
              placeholder="••••••••••••"
              className="w-full h-10 px-3 text-xs bg-[#0F172A] border border-[#334155] rounded-lg text-[#F8FAFC] focus:outline-none focus:border-[#8B5CF6]"
            />
          </div>

          {/* Confirm Password */}
          <div className="space-y-1.5">
            <label className="font-semibold text-[#94A3B8] uppercase tracking-wider text-[11px] flex items-center gap-1.5">
              <Lock className="w-3.5 h-3.5 text-[#8B5CF6]" /> Confirm New Password
            </label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              placeholder="••••••••••••"
              className="w-full h-10 px-3 text-xs bg-[#0F172A] border border-[#334155] rounded-lg text-[#F8FAFC] focus:outline-none focus:border-[#8B5CF6]"
            />
          </div>
        </div>

        {errorMsg && (
          <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 text-xs">
            ⚠️ {errorMsg}
          </div>
        )}

        {successMsg && (
          <div className="p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs flex items-center gap-2">
            <Check className="w-4 h-4" /> {successMsg}
          </div>
        )}

        <div className="flex justify-end pt-2">
          <button
            type="submit"
            disabled={loading}
            className="px-5 py-2 text-xs font-semibold rounded-lg bg-[#1E293B] hover:bg-[#334155] text-white transition-colors disabled:opacity-50 flex items-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin" /> Updating...
              </>
            ) : (
              "Update Password"
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
