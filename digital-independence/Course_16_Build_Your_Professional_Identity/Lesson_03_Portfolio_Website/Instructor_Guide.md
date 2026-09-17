# Instructor Guide — Course 16, Lesson 3: Build Your Portfolio Website

## Lesson Metadata
| Field | Value |
|---|---|
| Course | 16 — Build Your Professional Identity |
| Lesson | 3 of 8 — Build Your Portfolio Website |
| Age | 15–18 |
| Duration | 75–90 min |
| Difficulty | Beginner–Intermediate (basic HTML/CSS assumed from prior Lumexa courses) |
| Prerequisites | Lesson 2 (Strengths & Direction worksheet completed) |
| Tools | HTML, CSS, a code editor (VS Code recommended), the `Portfolio_Website` starter project |
| Objectives | Build a working, responsive multi-section portfolio site locally |
| Deliverables | A local, running portfolio site (not yet deployed — deployment is Lesson 7) |
| Skills developed | Semantic HTML structure, basic responsive CSS, information architecture for a personal site |
| Portfolio connection | This IS the portfolio website deliverable's skeleton — bio, brand, and case studies (L4–L6) get dropped into it |

## Lesson Overview
Students go from "I have a direction" to "I have a real, running website with my name on it."
This lesson uses the provided `Portfolio_Website` starter project (in `Projects/Portfolio_Website/starter/`)
so no student starts from a blank file — they customize a working structure rather than fighting boilerplate.

## Instructor Prep
- Open `Projects/Portfolio_Website/completed/index.html` in a browser beforehand as the reference example to show.
- Have the `starter/` folder ready to distribute (zip, shared drive, or GitHub Classroom — instructor's choice).
- Confirm VS Code (or comparable editor) + Live Server extension (or `python3 -m http.server`) works on your teaching machine for a live-reload demo.

## Required Files
- `Projects/Portfolio_Website/starter/` (given to students)
- `Projects/Portfolio_Website/completed/` (instructor reference only — do not distribute, since it spoils the exercise)

## Teaching Sequence
| Time | Activity |
|---|---|
| 0–10 min | Show the completed reference site; walk through its 5 sections (Intro, About, Skills, Projects, Contact) |
| 10–20 min | Distribute starter project; tour the file structure (`index.html`, `style.css`, `assets/`) |
| 20–45 min | Guided coding: edit the Intro/Hero section together — name, tagline, direction from Lesson 2 |
| 45–65 min | Guided coding: About + Skills sections; introduce CSS Grid/Flexbox basics used in the starter |
| 65–80 min | Independent work: students personalize colors/spacing (full branding comes in L5) and add placeholder project cards |
| 80–90 min | Live-reload check on each student's site; wrap-up |

## Instructor Talking Points
- "A portfolio site is not a resume — it's a workspace where people can see and click through real things you built."
- "Five sections is enough: Intro, About, Skills, Projects, Contact. Don't over-build before you have content — content comes in Lessons 4–6."
- Explain semantic HTML briefly: `<header>`, `<main>`, `<section>`, `<footer>` vs. a page made entirely of `<div>`s, and why it matters (accessibility, SEO, maintainability).

## Common Misconceptions
- "I need to build this from scratch to make it mine." → Customizing a solid structure is what real developers do; originality comes from content and design choices, not from avoiding starter code.
- "It has to look perfect today." → This is a working skeleton; brand polish happens in Lesson 5, real case studies in Lesson 4/6, and deployment in Lesson 7.

## Likely Student Difficulties & Troubleshooting
| Issue | Fix |
|---|---|
| CSS changes not showing | Hard-refresh (Ctrl/Cmd+Shift+R); confirm the `<link>` tag path to `style.css` is correct |
| Layout breaks on resize | Check for a missing `<meta name="viewport">` tag (already in starter — verify it wasn't deleted) |
| Local server won't start | Use VS Code Live Server extension as the simplest fallback; `python3 -m http.server 8000` as a backup |
| Nothing shows at all | Check the browser console (F12) for a typo'd tag or unclosed bracket |

## How to Review Student Work
Check: all 5 sections present, page doesn't visually break at 375px width (phone) and 1440px (laptop), no console errors, student's real name/direction (not the starter's placeholder text) is in place.

## Lesson Close
Preview Lesson 4: "Next class we write your real bio and your first project case study — the words that go inside the structure you just built."
