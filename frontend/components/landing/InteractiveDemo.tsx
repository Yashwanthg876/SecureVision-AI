'use client';

import { useState } from 'react';
import { 
  Globe, 
  Code, 
  ShieldAlert, 
  Sparkles, 
  CheckCircle2, 
  AlertCircle, 
  ExternalLink, 
  Terminal, 
  Lock, 
  Cpu, 
  TrendingUp, 
  FileCheck 
} from 'lucide-react';
import { Button } from '@/components/ui/button';

export function InteractiveDemo() {
  const [activeTab, setActiveTab] = useState<'website' | 'github' | 'intel' | 'copilot'>('website');

  return (
    <section id="demo" className="py-24 bg-transparent relative overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto space-y-4 mb-14">
          <span className="text-xs font-semibold px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase tracking-widest">
            Interactive Product Showcase
          </span>
          <h2 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight">
            See SecureVision AI in Action
          </h2>
          <p className="text-slate-400 text-lg">
            Explore how our unified dashboard gives security engineering teams instant visibility across all threat surfaces.
          </p>
        </div>

        {/* Tab Switcher Buttons */}
        <div className="flex justify-center mb-10 overflow-x-auto pb-2 scrollbar-none">
          <div className="p-1.5 rounded-2xl bg-slate-900 border border-slate-800 flex items-center gap-2">
            <button
              onClick={() => setActiveTab('website')}
              className={`flex items-center gap-2 px-5 py-3 rounded-xl text-sm font-semibold transition-all ${
                activeTab === 'website'
                  ? 'bg-primary text-white shadow-lg shadow-primary/30'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
              }`}
            >
              <Globe className="w-4 h-4" />
              Website Security
            </button>

            <button
              onClick={() => setActiveTab('github')}
              className={`flex items-center gap-2 px-5 py-3 rounded-xl text-sm font-semibold transition-all ${
                activeTab === 'github'
                  ? 'bg-primary text-white shadow-lg shadow-primary/30'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
              }`}
            >
              <Code className="w-4 h-4" />
              GitHub Security
            </button>

            <button
              onClick={() => setActiveTab('intel')}
              className={`flex items-center gap-2 px-5 py-3 rounded-xl text-sm font-semibold transition-all ${
                activeTab === 'intel'
                  ? 'bg-primary text-white shadow-lg shadow-primary/30'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
              }`}
            >
              <ShieldAlert className="w-4 h-4" />
              Threat Intelligence
            </button>

            <button
              onClick={() => setActiveTab('copilot')}
              className={`flex items-center gap-2 px-5 py-3 rounded-xl text-sm font-semibold transition-all ${
                activeTab === 'copilot'
                  ? 'bg-primary text-white shadow-lg shadow-primary/30'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
              }`}
            >
              <Sparkles className="w-4 h-4 text-yellow-300" />
              AI Copilot & Fixes
            </button>
          </div>
        </div>

        {/* Dashboard Mockup Display */}
        <div className="max-w-5xl mx-auto rounded-2xl bg-slate-900/90 border border-slate-800 shadow-[0_25px_70px_rgba(0,0,0,0.8)] overflow-hidden backdrop-blur-xl">
          {/* Header Bar */}
          <div className="px-6 py-4 bg-slate-950/90 border-b border-slate-800 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 rounded-full bg-red-500/80" />
                <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
                <div className="w-3 h-3 rounded-full bg-emerald-500/80" />
              </div>
              <span className="text-xs font-mono text-slate-400">
                app.securevision.ai / dashboard / {activeTab}
              </span>
            </div>
            <div className="flex items-center gap-2 text-xs text-slate-400 font-mono">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
              <span>Real-Time Telemetry</span>
            </div>
          </div>

          {/* Dynamic Tab Body */}
          <div className="p-6 md:p-8">
            {activeTab === 'website' && (
              <div className="space-y-6">
                <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-4 rounded-xl bg-slate-950/80 border border-slate-800">
                  <div>
                    <span className="text-xs text-slate-400 font-mono">Target Host</span>
                    <h4 className="text-lg font-bold text-white font-mono flex items-center gap-2">
                      https://api.payment-gateway-v2.org
                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    </h4>
                  </div>
                  <div className="flex gap-3">
                    <span className="px-3 py-1.5 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-semibold">
                      Security Grade: A
                    </span>
                    <span className="px-3 py-1.5 rounded-lg bg-primary/10 text-primary border border-primary/20 text-xs font-semibold">
                      XGBoost Score: 94/100
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80">
                    <span className="text-xs text-slate-400">SSL/TLS Configuration</span>
                    <p className="text-sm font-semibold text-white mt-1">TLS 1.3 Strict Compliance</p>
                    <p className="text-xs text-emerald-400 mt-2 flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Valid for 248 days
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80">
                    <span className="text-xs text-slate-400">HTTP Security Headers</span>
                    <p className="text-sm font-semibold text-white mt-1">HSTS, CSP, X-Frame-Options</p>
                    <p className="text-xs text-emerald-400 mt-2 flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5" /> 7 of 7 Enforced
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80">
                    <span className="text-xs text-slate-400">Tech Stack Detection</span>
                    <p className="text-sm font-semibold text-white mt-1">Next.js, NGINX, FastAPI</p>
                    <p className="text-xs text-slate-400 mt-2">Zero Known CVEs</p>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'github' && (
              <div className="space-y-6">
                <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <Code className="w-6 h-6 text-primary" />
                    <div>
                      <h4 className="text-white font-semibold">Repository: org/secure-api-gateway</h4>
                      <p className="text-xs text-slate-400 font-mono">Branch: main • Last Scan: 4 mins ago</p>
                    </div>
                  </div>
                  <span className="px-3 py-1 rounded-full bg-yellow-500/10 text-yellow-400 border border-yellow-500/20 text-xs font-mono">
                    1 Warning Found
                  </span>
                </div>

                <div className="space-y-3 font-mono text-sm">
                  <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <AlertCircle className="w-4 h-4 text-yellow-400" />
                      <span className="text-slate-200">Outdated Dependency: `axios@1.6.0` (CVE-2023-45857)</span>
                    </div>
                    <span className="text-xs text-primary bg-primary/10 px-2.5 py-1 rounded border border-primary/20">
                      Fix Available v1.7+
                    </span>
                  </div>

                  <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                      <span className="text-slate-200">Secret Scanner: 0 API keys or private tokens detected</span>
                    </div>
                    <span className="text-xs text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded border border-emerald-500/20">
                      Passed
                    </span>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'intel' && (
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800">
                    <span className="text-xs text-slate-400">Global Threat Vector Monitor</span>
                    <div className="mt-3 space-y-2 font-mono text-xs">
                      <div className="flex justify-between text-slate-300 pb-1 border-b border-slate-800">
                        <span>CVE-2024-3094 (XZ Utils)</span>
                        <span className="text-red-400">Critical</span>
                      </div>
                      <div className="flex justify-between text-slate-300 pb-1 border-b border-slate-800">
                        <span>SQLi Attempt Blocked (IP 185.220.x.x)</span>
                        <span className="text-emerald-400">Neutralized</span>
                      </div>
                      <div className="flex justify-between text-slate-300">
                        <span>Credential Stuffing Spike</span>
                        <span className="text-yellow-400">Mitigated</span>
                      </div>
                    </div>
                  </div>

                  <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 flex flex-col justify-between">
                    <div>
                      <span className="text-xs text-slate-400">Isolation Forest Anomaly Index</span>
                      <h4 className="text-2xl font-bold text-white mt-2 font-mono">0.031 <span className="text-xs font-normal text-emerald-400">(Normal Range)</span></h4>
                      <p className="text-xs text-slate-400 mt-2">
                        Zero-day behavior telemetry within standard baseline parameter boundaries.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'copilot' && (
              <div className="space-y-4">
                <div className="p-4 rounded-xl bg-primary/10 border border-primary/30 flex items-center gap-3">
                  <Sparkles className="w-5 h-5 text-primary shrink-0" />
                  <div>
                    <h4 className="text-sm font-semibold text-white">AI Security Copilot Recommendation</h4>
                    <p className="text-xs text-slate-300 mt-0.5">
                      To patch potential XSS risk, configure your NGINX header configuration as follows:
                    </p>
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs text-slate-300 overflow-x-auto">
                  <div className="text-red-400 mb-1">- add_header X-XSS-Protection "0";</div>
                  <div className="text-emerald-400">+ add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline';";</div>
                  <div className="text-emerald-400">+ add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;</div>
                </div>
              </div>
            )}
          </div>
        </div>

      </div>
    </section>
  );
}
