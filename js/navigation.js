/* ============================================================
   NOVIXA — NAVIGATION
   Sticky header state, accessible mobile drawer.
   ============================================================ */

(function () {
    "use strict";

    const header = document.getElementById("site-header");
    const toggle = document.getElementById("nav-toggle");
    const drawer = document.getElementById("mobile-nav");

    /* ---- Sticky header background on scroll ---- */
    if (header) {
        const onScroll = () => {
            header.classList.toggle("is-scrolled", window.scrollY > 8);
        };
        onScroll();
        window.addEventListener("scroll", onScroll, { passive: true });
    }

    /* ---- Mobile drawer ---- */
    if (toggle && drawer) {
        const setOpen = (open) => {
            toggle.setAttribute("aria-expanded", String(open));
            toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
            drawer.setAttribute("aria-hidden", String(!open));
            drawer.classList.toggle("is-open", open);
        };

        toggle.addEventListener("click", () => {
            const open = toggle.getAttribute("aria-expanded") === "true";
            setOpen(!open);
        });

        /* Close when a link is chosen */
        drawer.querySelectorAll("a").forEach((link) => {
            link.addEventListener("click", () => setOpen(false));
        });

        /* Close on Escape */
        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
                setOpen(false);
                toggle.focus();
            }
        });

        /* Close when resizing up to desktop */
        window.addEventListener("resize", () => {
            if (window.innerWidth > 860) setOpen(false);
        });
    }

    /* ---- Current year in footer ---- */
    const yearEl = document.getElementById("year");
    if (yearEl) yearEl.textContent = String(new Date().getFullYear());
})();
