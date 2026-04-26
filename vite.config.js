/** @type {import("vite").UserConfig} */
const config = {
  environments: {
    ssr: {
      build: {
        rolldownOptions: {
          output: {
            entryFileNames: "[name].js",
            chunkFileNames: "assets/[name]-[hash].js",
          },
        },
      },
    },
  },
};

export default config;
