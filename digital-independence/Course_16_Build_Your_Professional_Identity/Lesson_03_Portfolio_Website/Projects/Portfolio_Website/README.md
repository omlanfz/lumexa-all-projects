# Portfolio Website — Coding Project (Course 16)

## Purpose
This is the coding project behind Course 16, Lesson 3 ("Build Your Portfolio Website"), and
the deployment target for Lesson 7 ("Launch Your Professional Website"). It's the skeleton
every student's bio (Lesson 4), brand kit (Lesson 5), and case studies (Lessons 4 & 6) get
dropped into.

## Learning Objectives
- Structure a personal site with 5 clear, semantic sections.
- Write basic responsive CSS (flex/grid, a mobile breakpoint).
- Practice safe, professional contact-info choices.

## Folder Structure
```
Portfolio_Website/
├── README.md              (this file)
├── starter/                (given to students — blank/placeholder content)
│   ├── index.html
│   ├── style.css
│   └── script.js
└── completed/               (instructor reference only — fictional "Jordan R." example)
    ├── index.html
    ├── style.css
    └── script.js
```

## Functional Requirements
- 5 sections: Hero/Intro, About, Skills, Projects, Contact.
- Responsive at 375px (phone) and 1440px (laptop) widths.
- No console errors; footer year auto-updates via `script.js`.

## Optional Enhancement Requirements
- Add a dark-mode toggle.
- Add smooth-scroll behavior for the nav links.
- Add subtle scroll-triggered fade-in animation on each section.

## Local Testing Instructions
1. Open the `starter/` folder in VS Code (or any editor).
2. Easiest: install the "Live Server" VS Code extension → right-click `index.html` → "Open with Live Server".
3. No Live Server? Run `python3 -m http.server 8000` from inside the folder, then visit `http://localhost:8000` in a browser.
4. Edit `index.html`/`style.css`/`script.js` and refresh the browser to see changes.

## Deployment Instructions (used in Lesson 7 — not required for Lesson 3)
1. Create a free [GitHub](https://github.com) account (verify current sign-up requirements/age policy before class, as platform terms can change).
2. Create a new public repository and push this folder's contents to it (via `git` command line, or GitHub's web "Upload files" flow as a no-terminal fallback).
3. Create a free [Vercel](https://vercel.com) account and connect it to your GitHub account.
4. Import the repository in Vercel and deploy — no build command is needed for this static HTML/CSS/JS project.
5. Vercel will provide a live `.vercel.app` URL. A custom domain is optional and out of scope for this lesson.

## Teacher Demonstration Instructions
Show the `completed/` version first (fictional "Jordan R." example) as the target, then reset
to `starter/` on screen and build it live, section by section, matching the Lesson 3 Instructor Guide's timing table.

## Student Task Checklist
- [ ] All 5 sections present with my real name/direction
- [ ] Skills list reflects my Lesson 2 worksheet
- [ ] Page doesn't break at phone or laptop width
- [ ] Contact section uses a safe method only (school email, not home address/personal phone)

## Expected Final Result
A single-page, responsive, 5-section personal site running locally, ready to receive real
bio/brand/case-study content in Lessons 4–6 and go live in Lesson 7.

## Troubleshooting Guide
| Issue | Fix |
|---|---|
| Styles not applying | Confirm `<link rel="stylesheet" href="style.css">` path matches the file location |
| Layout breaks on mobile | Confirm the viewport `<meta>` tag wasn't removed; check `@media` query in `style.css` |
| Footer year missing | Confirm `script.js` is linked at the bottom of `<body>` and the `id="year"` span exists |
| Nothing loads locally | Use Live Server or `python3 -m http.server`; opening `index.html` directly by double-click can break relative asset paths in some browsers |

## Assessment Rubric
| Level | Criteria |
|---|---|
| Beginner | All 5 sections exist but layout breaks on mobile or has console errors |
| Developing | All 5 sections present and responsive, but content is still placeholder text |
| Proficient | All 5 sections present, responsive, no console errors, and populated with the student's real direction/skills |

## Reference Solution
See `completed/` — a fictional "Jordan R." example used only for instructor demonstration.
