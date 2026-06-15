(function () {
    var retries = 0;

    function initGlightbox() {
        if (typeof GLightbox !== "function") {
            if (retries < 20) {
                retries += 1;
                window.setTimeout(initGlightbox, 100);
            }
            return;
        }

        retries = 0;
        if (window.__hnGlightbox) {
            window.__hnGlightbox.reload();
            return;
        }

        window.__hnGlightbox = GLightbox({ selector: ".glightbox" });
    }

    if (typeof document$ !== "undefined") {
        document$.subscribe(initGlightbox);
    } else {
        document.addEventListener("DOMContentLoaded", initGlightbox);
    }
})();
