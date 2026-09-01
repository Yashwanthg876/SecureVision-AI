'use client';

import Link from 'next/link';
import { Shield, Sparkles, Activity, Lock, ArrowUpRight } from 'lucide-react';

export function Footer() {
  return (
    <footer className="bg-slate-950 border-t border-slate-800 text-slate-400 py-16 relative overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        
        <div className="grid grid-cols-1 md:grid-cols-5 gap-10 mb-14">
          
          {/* Brand Info (2 cols) */}
          <div className="md:col-span-2 space-y-4">
            <Link href="/" className="flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-primary/10 border border-primary/30">
                <Shield className="w-6 h-6 text-primary" />
              </div>
              <span className="font-bold text-xl text-white tracking-tight">
                SecureVision AI
              </span>
            </Link>
            
            <p className="text-sm text-slate-400 max-w-sm leading-relaxed">
              Autonomous AI-driven vulnerability assessment, ML risk classification, SHAP explainability, and AI Copilot remediation for enterprise infrastructure.
            </p>

            <div className="flex items-center gap-3 pt-2">
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs font-mono text-emerald-400">
                <Activity className="w-3.5 h-3.5 animate-pulse" />
                <span>All Subsystems Operational</span>
              </div>
            </div>
          </div>

          {/* Column 1: Platform */}
          <div className="space-y-3">
            <h4 className="text-sm font-semibold text-white uppercase tracking-wider">Platform</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#features" className="hover:text-white transition-colors">Website Scanner</a></li>
              <li><a href="#ai-engines" className="hover:text-white transition-colors">XGBoost Risk Model</a></li>
              <li><a href="#ai-engines" className="hover:text-white transition-colors">SHAP Explainability</a></li>
              <li><a href="#ai-engines" className="hover:text-white transition-colors">Isolation Forest</a></li>
              <li><a href="#ai-engines" className="hover:text-white transition-colors">LSTM Forecaster</a></li>
            </ul>
          </div>

          {/* Column 2: Solutions */}
          <div className="space-y-3">
            <h4 className="text-sm font-semibold text-white uppercase tracking-wider">Solutions</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/dashboard/website-security" className="hover:text-white transition-colors">Domain Audit</Link></li>
              <li><Link href="/dashboard/github-security" className="hover:text-white transition-colors">GitHub Security</Link></li>
              <li><Link href="/dashboard/threat-intelligence" className="hover:text-white transition-colors">Threat Intelligence</Link></li>
              <li><Link href="/dashboard/reports" className="hover:text-white transition-colors">Executive Reports</Link></li>
            </ul>
          </div>

          {/* Column 3: Account & Access */}
          <div className="space-y-3">
            <h4 className="text-sm font-semibold text-white uppercase tracking-wider">Account</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/login" className="hover:text-white transition-colors">Sign In</Link></li>
              <li><Link href="/register" className="hover:text-white transition-colors">Create Account</Link></li>
              <li><Link href="/forgot-password" className="hover:text-white transition-colors">Reset Password</Link></li>
              <li><Link href="/dashboard" className="hover:text-white transition-colors flex items-center gap-1">Dashboard <ArrowUpRight className="w-3.5 h-3.5" /></Link></li>
            </ul>
          </div>

        </div>

        {/* Compliance Badges & Copyright */}
        <div className="pt-8 border-t border-slate-800/80 flex flex-col md:flex-row items-center justify-between gap-4 text-xs">
          <p>© {new Date().getFullYear()} SecureVision AI Inc. All rights reserved.</p>
          
          <div className="flex items-center gap-4 text-slate-500 font-mono">
            <span className="flex items-center gap-1">
              <Lock className="w-3.5 h-3.5 text-primary" /> SOC2 Type II Certified
            </span>
            <span>•</span>
            <span>ISO 27001 Compliant</span>
            <span>•</span>
            <span>GDPR Ready</span>
          </div>
        </div>

      </div>
    </footer>
  );
}
