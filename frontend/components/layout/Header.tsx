'use client';

import { Search, Bell, Sun, User, LogOut, Settings as SettingsIcon, Shield, Menu } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useRouter } from 'next/navigation';
import { useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { useUser } from "@/context/UserContext";

interface HeaderProps {
  onMenuClick?: () => void;
}

export function Header({ onMenuClick }: HeaderProps) {
  const router = useRouter();
  const { user, logout } = useUser();
  const [isProfileOpen, setIsProfileOpen] = useState(false);

  const handleLogout = async () => {
    await logout();
  };

  return (
    <header className="flex h-16 shrink-0 items-center gap-x-4 border-b border-[#334155] bg-[#020817]/95 backdrop-blur supports-[backdrop-filter]:bg-[#020817]/80 px-4 shadow-sm sm:gap-x-6 sm:px-6 lg:px-8 z-30 relative sticky top-0">
      <div className="flex flex-1 gap-x-4 self-stretch justify-between items-center">
        
        {/* Left side: Hamburger (Mobile), Org Name & Search */}
        <div className="flex items-center gap-x-4 flex-1">
          {onMenuClick && (
            <Button 
              variant="ghost" 
              size="icon" 
              onClick={onMenuClick} 
              className="lg:hidden text-muted-foreground hover:text-[#F8FAFC]"
            >
              <Menu className="h-6 w-6" />
            </Button>
          )}

          <div className="hidden sm:flex items-center gap-2 pr-6 border-r border-[#334155]/50">
            <Shield className="h-5 w-5 text-[#2563EB]" />
            <span className="font-semibold text-sm text-[#F8FAFC]">SecureVision Workspace</span>
          </div>

          <form className="relative flex flex-1 max-w-md hidden md:flex group" action="#" method="GET" onSubmit={(e) => e.preventDefault()}>
            <label htmlFor="search-field" className="sr-only">Search</label>
            <Search
              className="pointer-events-none absolute inset-y-0 left-0 h-full w-5 text-muted-foreground ml-3 group-focus-within:text-[#2563EB] transition-colors"
              aria-hidden="true"
            />
            <Input
              id="search-field"
              className="block h-9 w-full border border-[#334155]/60 bg-[#111827]/50 py-2 pl-10 pr-3 text-sm text-[#F8FAFC] placeholder:text-muted-foreground focus:border-[#2563EB] focus:ring-1 focus:ring-[#2563EB] rounded-full transition-all duration-200 shadow-inner"
              placeholder="Search resources, threats..."
              type="search"
              name="search"
            />
          </form>
        </div>

        {/* Right side: Actions & Profile */}
        <div className="flex items-center gap-x-3 sm:gap-x-5 lg:gap-x-6 pl-4">
          <div className="relative">
            <button type="button" className="p-2 text-muted-foreground hover:text-[#F8FAFC] hover:bg-white/5 transition-colors rounded-full relative">
              <span className="sr-only">View notifications</span>
              <Bell className="h-5 w-5" aria-hidden="true" />
              {/* Notification Badge */}
              <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-red-500 ring-2 ring-[#020817]" />
            </button>
          </div>
          
          <button type="button" className="p-2 text-muted-foreground hover:text-[#F8FAFC] hover:bg-white/5 transition-colors rounded-full hidden sm:block">
            <span className="sr-only">Toggle theme</span>
            <Sun className="h-5 w-5" aria-hidden="true" />
          </button>

          <div className="hidden lg:block lg:h-6 lg:w-px lg:bg-[#334155]/50 mx-1" aria-hidden="true" />

          {/* Profile Dropdown */}
          <div className="relative">
            <button 
              type="button" 
              className="flex items-center gap-x-3 p-1 rounded-full hover:bg-white/5 transition-colors focus:outline-none focus:ring-2 focus:ring-[#2563EB] focus:ring-offset-2 focus:ring-offset-[#020817]"
              onClick={() => setIsProfileOpen(!isProfileOpen)}
            >
              <span className="sr-only">Open user menu</span>
              <div className="h-8 w-8 rounded-full bg-[#2563EB]/20 flex items-center justify-center border border-[#2563EB]/50 shadow-[0_0_10px_rgba(37,99,235,0.2)]">
                <User className="h-4 w-4 text-[#2563EB]" />
              </div>
            </button>

            <AnimatePresence>
              {isProfileOpen && (
                <motion.div 
                  initial={{ opacity: 0, y: 10, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: 10, scale: 0.95 }}
                  transition={{ duration: 0.2 }}
                  className="absolute right-0 z-50 mt-3 w-56 origin-top-right rounded-xl bg-[#111827] py-2 shadow-[0_10px_40px_-10px_rgba(0,0,0,0.5)] ring-1 ring-[#334155] focus:outline-none overflow-hidden"
                >
                  <div className="px-4 py-3 border-b border-[#334155]/50 mb-1">
                    <p className="text-sm font-medium text-[#F8FAFC]">{user.full_name || "Administrator"}</p>
                    <p className="text-xs text-muted-foreground truncate">{user.email || "admin@securevision.ai"}</p>
                  </div>
                  <Link href="/dashboard/profile" className="block px-4 py-2 text-sm text-[#F8FAFC] hover:bg-[#2563EB]/10 transition-colors flex items-center gap-3">
                    <User className="h-4 w-4 text-muted-foreground" />
                    Profile
                  </Link>
                  <Link href="/dashboard/settings" className="block px-4 py-2 text-sm text-[#F8FAFC] hover:bg-[#2563EB]/10 transition-colors flex items-center gap-3">
                    <SettingsIcon className="h-4 w-4 text-muted-foreground" />
                    Settings
                  </Link>
                  <button 
                    onClick={handleLogout}
                    className="w-full text-left px-4 py-2 text-sm text-red-400 hover:bg-red-500/10 transition-colors flex items-center gap-3 border-t border-[#334155]/50 mt-1 pt-2"
                  >
                    <LogOut className="h-4 w-4" />
                    Logout
                  </button>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </header>
  );
}
