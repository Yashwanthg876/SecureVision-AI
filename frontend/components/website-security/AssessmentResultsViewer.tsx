'use client';

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Lock, FileJson, Network, ShieldCheck, AlertTriangle, XCircle, Brain } from "lucide-react";
import { motion } from "framer-motion";

interface AssessmentResultsViewerProps {
  data: any;
}

export function AssessmentResultsViewer({ data }: AssessmentResultsViewerProps) {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
      <Card className="bg-card border-border shadow-sm overflow-hidden relative">
        <div className="absolute inset-0 bg-gradient-to-b from-primary/5 to-transparent pointer-events-none" />
        
        <CardHeader className="pb-6 border-b border-border relative flex flex-row items-start justify-between">
          <div>
            <CardTitle className="text-lg font-semibold text-foreground">Assessment Results: {data.domain || data.target_url}</CardTitle>
            <CardDescription>Comprehensive security findings generated on {new Date(data.created_at).toLocaleString()}</CardDescription>
          </div>
          <div className="flex gap-2">
            <Badge variant="outline" className={`font-medium shadow-none border-0 ${
                data.risk_level === 'Low' ? 'bg-green-500/10 text-green-600 dark:text-green-400' : 
                data.risk_level === 'Medium' ? 'bg-yellow-500/10 text-yellow-600 dark:text-yellow-400' : 
                data.risk_level === 'High' ? 'bg-orange-500/10 text-orange-600 dark:text-orange-400' : 'bg-red-500/10 text-red-600 dark:text-red-400'
              }`}>
              Risk: {data.risk_level}
            </Badge>
          </div>
        </CardHeader>
        
        <CardContent className="pt-8 relative space-y-8">
          
          {/* Overall Score */}
          <div className="space-y-4">
            <h4 className="text-sm font-semibold text-foreground flex items-center gap-2">
              <ShieldCheck className="h-5 w-5 text-primary" />
              Overall Security Score
            </h4>
            <div className="flex items-center gap-4">
              <div className="text-4xl font-bold text-foreground">{data.overall_score}/100</div>
              <div className="flex gap-2">
                 <Badge className="bg-red-500/20 text-red-600 dark:text-red-400 border-0">{data.critical_count} Critical</Badge>
                 <Badge className="bg-orange-500/20 text-orange-600 dark:text-orange-400 border-0">{data.high_count} High</Badge>
                 <Badge className="bg-yellow-500/20 text-yellow-600 dark:text-yellow-400 border-0">{data.medium_count} Medium</Badge>
                 <Badge className="bg-blue-500/20 text-blue-600 dark:text-blue-400 border-0">{data.low_count} Low</Badge>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* SSL/TLS */}
            <Card className="bg-muted/40 border-border">
              <CardHeader className="pb-3 border-b border-border">
                <CardTitle className="text-sm font-semibold text-foreground flex items-center justify-between">
                  <div className="flex items-center gap-2"><Lock className="h-4 w-4 text-primary" /> SSL/TLS Analysis</div>
                  <span className="text-xs text-muted-foreground">Score: {data.ssl_score}/100</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-4 text-sm text-muted-foreground space-y-2">
                <div className="flex justify-between items-center">
                  <span>Certificate Status:</span>
                  <span className={data.ssl_valid ? "text-green-600 dark:text-green-400 font-medium" : "text-red-600 dark:text-red-400 font-medium"}>
                    {data.ssl_valid ? "Valid" : "Invalid/Expired"}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span>Protocol:</span>
                  <span className="text-foreground">{data.ssl_details?.protocol || 'Unknown'}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span>Issuer:</span>
                  <span className="text-foreground">{data.ssl_details?.issuer || 'Unknown'}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span>Days Until Expiry:</span>
                  <span className="text-foreground">{data.ssl_days_remaining !== null ? `${data.ssl_days_remaining} days` : 'N/A'}</span>
                </div>
              </CardContent>
            </Card>

            {/* HTTP Headers */}
            <Card className="bg-muted/40 border-border">
              <CardHeader className="pb-3 border-b border-border">
                <CardTitle className="text-sm font-semibold text-foreground flex items-center justify-between">
                  <div className="flex items-center gap-2"><FileJson className="h-4 w-4 text-primary" /> HTTP Security Headers</div>
                  <span className="text-xs text-muted-foreground">Score: {data.headers_score}/100</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-4 text-sm text-muted-foreground space-y-2">
                <div className="flex justify-between items-center">
                  <span>HSTS Enforced:</span>
                  <span className={data.headers_details?.hsts ? "text-green-600 dark:text-green-400 font-medium" : "text-red-600 dark:text-red-400 font-medium"}>
                    {data.headers_details?.hsts ? "Yes" : "Missing"}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span>CSP Configured:</span>
                  <span className={data.headers_details?.csp ? "text-green-600 dark:text-green-400 font-medium" : "text-red-600 dark:text-red-400 font-medium"}>
                    {data.headers_details?.csp ? "Yes" : "Missing"}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span>X-Frame-Options:</span>
                  <span className={data.headers_details?.x_frame_options ? "text-green-600 dark:text-green-400 font-medium" : "text-yellow-600 dark:text-yellow-400 font-medium"}>
                    {data.headers_details?.x_frame_options || "Missing"}
                  </span>
                </div>
              </CardContent>
            </Card>

            {/* DNS Security */}
            <Card className="bg-muted/40 border-border">
              <CardHeader className="pb-3 border-b border-border">
                <CardTitle className="text-sm font-semibold text-foreground flex items-center justify-between">
                  <div className="flex items-center gap-2"><Network className="h-4 w-4 text-primary" /> DNS Configuration</div>
                  <span className="text-xs text-muted-foreground">Score: {data.dns_score}/100</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-4 text-sm text-muted-foreground space-y-2">
                <div className="flex justify-between items-center">
                  <span>DNSSEC Enabled:</span>
                  <span className={data.dns_details?.dnssec ? "text-green-600 dark:text-green-400 font-medium" : "text-yellow-600 dark:text-yellow-400 font-medium"}>
                    {data.dns_details?.dnssec ? "Yes" : "No"}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span>DMARC Configured:</span>
                  <span className={data.dns_details?.dmarc ? "text-green-600 dark:text-green-400 font-medium" : "text-red-600 dark:text-red-400 font-medium"}>
                    {data.dns_details?.dmarc ? "Yes" : "Missing"}
                  </span>
                </div>
              </CardContent>
            </Card>

            {/* Technology Stack */}
            <Card className="bg-muted/40 border-border">
              <CardHeader className="pb-3 border-b border-border">
                <CardTitle className="text-sm font-semibold text-foreground flex items-center justify-between">
                  <div className="flex items-center gap-2"><Network className="h-4 w-4 text-primary" /> Detected Technology</div>
                  <span className="text-xs text-muted-foreground">Fingerprint</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-4 text-sm text-muted-foreground space-y-2">
                 <div className="flex justify-between items-center">
                  <span>Server:</span>
                  <span className="text-foreground">{data.technology?.server || 'Hidden'}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span>X-Powered-By:</span>
                  <span className="text-foreground">{data.technology?.x_powered_by || 'Hidden'}</span>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* AI Recommendations */}
          <div className="space-y-4">
            <h4 className="text-sm font-semibold text-foreground flex items-center gap-2">
              <Brain className="h-5 w-5 text-primary" />
              Actionable Recommendations
            </h4>
            
            {data.recommendations && data.recommendations.length > 0 ? (
              <div className="space-y-3">
                {data.recommendations.map((rec: any, idx: number) => (
                  <div key={idx} className="p-4 border border-border bg-muted/40 rounded-lg space-y-2">
                    <div className="flex items-start justify-between gap-4">
                      <div className="font-medium text-foreground flex items-center gap-2">
                        {rec.severity === 'Critical' && <XCircle className="h-4 w-4 text-red-500" />}
                        {rec.severity === 'High' && <AlertTriangle className="h-4 w-4 text-orange-500" />}
                        {(rec.severity === 'Medium' || rec.severity === 'Low') && <AlertTriangle className="h-4 w-4 text-yellow-500" />}
                        {rec.title}
                      </div>
                      <Badge variant="outline" className={`font-medium shadow-none border-0 ${
                        rec.severity === 'Critical' ? 'bg-red-500/10 text-red-600 dark:text-red-400' : 
                        rec.severity === 'High' ? 'bg-orange-500/10 text-orange-600 dark:text-orange-400' : 
                        rec.severity === 'Medium' ? 'bg-yellow-500/10 text-yellow-600 dark:text-yellow-400' : 'bg-blue-500/10 text-blue-600 dark:text-blue-400'
                      }`}>
                        {rec.severity}
                      </Badge>
                    </div>
                    <p className="text-sm text-muted-foreground">{rec.description}</p>
                    <div className="bg-card p-3 rounded text-sm text-foreground mt-2 border border-border">
                      <span className="font-semibold text-primary">Recommendation:</span> {rec.recommendation}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-sm text-muted-foreground py-4 text-center bg-muted/40 border border-border rounded-lg">
                No vulnerabilities found. Your application is highly secure.
              </div>
            )}
          </div>

        </CardContent>
      </Card>
    </motion.div>
  );
}
