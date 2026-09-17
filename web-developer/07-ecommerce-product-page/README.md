# Project 07 — E-Commerce Product Page (Orbit Hoodie)

A React + Vite single-product e-commerce page built for the Lumexa "React and
Full-Stack Web" course. It demonstrates real component state, React Context
for a shared cart, and derived price calculations.

## What it is

- An image gallery with a large preview and clickable thumbnails (CSS-gradient
  "photos" — no external images, nothing to break).
- Color, size, and quantity selectors backed by real `useState`.
- Price calculation that accounts for size surcharges and quantity.
- An "Add to Cart" flow using React Context (`CartContext`) so the cart count
  and drawer are available anywhere in the app.
- A slide-out cart drawer where you can change quantities or remove items,
  with a live total.

## Run locally

```bash
npm install
npm run dev
```

Then open the URL Vite prints (usually `http://localhost:5173`).

## Build for production

```bash
npm run build
```

This outputs a static production build to `dist/`.

## Deploy to Vercel

1. Push this project to a GitHub repository.
2. Go to [vercel.com/new](https://vercel.com/new) and import the repository.
3. Framework preset: Vercel auto-detects **Vite**. If asked manually, set:
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. No environment variables are required for this project.
5. Click **Deploy** — Vercel builds and hosts it on a `*.vercel.app` URL.
