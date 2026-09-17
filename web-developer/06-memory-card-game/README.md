# Signal Match — Memory Card Game

A fully functional memory-matching game built with plain HTML5, CSS3, and
vanilla JavaScript (ES6+). Flip tiles to find every matching pair, with
three difficulty levels, a live move counter, a live timer, and a
per-difficulty best score saved permanently in Local Storage.

This project is the direct capstone of Course 08, Lesson 8 (game logic,
`setTimeout` timing, and multi-step state comparison).

## Features

- Fisher-Yates shuffle for genuinely fair, unbiased random tile placement every game
- Three difficulty levels: Easy (4 pairs), Medium (6 pairs), Hard (8 pairs)
- Click two tiles to reveal them; a real match stays face-up, a mismatch flips back automatically after a short delay
- Input is locked during the flip-back delay so a fast click can't corrupt the comparison
- Live move counter and a live running timer (started on your first click)
- Win detection with a summary message showing your final moves and time
- Best score (fewest moves) tracked separately per difficulty level and saved in Local Storage — it survives page reloads
- Restart button to reshuffle and start over at any time

## How It Works

- **State**: a `tiles` array (`{ id, symbol, isRevealed, isMatched }`) is the single source of truth for the whole board; `render()` rebuilds every tile's appearance from that array on every change.
- **Matching logic**: `selectedIds` remembers the tile(s) picked since the last successful match check. On the second click of a pair, `checkForMatch()` compares the two tiles' symbols directly.
- **Timing**: a real match updates state and re-renders immediately. A mismatch sets an `isChecking` lock flag, waits `800ms` with `setTimeout()` so the player can actually see both wrong tiles, then flips them back and clears the lock.
- **Safety**: starting a new game (via Restart or switching difficulty) explicitly cancels any still-pending flip-back `setTimeout` with `clearTimeout()`, so a delayed callback from the *previous* game can never fire late and corrupt the *new* board.
- **Persistence**: the best (lowest) move count for each difficulty is stored under its own Local Storage key, so Easy/Medium/Hard each keep their own separate best score.

## Folder Structure
```
06-memory-card-game/
├── index.html     # App structure and markup
├── styles.css     # All styling, layout, and responsive rules
├── script.js      # Game logic (shuffle, state, timer, matching, storage)
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

1. Play a full game on Medium and confirm the win message shows correct final moves and time.
2. Deliberately click two mismatched tiles and confirm you cannot click a third tile until they flip back.
3. Win a game, note your move count, then play again and try to beat it — confirm "Best" updates only when you actually improve.
4. Switch difficulty mid-game and confirm the board fully resets with the new tile count and no leftover state from the previous game.
5. Reload the page after setting a best score and confirm it's still shown.

## Deploy to Vercel

**Option A — Import via the Vercel website**
1. Push this folder to a new GitHub repository:
   ```
   git init
   git add .
   git commit -m "Initial commit: memory card game"
   git remote add origin https://github.com/<your-username>/memory-card-game.git
   git branch -M main
   git push -u origin main
   ```
2. Go to [vercel.com](https://vercel.com), sign in, click **Add New Project**, and select this repository.
3. No build command is needed for a static HTML/CSS/JS site — click **Deploy**.
4. Vercel gives you a live URL such as `https://memory-card-game.vercel.app`.

**Option B — Vercel CLI**
```
npm install -g vercel
vercel
```
Follow the CLI prompts; it deploys the current folder directly and prints a live URL.

Once connected to GitHub, every future `git push` to `main` automatically redeploys the live site.
