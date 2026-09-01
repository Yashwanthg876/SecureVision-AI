'use client';

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search, Loader2, Lock } from "lucide-react";
import { motion } from "framer-motion";

function GithubIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
    </svg>
  );
}
import api from "@/lib/api";

interface RepoScanFormProps {
  onScanStart?: () => void;
  onScanSuccess?: (data: any) => void;
  onScanError?: (msg: string) => void;
  isScanning?: boolean;
}

export function RepoScanForm({ onScanStart, onScanSuccess, onScanError, isScanning = false }: RepoScanFormProps) {
  const [repoUrl, setRepoUrl] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = repoUrl.trim();
    if (!trimmed) {
      setError("Please enter a GitHub repository URL.");
      return;
    }
    if (!trimmed.includes("github.com")) {
      setError("Please enter a valid GitHub repository URL (e.g. https://github.com/owner/repo).");
      return;
    }
    setError("");
    onScanStart?.();

    try {
      // Use direct backend URL with long timeout — Next.js proxy drops long-running requests
      const response = await api.post("/github/scan", { repo_url: trimmed }, { timeout: 90000 });
      const data = response.data?.data || response.data;
      onScanSuccess?.(data);
    } catch (err: any) {
      const msg =
        err.code === 'ECONNABORTED'
          ? 'Scan timed out. The repository may be very large. Please try again.'
          : err.response?.data?.error ||
            err.response?.data?.detail ||
            'Failed to scan repository. It may be private or the GitHub API rate limit was exceeded.';
      onScanError?.(msg);
    }
  };

  return (
    <Card className="bg-[#111827] border-[#334155] shadow-lg">
      <CardHeader className="pb-4 border-b border-[#334155]/50">
        <CardTitle className="text-lg font-semibold text-[#F8FAFC] flex items-center gap-2">
          <GithubIcon className="h-5 w-5 text-[#2563EB]" />
          Scan Repository
        </CardTitle>
        <CardDescription>
          Enter a public GitHub repository URL to scan for exposed secrets, risky files, and dependency manifests.
        </CardDescription>
      </CardHeader>
      <CardContent className="pt-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label htmlFor="repo-url" className="text-sm font-medium text-[#F8FAFC]">
              Repository URL
            </label>
            <div className="flex gap-3">
              <div className="relative flex-1">
                <GithubIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                <Input
                  id="repo-url"
                  placeholder="https://github.com/owner/repository"
                  value={repoUrl}
                  disabled={isScanning}
                  onChange={(e) => { setRepoUrl(e.target.value); setError(""); }}
                  className={`pl-10 h-12 bg-[#020817] ${error ? 'border-red-500' : 'border-[#334155]/60'} focus:border-[#2563EB] text-[#F8FAFC] transition-colors`}
                />
              </div>
              <Button
                type="submit"
                disabled={isScanning}
                className="h-12 px-8 bg-[#2563EB] hover:bg-[#2563EB]/90 text-white font-medium shadow-md shadow-[#2563EB]/20 transition-all disabled:opacity-50"
              >
                {isScanning ? (
                  <span className="flex items-center gap-2">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Scanning...
                  </span>
                ) : (
                  <span className="flex items-center gap-2">
                    <Search className="h-4 w-4" />
                    Scan
                  </span>
                )}
              </Button>
            </div>
            {error && <p className="text-sm text-red-500 mt-1">{error}</p>}
          </div>

          {/* Info panel */}
          <div className="rounded-lg border border-[#334155]/50 bg-[#020817]/60 p-4 space-y-2">
            <p className="text-xs font-semibold text-[#F8FAFC] flex items-center gap-2">
              <Lock className="h-3.5 w-3.5 text-[#2563EB]" />
              Public Repos Only
            </p>
            <ul className="text-xs text-muted-foreground space-y-1 ml-5 list-disc">
              <li>Scans up to 80 text files for secrets &amp; credentials</li>
              <li>Detects risky filenames (e.g. <code className="text-blue-400">.env</code>, <code className="text-blue-400">id_rsa</code>, <code className="text-blue-400">*.pem</code>)</li>
              <li>Identifies dependency manifests (npm, pip, maven, etc.)</li>
              <li>Uses GitHub's public API — no token required</li>
            </ul>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
