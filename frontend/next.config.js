/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverActions: true,
  },
  webpack: (config, context) => {
    config.watchOptions = {
      poll: 500,
      aggregateTimeout: 300,
    };

    return config;
  },
  images: {
    domains: ["accounts.google.com"],
  },
};

module.exports = nextConfig;
