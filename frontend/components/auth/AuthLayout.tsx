'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { 
  Shield, 
  ArrowLeft, 
  Sparkles, 
  CheckCircle2, 
  Lock, 
  Activity, 
  Cpu, 
  TrendingUp, 
  Zap 
} from 'lucide-react';

interface AuthLayoutProps {
  children: React.ReactNode;
  title: string;
  subtitle: string;
}

export function AuthLayout({ children, title, subtitle }: AuthLayoutProps) {
  return (
    <div className="min-h-screen flex bg-transparent text-foreground overflow-hidden selection:bg-primary/30 selection:text-primary-foreground relative">
      
      {/* Left Side Showcase Panel (Visible on lg screens) */}
      <div className="hidden lg:flex lg:w-1/2 relative bg-slate-950/70 backdrop-blur-md flex-col justify-between p-12 overflow-hidden border-r border-slate-800/80 z-10">
        
        {/* Glow background accents */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-[140px] pointer-events-none" />
        <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-emerald-500/15 rounded-full blur-[120px] pointer-events-none" />
        
        {/* Grid pattern overlay */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#1f293715_1px,transparent_1px),linear-gradient(to_bottom,#1f293715_1px,transparent_1px)] bg-[size:3rem_3rem] pointer-events-none" />

        {/* Top Header Logo */}
        <div className="relative z-10">
          <Link href="/" className="inline-flex items-center gap-3 group">
            <div className="p-2.5 rounded-xl bg-primary/10 border border-primary/30 group-hover:border-primary/60 transition-all shadow-[0_0_20px_rgba(37,99,235,0.3)]">
              <Shield className="w-7 h-7 text-primary" />
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-2xl text-white tracking-tight">SecureVision</span>
              <span className="text-xs text-primary font-mono flex items-center gap-1">
                <Sparkles className="w-3 h-3" /> Autonomous AI Defense
              </span>
            </div>
          </Link>
        </div>

        {/* Center Threat Intelligence Showcase */}
        <div className="relative z-10 space-y-8 my-auto max-w-lg">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="space-y-4"
          >
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs font-semibold text-emerald-400">
              <Activity className="w-3.5 h-3.5 animate-pulse" />
              <span>Real-Time Threat Telemetry Active</span>
            </div>

            <h2 className="text-3xl font-extrabold text-white leading-tight">
              Enterprise-Grade AI Security <br />
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400">
                At Your Fingertips
              </span>
            </h2>

            <p className="text-slate-400 text-sm leading-relaxed">
              Continuously monitor websites, GitHub repositories, SSL certificate chains, and predict 30-day security trajectories with explainable machine learning.
            </p>
          </motion.div>

          {/* Real-Time Subsystems Status Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800/80 backdrop-blur-md space-y-3 font-mono text-xs"
          >
            <div className="flex items-center justify-between text-slate-300 pb-2 border-b border-slate-800">
              <span className="flex items-center gap-2">
                <Cpu className="w-4 h-4 text-primary" /> XGBoost Risk Classifier
              </span>
              <span className="text-emerald-400 font-semibold">99.4% Accuracy</span>
            </div>

            <div className="flex items-center justify-between text-slate-300 pb-2 border-b border-slate-800">
              <span className="flex items-center gap-2">
                <Zap className="w-4 h-4 text-amber-400" /> Isolation Forest Anomaly
              </span>
              <span className="text-emerald-400 font-semibold">Operational</span>
            </div>

            <div className="flex items-center justify-between text-slate-300">
              <span className="flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-cyan-400" /> LSTM Threat Forecaster
              </span>
              <span className="text-emerald-400 font-semibold">30-Day Horizon</span>
            </div>
          </motion.div>
        </div>

        {/* Footer info */}
        <div className="relative z-10 flex items-center justify-between text-xs text-slate-500 font-mono">
          <span className="flex items-center gap-1.5">
            <Lock className="w-3.5 h-3.5 text-primary" /> 256-Bit Encrypted Portal
          </span>
          <span>v2.4.0 Production</span>
        </div>

      </div>

      {/* Right Side Form Panel */}
      <div className="flex-1 flex flex-col justify-between p-6 sm:p-12 relative z-10 overflow-y-auto bg-slate-950/50 backdrop-blur-sm">
        
        {/* Top Header bar with Home link */}
        <div className="flex items-center justify-between w-full max-w-md mx-auto mb-8">
          <Link
            href="/"
            className="inline-flex items-center gap-2 text-sm font-medium text-slate-400 hover:text-white transition-colors py-1.5 px-3 rounded-lg hover:bg-slate-900 border border-transparent hover:border-slate-800"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Home</span>
          </Link>

          {/* Mobile Logo */}
          <div className="lg:hidden flex items-center gap-2">
            <Shield className="w-5 h-5 text-primary" />
            <span className="font-bold text-white text-base">SecureVision AI</span>
          </div>
        </div>

        {/* Form Container */}
        <div className="w-full max-w-md mx-auto my-auto space-y-6">
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="text-center space-y-2"
          >
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">{title}</h1>
            <p className="text-sm text-slate-400">{subtitle}</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.4, delay: 0.1 }}
          >
            {children}
          </motion.div>
        </div>

        {/* Footer link */}
        <div className="mt-8 text-center text-xs text-slate-500 font-mono">
          Protected by SecureVision AI Sentinel • Privacy & Terms
        </div>

      </div>

    </div>
  );
}
