# Multiplayer Arena & Teams

A two-team tag arena: players are auto-balanced onto RedTeam/BlueTeam, tag enemies within range for team points during a timed round, and see a win/lose banner with a restart flow.

## Game Overview

- **Name:** Multiplayer Arena & Teams
- **Objective:** Tag opposing-team players within range to score points for your team before the round timer runs out.
- **Target experience:** A fast, replayable multiplayer PvP mini-game (2 minutes per round).

## Learning Objectives

- Team assignment and balancing using the `Teams` service
- Server-authoritative combat validation: range, team, and cooldown all re-checked server-side, never trusting the client's claimed hit
- A round state machine (`Countdown → InProgress → Ended → repeat`) broadcast to all clients
- Multi-client testing of genuinely multiplayer mechanics

## Requirements

- Roblox Studio
- A Roblox account
- **A second Studio "client" (Test tab → 2 Players) is required to test tagging** — with only one player there is never an opposing-team target.

## How to Open / Run

1. Open Roblox Studio.
2. **File → Open from File...** and select `multiplayer-arena-teams.rbxl`.
3. Use the **Test** tab → set **Players** to `2` → **Start** to properly test team assignment and tagging.
4. The place opens fully built — arena, teams, spawns, UI, and all scripts are already in place.

## Game Controls

| Input | Action |
|---|---|
| `W A S D` | Move |
| `Space` | Jump |
| `F` | Attempt to tag the nearest enemy within ~10 studs |
| Click **Restart Round** | Requests a new round once the current one has ended |

## Gameplay / Core Mechanics

1. Each joining player is auto-assigned to whichever team (`RedTeam`/`BlueTeam`) currently has fewer players.
2. A round begins with a 10-second Countdown, then 120 seconds InProgress, then a 10-second Ended phase showing the winner, then loops.
3. During InProgress, pressing `F` attempts to tag the nearest enemy; the server re-validates actual distance (≤8 studs), that attacker/target are on different teams, and a 1.5s per-attacker cooldown before awarding 1 point to the attacker's team and respawning the tagged player.
4. Team scores update live on all clients via `TeamScoreUpdate`.
5. When a round ends, the team with more points wins (or it's a tie); a `RestartButton` appears and any player can request a new round (server-validated, with its own cooldown).

## Game Structure

```
Workspace
├── Baseplate, ArenaFloor
├── RedSpawns  (Folder) → RedSpawn1, RedSpawn2   (Part, CanCollide=false, Transparency=1)
└── BlueSpawns (Folder) → BlueSpawn1, BlueSpawn2 (Part, CanCollide=false, Transparency=1)

Teams
├── RedTeam  (Team) → TeamScore (IntValue)
└── BlueTeam (Team) → TeamScore (IntValue)

ReplicatedStorage
└── Remotes (Folder) → TagPlayer, RoundStateChanged, TeamScoreUpdate, RestartRound (RemoteEvents)

ServerScriptService
├── GameManager (Script)                -- team color setup, round broadcast loop, tag/restart requests
└── Modules (Folder)
    ├── TeamManager (ModuleScript)      -- balanced assignment + team scores
    ├── RoundManager (ModuleScript)     -- Countdown/InProgress/Ended state machine
    ├── CombatManager (ModuleScript)    -- server-validated tag range/team/cooldown
    └── SafeCall (ModuleScript)         -- pcall wrapper for cosmetic effects

StarterPlayer/StarterPlayerScripts
└── TagController (LocalScript)         -- finds nearest enemy, fires TagPlayer on F

StarterGui
└── GameUI (ScreenGui)
    ├── RoundStateLabel, RedScoreLabel, BlueScoreLabel (TextLabel)
    ├── RestartButton (TextButton)
    └── ResultBanner (Frame) → ResultBannerLabel (TextLabel)
```

`RoundManager` owns the only real clock; `TeamManager` owns the only real scores; `CombatManager` independently re-validates every tag attempt using server-side positions and team membership. Clients only ever display broadcasts or request actions — the server always decides.

## Build / Setup Guide (recreating from a blank Baseplate)

1. **Teams:** Under the `Teams` service, add `Team` objects `RedTeam` and `BlueTeam` (`AutoAssignable=false`), each with a `TeamScore` `IntValue` child.
2. **Spawns:** In `Workspace`, add folders `RedSpawns`/`BlueSpawns`, each containing 2 invisible, non-collide spawn `Part`s on opposite sides of an arena floor (`ArenaFloor` Part).
3. **Remotes:** In `ReplicatedStorage`, add a `Folder` named `Remotes` with 4 `RemoteEvent`s: `TagPlayer`, `RoundStateChanged`, `TeamScoreUpdate`, `RestartRound`.
4. **Server logic:** In `ServerScriptService`, add `Modules` (Folder) with `ModuleScript`s `TeamManager`, `RoundManager`, `CombatManager`, `SafeCall` (all siblings — `CombatManager` requires the other two via `script.Parent`), then add the `GameManager` `Script`.
5. **UI:** In `StarterGui`, add `GameUI` (`ScreenGui`) with `RoundStateLabel`, `RedScoreLabel`, `BlueScoreLabel`, a `ResultBanner` `Frame` → `ResultBannerLabel`, and a `RestartButton`. Paste the `UIController` `LocalScript` into `GameUI`.
6. **Client tagging:** Paste `TagController` (`LocalScript`) into `StarterPlayer/StarterPlayerScripts`.

## Testing

- **Test tab → 2+ Players is required** to test tagging (a single player never has an opposing-team target, so tags always correctly reject).
- With 2 clients on opposite teams, stand within 8 studs during InProgress and press `F` from each side; confirm the attacker's team score increments and the tagged player respawns at their team's spawn.
- Confirm tagging your own teammate never scores.
- Confirm rapid F-mashing only scores once per 1.5s per attacker.
- Let the round timer run out (or temporarily shorten `ROUND_SECONDS` in `RoundManager.module.lua` while testing) and confirm `Ended` shows the correct winner and Restart works.

## Troubleshooting

- **Tags never land:** confirm both players are on different `Team`s and within ~8 studs.
- **Scores don't update on screen:** confirm `TeamScoreUpdate` remote name matches exactly in `GameManager` and `UIController`.
- **Nobody gets auto-assigned to a team:** confirm `RedTeam`/`BlueTeam` exist directly under `Teams` with those exact names.

## Customization / Extension Ideas

- Add a ranged "tag" via a thrown projectile instead of melee range.
- Add per-player tag counts as an additional `leaderstats` value.
- Add a "capture the flag" objective mode using the same team/round scaffolding.
