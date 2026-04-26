/** @type {import("zudoku").ZudokuConfig} */
const normalizeBasePath = (value) => {
  if (!value) {
    return undefined;
  }

  const trimmed = value.trim();
  if (!trimmed || trimmed === "/") {
    return undefined;
  }

  return `/${trimmed.replace(/^\/+|\/+$/g, "")}`;
};

const config = {
  basePath: normalizeBasePath(process.env.ZUDOKU_BASE_PATH),
  site: {
    title: "Social Network API Docs",
  },
  navigation: [
    {
      type: "category",
      label: "Documentation",
      items: [
        { type: "doc", file: "installation", label: "Installation" },
        { type: "doc", file: "authorization", label: "Authorization" },
        { type: "doc", file: "about", label: "About" },
      ],
    },
    { type: "link", to: "/about", label: "About" },
    { type: "link", to: "/api", label: "API Reference" },
  ],
  redirects: [{ from: "/", to: "/installation" }],
  apis: {
    type: "file",
    input: "./openapi/social_network_api.yaml",
    path: "/api",
  },
  docs: {
    files: "/pages/**/*.mdx",
  },
};

export default config;
