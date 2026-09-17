import { useMemo, useState } from "react";
import { useCart } from "../context/CartContext";

export default function ProductInfo({ product }) {
  const [selectedColorId, setSelectedColorId] = useState(product.colors[0].id);
  const [selectedSizeId, setSelectedSizeId] = useState(product.sizes[2].id); // default "M"
  const [quantity, setQuantity] = useState(1);
  const [justAdded, setJustAdded] = useState(false);

  const { addItem } = useCart();

  const unitPrice = useMemo(() => {
    const surcharge = product.sizeSurcharge[selectedSizeId] ?? 0;
    return product.basePrice + surcharge;
  }, [product, selectedSizeId]);

  const totalPrice = useMemo(() => unitPrice * quantity, [unitPrice, quantity]);

  const selectedColor = product.colors.find((c) => c.id === selectedColorId);
  const selectedSize = product.sizes.find((s) => s.id === selectedSizeId);

  function handleAddToCart() {
    const key = `${product.id}-${selectedColorId}-${selectedSizeId}`;
    addItem({
      key,
      name: product.name,
      color: selectedColor.name,
      size: selectedSize.id,
      unitPrice,
      quantity,
    });

    setJustAdded(true);
    // Reset the confirmation message after a short delay.
    setTimeout(() => setJustAdded(false), 1800);
  }

  function handleQuantityChange(delta) {
    setQuantity((prev) => {
      const next = prev + delta;
      if (next < 1) return 1;
      if (next > product.maxQuantity) return product.maxQuantity;
      return next;
    });
  }

  return (
    <div className="product-info">
      <p className="product-brand">{product.brand}</p>
      <h1 className="product-name">{product.name}</h1>

      <div className="product-rating">
        <span aria-hidden="true">{"★".repeat(Math.round(product.rating))}</span>
        <span className="product-rating-text">
          {product.rating.toFixed(1)} ({product.reviewCount} reviews)
        </span>
      </div>

      <p className="product-price">${unitPrice.toFixed(2)}</p>

      <p className="product-description">{product.description}</p>

      <fieldset className="option-group">
        <legend>Color: {selectedColor.name}</legend>
        <div className="swatches">
          {product.colors.map((color) => (
            <button
              key={color.id}
              type="button"
              className={`swatch ${selectedColorId === color.id ? "swatch--active" : ""}`}
              style={{ backgroundColor: color.hex }}
              onClick={() => setSelectedColorId(color.id)}
              aria-label={color.name}
              aria-pressed={selectedColorId === color.id}
            />
          ))}
        </div>
      </fieldset>

      <fieldset className="option-group">
        <legend>Size: {selectedSize.label}</legend>
        <div className="sizes">
          {product.sizes.map((size) => (
            <button
              key={size.id}
              type="button"
              className={`size-button ${selectedSizeId === size.id ? "size-button--active" : ""}`}
              onClick={() => setSelectedSizeId(size.id)}
              aria-pressed={selectedSizeId === size.id}
            >
              {size.label}
            </button>
          ))}
        </div>
      </fieldset>

      <fieldset className="option-group">
        <legend>Quantity</legend>
        <div className="quantity-stepper">
          <button
            type="button"
            onClick={() => handleQuantityChange(-1)}
            disabled={quantity <= 1}
            aria-label="Decrease quantity"
          >
            &minus;
          </button>
          <span className="quantity-value">{quantity}</span>
          <button
            type="button"
            onClick={() => handleQuantityChange(1)}
            disabled={quantity >= product.maxQuantity}
            aria-label="Increase quantity"
          >
            +
          </button>
        </div>
      </fieldset>

      <div className="add-to-cart-row">
        <button type="button" className="add-to-cart-button" onClick={handleAddToCart}>
          Add to Cart &mdash; ${totalPrice.toFixed(2)}
        </button>
        {justAdded && <p className="added-confirmation">Added to cart!</p>}
      </div>
    </div>
  );
}
