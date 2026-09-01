'use client';

import { Suspense, useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { PageTitle } from "@/components/layout/PageTitle";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { ArrowLeft, ArrowUpRight, ArrowDownRight, Minus, CheckCircle2, XCircle } from "lucide-react";
import { motion } from "framer-motion";

interface ComparisonData {
  assessment_old: { id: string; date: string; score: number };
  assessment_new: { id: string; date: string; score: number };
  score_delta: number;
  resolved_findings: string[];
  new_findings: string[];
  persistent_findings: string[];
}

function CompareAssessmentsContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const domain = searchParams.get('domain');
  
  const [data, setData] = useState<ComparisonData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchComparison() {
      try {
        const response = await fetch(`/api/v1/assessment/compare?domain=${domain}`);
        if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.detail || "Failed to fetch comparison");
        }
        const json = await response.json();
        setData(json.data ?? json);
      } catch (err: unknown) {
        console.error("Error fetching comparison:", err);
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    }
    
    if (domain) {
      fetchComparison();
    } else {
      setError("No domain provided for comparison.");
      setLoading(false);
    }
  }, [domain]);

  return (
    <div className="flex-1 space-y-6 p-8 pt-6">
      <div className="flex items-center gap-4">
        <button onClick={() => router.back()} className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-white/10 h-10 w-10 text-muted-foreground hover:text-white">
          <ArrowLeft className="h-5 w-5" />
        </button>
        <PageTitle 
          title="Compare Assessments" 
          subtitle={`Comparing latest two assessments for ${domain}`}
        />
      </div>

      {loading ? (
        <div className="text-center py-20 text-muted-foreground">Analyzing historical data...</div>
      ) : error || !data ? (
        <div className="text-center py-20 text-red-500">
          {error || "Failed to load comparison."}
        </div>
      ) : (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }} className="space-y-6">
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card className="bg-[#111827] border-[#334155]">
              <CardHeader className="pb-2">
                <CardDescription>Previous Assessment</CardDescription>
                <CardTitle className="text-[#F8FAFC]">{new Date(data.assessment_old.date).toLocaleDateString()}</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-4xl font-bold text-muted-foreground">{data.assessment_old.score}/100</div>
              </CardContent>
            </Card>

            <Card className="bg-[#111827] border-[#334155] border-t-4 border-t-[#2563EB]">
              <CardHeader className="pb-2">
                <CardDescription>Score Delta</CardDescription>
                <CardTitle className="text-[#F8FAFC]">Trend</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-2">
                  {data.score_delta > 0 ? (
                    <><ArrowUpRight className="h-8 w-8 text-green-500" /> <span className="text-4xl font-bold text-green-500">+{data.score_delta}</span></>
                  ) : data.score_delta < 0 ? (
                    <><ArrowDownRight className="h-8 w-8 text-red-500" /> <span className="text-4xl font-bold text-red-500">{data.score_delta}</span></>
                  ) : (
                    <><Minus className="h-8 w-8 text-muted-foreground" /> <span className="text-4xl font-bold text-muted-foreground">0</span></>
                  )}
                </div>
              </CardContent>
            </Card>

            <Card className="bg-[#111827] border-[#334155]">
              <CardHeader className="pb-2">
                <CardDescription>Latest Assessment</CardDescription>
                <CardTitle className="text-[#F8FAFC]">{new Date(data.assessment_new.date).toLocaleDateString()}</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-4xl font-bold text-white">{data.assessment_new.score}/100</div>
              </CardContent>
            </Card>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card className="bg-[#111827] border-[#334155]">
              <CardHeader className="pb-4 border-b border-[#334155]/50">
                <CardTitle className="text-[#F8FAFC] flex items-center gap-2">
                  <CheckCircle2 className="h-5 w-5 text-green-500" />
                  Resolved Findings ({data.resolved_findings.length})
                </CardTitle>
                <CardDescription>Issues fixed since the previous assessment</CardDescription>
              </CardHeader>
              <CardContent className="pt-4 space-y-3">
                {data.resolved_findings.length === 0 ? (
                  <div className="text-sm text-muted-foreground">No findings were resolved.</div>
                ) : (
                  data.resolved_findings.map((finding: string, idx: number) => (
                    <div key={idx} className="p-3 bg-green-500/10 border border-green-500/20 text-green-400 rounded text-sm">
                      {finding}
                    </div>
                  ))
                )}
              </CardContent>
            </Card>

            <Card className="bg-[#111827] border-[#334155]">
              <CardHeader className="pb-4 border-b border-[#334155]/50">
                <CardTitle className="text-[#F8FAFC] flex items-center gap-2">
                  <XCircle className="h-5 w-5 text-red-500" />
                  New Findings ({data.new_findings.length})
                </CardTitle>
                <CardDescription>New issues introduced since the previous assessment</CardDescription>
              </CardHeader>
              <CardContent className="pt-4 space-y-3">
                {data.new_findings.length === 0 ? (
                  <div className="text-sm text-muted-foreground">No new findings introduced.</div>
                ) : (
                  data.new_findings.map((finding: string, idx: number) => (
                    <div key={idx} className="p-3 bg-red-500/10 border border-red-500/20 text-red-400 rounded text-sm">
                      {finding}
                    </div>
                  ))
                )}
              </CardContent>
            </Card>
            
            <Card className="bg-[#111827] border-[#334155] md:col-span-2">
              <CardHeader className="pb-4 border-b border-[#334155]/50">
                <CardTitle className="text-[#F8FAFC] flex items-center gap-2">
                  <Minus className="h-5 w-5 text-muted-foreground" />
                  Persistent Findings ({data.persistent_findings.length})
                </CardTitle>
                <CardDescription>Issues that remain unresolved across both assessments</CardDescription>
              </CardHeader>
              <CardContent className="pt-4 space-y-3">
                {data.persistent_findings.length === 0 ? (
                  <div className="text-sm text-muted-foreground">No persistent findings.</div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {data.persistent_findings.map((finding: string, idx: number) => (
                      <div key={idx} className="p-3 bg-[#020817] border border-[#334155]/50 text-[#F8FAFC] rounded text-sm">
                        {finding}
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </motion.div>
      )}
    </div>
  );
}

export default function CompareAssessmentsPage() {
  return (
    <Suspense fallback={<div className="p-8 text-muted-foreground">Loading comparison...</div>}>
      <CompareAssessmentsContent />
    </Suspense>
  );
}
