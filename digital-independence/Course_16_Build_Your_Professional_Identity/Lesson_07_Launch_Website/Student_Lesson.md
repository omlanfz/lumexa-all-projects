
# Lesson 7: Launch Your Professional Website

## Digital Independence Path — Course 16: Build Your Professional Identity

## Why This Lesson Matters

You've done the real work already. Your site has your bio, your case studies, and your brand kit's colors and fonts on it. Right now, though, all of that only exists as files on one computer.

Here's the problem: a folder of files, or a zipped file you email someone, is not the same as a website. If you sent a recruiter, a college admissions reader, or a potential client a zip file, most of them would never open it. But if you send them a link — a real, clickable web address — they'll click it in three seconds, on their phone, without thinking twice.

**A live link is proof your work exists in the world. A zip file is proof it exists on your laptop.**

Today you're going to take the site you already built and put it on the actual internet, with a real address, for free, in one class period.

## Plain-Language Explanation: Git, GitHub, and Vercel

Think of your website files like a set of moving boxes you've packed up.

- **Git** is like a labeling system for your boxes. Every time you finish packing a version of your stuff, Git lets you seal that box and write a label on it: "Version 3 — added case studies." If something goes wrong later, you can always go back and open an earlier labeled box. Nothing gets thrown away.

- **GitHub** is a warehouse where you store those labeled boxes online, instead of just in your garage (your own laptop). Once your boxes are in the warehouse, anyone with the address can look inside — and more importantly, other services can grab your boxes automatically.

- **Vercel** is a shop that takes the boxes sitting in your GitHub warehouse and puts them in a display window on the street — a real, public web address anyone can walk up to and see. Every time you update your boxes in the warehouse, the shop window updates too, automatically.

So the full journey today is: **your files → packed and labeled by Git → stored in your GitHub warehouse → displayed live by Vercel → a real URL you can share with anyone.**

## Step-by-Step Walkthrough

Follow along live with your instructor. Don't skip ahead — each step depends on the one before it.

### Step 1: Create a GitHub Account
1. Go to github.com and sign up with your email.
2. Choose a username you'd be comfortable with a future employer or teacher seeing — something like `alex-codes` rather than an old gaming handle. This account can follow you for years.
3. Verify your email when the confirmation arrives.

*A note on accounts and age: GitHub's own terms describe rules about account holders' age, and those terms can change over time — it's worth actually reading them once. This course is built for ages 15–18, so this isn't a barrier for anyone in this class, but it's still good practice to know what any platform's terms say about your account before you sign up for things in general.*

### Step 2: Create a Repository
1. Click **New repository**.
2. Name it something clear, like `my-portfolio`.
3. Set it to **Public** — this is what lets Vercel find and display it later.
4. If you already have your project files ready to upload from your computer, do **not** check "Add a README file" — that avoids a headache later. Your instructor will tell you if your class is doing this differently.

### Step 3: Upload Your Code
**If your class is using Git/terminal commands**, type these one at a time, following your instructor:
```
git init
git add .
git commit -m "Initial portfolio site"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
git push -u origin main
```
Each line does one job: `init` starts tracking your project, `add .` gathers all your files, `commit` saves a labeled snapshot, and `push` uploads it to GitHub.

**If your class is using the no-terminal method:** open your repository page on GitHub, click **Add file → Upload files**, and drag your whole project folder in, then click **Commit changes**.

### Step 4: Connect Vercel and Deploy
1. Go to vercel.com and sign up **using your GitHub account** — this is the fastest way and connects the two immediately.
2. Click **Add New Project**.
3. Select the repository you just created.
4. Click **Deploy**.
5. Wait about 30–60 seconds while Vercel builds your site.

Vercel's free plan (called "Hobby") does not require a credit card for a personal project like this — if you're ever asked for payment information at this step, stop and flag it for your instructor before continuing.

### Step 5: Verify Your Live URL
1. Click the link Vercel gives you — it will look something like `https://your-portfolio.vercel.app`.
2. Open it on a second device if you can (your phone, if you built on a laptop).
3. Send the link to a classmate and have them open it too. If someone who isn't you can open it and see your real site, it's genuinely live.

## Troubleshooting FAQ

**My `git push` is asking for a password and it's not working.**
GitHub usually doesn't accept a typed-out password directly anymore for this. Look for a browser sign-in popup, or ask your instructor about the current recommended way to authenticate — this changes over time.

**I got a "failed to push" or merge conflict message.**
This usually happens if your GitHub repo was started with a README file at the same time your local files already existed. Ask your instructor — the fix is usually quick.

**My site deployed but looks broken/unstyled.**
Double check your CSS file name and the path in your HTML `<link>` tag match exactly, including capital/lowercase letters.

**Vercel showed a build error.**
Make sure your main HTML file (usually `index.html`) is sitting at the top level of your project folder, not buried in a subfolder.

**Is this permanent? What if I mess something up?**
No — nothing about this is permanent or risky. Every time you push new files, Vercel creates a fresh deployment. You can always fix a mistake by pushing an update; your earlier saved versions in Git are never deleted.

**Do I need to buy a domain name (like alexsmith.com)?**
No. Your `.vercel.app` address is a completely real, working, professional URL. Buying a custom domain later is a nice optional upgrade, not something you need today.

## Key Terms

- **Repository (repo):** The online "folder" on GitHub that holds all the files for one project, plus their full history.
- **Commit:** A saved, labeled snapshot of your project at one point in time.
- **Push:** The act of uploading your local commits up to GitHub.
- **Deploy:** Taking your code and making it live and viewable as an actual website on the internet.
- **Hosting:** A service (like Vercel) that keeps your website running and accessible online, all the time, without your own computer needing to be on.

## Knowledge Checks

1. What's the difference between a zip file of your website and a live URL, in terms of who can actually access your work?
2. Put these in the correct order: deploy, push, commit, write code.
3. True or False: Once you deploy your site, you can never make changes to it again.
4. Why does a repository need to be set to "Public" for this lesson's Vercel setup to work?
5. If your site deploys but the styling looks wrong, what's the first thing you should check?

## Reflection Prompts

1. What did it feel like the moment your live link actually loaded for the first time? Why do you think that feeling matters for how you see your own work?
2. Now that your portfolio has a real, permanent-feeling address, is there anything about your bio or case studies you want to revisit or improve, knowing a stranger could click this link today?
3. Where do you imagine sharing this link in real life — a job application, a college application, a social media bio, something else? Be specific.

## Submission Instructions

Submit both of the following to your instructor:
1. Your **live Vercel URL** (e.g., `https://your-portfolio.vercel.app`)
2. Your **GitHub repository URL** (e.g., `https://github.com/your-username/my-portfolio`)

Your lesson isn't complete until both links have been clicked and confirmed working by your instructor or a classmate.
