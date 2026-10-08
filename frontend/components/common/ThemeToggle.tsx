'use client';

import React from 'react';
import { Sun, Moon } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useTheme } from '@/context/ThemeContext';
import { cn } from '@/lib/utils';

interface ThemeToggleProps {
  className?: string;
  showLabel?: boolean;
}

export function ThemeToggle({ className, showLabel = false }: ThemeToggleProps) {
  const { theme, toggleTheme, mounted } = useTheme();

  // If not yet mounted on client, render a placeholder with consistent dimensions
  if (!mounted) {
    return (
      <button
        type="button"
        className={cn(
          "relative flex items-center justify-center h-9 w-9 rounded-full border border-border/60 bg-muted/40 text-muted-foreground transition-colors",
          className
        )}
        aria-label="Toggle theme"
        disabled
      >
        <Sun className="h-4 w-4" />
      </button>
    );
  }

  const isDark = theme === 'dark';

  return (
    <button
      type="button"
      onClick={toggleTheme}
      className={cn(
        "group relative flex items-center gap-2 rounded-full p-2 text-sm font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2",
        isDark
          ? "border border-border/70 bg-slate-900/60 text-amber-400 hover:bg-slate-800 hover:text-amber-300 hover:border-amber-400/40 shadow-[0_0_12px_rgba(251,191,36,0.15)]"
          : "border border-slate-300 bg-white/90 text-slate-700 hover:bg-slate-100 hover:text-indigo-600 hover:border-indigo-400/50 shadow-sm",
        showLabel ? "px-3 py-1.5" : "h-9 w-9 justify-center",
        className
      )}
      title={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
      aria-label={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
    >
      <AnimatePresence mode="wait" initial={false}>
        {isDark ? (
          <motion.div
            key="sun"
            initial={{ rotate: -90, scale: 0.6, opacity: 0 }}
            animate={{ rotate: 0, scale: 1, opacity: 1 }}
            exit={{ rotate: 90, scale: 0.6, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="flex items-center justify-center"
          >
            <Sun className="h-4 w-4 transition-transform group-hover:rotate-45 duration-300" />
          </motion.div>
        ) : (
          <motion.div
            key="moon"
            initial={{ rotate: 90, scale: 0.6, opacity: 0 }}
            animate={{ rotate: 0, scale: 1, opacity: 1 }}
            exit={{ rotate: -90, scale: 0.6, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="flex items-center justify-center"
          >
            <Moon className="h-4 w-4 transition-transform group-hover:-rotate-12 duration-300 text-indigo-600" />
          </motion.div>
        )}
      </AnimatePresence>

      {showLabel && (
        <span className="text-xs font-semibold capitalize select-none">
          {isDark ? "Light Mode" : "Dark Mode"}
        </span>
      )}
    </button>
  );
}
