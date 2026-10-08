'use client';

import { useState, useEffect } from "react";
import { Key, Eye, EyeOff, Check, Save, GitBranch, Bot } from "lucide-react";

export function APIKeysSettings() {
  const [geminiKey, setGeminiKey] = useState("");
  const [githubToken, setGithubToken] = useState("");
  const [showGemini, setShowGemini] = useState(false);
  const [showGithub, setShowGithub] = useState(false);
  const [savedMsg, setSavedMsg] = useState<string | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const storedGemini = localStorage.getItem("sv_gemini_key");
      const storedGithub = localStorage.getItem("sv_github_token");
      if (storedGemini) setGeminiKey(storedGemini);
      if (storedGithub) setGithubToken(storedGithub);
    }
  }, []);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    if (typeof window !== "undefined") {
      localStorage.setItem("sv_gemini_key", geminiKey);
      localStorage.setItem("sv_github_token", githubToken);
    }
    setSavedMsg("API key credentials saved successfully!");
    setTimeout(() => setSavedMsg(null), 3000);
  };

  return (
    <div className="rounded-xl border border-[#334155] bg-[#111827]/80 p-6 backdrop-blur-md space-y-5 shadow-xl">
      <div className="space-y-1">
        <h4 className="text-base font-bold text-[#F8FAFC] flex items-center gap-2">
          <Key className="w-4 h-4 text-[#8B5CF6]" />
          API Keys & Integration Credentials
        </h4>
        <p className="text-xs text-muted-foreground">Configure external API keys for Generative AI Copilot and GitHub repository access.</p>
      </div>

      <form onSubmit={handleSave} className="space-y-4 text-xs">
        {/* Gemini AI Key */}
        <div className="space-y-1.5">
          <label className="font-semibold text-[#94A3B8] uppercase tracking-wider text-[11px] flex items-center gap-1.5">
            <Bot className="w-3.5 h-3.5 text-[#8B5CF6]" /> Gemini AI Copilot Key
          </label>
          <div className="relative">
            <input
              type={showGemini ? "text" : "password"}
              value={geminiKey}
              onChange={(e) => setGeminiKey(e.target.value)}
              placeholder="Enter Gemini API key"
              className="w-full h-10 px-3 pr-10 text-xs bg-[#0F172A] border border-[#334155] rounded-lg text-[#F8FAFC] focus:outline-none focus:border-[#8B5CF6]"
            />
            <button
              type="button"
              onClick={() => setShowGemini(!showGemini)}
              className="absolute right-3 top-2.5 text-muted-foreground hover:text-white"
            >
              {showGemini ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            </button>
          </div>
          <p className="text-[11px] text-muted-foreground">Powers structured AI Copilot executive summaries and developer remediation advice.</p>
        </div>

        {/* GitHub Token */}
        <div className="space-y-1.5">
          <label className="font-semibold text-[#94A3B8] uppercase tracking-wider text-[11px] flex items-center gap-1.5">
            <GitBranch className="w-3.5 h-3.5 text-[#8B5CF6]" /> GitHub Personal Access Token (PAT)
          </label>
          <div className="relative">
            <input
              type={showGithub ? "text" : "password"}
              value={githubToken}
              onChange={(e) => setGithubToken(e.target.value)}
              placeholder="ghp_xxxxxxxxxxxxxxxxxxxx"
              className="w-full h-10 px-3 pr-10 text-xs bg-[#0F172A] border border-[#334155] rounded-lg text-[#F8FAFC] focus:outline-none focus:border-[#8B5CF6]"
            />
            <button
              type="button"
              onClick={() => setShowGithub(!showGithub)}
              className="absolute right-3 top-2.5 text-muted-foreground hover:text-white"
            >
              {showGithub ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            </button>
          </div>
          <p className="text-[11px] text-muted-foreground">Required for scanning private repositories and accessing higher API rate limits.</p>
        </div>
        
        {savedMsg && (
          <div className="p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs flex items-center gap-2">
            <Check className="w-4 h-4" /> {savedMsg}
          </div>
        )}

        <div className="flex justify-end pt-2">
          <button
            type="submit"
            className="px-5 py-2 text-xs font-semibold rounded-lg bg-gradient-to-r from-[#8B5CF6] to-[#6D28D9] text-white hover:from-[#7C3AED] hover:to-[#5B21B6] transition-all flex items-center gap-2 shadow-lg shadow-purple-900/30"
          >
            <Save className="w-3.5 h-3.5" /> Save API Credentials
          </button>
        </div>
      </form>
    </div>
  );
}
