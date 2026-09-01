'use client';

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { History, FileText, Code2 } from "lucide-react";
import { motion } from "framer-motion";
import api from "@/lib/api";

export function AIDetectionHistory({ refreshKey }: { refreshKey?: number }) {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchHistory() {
      setLoading(true);
      try {
        const res = await api.get("/ai-detection/history");
        const items = res.data?.data?.items ?? [];
        setData(items);
      } catch (e) {
        console.warn("AI detection history fetch failed", e);
      }
      setLoading(false);
    }
    fetchHistory();
  }, [refreshKey]);

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5, delay: 0.3 }}>
      <Card className="bg-[#111827] border-[#334155] shadow-sm">
        <CardHeader className="pb-4 border-b border-[#334155]/50">
          <CardTitle className="text-sm font-medium text-[#F8FAFC] flex items-center gap-2">
            <History className="h-4 w-4 text-[#8B5CF6]" />
            Scan History
          </CardTitle>
          <CardDescription>Previous AI detection scans.</CardDescription>
        </CardHeader>
        <CardContent className="pt-6">
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow className="border-[#334155] hover:bg-transparent">
                  {["Type", "Content Snippet", "Date", "AI Probability", "Risk"].map((h) => (
                    <TableHead key={h} className="text-muted-foreground font-medium">{h}</TableHead>
                  ))}
                </TableRow>
              </TableHeader>
              <TableBody>
                {loading ? (
                  <TableRow>
                    <TableCell colSpan={5} className="text-center py-8 text-muted-foreground">Loading history...</TableCell>
                  </TableRow>
                ) : data.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={5} className="text-center py-8 text-muted-foreground">No scans yet. Run your first scan above.</TableCell>
                  </TableRow>
                ) : data.map((scan) => (
                  <TableRow key={scan.id} className="border-[#334155]/50 hover:bg-white/5 transition-colors">
                    <TableCell>
                      {scan.content_type === "code" ? (
                        <Badge className="bg-blue-500/10 text-blue-400 border-0 flex w-fit items-center gap-1"><Code2 className="w-3 h-3"/> Code</Badge>
                      ) : (
                        <Badge className="bg-gray-500/10 text-gray-400 border-0 flex w-fit items-center gap-1"><FileText className="w-3 h-3"/> Text</Badge>
                      )}
                    </TableCell>
                    <TableCell className="font-medium text-[#F8FAFC] text-sm max-w-[300px] truncate">
                      {scan.content_snippet}
                    </TableCell>
                    <TableCell className="text-muted-foreground text-sm whitespace-nowrap">
                      {new Date(scan.created_at).toLocaleString()}
                    </TableCell>
                    <TableCell>
                      <span className={`text-sm font-semibold ${
                        scan.ai_probability >= 80 ? "text-red-500" :
                        scan.ai_probability >= 50 ? "text-yellow-500" : "text-green-500"
                      }`}>
                        {scan.ai_probability}%
                      </span>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline" className={`font-medium shadow-none border-0 ${
                        scan.risk_level === 'High' ? 'bg-red-500/10 text-red-500' :
                        scan.risk_level === 'Medium' ? 'bg-yellow-500/10 text-yellow-500' :
                        'bg-green-500/10 text-green-500'
                      }`}>
                        {scan.risk_level}
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
