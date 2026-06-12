(function () {
    var script = document.currentScript;
    if (!script) {
        script = Array.prototype.find.call(document.scripts, function (item) {
            return /(?:^|\/)site-stats\.js(?:[?#].*)?$/.test(item.src);
        });
    }

    if (!script) {
        return;
    }

    var statsUrl = new URL("../site-stats.json", script.src);

    fetch(statsUrl)
        .then(function (response) {
            if (!response.ok) {
                throw new Error("Failed to load site statistics");
            }
            return response.json();
        })
        .then(function (stats) {
            document
                .querySelectorAll("[data-site-stat]")
                .forEach(function (node) {
                    var key = node.getAttribute("data-site-stat");
                    if (Object.prototype.hasOwnProperty.call(stats, key)) {
                        node.textContent = stats[key].toLocaleString();
                    }
                });
        })
        .catch(function () {});
})();
