# Instructor Guide — Lesson 8: Build Social Proof

## Metadata

| Field | Value |
|---|---|
| Path | Digital Independence Path → Course 16: Build Your Professional Identity → Lesson 8 (Final Lesson) |
| Title | Build Social Proof |
| Format | Live, instructor-led, virtual classroom |
| Audience | Ages 15–18 |
| Duration | 60 minutes |
| Tools | HTML, CSS, Vercel, Canva, GitHub, Google Docs |
| Prerequisite | Lesson 7 — live deployed portfolio with bio, brand kit, and 2–3 case studies |
| Course position | Final lesson of Course 16; leads into Course 17: Skills That Pay |

## Overview

Students already have a live portfolio. This lesson closes Course 16 by teaching them how to earn and request *honest* social proof — real endorsements from people who actually know their work (teachers, mentors, parents, peers) — and by running a final quality pass on the portfolio itself before it becomes their calling card. The lesson draws a hard, explicit line between ethical social proof and fake or manufactured proof (fabricated testimonials, reviews from strangers, bought reviews, screenshots of fake client praise). Students leave with a polished, verified, live portfolio and a real endorsement-request message ready to send.

### Learning objectives

By the end of this lesson, students will be able to:

1. Explain what social proof is and why *credible* proof matters more than *quantity* of proof.
2. Distinguish real, ethical social proof (genuine written endorsements, documented outcomes) from fake or manufactured proof.
3. Write a polite, specific endorsement-request message to a teacher, mentor, or parent.
4. Run a full QA/polish pass on their live portfolio (broken links, typos, mobile view, load speed).
5. Complete a final portfolio review using a rubric, and articulate what's next in Course 17.

## Prep (before class)

- Confirm every student's Lesson 7 portfolio is still live on Vercel. Open each URL once before class — flag any that 404 or fail to load, and message those students to bring a laptop with their GitHub/Vercel login ready.
- Have your own "instructor demo" portfolio ready with 2–3 *intentionally seeded* problems: one broken link, one typo, one Canva image that overflows on mobile, and one paragraph of text that's too dense. You'll fix these live.
- Prepare a blank endorsement-request email template in Google Docs to co-write with the class.
- Draft one fictional "received endorsement" example (see Talking Points) to project.
- Have the Final Portfolio Review Rubric (below) ready to share as a doc link or screen share.
- Test your screen share of Chrome DevTools mobile view and a network throttle (or PageSpeed Insights / Lighthouse) in advance so the speed demo doesn't eat class time.

## Teaching Sequence

### 1. Hook and framing (5 min)
Ask: "If you were hiring a 16-year-old to build a website, and one portfolio said 'trusted by 50 happy clients!!' with no names, and another said 'My robotics teacher, Ms. Alvarez, wrote: *"He rebuilt our club's sign-up site and it's still running two years later"* — with a link to that site — which one do you believe?" Let students answer. Land the point: **specific, verifiable, real proof beats vague, unverifiable claims every time** — and at your age, having *zero* testimonials is completely normal and not a weakness.

### 2. Real vs. fake social proof — talking points (10 min)

Present this contrast directly. Do not soften it — this is the ethical core of the lesson.

**Real, ethical social proof looks like:**
- A short, specific written note from a teacher, coach, mentor, or club advisor who actually saw the work — e.g., "Jordan built our class's study-tracker app for our final project; it's still the best one I've seen from a student."
- A parent or family friend's honest note about a real project they watched happen (a small business site, a family tool).
- A documented outcome: "This site has been live for 6 months and the robotics club still uses it to publish meeting notes" — verifiable, not vague.
- A peer's genuine feedback from a code review or group project.
- A link to a real GitHub repo, a real deployed site, a real commit history — proof that *is itself* the evidence, no claim needed.

**Fake or manufactured social proof looks like — and is never acceptable:**
- Writing your own "testimonial" and attributing it to a made-up client or a real person who never said it.
- Asking strangers online (forums, social media, review sites) to leave praise for work they never saw.
- Testimonial carousels with stock photos and invented names ("Sarah M., CEO").
- Vague inflated claims with no attributable source: "Loved by hundreds!" "5-star rated!" with nothing behind it.
- Pressuring or paying someone for a positive quote, or editing a real quote to say more than the person meant.

Say explicitly: **"If you would be embarrassed to have the person you named see what you wrote and attributed to them, don't post it. If a quote didn't happen, in those words, from that real person, it doesn't go on your site — ever."** This applies for their whole career, not just this class.

### 3. Live demo — endorsement-request message (15 min)

Screen-share Google Docs. Co-write a message live with student input, thinking aloud:

> Subject: Quick favor — would you write a short line about my [project name]?
>
> Hi [Name],
>
> I'm finishing up my coding portfolio for a class, and I wanted to ask if you'd be willing to write a short, honest sentence or two about the [project/robot/site/app] I built [for your class / for the club / with your help]. It doesn't need to be long — just your real impression, good or constructive. I'll only use it if you're comfortable, and I'll show you exactly how it'll appear before I post anything.
>
> No worries at all if you'd rather not — totally understand.
>
> Thanks either way,
> [Student name]

