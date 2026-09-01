import { Navbar } from '@/components/landing/Navbar';
import { Hero } from '@/components/landing/Hero';
import { FeaturesGrid } from '@/components/landing/FeaturesGrid';
import { InteractiveDemo } from '@/components/landing/InteractiveDemo';
import { Pricing } from '@/components/landing/Pricing';
import { Footer } from '@/components/landing/Footer';

export const metadata = {
  title: 'SecureVision AI | Autonomous Cybersecurity & AI Threat Intelligence',
  description: 'Next-generation vulnerability scanner, ML risk classification, SHAP explainability, and AI Copilot for modern infrastructure.',
};

export default function Home() {
  return (
    <main className="min-h-screen bg-transparent text-foreground overflow-x-hidden selection:bg-primary/30 selection:text-primary-foreground">
      <Navbar />
      <Hero />
      <FeaturesGrid />
      <InteractiveDemo />
      <Pricing />
      <Footer />
    </main>
  );
}
