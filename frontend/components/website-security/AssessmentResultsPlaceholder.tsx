'use client';

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Lock, FileJson, Network, Globe, Code, Brain, ShieldCheck } from "lucide-react";
import { motion } from "framer-motion";

const resultSections = [
  { name: "Overall Security Score", icon: ShieldCheck },
  { name: "SSL/TLS Analysis", icon: Lock },
  { name: "HTTP Security Headers", icon: FileJson },
  { name: "DNS Configuration", icon: Network },
  { name: "WHOIS Information", icon: Globe },
  { name: "Technology Stack", icon: Code },
  { name: "AI Recommendations", icon: Brain },
];

export function AssessmentResultsPlaceholder() {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5, delay: 0.5 }}>
      <Card className="bg-[#111827] border-[#334155] shadow-sm overflow-hidden relative">
        <div className="absolute inset-0 bg-gradient-to-b from-[#020817]/20 to-transparent pointer-events-none" />
        
        <CardHeader className="pb-6 border-b border-[#334155]/50 relative">
          <CardTitle className="text-lg font-semibold text-[#F8FAFC]">Assessment Results</CardTitle>
          <CardDescription>Comprehensive findings will appear here once an assessment is completed.</CardDescription>
        </CardHeader>
        
        <CardContent className="pt-8 relative">
          <div className="absolute inset-0 flex items-center justify-center z-10 bg-[#111827]/60 backdrop-blur-[2px]">
            <div className="text-center px-6 py-8 border border-[#334155]/50 rounded-2xl bg-[#020817]/90 shadow-2xl">
              <ShieldCheck className="h-12 w-12 text-[#2563EB] mx-auto mb-4 opacity-80" />
              <h3 className="text-lg font-semibold text-[#F8FAFC] mb-2">Awaiting Target</h3>
              <p className="text-sm text-muted-foreground max-w-sm mx-auto">
                Enter a URL and run a passive assessment to generate a full security report.
              </p>
            </div>
          </div>
          
          <div className="space-y-6 opacity-30 select-none pointer-events-none blur-sm filter">
            {resultSections.map((section, index) => (
              <div key={index} className="space-y-3">
                <h4 className="text-sm font-semibold text-[#F8FAFC] flex items-center gap-2">
                  <section.icon className="h-4 w-4 text-[#2563EB]" />
                  {section.name}
                </h4>
                <div className="h-16 w-full rounded-md bg-[#334155]/40 animate-pulse" />
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
