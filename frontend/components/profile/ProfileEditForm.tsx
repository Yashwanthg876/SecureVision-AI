'use client';

import { useState } from "react";
import { User, Mail, Building, Save, Check, Loader2 } from "lucide-react";

interface ProfileEditFormProps {
  initialUser: {
    fullName: string;
    email: string;
    organization: string;
  };
  onUpdate: (updated: { fullName: string; email: string; organization: string }) => void;
}

export function ProfileEditForm({ initialUser, onUpdate }: ProfileEditFormProps) {
  const [fullName, setFullName] = useState(initialUser.fullName);
  const [email, setEmail] = useState(initialUser.email);
  const [organization, setOrganization] = useState(initialUser.organization);
  const [loading, setLoading] = useState(false);
  const [savedMsg, setSavedMsg] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setSavedMsg(null);

    setTimeout(() => {
      onUpdate({ fullName, email, organization });
      setLoading(false);
      setSavedMsg("Profile information updated successfully!");
      setTimeout(() => setSavedMsg(null), 3000);
    }, 600);
  };

  return (
    <div className="rounded-xl border border-[#334155] bg-[#111827]/80 p-6 backdrop-blur-md space-y-5 shadow-xl">
      <div className="space-y-1">
        <h4 className="text-base font-bold text-[#F8FAFC]">Personal Information</h4>
        <p className="text-xs text-muted-foreground">Update your personal account details and organization info.</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4 text-xs">
        <div className="grid gap-4 sm:grid-cols-2">
          {/* Full Name */}
          <div className="space-y-1.5">
            <label className="font-semibold text-[#94A3B8] uppercase tracking-wider text-[11px] flex items-center gap-1.5">
              <User className="w-3.5 h-3.5 text-[#8B5CF6]" /> Full Name
            </label>
            <input
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              required
              className="w-full h-10 px-3 text-xs bg-[#0F172A] border border-[#334155] rounded-lg text-[#F8FAFC] focus:outline-none focus:border-[#8B5CF6]"
            />
          </div>

          {/* Email */}
          <div className="space-y-1.5">
            <label className="font-semibold text-[#94A3B8] uppercase tracking-wider text-[11px] flex items-center gap-1.5">
              <Mail className="w-3.5 h-3.5 text-[#8B5CF6]" /> Email Address
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full h-10 px-3 text-xs bg-[#0F172A] border border-[#334155] rounded-lg text-[#F8FAFC] focus:outline-none focus:border-[#8B5CF6]"
            />
          </div>
        </div>

        {/* Organization */}
        <div className="space-y-1.5">
          <label className="font-semibold text-[#94A3B8] uppercase tracking-wider text-[11px] flex items-center gap-1.5">
            <Building className="w-3.5 h-3.5 text-[#8B5CF6]" /> Organization / Team Name
          </label>
          <input
            type="text"
            value={organization}
            onChange={(e) => setOrganization(e.target.value)}
            required
            className="w-full h-10 px-3 text-xs bg-[#0F172A] border border-[#334155] rounded-lg text-[#F8FAFC] focus:outline-none focus:border-[#8B5CF6]"
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
            disabled={loading}
            className="px-5 py-2 text-xs font-semibold rounded-lg bg-gradient-to-r from-[#8B5CF6] to-[#6D28D9] text-white hover:from-[#7C3AED] hover:to-[#5B21B6] transition-all disabled:opacity-50 flex items-center gap-2 shadow-lg shadow-purple-900/30"
          >
            {loading ? (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin" /> Saving...
              </>
            ) : (
              <>
                <Save className="w-3.5 h-3.5" /> Save Changes
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
