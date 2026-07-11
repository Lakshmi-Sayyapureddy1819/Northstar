import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Consume the workspace design system as source (transpiled by Next).
  transpilePackages: ["@northstar/ui"],
  // ESLint configuration is centralized in Milestone 5; do not block builds on it yet.
  eslint: { ignoreDuringBuilds: true },
};

export default nextConfig;
