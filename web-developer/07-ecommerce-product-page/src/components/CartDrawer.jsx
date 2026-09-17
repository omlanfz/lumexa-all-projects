import { useCart } from "../context/CartContext";

export default function CartDrawer() {
  const { items, isDrawerOpen, setDrawerOpen, removeItem, updateQuantity, cartTotal } =
    useCart();

  if (!isDrawerOpen) return null;

  return (
    <div className="drawer-overlay" onClick={() => setDrawerOpen(false)}>
      <aside className="drawer" onClick={(event) => event.stopPropagation()}>
        <div className="drawer-header">
          <h2>Your Cart</h2>
          <button
            type="button"
            className="drawer-close"
            onClick={() => setDrawerOpen(false)}
            aria-label="Close cart"
          >
            &times;
          </button>
        </div>

        {items.length === 0 ? (
          <p className="drawer-empty">Your cart is empty. Add something from the mission catalog!</p>
        ) : (
          <ul className="drawer-list">
            {items.map((item) => (
              <li key={item.key} className="drawer-item">
                <div>
                  <p className="drawer-item-name">{item.name}</p>
                  <p className="drawer-item-meta">
                    {item.color} / {item.size.toUpperCase()}
                  </p>
                  <p className="drawer-item-price">${item.unitPrice.toFixed(2)} each</p>
                </div>
                <div className="drawer-item-controls">
                  <label className="drawer-item-qty">
                    Qty
                    <select
                      value={item.quantity}
                      onChange={(event) =>
                        updateQuantity(item.key, Number(event.target.value))
                      }
                    >
                      {Array.from({ length: 10 }, (_, i) => i + 1).map((n) => (
                        <option key={n} value={n}>
                          {n}
                        </option>
                      ))}
                    </select>
                  </label>
                  <button
                    type="button"
                    className="drawer-item-remove"
                    onClick={() => removeItem(item.key)}
                  >
                    Remove
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}

        <div className="drawer-footer">
          <span>Total</span>
          <strong>${cartTotal.toFixed(2)}</strong>
        </div>
      </aside>
    </div>
  );
}
