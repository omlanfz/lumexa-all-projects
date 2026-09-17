// Product data for the Lumexa Orbit Hoodie demo product page.
// Images are generated with CSS gradients (see ProductGallery.jsx) so there
// are no external network requests and nothing can 404.

export const product = {
  id: "orbit-hoodie-001",
  name: "Orbit Hoodie",
  brand: "Lumexa Wear",
  rating: 4.7,
  reviewCount: 128,
  description:
    "A cozy, glow-in-the-dark hoodie inspired by deep space nebulae. Made from brushed cotton fleece, it keeps you warm during late-night coding missions while the reflective star print catches the light.",
  basePrice: 58,
  gallery: [
    { id: "g1", gradient: "linear-gradient(135deg, #1e1b4b 0%, #4c1d95 50%, #7c3aed 100%)", label: "Front view" },
    { id: "g2", gradient: "linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0ea5e9 100%)", label: "Back view" },
    { id: "g3", gradient: "linear-gradient(135deg, #312e81 0%, #6d28d9 50%, #db2777 100%)", label: "Hood detail" },
    { id: "g4", gradient: "linear-gradient(135deg, #052e16 0%, #065f46 50%, #10b981 100%)", label: "Sleeve print" },
  ],
  colors: [
    { id: "nebula-purple", name: "Nebula Purple", hex: "#7c3aed" },
    { id: "deep-space-blue", name: "Deep Space Blue", hex: "#0ea5e9" },
    { id: "comet-green", name: "Comet Green", hex: "#10b981" },
  ],
  sizes: [
    { id: "xs", label: "XS" },
    { id: "s", label: "S" },
    { id: "m", label: "M" },
    { id: "l", label: "L" },
    { id: "xl", label: "XL" },
  ],
  // A couple of sizes cost a little more because they use extra fabric.
  sizeSurcharge: {
    xs: 0,
    s: 0,
    m: 0,
    l: 3,
    xl: 5,
  },
  maxQuantity: 10,
};
