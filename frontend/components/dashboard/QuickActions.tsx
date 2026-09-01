'use client';

import { Button } from "@/components/ui/button";
import { Globe, GitBranch, Database, FileText } from "lucide-react";
import { motion } from "framer-motion";
import Link from "next/link";

const actions = [
  { label: "Scan Website", icon: Globe, href: "#", color: "text-blue-500", bg: "bg-blue-500/10" },
  { label: "Analyze GitHub", icon: GitBranch, href: "#", color: "text-orange-500", bg: "bg-orange-500/10" },
  { label: "Upload Dataset", icon: Database, href: "#", color: "text-green-500", bg: "bg-green-500/10" },
  { label: "Generate Report", icon: FileText, href: "#", color: "text-purple-500", bg: "bg-purple-500/10" },
];

export function QuickActions() {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }} 
      animate={{ opacity: 1, y: 0 }} 
      transition={{ duration: 0.4 }}
      className="grid grid-cols-2 md:grid-cols-4 gap-4"
    >
      {actions.map((action, i) => (
        <Link key={i} href={action.href}>
          <div className="h-full w-full py-4 flex flex-col items-center justify-center gap-3 bg-[#111827] border border-[#334155] hover:bg-[#111827]/80 hover:border-[#2563EB]/50 transition-all shadow-sm group rounded-md">
            <div className={`p-3 rounded-full ${action.bg} group-hover:scale-110 transition-transform`}>
              <action.icon className={`h-5 w-5 ${action.color}`} />
            </div>
            <span className="text-sm font-medium text-[#F8FAFC]">{action.label}</span>
          </div>
        </Link>
      ))}
    </motion.div>
  );
}
