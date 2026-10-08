'use client';

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard,
  Globe,
  GitBranch,
  Brain,
  ShieldAlert,
  FileText,
  Settings,
  User,
  LogOut,
  X,
  ChevronLeft,
} from "lucide-react";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useUser } from "@/context/UserContext";

const navigation = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Website Security", href: "/dashboard/website-security", icon: Globe },
  { name: "GitHub Security", href: "/dashboard/github-security", icon: GitBranch },
  { name: "AI Detection", href: "/dashboard/ai-detection", icon: Brain },
  { name: "Threat Intelligence", href: "/dashboard/threat-intelligence", icon: ShieldAlert },
  { name: "Reports", href: "/dashboard/reports", icon: FileText },
];

interface SidebarProps {
  isMobileMenuOpen: boolean;
  setIsMobileMenuOpen: (open: boolean) => void;
}

export function Sidebar({ isMobileMenuOpen, setIsMobileMenuOpen }: SidebarProps) {
  const pathname = usePathname();
  const router = useRouter();
  const { user, logout } = useUser();
  const [isCollapsed, setIsCollapsed] = useState(false);

  const handleLogout = async () => {
    await logout();
  };

  const SidebarContent = () => (
    <>
      <div className="flex shrink-0 items-center justify-between px-6 py-5 border-b border-border">
        <div className="flex items-center w-full">
          <ShieldAlert className="h-8 w-8 text-primary mr-3 shrink-0" />
          <AnimatePresence initial={false}>
            {(!isCollapsed || isMobileMenuOpen) && (
              <motion.div 
                initial={{ opacity: 0, width: 0 }}
                animate={{ opacity: 1, width: "auto" }}
                exit={{ opacity: 0, width: 0 }}
                transition={{ duration: 0.2, ease: "easeInOut" }}
                className="overflow-hidden whitespace-nowrap"
              >
                <span className="text-lg font-bold tracking-tight text-foreground block">
                  SecureVision AI
                </span>
                <span className="text-[10px] uppercase tracking-wider text-muted-foreground block mt-0.5 font-semibold">
                  Enterprise Cybersecurity
                </span>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
        
        {/* Mobile Close Button */}
        <button 
          className="lg:hidden text-muted-foreground hover:text-foreground transition-colors"
          onClick={() => setIsMobileMenuOpen(false)}
        >
          <X className="h-6 w-6" />
        </button>
      </div>

      <div className="flex flex-1 flex-col overflow-y-auto py-6">
        <nav className="flex-1 space-y-1.5 px-3">
          {navigation.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.name}
                href={item.href}
                onClick={() => setIsMobileMenuOpen(false)}
                className={cn(
                  isActive
                    ? "bg-primary/10 text-primary font-semibold"
                    : "text-muted-foreground hover:bg-muted hover:text-foreground font-medium",
                  "group relative flex items-center rounded-lg px-3 py-2.5 text-sm transition-all duration-200 overflow-hidden"
                )}
                title={isCollapsed && !isMobileMenuOpen ? item.name : undefined}
              >
                {/* Active Indicator Line */}
                {isActive && (
                  <motion.div 
                    layoutId="activeNavIndicator"
                    className="absolute left-0 top-0 bottom-0 w-1 bg-primary rounded-r-full"
                  />
                )}
                
                <item.icon
                  className={cn(
                    isActive ? "text-primary" : "text-muted-foreground group-hover:text-foreground",
                    "h-5 w-5 shrink-0 transition-colors duration-200 relative z-10"
                  )}
                  aria-hidden="true"
                />
                
                <AnimatePresence initial={false}>
                  {(!isCollapsed || isMobileMenuOpen) && (
                    <motion.span 
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: -10 }}
                      transition={{ duration: 0.2 }}
                      className="ml-3 truncate relative z-10"
                    >
                      {item.name}
                    </motion.span>
                  )}
                </AnimatePresence>
              </Link>
            );
          })}
        </nav>

        <div className="mt-auto px-3 space-y-1.5 pt-6 border-t border-border mt-6 mx-3">
          <Link
            href="/dashboard/profile"
            onClick={() => setIsMobileMenuOpen(false)}
            className={cn(
              pathname === "/dashboard/profile"
                ? "bg-primary/10 text-primary font-semibold"
                : "text-muted-foreground hover:bg-muted hover:text-foreground font-medium",
              "group relative flex items-center rounded-lg px-3 py-2.5 text-sm transition-all duration-200 overflow-hidden"
            )}
            title={isCollapsed && !isMobileMenuOpen ? "Profile" : undefined}
          >
            {pathname === "/dashboard/profile" && (
              <motion.div layoutId="activeNavIndicator" className="absolute left-0 top-0 bottom-0 w-1 bg-primary rounded-r-full" />
            )}
            <User className={cn(pathname === "/dashboard/profile" ? "text-primary" : "text-muted-foreground group-hover:text-foreground", "h-5 w-5 shrink-0 transition-colors")} />
            <AnimatePresence initial={false}>
              {(!isCollapsed || isMobileMenuOpen) && (
                <motion.span initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="ml-3 truncate">Profile</motion.span>
              )}
            </AnimatePresence>
          </Link>

          <Link
            href="/dashboard/settings"
            onClick={() => setIsMobileMenuOpen(false)}
            className={cn(
              pathname === "/dashboard/settings"
                ? "bg-primary/10 text-primary font-semibold"
                : "text-muted-foreground hover:bg-muted hover:text-foreground font-medium",
              "group relative flex items-center rounded-lg px-3 py-2.5 text-sm transition-all duration-200 overflow-hidden"
            )}
            title={isCollapsed && !isMobileMenuOpen ? "Settings" : undefined}
          >
            {pathname === "/dashboard/settings" && (
              <motion.div layoutId="activeNavIndicator" className="absolute left-0 top-0 bottom-0 w-1 bg-primary rounded-r-full" />
            )}
            <Settings className={cn(pathname === "/dashboard/settings" ? "text-primary" : "text-muted-foreground group-hover:text-foreground", "h-5 w-5 shrink-0 transition-colors")} />
            <AnimatePresence initial={false}>
              {(!isCollapsed || isMobileMenuOpen) && (
                <motion.span initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="ml-3 truncate">Settings</motion.span>
              )}
            </AnimatePresence>
          </Link>
        </div>
      </div>

      <div className="p-4 border-t border-border bg-muted/30">
        <div className={cn("flex items-center", isCollapsed && !isMobileMenuOpen ? "justify-center" : "justify-between")}>
          <AnimatePresence initial={false}>
            {(!isCollapsed || isMobileMenuOpen) && (
              <motion.div 
                initial={{ opacity: 0, width: 0 }}
                animate={{ opacity: 1, width: "auto" }}
                exit={{ opacity: 0, width: 0 }}
                className="flex items-center gap-3 overflow-hidden whitespace-nowrap"
              >
                <div className="h-9 w-9 rounded-full bg-primary/20 flex items-center justify-center border border-primary/30 shrink-0">
                  <User className="h-4 w-4 text-primary" />
                </div>
                <div className="flex flex-col">
                  <span className="text-sm font-semibold text-foreground">{user.full_name || "Administrator"}</span>
                  <span className="text-[11px] text-muted-foreground">{user.email || "admin@securevision.ai"}</span>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
          
          <button 
            onClick={handleLogout}
            className="p-2 text-muted-foreground hover:text-red-500 hover:bg-red-500/10 rounded-lg transition-all duration-200 shrink-0"
            title="Logout"
          >
            <LogOut className="h-5 w-5" />
          </button>
        </div>
      </div>

      {/* Desktop Collapse Toggle */}
      <button 
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="hidden lg:flex absolute -right-3.5 top-20 bg-card border border-border rounded-full p-1.5 text-muted-foreground hover:text-foreground hover:border-primary transition-all duration-200 shadow-md z-20"
        title={isCollapsed ? "Expand Sidebar" : "Collapse Sidebar"}
      >
        <motion.div
          animate={{ rotate: isCollapsed ? 180 : 0 }}
          transition={{ duration: 0.3, ease: "easeInOut" }}
        >
          <ChevronLeft className="h-4 w-4" />
        </motion.div>
      </button>
    </>
  );

  return (
    <>
      {/* Desktop Sidebar */}
      <motion.div 
        animate={{ width: isCollapsed ? 80 : 260 }}
        transition={{ duration: 0.3, ease: "easeInOut" }}
        className="hidden lg:flex h-full flex-col border-r border-border bg-card relative z-20 shadow-md transition-colors duration-200"
      >
        <SidebarContent />
      </motion.div>

      {/* Mobile Sidebar */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div 
            initial={{ x: "-100%" }}
            animate={{ x: 0 }}
            exit={{ x: "-100%" }}
            transition={{ type: "spring", bounce: 0, duration: 0.4 }}
            className="fixed inset-y-0 left-0 z-50 w-72 flex flex-col bg-card border-r border-border shadow-2xl lg:hidden"
          >
            <SidebarContent />
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
