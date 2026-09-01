'use client';

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Bot, Code2, FileText, Loader2, Play } from "lucide-react";
import { motion } from "framer-motion";
import api from "@/lib/api";

interface AIDetectionFormProps {
  onScanStart?: () => void;
  onScanSuccess?: (data: any) => void;
  onScanError?: (msg: string) => void;
  isScanning?: boolean;
}

export function AIDetectionForm({ onScanStart, onScanSuccess, onScanError, isScanning = false }: AIDetectionFormProps) {
  const [content, setContent] = useState("");
  const [contentType, setContentType] = useState<"text" | "code">("text");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!content.trim()) {
      setError("Please paste some text or code to analyze.");
      return;
    }
    if (content.trim().length < 50) {
      setError("Please provide at least 50 characters for a meaningful analysis.");
      return;
    }
    
    setError("");
    onScanStart?.();

    try {
      const response = await api.post("/ai-detection/scan", { 
        content: content.trim(),
        content_type: contentType
      });
      const data = response.data?.data || response.data;
      onScanSuccess?.(data);
    } catch (err: any) {
      const msg = err.response?.data?.error || err.response?.data?.detail || "Analysis failed. Please try again.";
      onScanError?.(msg);
    }
  };

  return (
    <Card className="bg-[#111827] border-[#334155] shadow-lg">
      <CardHeader className="pb-4 border-b border-[#334155]/50 flex flex-row justify-between items-start">
        <div>
          <CardTitle className="text-lg font-semibold text-[#F8FAFC] flex items-center gap-2">
            <Bot className="h-5 w-5 text-[#8B5CF6]" />
            Analyze Content
          </CardTitle>
          <CardDescription>
            Paste suspicious emails, articles, or code snippets to detect AI-generated patterns.
          </CardDescription>
        </div>
      </CardHeader>
      <CardContent className="pt-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="flex gap-2 p-1 bg-[#020817] rounded-lg border border-[#334155]/60 w-fit">
            <button
              type="button"
              onClick={() => setContentType("text")}
              className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                contentType === "text" ? "bg-[#334155] text-white" : "text-muted-foreground hover:text-white"
              }`}
            >
              <FileText className="h-4 w-4" /> Text
            </button>
            <button
              type="button"
              onClick={() => setContentType("code")}
              className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                contentType === "code" ? "bg-[#334155] text-white" : "text-muted-foreground hover:text-white"
              }`}
            >
              <Code2 className="h-4 w-4" /> Code
            </button>
          </div>

          <div className="space-y-2">
            <Textarea
              placeholder={contentType === "text" ? "Paste email content, essay, or message here..." : "Paste code snippet here..."}
              value={content}
              disabled={isScanning}
              onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => { setContent(e.target.value); setError(""); }}
              className={`min-h-[250px] bg-[#020817] ${error ? 'border-red-500' : 'border-[#334155]/60'} focus:border-[#8B5CF6] text-[#F8FAFC] font-mono text-sm resize-none`}
            />
            {error && <p className="text-sm text-red-500 mt-1">{error}</p>}
          </div>

          <Button
            type="submit"
            disabled={isScanning}
            className="w-full h-12 bg-[#8B5CF6] hover:bg-[#8B5CF6]/90 text-white font-medium shadow-md shadow-[#8B5CF6]/20 transition-all disabled:opacity-50"
          >
            {isScanning ? (
              <span className="flex items-center gap-2">
                <Loader2 className="h-4 w-4 animate-spin" />
                Analyzing Patterns...
              </span>
            ) : (
              <span className="flex items-center gap-2">
                <Play className="h-4 w-4" />
                Analyze Content
              </span>
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
