'use client';

import { Card, CardContent } from "@/components/ui/card";
import { Lock, FileJson, Network, Globe, Code, Brain } from "lucide-react";
import { motion } from "framer-motion";

const checks = [
  { name: "SSL/TLS Analysis", icon: Lock, desc: "Validates certificates and cipher suites" },
  { name: "Security Headers", icon: FileJson, desc: "Checks for strict transport and CORS" },
  { name: "DNS Configuration", icon: Network, desc: "Analyzes SPF, DKIM, and DMARC records" },
  { name: "WHOIS Registry", icon: Globe, desc: "Monitors domain expiry and ownership" },
  { name: "Tech Fingerprint", icon: Code, desc: "Identifies exposed frameworks and server versions" },
  { name: "AI Risk Scoring", icon: Brain, desc: "Evaluates heuristic vulnerabilities automatically" },
];

export function QuickChecks() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold text-[#F8FAFC] tracking-tight">Passive Inspection Capabilities</h3>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {checks.map((check, index) => (
          <motion.div 
            key={check.name}
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: index * 0.1 }}
            className="h-full"
          >
            <Card className="h-full bg-[#111827] border-[#334155] shadow-md hover:shadow-xl hover:border-[#2563EB]/50 transition-all duration-300 group overflow-hidden relative">
              <div className="absolute top-0 left-0 w-1 h-full bg-gradient-to-b from-[#2563EB]/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
              <CardContent className="p-8 flex flex-col items-start space-y-5 h-full justify-center">
                <div className="h-14 w-14 rounded-xl bg-[#020817] border border-[#334155] flex items-center justify-center group-hover:scale-105 group-hover:bg-[#2563EB]/10 group-hover:border-[#2563EB]/30 transition-all duration-300 shadow-sm">
                  <check.icon className="h-6 w-6 text-[#2563EB] group-hover:text-white transition-colors duration-300" />
                </div>
                <div className="w-full">
                  <h4 className="text-base font-semibold text-[#F8FAFC] tracking-wide truncate">{check.name}</h4>
                  <p className="text-sm text-muted-foreground mt-2 truncate font-medium">{check.desc}</p>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
