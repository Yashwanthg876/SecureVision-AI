'use client';

import { motion } from "framer-motion";
import { PageTitle } from "@/components/layout/PageTitle";
import { APIKeysSettings } from "@/components/settings/APIKeysSettings";
import { NotificationSettings } from "@/components/settings/NotificationSettings";
import { ScanPreferencesSettings } from "@/components/settings/ScanPreferencesSettings";

export default function SettingsPage() {
  return (
    <div className="relative space-y-10 pb-12">
      {/* Ambient glowing backdrop */}
      <div
        className="pointer-events-none absolute -top-20 -left-20 w-96 h-96 bg-[#8B5CF6]/5 rounded-full blur-[100px]"
        aria-hidden="true"
      />

      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
        <PageTitle
          title="System Settings"
          subtitle="Configure API credentials, security notifications, webhooks, and assessment engine behavior."
        />
      </motion.div>

      {/* API Keys Settings */}
      <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.1 }}>
        <APIKeysSettings />
      </motion.div>

      {/* Grid: Notifications + Scan Preferences */}
      <div className="grid gap-8 lg:grid-cols-2">
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.2 }}>
          <NotificationSettings />
        </motion.div>
        <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.3 }}>
          <ScanPreferencesSettings />
        </motion.div>
      </div>
    </div>
  );
}
