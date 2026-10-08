'use client';

import { motion } from "framer-motion";
import { PageTitle } from "@/components/layout/PageTitle";
import { ProfileCard } from "@/components/profile/ProfileCard";
import { ProfileEditForm } from "@/components/profile/ProfileEditForm";
import { SecuritySettingsForm } from "@/components/profile/SecuritySettingsForm";
import { useUser } from "@/context/UserContext";

export default function ProfilePage() {
  const { user, updateUser } = useUser();

  const handleProfileUpdate = async (updated: { fullName: string; email: string; organization: string }) => {
    await updateUser({
      full_name: updated.fullName,
      email: updated.email,
      organization: updated.organization,
    });
  };

  const profileData = {
    fullName: user.full_name || "Security Analyst",
    email: user.email || "analyst@securevision.ai",
    organization: user.organization || "Enterprise Workspace",
    role: user.role || "Lead Security Analyst",
    joinedDate: user.created_at ? new Date(user.created_at).toLocaleDateString('en-US', { month: 'long', year: 'numeric' }) : "Active Member",
  };

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
          title="User Profile"
          subtitle="Manage your personal account credentials, role authorization, and security preferences."
        />
      </motion.div>

      {/* Profile Overview Card */}
      <ProfileCard user={profileData} />

      {/* Grid: Edit Info + Security Settings */}
      <div className="grid gap-8 lg:grid-cols-2">
        <ProfileEditForm key={`${profileData.fullName}-${profileData.email}`} initialUser={profileData} onUpdate={handleProfileUpdate} />
        <SecuritySettingsForm />
      </div>
    </div>
  );
}
