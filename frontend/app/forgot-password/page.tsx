import { AuthLayout } from "@/components/auth/AuthLayout";
import { ForgotPasswordForm } from "@/components/auth/ForgotPasswordForm";

export const metadata = {
  title: "Forgot Password | SecureVision AI",
  description: "Reset your SecureVision AI password.",
};

export default function ForgotPasswordPage() {
  return (
    <AuthLayout
      title="Reset Password"
      subtitle="Recover access to your account"
    >
      <ForgotPasswordForm />
    </AuthLayout>
  );
}
