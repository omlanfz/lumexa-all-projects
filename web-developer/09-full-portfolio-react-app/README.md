# Project 09 — Full Portfolio React App (Capstone)

A real personal portfolio site built with **Next.js (App Router)** and
**Tailwind CSS** — the capstone project for the Lumexa "React and Full-Stack
Web" course.

## What it is

- **Home (`/`)** — intro and two featured projects.
- **Projects (`/projects`)** — a listing of all projects pulled from
  `src/data/projects.js`.
- **Project detail (`/projects/[slug]`)** — a dynamic route that renders a
  detail page per project using `generateStaticParams`, so every project gets
  its own statically generated page and its own shareable URL.
- **About (`/about`)** — bio and skills list.
- **Contact (`/contact`)** — a real controlled form (client component) with
  validation and a success/error message, ready to be wired to a real API
  route or form service later.
- Shared `NavBar` and `Footer` components used across every page via the root
  layout.

## Run locally

```bash
npm install
npm run dev
```

Then open `http://localhost:3000`.

## Build for production

```bash
npm run build
```

This was verified to complete cleanly, statically generating `/`, `/about`,
`/contact`, `/projects`, and one page per project under `/projects/[slug]`.

To preview the production build locally:

```bash
npm start
```

## Deploy to Vercel

1. Push this project to a GitHub repository.
2. Go to [vercel.com/new](https://vercel.com/new) and import the repository.
3. Vercel **auto-detects Next.js** — no build settings need to be changed
   (build command `next build`, output handled automatically).
4. This project doesn't require any environment variables. If you later add
   an API key (e.g. for a real contact-form email service), add it under
   **Project Settings → Environment Variables** in the Vercel dashboard
   before redeploying.
5. Click **Deploy**.
