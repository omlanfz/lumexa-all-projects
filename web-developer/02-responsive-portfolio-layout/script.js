// Responsive Portfolio Layout — mobile navigation toggle
// Opens/closes the primary nav on small screens and keeps the
// hamburger button's ARIA state in sync for screen readers.

document.addEventListener("DOMContentLoaded", () => {
  const navToggle = document.getElementById("navToggle");
  const primaryNav = document.getElementById("primaryNav");

  if (!navToggle || !primaryNav) return;

  const closeNav = () => {
    primaryNav.classList.remove("is-open");
    navToggle.setAttribute("aria-expanded", "false");
  };

  const toggleNav = () => {
    const isOpen = primaryNav.classList.toggle("is-open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
  };

  navToggle.addEventListener("click", toggleNav);

  // Close the menu after a link is tapped, and when the viewport
  // grows past the mobile breakpoint the CSS already handles.
  primaryNav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      if (window.matchMedia("(max-width: 767px)").matches) {
        closeNav();
      }
    });
  });

  window.addEventListener("resize", () => {
    if (window.matchMedia("(min-width: 768px)").matches) {
      closeNav();
    }
  });
});
