/* =========================================
   NOVIXA SCROLL REVEAL SYSTEM
   ========================================= */
console.log("Novixa animation.js loaded");


document.addEventListener("DOMContentLoaded", () => {

    /*
       Find the elements that should receive
       scroll-reveal animations.
    */

    const revealElements = document.querySelectorAll(
        ".section-heading, .about-card, .service-card, " +
        ".solution-card, .tech-card, .why-card, " +
        ".contact-info, .contact-form-card"
    );


    /*
       If IntersectionObserver is not supported,
       keep everything visible.

       Animation is an enhancement.
       It must never break the website.
    */

    if (!("IntersectionObserver" in window)) {

        revealElements.forEach((element) => {

            element.classList.add("is-visible");

        });

        return;
    }


    /*
       Prepare animation classes.
    */

    revealElements.forEach((element, index) => {

        /*
           Section headings receive the larger
           reveal movement.
        */

        if (element.classList.contains("section-heading")) {

            element.classList.add("scroll-reveal");

        } else {

            /*
               Cards and content blocks receive
               the smaller card animation.
            */

            element.classList.add("scroll-reveal-card");


            /*
               Create a controlled stagger.

               The delay cycles between four values.
            */

            const delayNumber = (index % 4) + 1;

            element.classList.add(
                `scroll-delay-${delayNumber}`
            );
        }
    });


    /*
       Observe elements entering and leaving
       the viewport.
    */

    const observer = new IntersectionObserver(
        (entries) => {

            entries.forEach((entry) => {

                if (entry.isIntersecting) {

                    /*
                       Element has entered the viewport.
                    */

                    entry.target.classList.add("is-visible");

                } else {

                    /*
                       Element has left the viewport.

                       Remove the class so the animation
                       can happen again when the user
                       returns to the section.
                    */

                    entry.target.classList.remove("is-visible");

                }

            });

        },
        {
            /*
               Start the animation when roughly
               15% of the element is visible.
            */

            threshold: 0.15
        }
    );


    /*
       Begin observing every animation target.
    */

    revealElements.forEach((element) => {

        observer.observe(element);

    });

});