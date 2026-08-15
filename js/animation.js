/* ============================================================
   NOVIXA — SCROLL REVEAL
   Progressive enhancement. Never hides content if JS fails.
   ============================================================ */

(function () {
    "use strict";

    const targets = document.querySelectorAll(".reveal");
    if (!targets.length) return;

    /* If IntersectionObserver is unsupported, reveal everything. */
    if (!("IntersectionObserver" in window)) {
        targets.forEach((el) => el.classList.add("is-visible"));
        return;
    }

    /* Add a subtle stagger to grouped cards sharing a parent. */
    document.querySelectorAll(
        ".solutions-grid, .tech-grid, .projects-grid, .about-grid, .process-track"
    ).forEach((group) => {
        const items = group.querySelectorAll(".reveal");
        items.forEach((el, i) => {
            el.classList.add("stagger-" + ((i % 4) + 1));
        });
    });

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.14, rootMargin: "0px 0px -8% 0px" }
    );

    targets.forEach((el) => observer.observe(el));
})();
