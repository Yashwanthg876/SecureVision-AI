import { useState, useEffect, useCallback } from 'react';
import { dashboardService } from '@/lib/services/dashboard.service';
import { DashboardData } from '@/types/dashboard';

export function useDashboard() {
  const [data, setData] = useState<DashboardData>({
    summary: null,
    threatTrend: [],
    riskDistribution: [],
    recentActivity: [],
    criticalFindings: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [
        summary,
        threatTrend,
        riskDistribution,
        recentActivity,
        criticalFindings
      ] = await Promise.all([
        dashboardService.getSummary(),
        dashboardService.getThreatTrend(),
        dashboardService.getRiskDistribution(),
        dashboardService.getRecentActivity(),
        dashboardService.getCriticalFindings(),
      ]);

      setData({
        summary,
        threatTrend,
        riskDistribution,
        recentActivity,
        criticalFindings
      });
    } catch (err) {
      console.error('Failed to fetch dashboard data:', err);
      setError('Failed to load dashboard data. Please try again.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return {
    ...data,
    loading,
    error,
    refresh
  };
}
