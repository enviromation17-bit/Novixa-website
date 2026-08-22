/* ============================================================
   NOVIXA — NAVIGATION
   Desktop + Mobile Navigation
   ============================================================ */

(function () {
    "use strict";

    const toggle = document.getElementById("nav-toggle");
    const mobileNav = document.getElementById("mobile-nav");

    if (!toggle || !mobileNav) {
        return;
    }

    function openMenu() {

        mobileNav.classList.add("is-open");

        toggle.setAttribute(
            "aria-expanded",
            "true"
        );

        toggle.setAttribute(
            "aria-label",
            "Close menu"
        );

        mobileNav.setAttribute(
            "aria-hidden",
            "false"
        );
    }


    function closeMenu() {

        mobileNav.classList.remove("is-open");

        toggle.setAttribute(
            "aria-expanded",
            "false"
        );

        toggle.setAttribute(
            "aria-label",
            "Open menu"
        );

        mobileNav.setAttribute(
            "aria-hidden",
            "true"
        );
    }


    toggle.addEventListener(
        "click",
        function () {

            const isOpen =
                mobileNav.classList.contains("is-open");

            if (isOpen) {
                closeMenu();
            } else {
                openMenu();
            }

        }
    );


    /*
     * Close the mobile menu after
     * selecting a navigation link.
     */

    mobileNav
        .querySelectorAll("a")
        .forEach(function (link) {

            link.addEventListener(
                "click",
                closeMenu
            );

        });


    /*
     * Allow Escape to close the menu.
     */

    document.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Escape" &&
                mobileNav.classList.contains("is-open")
            ) {

                closeMenu();

                toggle.focus();
            }

        }
    );


    /*
     * Reset mobile navigation when
     * returning to desktop width.
     */

    window.addEventListener(
        "resize",
        function () {

            if (window.innerWidth > 850) {
                closeMenu();
            }

        }
    );

})();