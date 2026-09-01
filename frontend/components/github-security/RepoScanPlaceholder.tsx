'use client';

import { ShieldCheck, Search } from "lucide-react";
import { motion } from "framer-motion";

function GithubIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
    </svg>
  );
}

export function RepoScanPlaceholder() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="h-full min-h-[420px] rounded-xl border border-dashed border-[#334155] bg-[#111827]/50 flex flex-col items-center justify-center p-10 text-center gap-5"
    >
      <div className="relative">
        <div className="absolute inset-0 rounded-full bg-[#2563EB]/10 blur-xl scale-150" />
        <div className="relative flex h-16 w-16 items-center justify-center rounded-full bg-[#111827] border border-[#334155]">
          <GithubIcon className="h-8 w-8 text-[#2563EB]" />
        </div>
      </div>
      <div className="space-y-2">
        <h3 className="text-lg font-semibold text-[#F8FAFC]">GitHub Security Scanner</h3>
        <p className="text-sm text-muted-foreground max-w-sm">
          Enter a public GitHub repository URL and click <span className="text-[#F8FAFC] font-medium">Scan</span> to
          detect exposed secrets, credential files, and dependency manifests.
        </p>
      </div>
      <div className="grid grid-cols-3 gap-3 mt-2 w-full max-w-sm">
        {[
          { icon: ShieldCheck, label: "Secret Detection", color: "text-red-400" },
          { icon: Search,      label: "File Analysis",    color: "text-orange-400" },
          { icon: GithubIcon,  label: "Repo Insights",    color: "text-purple-400" },
        ].map(({ icon: Icon, label, color }) => (
          <div key={label} className="flex flex-col items-center gap-2 p-3 rounded-lg bg-[#020817] border border-[#334155]/50">
            <Icon className={`h-5 w-5 ${color}`} />
            <span className="text-xs text-muted-foreground text-center">{label}</span>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
