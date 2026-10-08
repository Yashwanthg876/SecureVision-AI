'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Shield, Menu, X, ArrowRight, Activity, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ThemeToggle } from '@/components/common/ThemeToggle';

export function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? 'bg-background/85 backdrop-blur-md border-b border-border/60 py-3 shadow-md'
          : 'bg-transparent py-5'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          {/* Brand Logo */}
          <Link href="/" className="flex items-center gap-3 group">
            <div className="relative p-2.5 rounded-xl bg-primary/10 border border-primary/30 group-hover:border-primary/60 transition-all duration-300 shadow-[0_0_20px_rgba(37,99,235,0.25)]">
              <Shield className="w-6 h-6 text-primary group-hover:scale-110 transition-transform duration-300" />
              <div className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-emerald-500 rounded-full animate-ping" />
              <div className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-emerald-500 rounded-full" />
            </div>
            <div className="flex flex-col">
              <div className="flex items-center gap-2">
                <span className="font-bold text-xl tracking-tight text-foreground group-hover:text-primary transition-colors">
                  SecureVision
                </span>
                <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-primary/15 text-primary border border-primary/30 flex items-center gap-1">
                  <Sparkles className="w-3 h-3" /> AI
                </span>
              </div>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-8">
            <a href="#features" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
              Features
            </a>
            <a href="#ai-engines" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
              AI Subsystems
            </a>
            <a href="#demo" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
              Interactive Demo
            </a>
            <a href="#pricing" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
              Free Access
            </a>
          </nav>

          {/* Right Action Items & Status */}
          <div className="hidden md:flex items-center gap-3 lg:gap-4">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs font-medium text-emerald-500">
              <Activity className="w-3.5 h-3.5 animate-pulse" />
              <span>AI Defense Operational</span>
            </div>

            {/* Light Mode / Dark Mode Toggle Button */}
            <ThemeToggle />

            <Link href="/login">
              <Button variant="ghost" className="text-sm font-medium text-muted-foreground hover:text-foreground">
                Sign In
              </Button>
            </Link>

            <Link href="/dashboard">
              <Button className="bg-primary hover:bg-primary/90 text-white font-medium shadow-[0_0_20px_rgba(37,99,235,0.4)] hover:shadow-[0_0_25px_rgba(37,99,235,0.6)] transition-all gap-2">
                Launch Platform
                <ArrowRight className="w-4 h-4" />
              </Button>
            </Link>
          </div>

          {/* Mobile Menu & Theme Toggle */}
          <div className="flex items-center gap-2 md:hidden">
            <ThemeToggle />
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted/50"
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-card/95 backdrop-blur-xl border-b border-border px-4 pt-4 pb-6 mt-3 space-y-4 animate-in slide-in-from-top-4 duration-200 shadow-xl">
          <nav className="flex flex-col space-y-3">
            <a
              href="#features"
              onClick={() => setMobileMenuOpen(false)}
              className="text-base font-medium text-foreground hover:text-primary py-2 border-b border-border/40"
            >
              Features
            </a>
            <a
              href="#ai-engines"
              onClick={() => setMobileMenuOpen(false)}
              className="text-base font-medium text-foreground hover:text-primary py-2 border-b border-border/40"
            >
              AI Subsystems
            </a>
            <a
              href="#demo"
              onClick={() => setMobileMenuOpen(false)}
              className="text-base font-medium text-foreground hover:text-primary py-2 border-b border-border/40"
            >
              Interactive Demo
            </a>
            <a
              href="#pricing"
              onClick={() => setMobileMenuOpen(false)}
              className="text-base font-medium text-foreground hover:text-primary py-2 border-b border-border/40"
            >
              Free Access
            </a>
          </nav>
          <div className="pt-2 flex flex-col gap-3">
            <div className="flex items-center justify-between px-1 py-2 border-b border-border/40">
              <span className="text-sm font-medium text-muted-foreground">Theme Mode</span>
              <ThemeToggle showLabel />
            </div>
            <Link href="/login" onClick={() => setMobileMenuOpen(false)}>
              <Button variant="outline" className="w-full justify-center">
                Sign In
              </Button>
            </Link>
            <Link href="/dashboard" onClick={() => setMobileMenuOpen(false)}>
              <Button className="w-full justify-center bg-primary text-white">
                Launch Platform
              </Button>
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
