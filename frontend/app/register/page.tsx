import { AuthLayout } from "@/components/auth/AuthLayout";
import { RegisterForm } from "@/components/auth/RegisterForm";

export const metadata = {
  title: "Register | SecureVision AI",
  description: "Create a new SecureVision AI account.",
};

export default function RegisterPage() {
  return (
    <AuthLayout
      title="Create Account"
      subtitle="Join SecureVision AI to start monitoring your infrastructure"
    >
      <RegisterForm />
    </AuthLayout>
  );
}
