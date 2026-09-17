# Personal Landing Page — Mira Vasquez

A one-page personal site for a fictional junior front-end developer, built with
plain HTML5 and CSS3. It includes a hero, about section, skills, a projects
gallery, and a contact section, and is fully responsive from small phones to
wide desktop screens.

## Folder Structure
```
01-personal-landing-page/
├── index.html     # All page content and structure
├── styles.css      # All styling, layout, and responsive rules
└── README.md       # This file
```

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
   git commit -m "Initial commit: personal landing page"
   git remote add origin https://github.com/<your-username>/personal-landing-page.git
   git branch -M main
   git push -u origin main
   ```
2. Go to [vercel.com](https://vercel.com), sign in, click **Add New Project**, and select this repository.
3. No build command is needed for a static HTML/CSS site — click **Deploy**.
4. Vercel gives you a live URL such as `https://personal-landing-page.vercel.app`.

**Option B — Vercel CLI**
```
npm install -g vercel
vercel
```
Follow the CLI prompts; it deploys the current folder directly and prints a live URL.

Once connected to GitHub, every future `git push` to `main` automatically redeploys the live site.
