/* ============================================================
   NOVIXA — SCROLL REVEAL
   Enter viewport  → visible
   Leave viewport  → hidden
   Enter again     → visible again

   Progressive enhancement:
   JavaScript failure must never hide website content.
   ============================================================ */

(function () {
    "use strict";

    function initScrollReveal() {

        const targets = document.querySelectorAll(".reveal");

        if (!targets.length) {
            return;
        }
        document.documentElement.classList.add("reveal-ready");

        /*
         * If IntersectionObserver is unavailable,
         * keep everything visible.
         */
        if (!("IntersectionObserver" in window)) {

            targets.forEach((element) => {
                element.classList.add("is-visible");
            });

            return;
        }

        /*
         * Add stagger classes to groups of cards.
         */
        const groups = document.querySelectorAll(
            ".services-grid, " +
            ".solutions-grid, " +
            ".projects-grid, " +
            ".tech-grid, " +
            ".about-grid, " +
            ".why-grid, " +
            ".process-track"
        );

        groups.forEach((group) => {

            const items = group.querySelectorAll(".reveal");

            items.forEach((element, index) => {

                const delayNumber = (index % 4) + 1;

                element.classList.add(
                    "reveal-delay-" + delayNumber
                );

            });

        });

        /*
         * Observe elements whenever they enter
         * and leave the viewport.
         */
        const observer = new IntersectionObserver(
            (entries) => {

                entries.forEach((entry) => {

                    if (entry.isIntersecting) {

                        /*
                         * Element entered viewport.
                         */
                        entry.target.classList.add("is-visible");

                    } else {

                        /*
                         * Element left viewport.
                         *
                         * Removing the class means the
                         * animation can happen again.
                         */
                        entry.target.classList.remove("is-visible");

                    }

                });

            },
            {
                threshold: 0.14,
                rootMargin: "0px 0px -8% 0px"
            }
        );

        targets.forEach((element) => {
            observer.observe(element);
        });
    }

    /* ============================================================
       SUBTLE CURSOR LIGHT
       ============================================================ */

    let mouseX = 50;
    let mouseY = 20;

    let targetX = 50;
    let targetY = 20;

    window.addEventListener("pointermove", (event) => {

        targetX = (event.clientX / window.innerWidth) * 100;
        targetY = (event.clientY / window.innerHeight) * 100;

    });


    function animateAmbientLight() {

        mouseX += (targetX - mouseX) * 0.08;
        mouseY += (targetY - mouseY) * 0.08;

        document.documentElement.style.setProperty(
            "--mouse-x",
            mouseX + "%"
        );

        document.documentElement.style.setProperty(
            "--mouse-y",
            mouseY + "%"
        );

        requestAnimationFrame(animateAmbientLight);
    }

    animateAmbientLight();


    /*
     * Wait until the document is ready.
     */
    if (document.readyState === "loading") {

        document.addEventListener(
            "DOMContentLoaded",
            initScrollReveal
        );

    } else {

        initScrollReveal();

    }

})();