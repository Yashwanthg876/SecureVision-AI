'use client';

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { History } from "lucide-react";
import { motion } from "framer-motion";

const RISK_CLASS = (risk: string) =>
  risk === "Low" ? "bg-green-500/10 text-green-500" :
  risk === "Medium" ? "bg-yellow-500/10 text-yellow-500" :
  risk === "High" ? "bg-orange-500/10 text-orange-500" :
  "bg-red-500/10 text-red-500";

const SCORE_COLOR = (score: number) =>
  score >= 85 ? "text-green-500" :
  score >= 65 ? "text-yellow-500" :
  score >= 40 ? "text-orange-500" : "text-red-500";

import api from "@/lib/api";

export function RepoScanHistoryTable({ refreshKey }: { refreshKey?: number }) {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchHistory() {
      setLoading(true);
      try {
        const res = await api.get("/github/history");
        const items = res.data?.data?.items ?? res.data?.items ?? [];
        setData(items);
        setLoading(false);
        return;
      } catch (e) {
        console.warn("GitHub history fetch failed", e);
      }
      setData([]);
      setLoading(false);
    }
    fetchHistory();
  }, [refreshKey]);

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5, delay: 0.3 }}>
      <Card className="bg-[#111827] border-[#334155] shadow-sm">
        <CardHeader className="pb-4 border-b border-[#334155]/50">
          <CardTitle className="text-sm font-medium text-[#F8FAFC] flex items-center gap-2">
            <History className="h-4 w-4 text-[#2563EB]" />
            Scan History
          </CardTitle>
          <CardDescription>Previous GitHub repository security scans.</CardDescription>
        </CardHeader>
        <CardContent className="pt-6">
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow className="border-[#334155] hover:bg-transparent">
                  {["Repository", "Date", "Score", "Risk", "Secrets", "Status"].map((h) => (
                    <TableHead key={h} className="text-muted-foreground font-medium">{h}</TableHead>
                  ))}
                </TableRow>
              </TableHeader>
              <TableBody>
                {loading ? (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center py-8 text-muted-foreground">Loading history...</TableCell>
                  </TableRow>
                ) : data.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center py-8 text-muted-foreground">No scans yet. Run your first scan above.</TableCell>
                  </TableRow>
                ) : data.map((scan) => (
                  <TableRow key={scan.id} className="border-[#334155]/50 hover:bg-white/5 transition-colors">
                    <TableCell className="font-medium text-[#F8FAFC] text-sm whitespace-nowrap">
                      {scan.owner}/{scan.repo_name}
                    </TableCell>
                    <TableCell className="text-muted-foreground text-sm whitespace-nowrap">
                      {new Date(scan.created_at).toLocaleString()}
                    </TableCell>
                    <TableCell>
                      <span className={`text-sm font-semibold ${SCORE_COLOR(scan.security_score)}`}>
                        {scan.security_score}/100
                      </span>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline" className={`font-medium shadow-none border-0 ${RISK_CLASS(scan.risk_level)}`}>
                        {scan.risk_level}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <span className={`text-sm font-semibold ${scan.secrets_count > 0 ? "text-red-400" : "text-green-400"}`}>
                        {scan.secrets_count}
                      </span>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline" className={`font-medium shadow-none border-0 ${scan.status === "Completed" ? "bg-green-500/10 text-green-500" : "bg-red-500/10 text-red-500"}`}>
                        {scan.status}
                      </Badge>
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
