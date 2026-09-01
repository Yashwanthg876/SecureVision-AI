export interface DashboardSummary {
  score: number;
  score_status: string;
  score_trend: string;
  websites_total: number;
  websites_scanned_today: number;
  repos_total: number;
  repos_high_risk: number;
  ai_threats_total: number;
  ai_threats_critical: number;
}

export interface ThreatTrend {
  date: string;
  critical: number;
  high: number;
  medium: number;
  low: number;
}

export interface RiskDistribution {
  name: string;
  value: number;
  color: string;
}

export interface RecentActivity {
  id: string;
  timestamp: string;
  module: string;
  action: string;
  target: string;
  status: 'Success' | 'Failed' | 'Warning' | 'Pending';
}

export interface CriticalFinding {
  id: string;
  title: string;
  severity: 'Critical' | 'High' | 'Medium' | 'Low';
  module: string;
  target: string;
  timestamp: string;
  status: 'Open' | 'Investigating' | 'Resolved';
}

export interface DashboardData {
  summary: DashboardSummary | null;
  threatTrend: ThreatTrend[];
  riskDistribution: RiskDistribution[];
  recentActivity: RecentActivity[];
  criticalFindings: CriticalFinding[];
}
