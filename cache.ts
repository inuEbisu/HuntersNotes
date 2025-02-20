import { tsImport } from "tsx/esm/api";

// Thx to motherfxxking Node.js TypeScript support
const launch: typeof import("vite-plugin-vue-xecades-note/src/index").launch = (await tsImport("vite-plugin-vue-xecades-note/src/index", import.meta.url)).launch;

launch({
    componentDir: "src/components/md",
    pluginName: "vite-plugin-vue-xecades-note",
});
