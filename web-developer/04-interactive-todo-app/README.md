# Crew Task Tracker — Interactive To-Do App

A fully functional to-do list app built with plain HTML5, CSS3, and vanilla
JavaScript (ES6+). Add tasks with a priority level, mark them complete,
edit them in place, filter by all/active/completed, clear completed tasks
in bulk, and everything persists automatically in the browser's Local
Storage — reload the page or close the tab and every task is still there.

This project is the direct capstone of Course 08, Lessons 6 and 7
(Local Storage, and the "render from state" architecture).

## Features

- Add a task with a text label and a low/medium/high priority
- Mark a task complete/incomplete with a checkbox
- **Double-click** any task's text to edit it in place (Enter or clicking away saves it, Escape cancels)
- Delete any individual task
- Filter the list: All / Active / Completed
- "Clear Completed" removes every completed task at once
- Live counter: "N tasks left of M total"
- Everything is saved to Local Storage on every change and reloaded automatically on page load
- Fully responsive layout (phone width and up)

## How It Works

The whole app follows a **single source of truth + render()** architecture:
- `tasks` (an array of `{ id, text, completed, priority }` objects) and `currentFilter` are the only two variables that determine what's on screen.
- Every user action (add / toggle / delete / edit / filter / clear completed) updates that state, saves it to Local Storage, and then calls one shared `render()` function that rebuilds the entire task list from scratch.
- Click handling uses **event delegation** — one listener on the `<ul>` handles every task's checkbox and delete button, including tasks added long after the page first loaded.

## Folder Structure
```
04-interactive-todo-app/
├── index.html     # App structure and markup
├── styles.css     # All styling, layout, and responsive rules
├── script.js      # Application logic (state, storage, rendering, events)
└── README.md      # This file
```

## Run It Locally
No build tools or installation required.

- **Option A:** Double-click `index.html`, or drag it into any browser window.
- **Option B (recommended, avoids any local file quirks):**
  ```
  npx serve .
  ```
  then open the printed `http://localhost:...` address in your browser.

## Try It Yourself

1. Add a few tasks with different priorities.
2. Mark one complete, then click the "Completed" filter to confirm only it shows.
3. Double-click a task's text, change it, and press Enter — confirm the new text saved.
4. Reload the page (or close and reopen the tab) — confirm every task, its completed state, and its priority are still exactly as you left them.
5. Open DevTools → Application tab → Local Storage to see the raw JSON being stored under the key `lumexa-crew-tasks-v1`.

## Deploy to Vercel

**Option A — Import via the Vercel website**
1. Push this folder to a new GitHub repository:
   ```
   git init
   git add .
   git commit -m "Initial commit: interactive to-do app"
   git remote add origin https://github.com/<your-username>/interactive-todo-app.git
   git branch -M main
   git push -u origin main
   ```
2. Go to [vercel.com](https://vercel.com), sign in, click **Add New Project**, and select this repository.
3. No build command is needed for a static HTML/CSS/JS site — click **Deploy**.
4. Vercel gives you a live URL such as `https://interactive-todo-app.vercel.app`.

**Option B — Vercel CLI**
```
npm install -g vercel
vercel
```
Follow the CLI prompts; it deploys the current folder directly and prints a live URL.

Once connected to GitHub, every future `git push` to `main` automatically redeploys the live site.
