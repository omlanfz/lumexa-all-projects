// Signal Match — Memory Card Game
// Core mechanics (Fisher-Yates shuffle, two-click match comparison, setTimeout
// flip-back delay) are the direct expansion of Course 08, Lesson 8.

const ALL_SYMBOLS = ["🛰️", "🪐", "🚀", "⭐", "🌙", "☄️", "🔭", "🌌"];
const BEST_SCORE_KEY_PREFIX = "lumexa-signal-match-best-";
const FLIP_BACK_DELAY_MS = 800;

// --- ELEMENTS ---
const boardEl = document.querySelector("#board");
const moveCountEl = document.querySelector("#move-count");
const timerEl = document.querySelector("#timer");
const bestScoreEl = document.querySelector("#best-score");
const statusEl = document.querySelector("#status");
const restartBtn = document.querySelector("#restart-btn");
const difficultyButtons = document.querySelectorAll(".difficulty-btn");

// --- STATE ---
let pairCount = 6; // default: Medium
let tiles = [];          // { id, symbol, isRevealed, isMatched }
let selectedIds = [];    // ids currently flipped, awaiting a match check
let isChecking = false;  // input lock while a mismatch is being shown
let moveCount = 0;
let secondsElapsed = 0;
let timerIntervalId = null;
let hasGameStarted = false;
let pendingFlipBackTimeoutId = null;

// --- FISHER-YATES SHUFFLE ---
function shuffle(array) {
  const result = [...array];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

// --- BEST SCORE (per difficulty, persisted in Local Storage) ---
function bestScoreKey() {
  return `${BEST_SCORE_KEY_PREFIX}${pairCount}`;
}

function loadBestScore() {
  const raw = localStorage.getItem(bestScoreKey());
  if (raw === null) return null;
  const parsed = Number(raw);
  return Number.isFinite(parsed) ? parsed : null;
}

function saveBestScoreIfBetter(finalMoveCount) {
  const currentBest = loadBestScore();
  if (currentBest === null || finalMoveCount < currentBest) {
    localStorage.setItem(bestScoreKey(), String(finalMoveCount));
  }
}

function renderBestScore() {
  const best = loadBestScore();
  bestScoreEl.textContent = best === null ? "--" : `${best} moves`;
}

// --- BUILD A FRESH SET OF TILES ---
function createTiles(numberOfPairs) {
  const chosenSymbols = ALL_SYMBOLS.slice(0, numberOfPairs);
  const doubled = shuffle([...chosenSymbols, ...chosenSymbols]);
  return doubled.map((symbol, index) => ({
    id: index,
    symbol,
    isRevealed: false,
    isMatched: false,
  }));
}

// --- TIMER ---
function startTimer() {
  stopTimer();
  timerIntervalId = setInterval(() => {
    secondsElapsed++;
    renderTimer();
  }, 1000);
}

function stopTimer() {
  if (timerIntervalId !== null) {
    clearInterval(timerIntervalId);
    timerIntervalId = null;
  }
}

function renderTimer() {
  const minutes = Math.floor(secondsElapsed / 60);
  const seconds = secondsElapsed % 60;
  timerEl.textContent = `${minutes}:${String(seconds).padStart(2, "0")}`;
}

// --- RENDER ---
function render() {
  boardEl.innerHTML = "";
  boardEl.style.gridTemplateColumns = `repeat(${columnsForPairCount(pairCount)}, 1fr)`;

  tiles.forEach((tile) => {
    const tileEl = document.createElement("div");
    tileEl.classList.add("tile");
    if (tile.isMatched) tileEl.classList.add("matched");
    else if (tile.isRevealed) tileEl.classList.add("revealed");
    tileEl.textContent = tile.isRevealed || tile.isMatched ? tile.symbol : "";
    tileEl.dataset.id = tile.id;
    tileEl.setAttribute("role", "button");
    tileEl.setAttribute(
      "aria-label",
      tile.isMatched || tile.isRevealed ? `Tile showing ${tile.symbol}` : "Hidden tile"
    );
    boardEl.appendChild(tileEl);
  });

  moveCountEl.textContent = moveCount;
}

function columnsForPairCount(numberOfPairs) {
  // Keeps the grid roughly square-ish for each difficulty level.
  if (numberOfPairs <= 4) return 4; // 8 tiles -> 4x2
  if (numberOfPairs <= 6) return 4; // 12 tiles -> 4x3
  return 4; // 16 tiles -> 4x4
}

// --- CLICK HANDLING (event delegation) ---
boardEl.addEventListener("click", (event) => {
  const tileEl = event.target.closest(".tile");
  if (!tileEl || isChecking) return; // guard clause: ignore clicks while locked or off-board

  const id = Number(tileEl.dataset.id);
  const tile = tiles.find((t) => t.id === id);

  if (!tile || tile.isMatched || tile.isRevealed || selectedIds.includes(id)) return;

  if (!hasGameStarted) {
    hasGameStarted = true;
    startTimer();
  }

  tile.isRevealed = true;
  selectedIds.push(id);
  render();

  if (selectedIds.length === 2) {
    moveCount++;
    checkForMatch();
  }
});

function checkForMatch() {
  const [firstId, secondId] = selectedIds;
  const firstTile = tiles.find((t) => t.id === firstId);
  const secondTile = tiles.find((t) => t.id === secondId);

  if (firstTile.symbol === secondTile.symbol) {
    firstTile.isMatched = true;
    secondTile.isMatched = true;
    selectedIds = [];
    render();
    checkForWin();
  } else {
    isChecking = true; // lock input so a third click can't corrupt the comparison
    pendingFlipBackTimeoutId = setTimeout(() => {
      firstTile.isRevealed = false;
      secondTile.isRevealed = false;
      selectedIds = [];
      isChecking = false;
      pendingFlipBackTimeoutId = null;
      render();
    }, FLIP_BACK_DELAY_MS);
  }
}

function checkForWin() {
  const allMatched = tiles.every((tile) => tile.isMatched);
  if (!allMatched) return;

  stopTimer();
  saveBestScoreIfBetter(moveCount);
  renderBestScore();
  statusEl.textContent = `You matched every signal in ${moveCount} moves and ${timerEl.textContent}!`;
}

// --- GAME LIFECYCLE ---
function startNewGame() {
  // Cancel any in-flight flip-back timer from the previous game so it can't
  // fire late and mutate a board that no longer exists.
  if (pendingFlipBackTimeoutId !== null) {
    clearTimeout(pendingFlipBackTimeoutId);
    pendingFlipBackTimeoutId = null;
  }
  stopTimer();

  tiles = createTiles(pairCount);
  selectedIds = [];
  isChecking = false;
  moveCount = 0;
  secondsElapsed = 0;
  hasGameStarted = false;
  statusEl.textContent = "";

  render();
  renderTimer();
  renderBestScore();
}

// --- EVENTS ---
restartBtn.addEventListener("click", startNewGame);

difficultyButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    pairCount = Number(btn.dataset.pairs);
    difficultyButtons.forEach((b) => b.classList.toggle("active", b === btn));
    startNewGame();
  });
});

// --- START ---
startNewGame();
