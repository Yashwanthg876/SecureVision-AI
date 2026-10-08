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
        <h3 className="text-xl font-semibold text-foreground tracking-tight">Passive Inspection Capabilities</h3>
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
            <Card className="h-full bg-card border-border shadow-sm hover:shadow-md hover:border-primary/50 transition-all duration-300 group overflow-hidden relative">
              <div className="absolute top-0 left-0 w-1 h-full bg-gradient-to-b from-primary/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
              <CardContent className="p-8 flex flex-col items-start space-y-5 h-full justify-center">
                <div className="h-14 w-14 rounded-xl bg-muted border border-border flex items-center justify-center group-hover:scale-105 group-hover:bg-primary/10 group-hover:border-primary/30 transition-all duration-300 shadow-sm">
                  <check.icon className="h-6 w-6 text-primary transition-colors duration-300" />
                </div>
                <div className="w-full">
                  <h4 className="text-base font-semibold text-foreground tracking-wide truncate">{check.name}</h4>
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
