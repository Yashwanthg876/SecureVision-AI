export interface ThreatIOC {
  id: string;
  ioc_value: string;
  ioc_type: "ip" | "domain" | "hash" | "url" | "cve" | string;
  threat_type: string;
  severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
  confidence_score: number;
  source: string;
  target_sector: string;
  description?: string;
  recommended_action?: string;
  status: "ACTIVE" | "MITIGATED" | "INVESTIGATING";
  country_code?: string;
  created_at: string;
}

export interface IOCLookupResult {
  query: string;
  matched: boolean;
  ioc: ThreatIOC | null;
  risk_level: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
  verdict: string;
  reputation_score: number;
  analysis_details: string;
  recommended_action: string;
}

export interface ThreatIntelStats {
  total_active_iocs: number;
  critical_threats: number;
  high_threats: number;
  medium_threats: number;
  low_threats: number;
  top_threat_vector: string;
  avg_confidence_score: number;
  category_distribution: Record<string, number>;
}
