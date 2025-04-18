import routes from "@cache/routes";
import { createRouter, createWebHistory } from "vue-router";
import { assertType } from "@/assets/ts/types";

import type { RouteMeta } from "vite-plugin-vue-xecades-note";

const router = createRouter({
    routes: routes,
    scrollBehavior: (_, __, saved) => saved ?? { left: 0, top: 0 },
    history: createWebHistory(),
});

router.afterEach((to, from) => {
    const meta = assertType<RouteMeta>(to.meta);
    if (meta.type === "root") document.title = "猎人笔记";
    else document.title = `${meta.attr.title} | 猎人笔记`;
});

export default router;
