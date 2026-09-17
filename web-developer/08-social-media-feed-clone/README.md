# Project 08 — Social Media Feed Clone (Lumexa Orbit)

A React + Vite scrollable social feed built for the Lumexa "React and
Full-Stack Web" course. It demonstrates list rendering with keys, lifting
state up, and controlled forms.

## What it is

- A feed seeded with real (fictional) posts, each with an author, avatar,
  timestamp, image, like count, and comments.
- Like/unlike toggle that updates the like count in real time.
- Expandable comments per post, with a form that adds a real comment to that
  post's comment list (state only, no backend, but it genuinely persists for
  the session).
- A "new post" composer at the top of the feed that adds your post to the
  top of the list immediately.

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
5. Click **Deploy**.
