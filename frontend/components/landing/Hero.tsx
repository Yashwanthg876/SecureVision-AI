'use client';

import { useState } from 'react';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ShieldCheck, 
  Search, 
  Sparkles, 
  Zap, 
  ArrowRight, 
  Lock, 
  Globe, 
  CheckCircle2, 
  AlertTriangle, 
  Cpu, 
  TrendingUp, 
  FileCode,
  Play
} from 'lucide-react';
import { Button } from '@/components/ui/button';

export function Hero() {
  const [targetUrl, setTargetUrl] = useState('api.securevision-demo.io');
  const [isScanning, setIsScanning] = useState(false);
  const [scanStep, setScanStep] = useState(0);
  const [scanResult, setScanResult] = useState<any>(null);

  const sampleTargets = [
    'api.securevision-demo.io',
    'auth-service.cloud',
    'payment-gateway.net'
  ];

  const handleSimulateScan = (urlToScan?: string) => {
    const url = urlToScan || targetUrl;
    setTargetUrl(url);
    setIsScanning(true);
    setScanStep(1);
    setScanResult(null);

    // Simulate multi-engine scanning sequence
    setTimeout(() => setScanStep(2), 600);
    setTimeout(() => setScanStep(3), 1200);
    setTimeout(() => setScanStep(4), 1800);
    setTimeout(() => {
      setIsScanning(false);
      setScanResult({
        url: url,
        securityScore: 92,
        riskLevel: 'LOW',
        sslValid: true,
        headerScore: 'A+',
        xgboostConfidence: '98.4%',
        zeroDayAnomaly: 'None Detected',
        trend30Days: 'Stable (0.2% variance)',
        aiSummary: 'System configuration complies with high security posture. No critical vulnerabilities found in SSL/TLS configuration or HTTP response headers.'
      });
    }, 2200);
  };

  return (
    <section className="relative pt-32 pb-20 md:pt-40 md:pb-28 overflow-hidden bg-transparent">
      {/* Glow background effects */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[400px] bg-primary/20 rounded-full blur-[140px] pointer-events-none" />
      <div className="absolute top-1/3 left-1/4 w-[350px] h-[350px] bg-blue-600/15 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute top-1/2 right-1/4 w-[300px] h-[300px] bg-emerald-500/10 rounded-full blur-[100px] pointer-events-none" />
      
      {/* Grid pattern overlay */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#1f293715_1px,transparent_1px),linear-gradient(to_bottom,#1f293715_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center max-w-3xl mx-auto space-y-6">
          
          {/* Top Pill */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-900/90 border border-primary/40 shadow-[0_0_15px_rgba(37,99,235,0.2)] text-xs font-semibold text-primary-foreground"
          >
            <Sparkles className="w-4 h-4 text-primary animate-spin" style={{ animationDuration: '8s' }} />
            <span>XGBoost ML + SHAP Explainability + LSTM Forecasting</span>
          </motion.div>

          {/* Main Title */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white leading-[1.15]"
          >
            Autonomous <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-primary to-emerald-400">AI Threat Intelligence</span> & Security Platform
          </motion.h1>

          {/* Subtitle */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="text-lg sm:text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed"
          >
            Comprehensive infrastructure defense powered by ML risk classification, Isolation Forest zero-day anomaly detection, GitHub audit, and instant AI Copilot remediation.
          </motion.p>

          {/* CTAs */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2"
          >
            <Link href="/dashboard">
              <Button size="lg" className="w-full sm:w-auto bg-primary hover:bg-primary/90 text-white px-8 py-6 text-base font-semibold shadow-[0_0_30px_rgba(37,99,235,0.5)] hover:shadow-[0_0_40px_rgba(37,99,235,0.7)] transition-all gap-2 group">
                Launch Security Dashboard
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Button>
            </Link>

            <Link href="/login">
              <Button size="lg" variant="outline" className="w-full sm:w-auto border-slate-700 bg-slate-900/60 hover:bg-slate-800 text-slate-200 px-8 py-6 text-base font-medium">
                Sign In to Account
              </Button>
            </Link>
          </motion.div>
        </div>

        {/* Live Simulator Widget */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.4 }}
          className="mt-14 max-w-4xl mx-auto"
        >
          <div className="relative rounded-2xl bg-slate-900/90 border border-slate-800 shadow-[0_20px_60px_rgba(0,0,0,0.8)] overflow-hidden backdrop-blur-xl">
            {/* Top Bar */}
            <div className="flex items-center justify-between px-6 py-4 bg-slate-950/80 border-b border-slate-800">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-red-500/80" />
                <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
                <div className="w-3 h-3 rounded-full bg-emerald-500/80" />
                <span className="ml-2 text-xs font-mono text-slate-400 flex items-center gap-1.5">
                  <Globe className="w-3.5 h-3.5 text-primary" /> Live AI Vulnerability Scanner
                </span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-xs text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20 font-mono">
                  Engine Ready
                </span>
              </div>
            </div>

            {/* Scan Control Input */}
            <div className="p-6">
              <div className="flex flex-col md:flex-row gap-3">
                <div className="relative flex-1">
                  <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                  <input
                    type="text"
                    value={targetUrl}
                    onChange={(e) => setTargetUrl(e.target.value)}
                    placeholder="Enter target domain (e.g. enterprise-api.com)"
                    className="w-full pl-12 pr-4 py-3 bg-slate-950/90 border border-slate-700/80 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary font-mono text-sm"
                  />
                </div>
                <Button
                  onClick={() => handleSimulateScan()}
                  disabled={isScanning}
                  className="bg-gradient-to-r from-primary to-blue-600 hover:from-primary/90 hover:to-blue-700 text-white px-6 py-3 rounded-xl font-medium shadow-md flex items-center justify-center gap-2"
                >
                  {isScanning ? (
                    <>
                      <Zap className="w-4 h-4 animate-bounce text-yellow-400" />
                      Analyzing Target...
                    </>
                  ) : (
                    <>
                      <Play className="w-4 h-4 fill-white" />
                      Run AI Scan Demo
                    </>
                  )}
                </Button>
              </div>

              {/* Sample Preset Tags */}
              <div className="flex items-center gap-2 mt-3 flex-wrap">
                <span className="text-xs text-slate-500">Try sample target:</span>
                {sampleTargets.map((sample) => (
                  <button
                    key={sample}
                    onClick={() => handleSimulateScan(sample)}
                    className="text-xs font-mono text-slate-400 bg-slate-800/60 hover:bg-slate-700 hover:text-white px-2.5 py-1 rounded-md transition-colors"
                  >
                    {sample}
                  </button>
                ))}
              </div>

              {/* Scan Execution & Results Box */}
              <div className="mt-6 border-t border-slate-800/80 pt-6">
                {isScanning ? (
                  <div className="py-8 text-center space-y-4">
                    <div className="inline-flex p-4 rounded-2xl bg-primary/10 border border-primary/30 text-primary">
                      <Cpu className="w-8 h-8 animate-spin" />
                    </div>
                    <div className="space-y-1">
                      <h4 className="text-white font-semibold text-lg">
                        Executing Multimodal AI Pipeline...
                      </h4>
                      <p className="text-slate-400 text-sm font-mono">
                        {scanStep === 1 && '[Phase 1/4] Inspecting SSL, DNS, and HTTP Security Headers...'}
                        {scanStep === 2 && '[Phase 2/4] Passing features into XGBoost ML Classifier...'}
                        {scanStep === 3 && '[Phase 3/4] Running Isolation Forest Zero-Day Anomaly Detection...'}
                        {scanStep === 4 && '[Phase 4/4] Generating SHAP Feature Importance & AI Summary...'}
                      </p>
                    </div>
                    <div className="w-full bg-slate-950 rounded-full h-2 max-w-md mx-auto overflow-hidden border border-slate-800">
                      <div
                        className="bg-primary h-full transition-all duration-500 rounded-full"
                        style={{ width: `${scanStep * 25}%` }}
                      />
                    </div>
                  </div>
                ) : scanResult ? (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.98 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="space-y-4"
                  >
                    {/* Header metrics row */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                      <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800">
                        <span className="text-xs text-slate-400 block">Security Score</span>
                        <div className="flex items-center gap-2 mt-1">
                          <ShieldCheck className="w-5 h-5 text-emerald-400" />
                          <span className="text-xl font-bold text-white">{scanResult.securityScore}/100</span>
                        </div>
                      </div>

                      <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800">
                        <span className="text-xs text-slate-400 block">XGBoost ML Risk</span>
                        <div className="flex items-center gap-2 mt-1">
                          <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                          <span className="text-xl font-bold text-emerald-400">{scanResult.riskLevel}</span>
                        </div>
                      </div>

                      <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800">
                        <span className="text-xs text-slate-400 block">Anomaly Engine</span>
                        <div className="flex items-center gap-2 mt-1">
                          <Zap className="w-5 h-5 text-blue-400" />
                          <span className="text-sm font-semibold text-slate-200">{scanResult.zeroDayAnomaly}</span>
                        </div>
                      </div>

                      <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800">
                        <span className="text-xs text-slate-400 block">30-Day Trend</span>
                        <div className="flex items-center gap-2 mt-1">
                          <TrendingUp className="w-5 h-5 text-emerald-400" />
                          <span className="text-sm font-semibold text-slate-200">{scanResult.trend30Days}</span>
                        </div>
                      </div>
                    </div>

                    {/* AI Copilot Explanation Banner */}
                    <div className="p-4 rounded-xl bg-primary/10 border border-primary/30 flex items-start gap-3">
                      <Sparkles className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                      <div className="space-y-1">
                        <span className="text-xs font-semibold text-primary uppercase tracking-wider">
                          AI Copilot Analysis Summary
                        </span>
                        <p className="text-sm text-slate-300 leading-relaxed">
                          {scanResult.aiSummary}
                        </p>
                      </div>
                    </div>
                  </motion.div>
                ) : (
                  <div className="py-6 text-center text-slate-500 text-sm flex items-center justify-center gap-2">
                    <Zap className="w-4 h-4 text-primary" />
                    Click <strong>"Run AI Scan Demo"</strong> above to see live ML vulnerability detection in action.
                  </div>
                )}
              </div>
            </div>
          </div>
        </motion.div>

        {/* Live Metrics Ticker Bar */}
        <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-6 pt-10 border-t border-slate-800/80">
          <div className="text-center">
            <h3 className="text-3xl font-extrabold text-white font-mono">10M+</h3>
            <p className="text-sm text-slate-400 mt-1">Vulnerabilities Scanned</p>
          </div>
          <div className="text-center">
            <h3 className="text-3xl font-extrabold text-primary font-mono">99.4%</h3>
            <p className="text-sm text-slate-400 mt-1">ML Classification Accuracy</p>
          </div>
          <div className="text-center">
            <h3 className="text-3xl font-extrabold text-emerald-400 font-mono">&lt; 1.2s</h3>
            <p className="text-sm text-slate-400 mt-1">Real-Time Scan Speed</p>
          </div>
          <div className="text-center">
            <h3 className="text-3xl font-extrabold text-indigo-400 font-mono">24/7</h3>
            <p className="text-sm text-slate-400 mt-1">Zero-Day Anomaly Guard</p>
          </div>
        </div>

      </div>
    </section>
  );
}
