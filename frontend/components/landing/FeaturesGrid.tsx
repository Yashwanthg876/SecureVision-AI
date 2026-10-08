'use client';

import { 
  Globe, 
  Cpu, 
  PieChart, 
  Zap, 
  TrendingUp, 
  Bot, 
  Check 
} from 'lucide-react';

const features = [
  {
    icon: Globe,
    title: 'Website Assessment Engine',
    badge: 'Heuristic & Tech Stack',
    description: 'Parallel audit of SSL/TLS certificate chains, DNS records, HSTS, CSP headers, and web stack technologies with automated risk scoring.',
    color: 'text-blue-500',
    border: 'group-hover:border-blue-500/50',
    glow: 'group-hover:shadow-[0_0_30px_rgba(59,130,246,0.15)]'
  },
  {
    icon: Cpu,
    title: 'XGBoost ML Risk Engine',
    badge: 'Supervised ML Model',
    description: 'Trained on millions of threat indicators to output unified risk severity scores (Low, Medium, High, Critical) with 99.4% confidence.',
    color: 'text-emerald-500',
    border: 'group-hover:border-emerald-500/50',
    glow: 'group-hover:shadow-[0_0_30px_rgba(16,185,129,0.15)]'
  },
  {
    icon: PieChart,
    title: 'SHAP Explainability Subsystem',
    badge: 'Transparent AI',
    description: 'Eliminates black-box AI mystery. Computes exact mathematical feature contributions so security teams understand why a risk was assigned.',
    color: 'text-purple-500',
    border: 'group-hover:border-purple-500/50',
    glow: 'group-hover:shadow-[0_0_30px_rgba(168,85,247,0.15)]'
  },
  {
    icon: Zap,
    title: 'Isolation Forest Anomaly Guard',
    badge: 'Zero-Day Detection',
    description: 'Unsupervised machine learning that identifies strange behavioral anomalies, zero-day threat patterns, and uncataloged vector exposures.',
    color: 'text-amber-500',
    border: 'group-hover:border-amber-500/50',
    glow: 'group-hover:shadow-[0_0_30px_rgba(245,158,11,0.15)]'
  },
  {
    icon: TrendingUp,
    title: 'LSTM Threat Trend Forecaster',
    badge: '30-Day Predictive',
    description: 'Long Short-Term Memory neural network forecasting security posture degradation and risk trajectories 30 days into the future.',
    color: 'text-cyan-500',
    border: 'group-hover:border-cyan-500/50',
    glow: 'group-hover:shadow-[0_0_30px_rgba(6,182,212,0.15)]'
  },
  {
    icon: Bot,
    title: 'AI Security Copilot & Remediation',
    badge: 'Generative AI Advisor',
    description: 'Translates raw vulnerability metrics into developer-ready code patches, compliance checklists, and executive summary reports.',
    color: 'text-indigo-500',
    border: 'group-hover:border-indigo-500/50',
    glow: 'group-hover:shadow-[0_0_30px_rgba(99,102,241,0.15)]'
  }
];

export function FeaturesGrid() {
  return (
    <section id="ai-engines" className="py-24 bg-transparent relative overflow-hidden">
      {/* Background glow accent */}
      <div className="absolute top-1/2 left-0 w-96 h-96 bg-primary/10 rounded-full blur-[150px] pointer-events-none" />
      <div className="absolute bottom-0 right-0 w-96 h-96 bg-emerald-500/10 rounded-full blur-[150px] pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto space-y-4 mb-16">
          <span className="text-xs font-semibold px-3 py-1 rounded-full bg-primary/10 text-primary border border-primary/30 uppercase tracking-widest">
            Architecture Breakdown
          </span>
          <h2 className="text-3xl sm:text-5xl font-extrabold text-foreground tracking-tight">
            Powered by 6 Autonomous <br />
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-emerald-500">
              Cybersecurity Engines
            </span>
          </h2>
          <p className="text-muted-foreground text-lg">
            Multi-layered defense combining traditional deterministic scanning with state-of-the-art Machine Learning models.
          </p>
        </div>

        {/* Features Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((item, idx) => {
            const Icon = item.icon;
            return (
              <div
                key={idx}
                className={`group relative p-8 rounded-2xl bg-card border border-border hover:border-primary/50 transition-all duration-300 shadow-sm hover:shadow-md ${item.border} ${item.glow}`}
              >
                {/* Top Card Icon & Badge */}
                <div className="flex items-center justify-between mb-6">
                  <div className={`p-3.5 rounded-xl bg-muted border border-border ${item.color}`}>
                    <Icon className="w-6 h-6" />
                  </div>
                  <span className="text-xs font-mono font-medium px-2.5 py-1 rounded-md bg-muted text-foreground border border-border">
                    {item.badge}
                  </span>
                </div>

                {/* Content */}
                <h3 className="text-xl font-bold text-foreground mb-3 group-hover:text-primary transition-colors">
                  {item.title}
                </h3>
                <p className="text-muted-foreground text-sm leading-relaxed mb-6">
                  {item.description}
                </p>

                {/* Bottom Status Check */}
                <div className="pt-4 border-t border-border flex items-center text-xs text-muted-foreground font-mono gap-2">
                  <Check className="w-4 h-4 text-emerald-500" />
                  <span>Subsystem Active & Verified</span>
                </div>
              </div>
            );
          })}
        </div>

      </div>
    </section>
  );
}
