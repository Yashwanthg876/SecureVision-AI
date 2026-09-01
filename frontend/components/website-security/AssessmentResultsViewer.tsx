'use client';

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Lock, FileJson, Network, Globe, Code, Brain, ShieldCheck, CheckCircle2, XCircle, AlertTriangle } from "lucide-react";
import { motion } from "framer-motion";

interface AssessmentResultsViewerProps {
  data: any;
}

export function AssessmentResultsViewer({ data }: AssessmentResultsViewerProps) {
  if (!data) return null;

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
      <Card className="bg-[#111827] border-[#334155] shadow-sm overflow-hidden relative">
        <div className="absolute inset-0 bg-gradient-to-b from-[#020817]/20 to-transparent pointer-events-none" />
        
        <CardHeader className="pb-6 border-b border-[#334155]/50 relative flex flex-row items-start justify-between">
          <div>
            <CardTitle className="text-lg font-semibold text-[#F8FAFC]">Assessment Results: {data.domain || data.target_url}</CardTitle>
            <CardDescription>Comprehensive security findings generated on {new Date(data.created_at).toLocaleString()}</CardDescription>
          </div>
          <div className="flex gap-2">
            <Badge variant="outline" className={`font-medium shadow-none border-0 ${
                data.risk_level === 'Low' ? 'bg-green-500/10 text-green-500' : 
                data.risk_level === 'Medium' ? 'bg-yellow-500/10 text-yellow-500' : 
                data.risk_level === 'High' ? 'bg-orange-500/10 text-orange-500' : 'bg-red-500/10 text-red-500'
              }`}>
              Risk: {data.risk_level}
            </Badge>
          </div>
        </CardHeader>
        
        <CardContent className="pt-8 relative space-y-8">
          
          {/* Overall Score */}
          <div className="space-y-4">
            <h4 className="text-sm font-semibold text-[#F8FAFC] flex items-center gap-2">
              <ShieldCheck className="h-5 w-5 text-[#2563EB]" />
              Overall Security Score
            </h4>
            <div className="flex items-center gap-4">
              <div className="text-4xl font-bold text-white">{data.overall_score}/100</div>
              <div className="flex gap-2">
                 <Badge className="bg-red-500/20 text-red-500 hover:bg-red-500/30 border-0">{data.critical_count} Critical</Badge>
                 <Badge className="bg-orange-500/20 text-orange-500 hover:bg-orange-500/30 border-0">{data.high_count} High</Badge>
                 <Badge className="bg-yellow-500/20 text-yellow-500 hover:bg-yellow-500/30 border-0">{data.medium_count} Medium</Badge>
                 <Badge className="bg-blue-500/20 text-blue-500 hover:bg-blue-500/30 border-0">{data.low_count} Low</Badge>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* SSL/TLS */}
            <Card className="bg-[#020817] border-[#334155]">
              <CardHeader className="pb-3 border-b border-[#334155]/50">
                <CardTitle className="text-sm font-semibold text-[#F8FAFC] flex items-center justify-between">
                  <div className="flex items-center gap-2"><Lock className="h-4 w-4 text-[#2563EB]" /> SSL/TLS Analysis</div>
                  <span className="text-xs text-muted-foreground">Score: {data.ssl_score}/100</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-4 text-sm text-muted-foreground space-y-2">
                <div className="flex justify-between items-center">
                  <span>Valid Certificate:</span>
                  {data.ssl_tls?.is_valid ? <CheckCircle2 className="h-4 w-4 text-green-500" /> : <XCircle className="h-4 w-4 text-red-500" />}
                </div>
                <div className="flex justify-between items-center">
                  <span>Issuer:</span>
                  <span className="text-white">{data.ssl_tls?.issuer || 'Unknown'}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span>Expires In:</span>
                  <span className="text-white">{data.ssl_tls?.expires_in_days || 0} days</span>
                </div>
              </CardContent>
            </Card>

            {/* HTTP Headers */}
            <Card className="bg-[#020817] border-[#334155]">
              <CardHeader className="pb-3 border-b border-[#334155]/50">
                <CardTitle className="text-sm font-semibold text-[#F8FAFC] flex items-center justify-between">
                  <div className="flex items-center gap-2"><FileJson className="h-4 w-4 text-[#2563EB]" /> HTTP Security Headers</div>
                  <span className="text-xs text-muted-foreground">Score: {data.headers_score}/100</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-4 text-sm text-muted-foreground space-y-2">
                <div className="flex justify-between items-center">
                  <span>HSTS:</span>
                  {data.http_headers?.strict_transport_security ? <CheckCircle2 className="h-4 w-4 text-green-500" /> : <XCircle className="h-4 w-4 text-red-500" />}
                </div>
                <div className="flex justify-between items-center">
                  <span>CSP:</span>
                  {data.http_headers?.content_security_policy ? <CheckCircle2 className="h-4 w-4 text-green-500" /> : <XCircle className="h-4 w-4 text-red-500" />}
                </div>
                <div className="flex justify-between items-center">
                  <span>X-Frame-Options:</span>
                  {data.http_headers?.x_frame_options ? <CheckCircle2 className="h-4 w-4 text-green-500" /> : <XCircle className="h-4 w-4 text-red-500" />}
                </div>
              </CardContent>
            </Card>
            
            {/* DNS */}
            <Card className="bg-[#020817] border-[#334155]">
              <CardHeader className="pb-3 border-b border-[#334155]/50">
                <CardTitle className="text-sm font-semibold text-[#F8FAFC] flex items-center justify-between">
                  <div className="flex items-center gap-2"><Network className="h-4 w-4 text-[#2563EB]" /> DNS Configuration</div>
                  <span className="text-xs text-muted-foreground">Score: {data.dns_score}/100</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-4 text-sm text-muted-foreground space-y-2">
                <div className="flex justify-between items-center">
                  <span>SPF Record:</span>
                  {data.dns?.has_spf ? <CheckCircle2 className="h-4 w-4 text-green-500" /> : <XCircle className="h-4 w-4 text-red-500" />}
                </div>
                <div className="flex justify-between items-center">
                  <span>DMARC Record:</span>
                  {data.dns?.has_dmarc ? <CheckCircle2 className="h-4 w-4 text-green-500" /> : <XCircle className="h-4 w-4 text-red-500" />}
                </div>
              </CardContent>
            </Card>
            
            {/* Technology */}
            <Card className="bg-[#020817] border-[#334155]">
              <CardHeader className="pb-3 border-b border-[#334155]/50">
                <CardTitle className="text-sm font-semibold text-[#F8FAFC] flex items-center justify-between">
                  <div className="flex items-center gap-2"><Code className="h-4 w-4 text-[#2563EB]" /> Technology Stack</div>
                  <span className="text-xs text-muted-foreground">Score: {data.tech_score}/100</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-4 text-sm text-muted-foreground space-y-2">
                 <div className="flex justify-between items-center">
                  <span>Server:</span>
                  <span className="text-white">{data.technology?.server || 'Hidden'}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span>X-Powered-By:</span>
                  <span className="text-white">{data.technology?.x_powered_by || 'Hidden'}</span>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* AI Recommendations */}
          <div className="space-y-4">
            <h4 className="text-sm font-semibold text-[#F8FAFC] flex items-center gap-2">
              <Brain className="h-5 w-5 text-[#2563EB]" />
              Actionable Recommendations
            </h4>
            
            {data.recommendations && data.recommendations.length > 0 ? (
              <div className="space-y-3">
                {data.recommendations.map((rec: any, idx: number) => (
                  <div key={idx} className="p-4 border border-[#334155] bg-[#020817] rounded-lg space-y-2">
                    <div className="flex items-start justify-between gap-4">
                      <div className="font-medium text-white flex items-center gap-2">
                        {rec.severity === 'Critical' && <XCircle className="h-4 w-4 text-red-500" />}
                        {rec.severity === 'High' && <AlertTriangle className="h-4 w-4 text-orange-500" />}
                        {(rec.severity === 'Medium' || rec.severity === 'Low') && <AlertTriangle className="h-4 w-4 text-yellow-500" />}
                        {rec.title}
                      </div>
                      <Badge variant="outline" className={`font-medium shadow-none border-0 ${
                        rec.severity === 'Critical' ? 'bg-red-500/10 text-red-500' : 
                        rec.severity === 'High' ? 'bg-orange-500/10 text-orange-500' : 
                        rec.severity === 'Medium' ? 'bg-yellow-500/10 text-yellow-500' : 'bg-blue-500/10 text-blue-500'
                      }`}>
                        {rec.severity}
                      </Badge>
                    </div>
                    <p className="text-sm text-muted-foreground">{rec.description}</p>
                    <div className="bg-[#111827] p-3 rounded text-sm text-blue-200 mt-2 border border-blue-900/30">
                      <span className="font-semibold text-blue-400">Recommendation:</span> {rec.recommendation}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-sm text-muted-foreground py-4 text-center bg-[#020817] border border-[#334155]/50 rounded-lg">
                No vulnerabilities found. Your application is highly secure.
              </div>
            )}
          </div>

        </CardContent>
      </Card>
    </motion.div>
  );
}
