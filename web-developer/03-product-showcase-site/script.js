// Aurora Buds — Product Showcase Site
// Handles: mobile nav toggle, color thumbnail gallery switching,
// quantity stepper, and a client-side "add to cart" confirmation.

document.addEventListener("DOMContentLoaded", () => {
  /* ---------- Mobile nav toggle ---------- */
  const navToggle = document.getElementById("navToggle");
  const primaryNav = document.getElementById("primaryNav");

  if (navToggle && primaryNav) {
    const closeNav = () => {
      primaryNav.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
    };

    navToggle.addEventListener("click", () => {
      const isOpen = primaryNav.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
    });

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
  }

  /* ---------- Color thumbnail gallery ---------- */
  const thumbs = document.querySelectorAll(".thumb");
  const mainImage = document.getElementById("mainImage");

  const gradients = {
    violet: "linear-gradient(135deg, #7209b7, #f72585)",
    cyan: "linear-gradient(135deg, #06b6d4, #4361ee)",
    coral: "linear-gradient(135deg, #f72585, #ff9770)",
    slate: "linear-gradient(135deg, #4b5563, #1f2937)",
  };

  thumbs.forEach((thumb) => {
    thumb.addEventListener("click", () => {
      const variant = thumb.dataset.variant;

      thumbs.forEach((t) => t.classList.remove("thumb--active"));
      thumb.classList.add("thumb--active");

      if (mainImage && gradients[variant]) {
        mainImage.style.background = gradients[variant];
      }

      // Keep the "Buy" color picker in sync with the gallery selection.
      const matchingRadio = document.querySelector(
        `.color-option input[value="${variant}"]`
      );
      if (matchingRadio) {
        matchingRadio.checked = true;
      }
    });
  });

  /* ---------- Quantity stepper ---------- */
  const qtyInput = document.getElementById("qty");
  const qtyMinus = document.getElementById("qtyMinus");
  const qtyPlus = document.getElementById("qtyPlus");

  const clampQty = (value) => {
    const min = Number(qtyInput.min) || 1;
    const max = Number(qtyInput.max) || 10;
    return Math.min(max, Math.max(min, value));
  };

  if (qtyInput && qtyMinus && qtyPlus) {
    qtyMinus.addEventListener("click", () => {
      qtyInput.value = clampQty((Number(qtyInput.value) || 1) - 1);
    });

    qtyPlus.addEventListener("click", () => {
      qtyInput.value = clampQty((Number(qtyInput.value) || 1) + 1);
    });

    qtyInput.addEventListener("change", () => {
      qtyInput.value = clampQty(Number(qtyInput.value) || 1);
    });
  }

  /* ---------- Buy form ---------- */
  const buyForm = document.getElementById("buyForm");
  const buyConfirmation = document.getElementById("buyConfirmation");

  if (buyForm && buyConfirmation) {
    buyForm.addEventListener("submit", (event) => {
      event.preventDefault();

      const selectedColor = buyForm.querySelector(
        'input[name="color"]:checked'
      );
      const colorName = selectedColor ? selectedColor.value : "violet";
      const qty = qtyInput ? Number(qtyInput.value) || 1 : 1;
      const unitPrice = 129;
      const total = (unitPrice * qty).toFixed(2);

      buyConfirmation.textContent = `Added ${qty} × Aurora Buds (${colorName}) to cart — $${total} total.`;
    });
  }
});
