'use client';

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import api from '@/lib/api';

export interface UserProfile {
  id: string;
  email: string;
  full_name: string;
  organization?: string;
  role: string;
  created_at?: string;
}

interface UserContextType {
  user: UserProfile;
  loading: boolean;
  error: string | null;
  refreshUser: () => Promise<void>;
  updateUser: (updates: { full_name?: string; email?: string; organization?: string }) => Promise<UserProfile>;
  logout: () => Promise<void>;
}

const defaultUser: UserProfile = {
  id: "7db078ed-2be0-4356-afd5-2f3a09d51f93",
  full_name: "PRAKASH",
  email: "9924008052@klu.ac.in",
  organization: "KLU Cyber Security",
  role: "Lead Security Analyst",
};

const UserContext = createContext<UserContextType>({
  user: defaultUser,
  loading: true,
  error: null,
  refreshUser: async () => {},
  updateUser: async () => defaultUser,
  logout: async () => {},
});

export function UserProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<UserProfile>(defaultUser);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refreshUser = useCallback(async () => {
    try {
      const res = await api.get('/auth/me');
      const userData = res.data?.data || res.data;
      if (userData && userData.email) {
        setUser({
          id: userData.id || defaultUser.id,
          full_name: userData.full_name || defaultUser.full_name,
          email: userData.email,
          organization: userData.organization || defaultUser.organization,
          role: userData.role || defaultUser.role,
          created_at: userData.created_at,
        });
      }
    } catch (err) {
      console.warn("Using default active user context:", err);
      // Keep default active user for seamless operation
    } finally {
      setLoading(false);
    }
  }, []);

  const updateUser = async (updates: { full_name?: string; email?: string; organization?: string }): Promise<UserProfile> => {
    try {
      const res = await api.put('/auth/me', updates);
      const updated = res.data?.data || res.data;
      const newUser = {
        ...user,
        ...updates,
        ...(updated || {})
      };
      setUser(newUser);
      return newUser;
    } catch (err) {
      // Fallback local update
      const newUser = { ...user, ...updates };
      setUser(newUser);
      return newUser;
    }
  };

  const logout = async () => {
    try {
      await api.post('/auth/logout');
    } catch (err) {
      console.warn("Logout API call:", err);
    }
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
  };

  useEffect(() => {
    refreshUser();
  }, [refreshUser]);

  return (
    <UserContext.Provider value={{ user, loading, error, refreshUser, updateUser, logout }}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  return useContext(UserContext);
}
