'use client';

import { motion } from "framer-motion";
import { User, ShieldCheck, Mail, Building, Calendar, Award } from "lucide-react";

interface ProfileCardProps {
  user: {
    fullName: string;
    email: string;
    organization: string;
    role: string;
    joinedDate: string;
  };
}

export function ProfileCard({ user }: ProfileCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="relative overflow-hidden rounded-xl border border-[#334155] bg-[#111827]/80 p-6 backdrop-blur-md shadow-xl"
    >
      <div className="flex flex-col sm:flex-row items-start sm:items-center gap-5">
        {/* Avatar */}
        <div className="relative">
          <div className="h-20 w-20 rounded-2xl bg-gradient-to-br from-[#8B5CF6] to-[#6D28D9] p-0.5 shadow-lg shadow-purple-900/30">
            <div className="flex h-full w-full items-center justify-center rounded-[14px] bg-[#0F172A]">
              <User className="h-10 w-10 text-[#8B5CF6]" />
            </div>
          </div>
          <div className="absolute -bottom-1 -right-1 flex h-6 w-6 items-center justify-center rounded-full bg-emerald-500 text-white ring-4 ring-[#111827]">
            <ShieldCheck className="h-3.5 w-3.5" />
          </div>
        </div>

        {/* User Metadata */}
        <div className="space-y-1.5 flex-1">
          <div className="flex flex-wrap items-center gap-2.5">
            <h3 className="text-xl font-bold text-[#F8FAFC]">{user.fullName}</h3>
            <span className="inline-flex items-center gap-1 rounded-full bg-[#8B5CF6]/15 px-2.5 py-0.5 text-xs font-bold text-[#8B5CF6] border border-[#8B5CF6]/30">
              <Award className="h-3 w-3" /> {user.role}
            </span>
          </div>

          <div className="flex flex-wrap items-center gap-y-1 gap-x-4 text-xs text-muted-foreground">
            <span className="flex items-center gap-1.5">
              <Mail className="h-3.5 w-3.5 text-[#64748B]" /> {user.email}
            </span>
            <span className="flex items-center gap-1.5">
              <Building className="h-3.5 w-3.5 text-[#64748B]" /> {user.organization}
            </span>
            <span className="flex items-center gap-1.5">
              <Calendar className="h-3.5 w-3.5 text-[#64748B]" /> Joined {user.joinedDate}
            </span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
