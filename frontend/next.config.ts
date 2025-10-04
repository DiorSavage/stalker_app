import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  experimental: {
    serverActions: {
      bodySizeLimit: '1mb',
    }
  },
  devIndicators: {
    buildActivity: false
  },
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "t.me",
        port: "",
        pathname: '/i/userpic/**'
      },
      {
        protocol: "http",
        hostname: "localhost",
        port: "8000",
        pathname: "/uploads/**"
      }
    ]
  }
};

export default nextConfig;
