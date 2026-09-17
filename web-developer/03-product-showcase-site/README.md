# Product Showcase Site — Aurora Buds

A responsive single-product marketing/showcase page for a fictional pair of
wireless earbuds ("Aurora Buds"), built with plain HTML5, CSS3 (Flexbox +
CSS Grid), and vanilla JavaScript. It includes a hero/gallery, a features
grid, a specs table, customer reviews, and a working "buy" panel with color
selection and a quantity stepper.

## Folder Structure
```
03-product-showcase-site/
├── index.html    # Page content and structure
├── styles.css    # Layout, responsive breakpoints, and styling
├── script.js     # Nav toggle, gallery switching, qty stepper, buy form
└── README.md     # This file
```

## Features
- **Mobile-first responsive design** with breakpoints at 768px and 1024px.
- **CSS Grid** features grid and reviews grid; **Flexbox** header, buy form,
  and quantity stepper.
- Clickable color thumbnails that update the hero illustration's gradient
  and stay in sync with the color radio buttons in the buy panel.
- A quantity stepper (+/-) clamped between 1 and 10.
- A client-side "Add to cart" flow: submitting the form computes the total
  from the selected color and quantity and shows a confirmation message
  (`aria-live="polite"`) — no backend required, everything runs in-browser.
- Accessible hamburger menu, radio-button color picker with visible focus
  styles, and a semantic specs `<table>` with `scope="row"` headers.
- Respects `prefers-reduced-motion`.

## Run It Locally
No build tools or installation required.

- **Option A:** Double-click `index.html`, or drag it into any browser window.
- **Option B (recommended, avoids any local file quirks):**
  ```
  npx serve .
  ```
  then open the printed `http://localhost:...` address in your browser.

## Deploy to Vercel

**Option A — Import via the Vercel website**
1. Push this folder to a new GitHub repository:
   ```
   git init
   git add .
   git commit -m "Initial commit: product showcase site"
   git remote add origin https://github.com/<your-username>/product-showcase-site.git
   git branch -M main
   git push -u origin main
   ```
2. Go to [vercel.com](https://vercel.com), sign in, click **Add New Project**, and select this repository.
3. No build command is needed for a static HTML/CSS/JS site — click **Deploy**.
4. Vercel gives you a live URL such as `https://product-showcase-site.vercel.app`.

**Option B — Vercel CLI**
```
npm install -g vercel
vercel
```
Follow the CLI prompts; it deploys the current folder directly and prints a live URL.

Once connected to GitHub, every future `git push` to `main` automatically redeploys the live site.
