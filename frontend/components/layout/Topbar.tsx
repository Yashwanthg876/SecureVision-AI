'use client';
import { Search, Bell, User, LogOut } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useRouter } from 'next/navigation';
import api from '@/lib/api';
import { ThemeToggle } from "@/components/common/ThemeToggle";

export function Topbar() {
  const router = useRouter();

  const handleLogout = async () => {
    try {
      await api.post('/auth/logout');
      router.push('/login');
    } catch (error) {
      console.error('Logout failed', error);
      // Fallback redirect
      router.push('/login');
    }
  };

  return (
    <header className="flex h-16 shrink-0 items-center gap-x-4 border-b border-border bg-background px-4 shadow-sm sm:gap-x-6 sm:px-6 lg:px-8 transition-colors duration-200">
      <div className="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
        <form className="relative flex flex-1" action="#" method="GET">
          <label htmlFor="search-field" className="sr-only">
            Search
          </label>
          <Search
            className="pointer-events-none absolute inset-y-0 left-0 h-full w-5 text-muted-foreground"
            aria-hidden="true"
          />
          <Input
            id="search-field"
            className="block h-full w-full border-0 bg-transparent py-0 pl-8 pr-0 text-foreground placeholder:text-muted-foreground focus:ring-0 sm:text-sm shadow-none focus-visible:ring-0 focus-visible:ring-offset-0"
            placeholder="Search resources, threats, devices..."
            type="search"
            name="search"
          />
        </form>
        <div className="flex items-center gap-x-4 lg:gap-x-6">
          <button type="button" className="-m-2.5 p-2.5 text-muted-foreground hover:text-foreground">
            <span className="sr-only">View notifications</span>
            <Bell className="h-5 w-5" aria-hidden="true" />
          </button>
          
          {/* Light / Dark Mode Button in Topbar */}
          <ThemeToggle />

          <div className="hidden lg:block lg:h-6 lg:w-px lg:bg-border" aria-hidden="true" />

          {/* Profile Dropdown Simulation */}
          <div className="flex items-center gap-x-4">
            <span className="sr-only">Your profile</span>
            <div className="h-8 w-8 rounded-full bg-primary/20 flex items-center justify-center">
              <User className="h-4 w-4 text-primary" />
            </div>
            <span className="hidden lg:flex lg:items-center">
              <span className="text-sm font-semibold leading-6 text-foreground" aria-hidden="true">
                Admin
              </span>
            </span>
            <Button variant="outline" size="sm" onClick={handleLogout} className="ml-2 h-8 border-border hover:bg-muted">
              <LogOut className="h-4 w-4 sm:mr-2" />
              <span className="hidden sm:inline">Logout</span>
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
}
