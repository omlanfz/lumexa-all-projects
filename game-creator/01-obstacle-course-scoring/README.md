# Obstacle Course & Scoring

A timed obstacle-course race: players sprint through moving hazards, touch five checkpoints in order, and cross a finish line — with a live scoreboard, race timer, finish bonus, and one-click restart.

## Game Overview

- **Name:** Obstacle Course & Scoring
- **Objective:** Touch all five checkpoints in ascending order while dodging two moving obstacles, then cross the finish line as fast as possible for bonus points.
- **Target experience:** A short, replayable single- or multi-player skill/speed challenge (2–5 minutes per run).

## Learning Objectives

- Server-authoritative checkpoint ordering and scoring
- ModuleScript architecture (`ScoreManager`, `CheckpointManager`, `SafeCall`)
- RemoteEvents for score/timer sync and restart requests
- `TweenService`-driven obstacles and reward feedback
- Defensive coding with `pcall`/`SafeCall`

## Requirements

- Roblox Studio (any current version)
- A Roblox account

## How to Open / Run

1. Open Roblox Studio.
2. **File → Open from File...** and select `obstacle-course-scoring.rbxl`.
3. Click **Play** (or **Play Here**) in the Home ribbon to test solo, or use the **Test** tab → set **Clients** to `2` → **Start** to test multiplayer.
4. The place opens fully built — course, obstacles, UI, and all scripts are already in place. No extra setup is required.

## Game Controls

| Input | Action |
|---|---|
| `W A S D` | Move |
| `Space` | Jump |
| Click **Restart Race** | Requests a fresh run (server enforces a 5s per-player cooldown) |

## Gameplay / Core Mechanics

1. Player spawns near `SpawnLocation`; the server starts their personal race timer.
2. Player must touch `Checkpoint1` → `Checkpoint2` → `Checkpoint3` → `Checkpoint4` → `Checkpoint5` **in order** — touching one out of order (or twice) awards nothing.
3. Each checkpoint awards points (10/15/20/25/30) and triggers a particle burst, ding sound, and color-flash tween.
4. Two `MovingPlatform` obstacles slide back and forth via `TweenService`, forcing timing/jumping skill.
5. Touching `FinishLine` (only allowed after Checkpoint5) records the elapsed time, awards a 50-point finish bonus, and broadcasts a finish banner to all players.
6. `leaderstats` (`Score`, `BestTime`) show live in Roblox's built-in Tab leaderboard for every player.

## Game Structure

```
Workspace
├── Baseplate, SpawnLocation, StartPad
├── Course
│   ├── Checkpoints/Checkpoint1..5   (Part, CheckpointOrder + PointValue IntValues,
│   │                                 ParticleEmitter, CheckpointDing Sound, CheckpointTouch Script)
│   └── Obstacles/MovingPlatform1..2 (Part, ObstacleMover Script)
└── FinishLine                        (Part, ParticleEmitter, FinishFanfare Sound, FinishLineTouch Script)

ReplicatedStorage
└── Remotes (Folder)
    ├── CheckpointReached, UpdateScore, RaceFinished, RestartRace (RemoteEvents)

ServerScriptService
├── GameManager (Script)               -- leaderstats setup, restart handling, per-second timer sync
└── Modules (Folder)
    ├── ScoreManager (ModuleScript)     -- owns Score/BestTime
    ├── CheckpointManager (ModuleScript)-- owns checkpoint order + race timer
    └── SafeCall (ModuleScript)         -- pcall wrapper for cosmetic effects

StarterPlayer/StarterPlayerScripts
└── CameraController (LocalScript)     -- cosmetic FOV pulse on scoring

StarterGui
└── GameUI (ScreenGui)
    ├── ScoreLabel, TimerLabel (TextLabel)
    ├── RestartButton (TextButton)
    └── FinishBanner (Frame) → FinishBannerLabel (TextLabel)
```

All scoring, checkpoint validation, and timer state are computed and owned entirely by the server. RemoteEvents only ever carry **display information** to clients or **requests** from clients — the server independently validates every request before acting on it.

## Build / Setup Guide (recreating from a blank Baseplate)

1. **Course:** Insert `StartPad` (Part, 12×1×12, green) near spawn. Add folders `Course/Checkpoints` and `Course/Obstacles`.
2. **Checkpoints:** Add `Checkpoint1..5` (Part, 8×6×2, `CanCollide=false`) at increasing Z positions. Each needs two `IntValue` children — `CheckpointOrder` (1–5) and `PointValue` (10/15/20/25/30) — plus a `ParticleEmitter` (`Enabled=false`) and a `Sound` named `CheckpointDing`.
3. **Obstacles:** Add `MovingPlatform1..2` (Part, 10×1×10) between checkpoints.
4. **Finish line:** Add `FinishLine` (Part, 12×1×12, gold, `CanCollide=true`) with a `ParticleEmitter` and a `Sound` named `FinishFanfare`.
5. **Remotes:** In `ReplicatedStorage`, add a `Folder` named `Remotes` containing 4 `RemoteEvent`s: `CheckpointReached`, `UpdateScore`, `RaceFinished`, `RestartRace`.
6. **Server logic:** In `ServerScriptService`, add `Modules` (Folder) with `ModuleScript`s `ScoreManager`, `CheckpointManager`, `SafeCall`, then add the `GameManager` `Script`.
7. **Per-instance scripts:** Paste the identical `CheckpointTouch` `Script` into every `Checkpoint1..5` (behavior differs only via each checkpoint's own `CheckpointOrder`/`PointValue`), and the identical `ObstacleMover` `Script` into every `MovingPlatform`. Paste `FinishLineTouch` into `FinishLine`.
8. **UI:** In `StarterGui`, add a `ScreenGui` named `GameUI` with `ScoreLabel`, `TimerLabel`, `RestartButton`, and a `FinishBanner` `Frame` containing `FinishBannerLabel`. Paste the `UIController` `LocalScript` into `GameUI`.
9. **Client polish:** Paste `CameraController` `LocalScript` into `StarterPlayer/StarterPlayerScripts`.
10. **Lighting (optional):** Set `Lighting.ClockTime = 17`, a soft purple `Ambient`, `Brightness = 2`, `FogEnd = 900`.

## Testing

- **Play Here**: quick solo test of movement, checkpoints in order, obstacles, finish line, restart.
- **Test tab → 2 Players**: confirm each player's Score/Time is independent, both see feedback and the shared finish banner, and restart cooldown is per-player.
- Confirm touching checkpoints out of order awards nothing (e.g. walk straight to Checkpoint3 first).
- Confirm touching `FinishLine` before Checkpoint5 does nothing.
- Confirm spamming `RestartButton` only restarts once per 5 seconds per player.
- Expected full run score if nothing is missed: 10+15+20+25+30+50 = **150 points**.

## Troubleshooting

- **Score doesn't update:** confirm the `Remotes` folder and its 4 `RemoteEvent`s exist in `ReplicatedStorage` with exact names.
- **Checkpoint scripts error on `require`:** confirm `ServerScriptService/Modules/ScoreManager` (etc.) exists with the exact name (case-sensitive).
- **Obstacle doesn't move:** confirm `ObstacleMover` is a `Script` (not `LocalScript`) parented directly under the moving Part.
- **Finish line does nothing:** confirm all 5 checkpoints were touched in order first; check Output for warnings.

## Customization / Extension Ideas

- Add a global leaderboard of best times using `DataStoreService`.
- Add more obstacle types (rotating parts, disappearing platforms).
- Add a ghost/replay of your best run.
