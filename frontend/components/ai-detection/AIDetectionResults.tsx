'use client';

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Bot, User as UserIcon, Activity, AlertTriangle, CheckCircle2, Info } from "lucide-react";
import { motion } from "framer-motion";

export function AIDetectionResults({ data }: { data: any }) {
  if (!data) return null;

  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-red-500";
    if (score >= 50) return "text-yellow-500";
    return "text-green-500";
  };

  const getHighlightColor = (score: number) => {
    if (score >= 80) return "bg-red-500/30 text-white";
    if (score >= 50) return "bg-yellow-500/30 text-white";
    return "text-muted-foreground"; // Human-like text stays muted
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
      <Card className="bg-[#111827] border-[#334155] shadow-sm">
        <CardHeader className="pb-4 border-b border-[#334155]/50 flex flex-row justify-between items-start">
          <div>
            <CardTitle className="text-lg font-semibold text-[#F8FAFC] flex items-center gap-2">
              <Activity className="h-5 w-5 text-[#8B5CF6]" />
              Analysis Results
            </CardTitle>
            <CardDescription>Detailed breakdown of AI patterns and heuristics.</CardDescription>
          </div>
          <Badge className={`font-semibold border-0 ${
            data.risk_level === 'High' ? 'bg-red-500/10 text-red-500' :
            data.risk_level === 'Medium' ? 'bg-yellow-500/10 text-yellow-500' :
            'bg-green-500/10 text-green-500'
          }`}>
            {data.risk_level} Risk
          </Badge>
        </CardHeader>
        
        <CardContent className="pt-6 space-y-8">
          {/* Main Gauges */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-[#020817] rounded-xl border border-[#334155]/50 p-6 flex flex-col items-center justify-center text-center">
              <Bot className={`h-10 w-10 mb-2 ${getScoreColor(data.ai_probability)}`} />
              <div className={`text-5xl font-bold ${getScoreColor(data.ai_probability)}`}>
                {data.ai_probability}%
              </div>
              <p className="text-sm text-muted-foreground mt-2 font-medium">AI Generated</p>
            </div>
            
            <div className="bg-[#020817] rounded-xl border border-[#334155]/50 p-6 flex flex-col items-center justify-center text-center">
              <UserIcon className="h-10 w-10 mb-2 text-blue-400" />
              <div className="text-5xl font-bold text-blue-400">
                {data.human_probability}%
              </div>
              <p className="text-sm text-muted-foreground mt-2 font-medium">Human Written</p>
            </div>
          </div>

          {/* Metrics */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-[#020817] p-4 rounded-lg border border-[#334155]/50">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm text-muted-foreground">Perplexity</span>
                <span className="text-[#F8FAFC] font-mono">{data.perplexity}</span>
              </div>
              <div className="w-full bg-[#111827] rounded-full h-2">
                <div className="bg-[#8B5CF6] h-2 rounded-full" style={{ width: `${data.perplexity}%` }}></div>
              </div>
              <p className="text-xs text-muted-foreground mt-2">Lower = more predictable (AI-like)</p>
            </div>
            
            <div className="bg-[#020817] p-4 rounded-lg border border-[#334155]/50">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm text-muted-foreground">Burstiness</span>
                <span className="text-[#F8FAFC] font-mono">{data.burstiness}</span>
              </div>
              <div className="w-full bg-[#111827] rounded-full h-2">
                <div className="bg-[#10B981] h-2 rounded-full" style={{ width: `${data.burstiness}%` }}></div>
              </div>
              <p className="text-xs text-muted-foreground mt-2">Variance in sentence structure</p>
            </div>
          </div>

          {/* Verdict */}
          <div className={`p-4 rounded-lg flex gap-3 border ${
            data.risk_level === 'High' ? 'bg-red-500/10 border-red-500/30 text-red-200' :
            data.risk_level === 'Medium' ? 'bg-yellow-500/10 border-yellow-500/30 text-yellow-200' :
            'bg-green-500/10 border-green-500/30 text-green-200'
          }`}>
            {data.risk_level === 'High' ? <AlertTriangle className="h-5 w-5 shrink-0 text-red-500" /> :
             data.risk_level === 'Medium' ? <Info className="h-5 w-5 shrink-0 text-yellow-500" /> :
             <CheckCircle2 className="h-5 w-5 shrink-0 text-green-500" />}
            <div>
              <p className="font-semibold">{data.verdict}</p>
              <p className="text-sm mt-1 opacity-80">
                {data.content_type === 'text' 
                  ? "Based on statistical analysis of word choices and sentence variance." 
                  : "Based on code structure and commenting patterns."}
              </p>
            </div>
          </div>

          {/* Sentence Highlight Map */}
          {data.content_type === 'text' && data.sentences && data.sentences.length > 0 && (
            <div className="space-y-3">
              <h4 className="text-sm font-semibold text-[#F8FAFC]">Text Analysis Map</h4>
              <div className="p-4 bg-[#020817] border border-[#334155]/50 rounded-lg text-sm leading-relaxed font-mono">
                {data.sentences.map((s: any, i: number) => (
                  <span key={i} className={`mr-1 px-1 rounded ${getHighlightColor(s.ai_probability)} transition-colors cursor-help`} title={`AI Prob: ${s.ai_probability}%`}>
                    {s.sentence}
                  </span>
                ))}
              </div>
              <div className="flex gap-4 text-xs text-muted-foreground justify-end">
                <span className="flex items-center gap-1"><div className="w-3 h-3 bg-red-500/30 rounded" /> High AI Prob</span>
                <span className="flex items-center gap-1"><div className="w-3 h-3 bg-yellow-500/30 rounded" /> Med AI Prob</span>
                <span className="flex items-center gap-1"><div className="w-3 h-3 bg-transparent border border-muted-foreground rounded" /> Human</span>
              </div>
            </div>
          )}
          
        </CardContent>
      </Card>
    </motion.div>
  );
}
