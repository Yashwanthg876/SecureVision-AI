'use client';

import { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { Eye, EyeOff, Loader2, Mail, Lock, Sparkles, AlertCircle, ArrowRight } from 'lucide-react';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import api from '@/lib/api';

export function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const requestedPath = searchParams.get('next');
  const destination = requestedPath?.startsWith('/') && !requestedPath.startsWith('//') ? requestedPath : '/dashboard';
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await api.post('/auth/login', { email, password });
      router.push(destination);
    } catch (err: any) {
      setError(err.response?.data?.error || err.response?.data?.detail || 'An error occurred during login. Check credentials and backend server.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoLogin = async () => {
    setIsLoading(true);
    setError('');
    try {
      await api.post('/auth/demo-login');
      router.push(destination);
      router.refresh();
    } catch (err: any) {
      setError(err.response?.data?.error || err.response?.data?.detail || 'Demo login is unavailable. Please register or sign in.');
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full bg-slate-900/90 border-slate-800 shadow-[0_10px_40px_rgba(0,0,0,0.6)] backdrop-blur-xl">
      <CardContent className="pt-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          
          {/* Email Input */}
          <div className="space-y-2">
            <Label htmlFor="email" className="text-slate-300 text-sm font-medium">
              Email Address
            </Label>
            <div className="relative">
              <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
              <Input
                id="email"
                type="email"
                placeholder="admin@enterprise.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="bg-slate-950/80 border-slate-800 focus:border-primary pl-10 text-white placeholder-slate-500 rounded-xl"
              />
            </div>
          </div>

          {/* Password Input */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="password" className="text-slate-300 text-sm font-medium">
                Password
              </Label>
              <Link href="/forgot-password" className="text-xs font-medium text-primary hover:text-primary/80 transition-colors">
                Forgot password?
              </Link>
            </div>
            <div className="relative">
              <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
              <Input
                id="password"
                type={showPassword ? 'text' : 'password'}
                placeholder="••••••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="bg-slate-950/80 border-slate-800 focus:border-primary pl-10 pr-10 text-white placeholder-slate-500 rounded-xl"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300 transition-colors"
              >
                {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
          </div>

          {/* Remember Me */}
          <div className="flex items-center space-x-2 pt-1">
            <input
              type="checkbox"
              id="remember"
              className="rounded border-slate-800 bg-slate-950 text-primary focus:ring-primary h-4 w-4 accent-primary cursor-pointer"
            />
            <Label htmlFor="remember" className="text-xs text-slate-400 font-normal cursor-pointer select-none">
              Remember me for 30 days
            </Label>
          </div>

          {/* Error Message */}
          {error && (
            <div className="p-3 rounded-xl bg-red-500/10 border border-red-500/20 flex items-center gap-2 text-xs text-red-400">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* Sign In Button */}
          <Button
            type="submit"
            className="w-full bg-primary hover:bg-primary/90 text-white py-2.5 rounded-xl font-semibold shadow-[0_0_20px_rgba(37,99,235,0.4)] transition-all"
            disabled={isLoading}
          >
            {isLoading ? (
              <span className="flex items-center justify-center gap-2">
                <Loader2 className="h-4 w-4 animate-spin" /> Verifying Credentials...
              </span>
            ) : (
              'Sign In to Portal'
            )}
          </Button>
        </form>

        {/* Divider */}
        <div className="relative my-6 text-center">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-slate-800" />
          </div>
          <div className="relative inline-block px-3 bg-slate-900 text-xs text-slate-500 font-mono">
            OR PREVIEW DEMO
          </div>
        </div>

        {/* Quick Demo Login Button */}
        <Button
          type="button"
          onClick={handleDemoLogin}
          disabled={isLoading}
          variant="outline"
          className="w-full border-slate-800 bg-slate-950/90 hover:bg-slate-800 text-slate-200 py-2.5 rounded-xl font-medium flex items-center justify-center gap-2 group"
        >
          <Sparkles className="w-4 h-4 text-amber-400 group-hover:rotate-12 transition-transform" />
          <span>Try Quick Demo Access</span>
          <ArrowRight className="w-4 h-4 text-slate-400 group-hover:translate-x-1 transition-transform" />
        </Button>
      </CardContent>

      <CardFooter className="flex justify-center border-t border-slate-800/80 py-4 bg-slate-950/40 rounded-b-xl">
        <p className="text-xs text-slate-400">
          Don't have an account?{' '}
          <Link href="/register" className="font-semibold text-primary hover:underline">
            Register here
          </Link>
        </p>
      </CardFooter>
    </Card>
  );
}
