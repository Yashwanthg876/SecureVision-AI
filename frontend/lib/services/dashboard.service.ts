import api from '@/lib/api';
import {
  DashboardSummary,
  ThreatTrend,
  RiskDistribution,
  RecentActivity,
  CriticalFinding
} from '@/types/dashboard';

export const dashboardService = {
  getSummary: async (): Promise<DashboardSummary> => {
    try {
      const response = await api.get('/dashboard/summary');
      return response.data?.data || response.data;
    } catch (error) {
      console.warn("Failed to fetch genuine dashboard summary from API", error);
      return {
        score: 0,
        score_status: "No Data",
        score_trend: "0%",
        websites_total: 0,
        websites_scanned_today: 0,
        repos_total: 0,
        repos_high_risk: 0,
        ai_threats_total: 0,
        ai_threats_critical: 0
      };
    }
  },

  getThreatTrend: async (): Promise<ThreatTrend[]> => {
    try {
      const response = await api.get('/dashboard/threat-trend');
      const data = response.data?.data || response.data || [];
      return data.map((item: any) => ({
        date: item.date,
        critical: item.Critical || 0,
        high: item.High || 0,
        medium: item.Medium || 0,
        low: item.Low || 0,
      }));
    } catch (error) {
      console.warn("Failed to fetch threat trend from API", error);
      return [];
    }
  },

  getRiskDistribution: async (): Promise<RiskDistribution[]> => {
    try {
      const response = await api.get('/dashboard/risk-distribution');
      return response.data?.data || response.data || [];
    } catch (error) {
      console.warn("Failed to fetch risk distribution from API", error);
      return [];
    }
  },

  getRecentActivity: async (): Promise<RecentActivity[]> => {
    try {
      const response = await api.get('/dashboard/recent-activity');
      const items = response.data?.data || response.data || [];
      return items.map((item: any) => ({
        id: item.id,
        timestamp: item.time ? new Date(item.time).toLocaleString() : 'Just now',
        module: item.module,
        action: item.action,
        target: item.action,
        status: item.status,
      }));
    } catch (error) {
      console.warn("Failed to fetch recent activity from API", error);
      return [];
    }
  },

  getCriticalFindings: async (): Promise<CriticalFinding[]> => {
    try {
      const response = await api.get('/dashboard/critical-findings');
      const items = response.data?.data || response.data || [];
      return items.map((item: any) => ({
        id: item.id,
        title: item.description,
        severity: item.severity,
        module: item.module,
        target: item.module,
        timestamp: item.timestamp ? new Date(item.timestamp).toLocaleString() : 'Recently',
        status: 'Open',
      }));
    } catch (error) {
      console.warn("Failed to fetch critical findings from API", error);
      return [];
    }
  }
};
