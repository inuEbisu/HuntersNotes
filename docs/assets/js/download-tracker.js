(function () {
    function getFileName(url) {
        try {
            return decodeURIComponent(
                new URL(url, window.location.href).pathname,
            )
                .split("/")
                .filter(Boolean)
                .pop();
        } catch (_) {
            return url.split("/").pop();
        }
    }

    function trackDownload(link) {
        var href = link.getAttribute("href");
        if (!href || !/\.pdf(?:[?#]|$)/i.test(href)) {
            return;
        }

        var url = new URL(href, window.location.href);
        var fileName = getFileName(url.href);

        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push({
            event: "file_download",
            file_extension: "pdf",
            file_name: fileName,
            link_text: link.textContent.trim(),
            link_url: url.href,
            page_location: window.location.href,
            page_path: window.location.pathname,
        });
    }

    if (window.__downloadTrackerInstalled) {
        return;
    }

    window.__downloadTrackerInstalled = true;
    document.addEventListener("click", function (event) {
        var link = event.target.closest("a.down-button[href]");
        if (link) {
            trackDownload(link);
        }
    });
})();
