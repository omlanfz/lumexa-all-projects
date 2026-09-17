# Responsive Portfolio Layout — Jonah Reyes

A mobile-first, fully responsive portfolio page for a fictional front-end
developer, built with plain HTML5, CSS3 (Flexbox + CSS Grid), and a small
vanilla-JS mobile navigation toggle. It includes a sticky header with a
hamburger menu on small screens, a hero, an about section, a CSS Grid
projects gallery, a flexbox skills row, and a contact section.

## Folder Structure
```
02-responsive-portfolio-layout/
├── index.html    # Page content and structure
├── styles.css    # Layout, responsive breakpoints, and styling
├── script.js     # Mobile nav toggle (hamburger open/close)
└── README.md     # This file
```

## Features
- **Mobile-first responsive design** with breakpoints at 768px and 1024px.
- **Flexbox** header/nav and skills row.
- **CSS Grid** projects gallery with a featured, wider card.
- Accessible hamburger menu: `aria-expanded`, `aria-controls`, and
  keyboard-operable button, closing automatically on link tap or on
  resize past the mobile breakpoint.
- Respects `prefers-reduced-motion` for users who disable animation.

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
   git commit -m "Initial commit: responsive portfolio layout"
   git remote add origin https://github.com/<your-username>/responsive-portfolio-layout.git
   git branch -M main
   git push -u origin main
   ```
2. Go to [vercel.com](https://vercel.com), sign in, click **Add New Project**, and select this repository.
3. No build command is needed for a static HTML/CSS/JS site — click **Deploy**.
4. Vercel gives you a live URL such as `https://responsive-portfolio-layout.vercel.app`.

**Option B — Vercel CLI**
```
npm install -g vercel
vercel
```
Follow the CLI prompts; it deploys the current folder directly and prints a live URL.

Once connected to GitHub, every future `git push` to `main` automatically redeploys the live site.
