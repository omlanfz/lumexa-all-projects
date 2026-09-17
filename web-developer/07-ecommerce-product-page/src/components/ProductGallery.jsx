import { useState } from "react";

export default function ProductGallery({ images }) {
  const [activeIndex, setActiveIndex] = useState(0);
  const active = images[activeIndex];

  return (
    <div className="gallery">
      <div className="gallery-main" style={{ background: active.gradient }}>
        <span className="gallery-main-label">{active.label}</span>
      </div>
      <div className="gallery-thumbs">
        {images.map((image, index) => (
          <button
            key={image.id}
            type="button"
            className={`gallery-thumb ${index === activeIndex ? "gallery-thumb--active" : ""}`}
            style={{ background: image.gradient }}
            onClick={() => setActiveIndex(index)}
            aria-label={`Show ${image.label}`}
            aria-pressed={index === activeIndex}
          />
        ))}
      </div>
    </div>
  );
}
