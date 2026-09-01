import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  experimental: {
    // Allow long-running backend scan requests (GitHub scanner can take 20-40s)
    proxyTimeout: 90000,
  },
  async rewrites() {
    return [
      {
        source: "/api/v1/:path*",
        destination: "http://localhost:8000/api/v1/:path*",
      },
    ];
  },
};

export default nextConfig;
