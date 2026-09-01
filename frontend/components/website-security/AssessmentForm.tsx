'use client';

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search, Shield, ShieldAlert, Info, Loader2 } from "lucide-react";
import { motion } from "framer-motion";
import api from "@/lib/api";

interface AssessmentFormProps {
  onScanStart?: (url: string) => void;
  onScanSuccess?: (data: any) => void;
  onScanError?: (errorMsg: string) => void;
  isScanning?: boolean;
}

export function AssessmentForm({ onScanStart, onScanSuccess, onScanError, isScanning = false }: AssessmentFormProps) {
  const [url, setUrl] = useState("");
  const [error, setError] = useState("");
  const [isHoveringDisabled, setIsHoveringDisabled] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = url.trim();
    if (!trimmed) {
      setError("Please enter a valid URL.");
      return;
    }

    let targetUrl = trimmed;
    try {
      if (!targetUrl.startsWith('http://') && !targetUrl.startsWith('https://')) {
        targetUrl = `https://${targetUrl}`;
      }
      new URL(targetUrl);
      setError("");
    } catch {
      setError("Invalid URL format.");
      return;
    }

    if (onScanStart) {
      onScanStart(targetUrl);
    }

    try {
      const response = await api.post('/assessment/scan', { url: targetUrl });
      const scanData = response.data?.data || response.data;
      if (typeof window !== 'undefined') {
        window.dispatchEvent(new Event('assessment-scan-completed'));
      }
      if (onScanSuccess) {
        onScanSuccess(scanData);
      }
    } catch (err: any) {
      const message = err.response?.data?.error || err.response?.data?.detail || "Assessment failed. Please try again.";
      onScanError?.(message);
      return;
      
      // Calculate dynamic domain-specific metrics based on domain hash
      const domain = new URL(targetUrl).hostname.toLowerCase();
      let charSum = 0;
      for (let i = 0; i < domain.length; i++) {
        charSum += domain.charCodeAt(i);
      }
      
      const overallScore = 65 + (charSum % 31); // Score between 65 and 95
      const sslScore = 70 + ((charSum * 3) % 29);
      const headersScore = 55 + ((charSum * 7) % 40);
      const dnsScore = 80 + ((charSum * 11) % 20);
      const techScore = 70 + ((charSum * 13) % 25);
      
      const riskLevel = overallScore >= 85 ? "Low" : overallScore >= 72 ? "Medium" : "High";
      
      const knownIssuers = [
        "Google Trust Services LLC",
        "DigiCert Inc",
        "Cloudflare Inc ECC CA-3",
        "Let's Encrypt Authority X3",
        "Amazon RSA 2048 M01"
      ];
      const issuer = knownIssuers[charSum % knownIssuers.length];
      
      const servers = ["cloudflare", "nginx/1.24.0", "Apache/2.4.52", "gws", "AWS CloudFront"];
      const serverName = servers[(charSum * 5) % servers.length];

      const fallbackResult = {
        id: `scan-${Date.now()}`,
        target_url: targetUrl,
        domain: domain,
        overall_score: overallScore,
        risk_level: riskLevel,
        ssl_score: sslScore,
        headers_score: headersScore,
        dns_score: dnsScore,
        tech_score: techScore,
        recommendation_count: overallScore < 85 ? 3 : 1,
        critical_count: overallScore < 70 ? 1 : 0,
        high_count: overallScore < 78 ? 1 : 0,
        medium_count: overallScore < 85 ? 1 : 0,
        low_count: 1,
        scan_duration: 800 + (charSum % 700),
        status: "Completed",
        ssl_tls: {
          is_valid: true,
          issuer: issuer,
          subject: domain,
          expires_in_days: 30 + (charSum % 330),
          protocol: charSum % 2 === 0 ? "TLSv1.3" : "TLSv1.2",
          error: null
        },
        http_headers: {
          strict_transport_security: charSum % 2 === 0,
          content_security_policy: charSum % 3 === 0,
          x_frame_options: charSum % 2 === 0,
          x_content_type_options: true,
          missing_headers: charSum % 3 !== 0 ? ["Content-Security-Policy"] : []
        },
        dns: {
          has_spf: charSum % 2 === 0,
          has_dmarc: charSum % 4 !== 0,
          mx_records: 1 + (charSum % 4),
          txt_records: 2 + (charSum % 5)
        },
        whois: {
          registrar: "Domain Registrar LLC",
          creation_date: "2018-05-14",
          expiration_date: "2029-05-14"
        },
        technology: {
          server: serverName,
          x_powered_by: charSum % 2 === 0 ? "Next.js / Vercel" : "React / Node.js"
        },
        recommendations: [
          ...(overallScore < 85 ? [{
            category: "HTTP Security",
            title: `Content Security Policy Optimization for ${domain}`,
            description: `Review origin permissions and script execution sources on ${domain}.`,
            severity: overallScore < 72 ? "High" : "Medium",
            recommendation: "Implement strict Content-Security-Policy headers to prevent unauthorized script injections.",
            reference: "OWASP Secure Headers Project"
          }] : []),
          {
            category: "Information Disclosure",
            title: `Server Header Banner Exposure on ${domain}`,
            description: `The web server identifies as '${serverName}'.`,
            severity: "Low",
            recommendation: "Suppress software version banners in web server configuration files.",
            reference: "CWE-200: Information Exposure"
          }
        ],
        created_at: new Date().toISOString()
      };

      setTimeout(() => {
        if (onScanSuccess) {
          onScanSuccess(fallbackResult);
        }
      }, 1200);
    }
  };

  return (
    <Card className="bg-[#111827] border-[#334155] shadow-lg">
      <CardHeader className="pb-4 border-b border-[#334155]/50">
        <CardTitle className="text-lg font-semibold text-[#F8FAFC] flex items-center gap-2">
          <Search className="h-5 w-5 text-[#2563EB]" />
          Initiate Security Assessment
        </CardTitle>
        <CardDescription>Enter a domain or URL to run a comprehensive passive security analysis.</CardDescription>
      </CardHeader>
      <CardContent className="pt-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label htmlFor="url" className="text-sm font-medium text-[#F8FAFC]">Target URL</label>
            <div className="flex gap-3">
              <div className="relative flex-1">
                <GlobeIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                <Input
                  id="url"
                  placeholder="e.g., https://example.com or example.com"
                  value={url}
                  disabled={isScanning}
                  onChange={(e) => { setUrl(e.target.value); setError(""); }}
                  className={`pl-10 h-12 bg-[#020817] ${error ? 'border-red-500' : 'border-[#334155]/60'} focus:border-[#2563EB] text-[#F8FAFC] transition-colors`}
                />
              </div>
              <Button 
                type="submit" 
                disabled={isScanning}
                className="h-12 px-8 bg-[#2563EB] hover:bg-[#2563EB]/90 text-white font-medium shadow-md shadow-[#2563EB]/20 transition-all disabled:opacity-50"
              >
                {isScanning ? (
                  <span className="flex items-center gap-2">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Scanning...
                  </span>
                ) : (
                  "Run Assessment"
                )}
              </Button>
            </div>
            {error && <p className="text-sm text-red-500 mt-1">{error}</p>}
          </div>

          <div className="space-y-3">
            <label className="text-sm font-medium text-[#F8FAFC]">Assessment Mode</label>
            <div className="grid sm:grid-cols-2 gap-4">
              
              {/* Passive Assessment (Enabled) */}
              <label className="relative flex cursor-pointer rounded-lg border border-[#2563EB] bg-[#2563EB]/10 p-4 shadow-sm focus:outline-none">
                <input type="radio" name="mode" value="passive" className="sr-only" defaultChecked />
                <span className="flex flex-1">
                  <span className="flex flex-col">
                    <span className="block text-sm font-semibold text-[#F8FAFC] flex items-center gap-2">
                      <Shield className="h-4 w-4 text-[#2563EB]" />
                      Passive Assessment
                    </span>
                    <span className="mt-1 flex items-center text-xs text-muted-foreground">
                      Safe, non-intrusive public data gathering.
                    </span>
                  </span>
                </span>
                <span className="pointer-events-none absolute -inset-px rounded-lg border-2 border-[#2563EB]" aria-hidden="true" />
              </label>

              {/* Authorized Active Scan (Disabled) */}
              <div 
                className="relative flex cursor-not-allowed opacity-60 rounded-lg border border-[#334155]/50 bg-[#020817]/50 p-4 shadow-sm group"
                onMouseEnter={() => setIsHoveringDisabled(true)}
                onMouseLeave={() => setIsHoveringDisabled(false)}
              >
                <input type="radio" name="mode" value="active" className="sr-only" disabled />
                <span className="flex flex-1">
                  <span className="flex flex-col">
                    <span className="block text-sm font-medium text-[#F8FAFC] flex items-center gap-2">
                      <ShieldAlert className="h-4 w-4 text-muted-foreground" />
                      Authorized Active Scan
                    </span>
                    <span className="mt-1 flex items-center text-xs text-muted-foreground">
                      Intrusive vulnerability scanning (Requires Auth).
                    </span>
                  </span>
                </span>
                {isHoveringDisabled && (
                  <motion.div 
                    initial={{ opacity: 0, y: 5 }} 
                    animate={{ opacity: 1, y: 0 }} 
                    className="absolute -top-10 left-1/2 -translate-x-1/2 bg-[#111827] border border-[#334155] px-3 py-1.5 rounded-md text-xs text-[#F8FAFC] shadow-xl flex items-center gap-1.5 whitespace-nowrap z-10"
                  >
                    <Info className="h-3.5 w-3.5 text-[#2563EB]" />
                    Coming Soon in Sprint 4B
                  </motion.div>
                )}
              </div>

            </div>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}

function GlobeIcon(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="12" r="10" />
      <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
      <path d="M2 12h20" />
    </svg>
  );
}
