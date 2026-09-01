export interface ReportItem {
  id: string;
  title: string;
  target_domain: string;
  target_url: string;
  overall_score: number;
  risk_level: "Healthy" | "Low" | "Medium" | "High" | "Critical" | string;
  total_findings: number;
  report_type: string;
  created_at: string;
  formats: ("pdf" | "csv" | "json")[];
}

export interface ReportGenerateRequest {
  assessment_id?: string;
  target_domain?: string;
  report_type: string;
  format_type: "pdf" | "csv" | "json";
}

export interface ReportStats {
  total_reports: number;
  pdf_downloads: number;
  latest_score: number;
  compliance_status: string;
}