Call out the components explicitly: it's short, specific (names the actual project), gives an easy out, and promises the person a preview/approval step before anything goes live. Emphasize: **always show the person the final wording before publishing it, and get their okay** — even a real quote can be shortened or reworded in a way the person didn't intend.

Have students open a Google Doc and draft their own version for one real person (teacher, mentor, coach, parent) right now, naming a real project from their portfolio.

### 4. Live demo — full portfolio polish/QA pass (15 min)

On your seeded demo portfolio, walk through each check live, fixing issues as you go:

- **Broken links**: click every nav link, every case study link, every external link (GitHub, Canva, social). Show the broken one 404-ing, then fix the `href`.
- **Typos**: read the bio and each case study aloud slowly — typos hide in text you've read before. Fix the seeded typo.
- **Mobile view**: open Chrome DevTools → Toggle device toolbar → pick an iPhone/Android preset. Show the image overflowing its container; fix with `max-width: 100%` on the image or container.
- **Load speed basics**: mention image file size as the #1 culprit for slow student portfolios. Show a quick check (browser Network tab load time, or a PageSpeed Insights score) and demonstrate compressing/resizing an oversized Canva export before re-uploading.
- **Contact safety check**: confirm the visible contact method is a school email or a contact form — never a home address or personal phone number.

Then release students to run this same pass on their *own* live site for the remaining time, using the Worksheet checklist.

### 5. Discussion questions (5 min, can run concurrently with QA work)

- "Why might having zero testimonials right now actually be more trustworthy than having ten generic ones?"
- "If a teacher says yes but asks you to soften a sentence before you post it, what do you do?"
- "What's the difference between a review from a stranger on the internet and an endorsement from your robotics coach?"
- "Your friend says 'just write it yourself and say your mom said it, she won't mind.' What do you say?"

### 6. Wrap-up and course close (10 min)

Recap Course 16 in one sentence per lesson if time allows, then close with:

> "You now have a live, working, honest professional portfolio — built by you, hosted by you, and backed only by things that are actually true. That's rare, and it's worth more than a flashy site full of fake praise. Course 17, Skills That Pay, is where we turn this portfolio into real opportunities — freelancing basics, pricing your work, and finding your first paid or resume-worthy project."

## Common Misconceptions

- **"I need lots of testimonials right away."** Correction: one real, specific endorsement beats ten vague ones, and zero is fine at this stage — a strong live portfolio with real projects speaks for itself.
- **"No one will vouch for me, I'm just a student."** Correction: teachers, coaches, and mentors are asked for exactly this kind of note constantly and are almost always willing — the ask in the demo template makes it low-pressure and easy to decline.
- **"It's fine to write it myself if it's basically true."** Correction: if the words weren't the person's own and approved by them, it's fabricated — full stop, regardless of how true the sentiment feels.
- **"More reviews = more credible."** Correction: unverifiable quantity reads as suspicious to anyone experienced; a named, specific, real source is what builds trust.

## Student Difficulties & Troubleshooting

| Difficulty | What you'll see | Fix |
|---|---|---|
| Freezes on who to ask | Blank draft, "I don't know who" | Prompt with a specific list: current teacher, past teacher, coding club advisor, coach, parent, family friend who saw the project |
| Message reads as demanding | "Write me a testimonial saying my site is amazing" | Model the soft, optional-feeling phrasing again; have them add "no worries if not" |
| Can't find their own broken links | Skims instead of clicking each one | Require them to literally click every link on the page, one at a time, checked off on the worksheet |
| Mobile view looks fine to them (desktop-only testing) | Never opened DevTools device toolbar | Pair them with a neighbor's phone or your live demo screen share to check firsthand |
| Personal contact info exposed (home address, cell number) | Bio or contact section lists it | Immediately have them replace with school email or a contact form; treat as a required fix, not optional |
| Wants to invent a testimonial "just as a placeholder" | Suggests using a fake quote "for now" | Reinforce zero-tolerance rule: leave the endorsement section empty or labeled "coming soon" rather than fake |

## How to Review — Final Portfolio Review Rubric

| Criterion | Meets expectations |
|---|---|
| Live and accessible | Portfolio loads at its Vercel URL with no errors |
| No broken links | Every internal and external link works |
| No typos | Bio and case study text is proofread and clean |
| Mobile-friendly | No overflow, unreadable text, or broken layout on a phone-size screen |
| Brand consistent | Colors, fonts, and tone match the Lesson 6/7 brand kit throughout |
| Case studies present | 2–3 real case studies are visible and complete |
| Bio present | A short, current bio is visible and accurate |
| Contact method present and safe | A school email or contact form is listed — no home address or personal phone number |
| Social proof (if included) is real | Any endorsement is a genuine, attributed, approved quote — never fabricated |

## Lesson Close

Confirm every student has: a fixed, live portfolio; a drafted (not necessarily sent) endorsement-request message; and a completed final review checklist. Tell students sending the message is optional homework, not a grade requirement, since it depends on a real person's availability — but encourage them to send it this week while the project is fresh. Preview Course 17: Skills That Pay, starting with turning this exact portfolio into paid or resume-ready opportunities.
