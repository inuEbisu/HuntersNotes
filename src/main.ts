// Modules
import { createApp } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import MasonryWall from "@yeger/vue-masonry-wall";

// Vue
import App from "./App.vue";

// JS
import "./assets/ts/fontawesome";
// import "./assets/ts/cursor";
import router from "./router";

// CSS
import "./assets/css/reset.styl";
// import "./assets/css/cursor.styl";
import "katex/dist/katex.min.css";
import "overlayscrollbars/overlayscrollbars.css";

// Console
const consoleMessage = () => {
    console.log(atob("ICBfX19fXyAgICBfIF8gICAgICAgICAgICAgICAgICBfICAgICAgICAgCiB8XyAgIF98IF8oXykgfF9fIF8gIF8gX18gXyBfIF8oXylfICBfIF9fXwogICB8IHx8ICdffCB8ICdfIFwgfHwgLyBfYCB8ICdffCB8IHx8IChfLTwKICAgfF98fF98IHxffF8uX18vXF8sX1xfXyxffF98IHxffFxfLF8vX18v"));
};

// Main
(async () => {
    consoleMessage();

    const app = createApp(App);
    app.use(router);
    app.use(MasonryWall);
    app.component("font-awesome-icon", FontAwesomeIcon);
    app.mount("#app");
})();
