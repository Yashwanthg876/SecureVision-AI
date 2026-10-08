'use client';

import Link from 'next/link';
import { Check, Sparkles, ArrowRight, Globe, GitBranch, Brain, FileText } from 'lucide-react';
import { Button } from '@/components/ui/button';

export function Pricing() {
  return (
    <section id="pricing" className="py-24 bg-transparent relative overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto space-y-4 mb-16">
          <span className="text-xs font-bold px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-500 border border-emerald-500/30 uppercase tracking-widest inline-flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5" /> 100% Free & Open Access
          </span>
          <h2 className="text-3xl sm:text-5xl font-extrabold text-foreground tracking-tight">
            Cybersecurity Intelligence for Everyone
          </h2>
          <p className="text-muted-foreground text-lg">
            No credit cards. No hidden paywalls. SecureVision AI is completely free and open for developers, security researchers, and teams worldwide.
          </p>
        </div>

        {/* Highlight Showcase Box */}
        <div className="relative rounded-3xl bg-card border border-border p-8 lg:p-12 shadow-sm space-y-10 overflow-hidden">
          <div className="absolute top-0 right-0 w-96 h-96 bg-primary/10 rounded-full blur-[120px] pointer-events-none" />

          {/* Top Feature Highlights */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="p-6 rounded-2xl bg-muted/40 border border-border space-y-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-500/10 text-blue-500 border border-blue-500/20">
                <Globe className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-foreground">Website Security</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Full passive SSL, HTTP header, DNS analysis, and heuristic vulnerability scoring.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-muted/40 border border-border space-y-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-purple-500/10 text-purple-500 border border-purple-500/20">
                <GitBranch className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-foreground">GitHub Scanner</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Automated secret detection, SAST code audits, and dependency security checks.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-muted/40 border border-border space-y-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-500 border border-emerald-500/20">
                <Brain className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-foreground">AI Detection & Threat Intel</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Real-time IP/Domain reputation lookups, AI content signatures, and threat feeds.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-muted/40 border border-border space-y-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-500/10 text-amber-500 border border-amber-500/20">
                <FileText className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-foreground">Executive Reports</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Instant PDF, CSV, and JSON report downloads with OWASP Top 10 compliance audits.
              </p>
            </div>
          </div>

          {/* Bottom Action Row */}
          <div className="pt-6 border-t border-border flex flex-col sm:flex-row items-center justify-between gap-6">
            <div className="flex items-center gap-3 text-sm text-foreground">
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-emerald-500/20 text-emerald-500">
                <Check className="w-5 h-5" />
              </div>
              <span className="text-muted-foreground">Unlimited usage • 100% Free Forever • Instant Access</span>
            </div>

            <Link href="/dashboard">
              <Button className="h-12 px-8 bg-primary hover:bg-primary/90 text-white font-semibold rounded-xl shadow-md transition-all gap-2">
                Launch Free Security Platform <ArrowRight className="w-4 h-4" />
              </Button>
            </Link>
          </div>
        </div>

      </div>
    </section>
  );
}
