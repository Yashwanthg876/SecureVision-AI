'use client';

import { Card, CardContent } from "@/components/ui/card";
import { CheckCircle2, Circle, Loader2 } from "lucide-react";
import { motion } from "framer-motion";

const STEPS = [
  { id: 1, name: "Resolving repository URL" },
  { id: 2, name: "Fetching repository metadata" },
  { id: 3, name: "Mapping file tree" },
  { id: 4, name: "Classifying risky filenames" },
  { id: 5, name: "Scanning files for secrets" },
  { id: 6, name: "Computing security score" },
];

interface RepoScanProgressProps {
  isVisible?: boolean;
}

export function RepoScanProgress({ isVisible = false }: RepoScanProgressProps) {
  if (!isVisible) return null;

  return (
    <motion.div
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: "auto" }}
      exit={{ opacity: 0, height: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Card className="bg-[#111827] border-[#334155] shadow-sm mt-4">
        <CardContent className="p-6">
          <h3 className="text-sm font-semibold text-[#F8FAFC] mb-4">Scan in Progress...</h3>
          <div className="space-y-4">
            {STEPS.map((step, index) => {
              const status = index === 0 ? "complete" : index === 1 ? "current" : "upcoming";
              return (
                <div key={step.id} className="flex items-center gap-3 relative">
                  {index !== STEPS.length - 1 && (
                    <div className="absolute left-2.5 top-6 bottom-[-16px] w-[2px] bg-[#334155]" />
                  )}
                  <div className="relative z-10 flex items-center justify-center bg-[#111827]">
                    {status === "complete" ? (
                      <CheckCircle2 className="h-5 w-5 text-green-500" />
                    ) : status === "current" ? (
                      <Loader2 className="h-5 w-5 text-[#2563EB] animate-spin" />
                    ) : (
                      <Circle className="h-5 w-5 text-[#334155]" />
                    )}
                  </div>
                  <span className={`text-sm font-medium ${
                    status === "complete" ? "text-muted-foreground" :
                    status === "current" ? "text-[#F8FAFC]" : "text-muted-foreground/50"
                  }`}>
                    {step.name}
                  </span>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
