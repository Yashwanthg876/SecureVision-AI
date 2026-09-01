'use client';

import { Card, CardContent } from "@/components/ui/card";
import { CheckCircle2, Circle, Loader2 } from "lucide-react";
import { motion } from "framer-motion";

const steps = [
  { id: 1, name: 'Initializing Assessment', status: 'complete' },
  { id: 2, name: 'Resolving DNS & WHOIS', status: 'current' },
  { id: 3, name: 'Analyzing SSL/TLS Configuration', status: 'upcoming' },
  { id: 4, name: 'Evaluating HTTP Security Headers', status: 'upcoming' },
  { id: 5, name: 'Detecting Technology Stack', status: 'upcoming' },
  { id: 6, name: 'Generating AI Security Score', status: 'upcoming' },
];

interface AssessmentProgressProps {
  isVisible?: boolean;
}

export function AssessmentProgress({ isVisible = false }: AssessmentProgressProps) {
  if (!isVisible) return null;

  return (
    <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }}>
      <Card className="bg-[#111827] border-[#334155] shadow-sm mb-6">
        <CardContent className="p-6">
          <h3 className="text-sm font-semibold text-[#F8FAFC] mb-4">Assessment in Progress...</h3>
          <div className="space-y-4">
            {steps.map((step, index) => (
              <div key={step.id} className="flex items-center gap-3 relative">
                {/* Connector Line */}
                {index !== steps.length - 1 && (
                  <div className="absolute left-2.5 top-6 bottom-[-16px] w-[2px] bg-[#334155]" />
                )}
                
                <div className="relative z-10 flex items-center justify-center bg-[#111827]">
                  {step.status === 'complete' ? (
                    <CheckCircle2 className="h-5 w-5 text-green-500" />
                  ) : step.status === 'current' ? (
                    <Loader2 className="h-5 w-5 text-[#2563EB] animate-spin" />
                  ) : (
                    <Circle className="h-5 w-5 text-[#334155]" />
                  )}
                </div>
                
                <span className={`text-sm font-medium ${
                  step.status === 'complete' ? 'text-muted-foreground' : 
                  step.status === 'current' ? 'text-[#F8FAFC]' : 'text-muted-foreground/50'
                }`}>
                  {step.name}
                </span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
