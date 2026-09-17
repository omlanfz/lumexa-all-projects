import { CartProvider } from "./context/CartContext";
import Header from "./components/Header";
import ProductGallery from "./components/ProductGallery";
import ProductInfo from "./components/ProductInfo";
import CartDrawer from "./components/CartDrawer";
import { product } from "./data/product";
import "./index.css";

export default function App() {
  return (
    <CartProvider>
      <Header />
      <main className="product-page">
        <ProductGallery images={product.gallery} />
        <ProductInfo product={product} />
      </main>
      <CartDrawer />
    </CartProvider>
  );
}
