import { useCart } from "../context/CartContext";

export default function Header() {
  const { cartCount, setDrawerOpen } = useCart();

  return (
    <header className="site-header">
      <span className="site-logo">Lumexa Shop</span>
      <button
        type="button"
        className="cart-button"
        onClick={() => setDrawerOpen(true)}
        aria-label="Open cart"
      >
        🛒 <span className="cart-count">{cartCount}</span>
      </button>
    </header>
  );
}
