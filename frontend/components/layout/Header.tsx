'use client';

import { Search, Bell, User, LogOut, Settings as SettingsIcon, Shield, Menu } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useRouter } from 'next/navigation';
import { useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { useUser } from "@/context/UserContext";
import { ThemeToggle } from "@/components/common/ThemeToggle";

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
    <header className="flex h-16 shrink-0 items-center gap-x-4 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80 px-4 shadow-sm sm:gap-x-6 sm:px-6 lg:px-8 z-30 relative sticky top-0 transition-colors duration-200">
      <div className="flex flex-1 gap-x-4 self-stretch justify-between items-center">
        
        {/* Left side: Hamburger (Mobile), Org Name & Search */}
        <div className="flex items-center gap-x-4 flex-1">
          {onMenuClick && (
            <Button 
              variant="ghost" 
              size="icon" 
              onClick={onMenuClick} 
              className="lg:hidden text-muted-foreground hover:text-foreground"
            >
              <Menu className="h-6 w-6" />
            </Button>
          )}

          <div className="hidden sm:flex items-center gap-2 pr-6 border-r border-border">
            <Shield className="h-5 w-5 text-primary" />
            <span className="font-semibold text-sm text-foreground">SecureVision Workspace</span>
          </div>

          <form className="relative flex flex-1 max-w-md hidden md:flex group" action="#" method="GET" onSubmit={(e) => e.preventDefault()}>
            <label htmlFor="search-field" className="sr-only">Search</label>
            <Search
              className="pointer-events-none absolute inset-y-0 left-0 h-full w-5 text-muted-foreground ml-3 group-focus-within:text-primary transition-colors"
              aria-hidden="true"
            />
            <Input
              id="search-field"
              className="block h-9 w-full border border-border bg-muted/50 py-2 pl-10 pr-3 text-sm text-foreground placeholder:text-muted-foreground focus:border-primary focus:ring-1 focus:ring-primary rounded-full transition-all duration-200 shadow-inner"
              placeholder="Search resources, threats..."
              type="search"
              name="search"
            />
          </form>
        </div>

        {/* Right side: Actions & Profile */}
        <div className="flex items-center gap-x-2 sm:gap-x-4 lg:gap-x-5 pl-2">
          {/* Notifications */}
          <div className="relative">
            <button 
              type="button" 
              className="p-2 text-muted-foreground hover:text-foreground hover:bg-muted/60 transition-colors rounded-full relative"
              title="Notifications"
            >
              <span className="sr-only">View notifications</span>
              <Bell className="h-5 w-5" aria-hidden="true" />
              {/* Notification Badge */}
              <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-red-500 ring-2 ring-background" />
            </button>
          </div>
          
          {/* Light / Dark Mode Toggle Button in the Top Bar */}
          <ThemeToggle />

          <div className="hidden lg:block lg:h-6 lg:w-px lg:bg-border mx-1" aria-hidden="true" />

          {/* Profile Dropdown */}
          <div className="relative">
            <button 
              type="button" 
              className="flex items-center gap-x-3 p-1 rounded-full hover:bg-muted/60 transition-colors focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 focus:ring-offset-background"
              onClick={() => setIsProfileOpen(!isProfileOpen)}
            >
              <span className="sr-only">Open user menu</span>
              <div className="h-8 w-8 rounded-full bg-primary/20 flex items-center justify-center border border-primary/40 shadow-sm">
                <User className="h-4 w-4 text-primary" />
              </div>
            </button>

            <AnimatePresence>
              {isProfileOpen && (
                <motion.div 
                  initial={{ opacity: 0, y: 10, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: 10, scale: 0.95 }}
                  transition={{ duration: 0.2 }}
                  className="absolute right-0 z-50 mt-3 w-56 origin-top-right rounded-xl bg-card py-2 shadow-xl ring-1 ring-border focus:outline-none overflow-hidden"
                >
                  <div className="px-4 py-3 border-b border-border mb-1">
                    <p className="text-sm font-medium text-foreground">{user.full_name || "Administrator"}</p>
                    <p className="text-xs text-muted-foreground truncate">{user.email || "admin@securevision.ai"}</p>
                  </div>
                  <Link 
                    href="/dashboard/profile" 
                    onClick={() => setIsProfileOpen(false)}
                    className="block px-4 py-2 text-sm text-foreground hover:bg-primary/10 transition-colors flex items-center gap-3"
                  >
                    <User className="h-4 w-4 text-muted-foreground" />
                    Profile
                  </Link>
                  <Link 
                    href="/dashboard/settings" 
                    onClick={() => setIsProfileOpen(false)}
                    className="block px-4 py-2 text-sm text-foreground hover:bg-primary/10 transition-colors flex items-center gap-3"
                  >
                    <SettingsIcon className="h-4 w-4 text-muted-foreground" />
                    Settings
                  </Link>
                  <button 
                    onClick={() => {
                      setIsProfileOpen(false);
                      handleLogout();
                    }}
                    className="w-full text-left px-4 py-2 text-sm text-red-500 hover:bg-red-500/10 transition-colors flex items-center gap-3 border-t border-border mt-1 pt-2"
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
