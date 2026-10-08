'use client';

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { History, ArrowRight, Activity, Download } from "lucide-react";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import Link from "next/link";
import { useRouter } from "next/navigation";

import api from "@/lib/api";

interface HistoryData {
  id: string;
  domain: string;
  overall_score: number;
  risk_level: string;
  scan_duration: number;
  status: string;
  created_at: string;
}

export function AssessmentHistoryTable({ refreshKey }: { refreshKey?: number }) {
  const router = useRouter();
  const [data, setData] = useState<HistoryData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    async function fetchHistory() {
      setLoading(true);
      setError(false);
      try {
        const response = await api.get('/assessment/history');
        const items = response.data?.data?.items || response.data?.items || (Array.isArray(response.data?.data) ? response.data.data : []) || [];
        setData(items);
        setLoading(false);
        return;
      } catch (err) {
        console.warn("Assessment history fetch failed", err);
      }
      setData([]);
      setError(true);
      setLoading(false);
    }
    
    fetchHistory();

    const handleScanDone = () => {
      fetchHistory();
    };
    window.addEventListener('assessment-scan-completed', handleScanDone);
    return () => {
      window.removeEventListener('assessment-scan-completed', handleScanDone);
    };
  }, [refreshKey]);

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5, delay: 0.4 }}>
      <Card className="bg-[#111827] border-[#334155] shadow-sm">
        <CardHeader className="pb-4 border-b border-[#334155]/50 flex flex-row items-center justify-between">
          <div>
            <CardTitle className="text-sm font-medium text-[#F8FAFC] flex items-center gap-2">
              <History className="h-4 w-4 text-[#2563EB]" />
              Assessment History
            </CardTitle>
            <CardDescription className="mt-1">Historical log of previously scanned targets.</CardDescription>
          </div>
        </CardHeader>
        <CardContent className="pt-6">
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow className="border-[#334155] hover:bg-transparent">
                  <TableHead className="text-muted-foreground font-medium">Domain</TableHead>
                  <TableHead className="text-muted-foreground font-medium">Date</TableHead>
                  <TableHead className="text-muted-foreground font-medium">Score</TableHead>
                  <TableHead className="text-muted-foreground font-medium">Risk</TableHead>
                  <TableHead className="text-muted-foreground font-medium">Duration</TableHead>
                  <TableHead className="text-muted-foreground font-medium">Status</TableHead>
                  <TableHead className="text-right text-muted-foreground font-medium">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {loading ? (
                  <TableRow>
                    <TableCell colSpan={7} className="text-center py-6 text-muted-foreground">Loading history...</TableCell>
                  </TableRow>
                ) : data.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={7} className="text-center py-6 text-muted-foreground">
                      {error ? "Unable to connect to database." : "No assessments found."}
                    </TableCell>
                  </TableRow>
                ) : data.map((assessment) => (
                  <TableRow key={assessment.id} className="border-[#334155]/50 hover:bg-white/5 transition-colors">
                    <TableCell className="font-medium text-[#F8FAFC] whitespace-nowrap text-sm">
                      {assessment.domain}
                    </TableCell>
                    <TableCell className="text-muted-foreground whitespace-nowrap text-sm">
                      {new Date(assessment.created_at).toLocaleString()}
                    </TableCell>
                    <TableCell>
                      <span className={`text-sm font-semibold ${assessment.overall_score >= 90 ? 'text-green-500' : assessment.overall_score >= 70 ? 'text-yellow-500' : assessment.overall_score >= 40 ? 'text-orange-500' : 'text-red-500'}`}>
                        {assessment.overall_score}/100
                      </span>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline" className={`font-medium shadow-none border-0 ${
                        assessment.risk_level === 'Low' ? 'bg-green-500/10 text-green-500' : 
                        assessment.risk_level === 'Medium' ? 'bg-yellow-500/10 text-yellow-500' : 
                        assessment.risk_level === 'High' ? 'bg-orange-500/10 text-orange-500' : 'bg-red-500/10 text-red-500'
                      }`}>
                        {assessment.risk_level}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-muted-foreground text-sm">
                      {(assessment.scan_duration / 1000).toFixed(1)}s
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline" className={`font-medium shadow-none border-0 ${assessment.status === 'Completed' ? 'bg-green-500/10 text-green-500' : 'bg-red-500/10 text-red-500'}`}>
                        {assessment.status}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right">
                      <div className="flex justify-end gap-2">
                        <button className="inline-flex items-center justify-center whitespace-nowrap rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50 h-8 px-3 text-xs text-[#2563EB] hover:text-[#2563EB]/80 hover:bg-[#2563EB]/10" onClick={() => router.push(`/dashboard/website-security/history/${assessment.id}`)}>
                          View
                        </button>
                        <button className="inline-flex items-center justify-center whitespace-nowrap rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50 h-8 w-8 text-muted-foreground hover:text-white hover:bg-white/10" onClick={() => router.push(`/dashboard/website-security/compare?domain=${assessment.domain}`)}>
                          <Activity className="h-4 w-4" />
                        </button>
                        <button className="inline-flex items-center justify-center whitespace-nowrap rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50 h-8 w-8 text-muted-foreground hover:text-white hover:bg-white/10">
                          <Download className="h-4 w-4" />
                        </button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
