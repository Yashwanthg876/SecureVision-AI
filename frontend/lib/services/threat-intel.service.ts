import api from '@/lib/api';
import { ThreatIOC, IOCLookupResult, ThreatIntelStats } from '@/types/threat-intel';

export interface ThreatFeedParams {
  limit?: number;
  severity?: string;
  ioc_type?: string;
  query?: string;
}

export const threatIntelService = {
  getFeed: async (params: ThreatFeedParams = {}): Promise<ThreatIOC[]> => {
    try {
      const response = await api.get('/threat-intel/feed', {
        params: {
          limit: params.limit || 50,
          severity: params.severity || undefined,
          ioc_type: params.ioc_type || undefined,
          q: params.query || undefined,
        },
      });
      const data = response.data?.data?.items || response.data?.items || [];
      return data;
    } catch (error) {
      console.warn("Failed to fetch threat intel feed from API", error);
      return [];
    }
  },

  lookupIOC: async (query: string): Promise<IOCLookupResult> => {
    try {
      const response = await api.post('/threat-intel/lookup', { query });
      return response.data?.data || response.data;
    } catch (error) {
      console.warn("Failed to perform lookup via API", error);
      return {
        query,
        matched: false,
        ioc: null,
        risk_level: "LOW",
        verdict: "UNABLE TO PROCESS LOOKUP",
        reputation_score: 50.0,
        analysis_details: `Unable to complete lookup for '${query}'. Check backend connection.`,
        recommended_action: "Ensure backend API service is running.",
      };
    }
  },

  getStats: async (): Promise<ThreatIntelStats> => {
    try {
      const response = await api.get('/threat-intel/stats');
      return response.data?.data || response.data;
    } catch (error) {
      console.warn("Failed to fetch threat stats from API", error);
      return {
        total_active_iocs: 0,
        critical_threats: 0,
        high_threats: 0,
        medium_threats: 0,
        low_threats: 0,
        top_threat_vector: "None",
        avg_confidence_score: 0.0,
        category_distribution: {},
      };
    }
  },
};
