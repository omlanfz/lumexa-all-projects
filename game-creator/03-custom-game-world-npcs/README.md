# Custom Game World & NPCs

An explorable world with two interactive NPCs (a Guide and a Merchant), collectible crystals that award coins, a coin-for-reward trade quest, and a slowly cycling day/night lighting atmosphere.

## Game Overview

- **Name:** Custom Game World & NPCs
- **Objective:** Explore the world, collect crystals for coins, talk to both NPCs, and trade coins with the Merchant for a reward badge.
- **Target experience:** A relaxed, single- or multi-player exploration/collection loop.

## Learning Objectives

- `ProximityPrompt`-based NPC interaction and simple progressive dialogue
- A collectible/reward loop with respawning pickups
- Server-authoritative "currency spend" validation — the server re-checks the player's real coin balance before ever granting a reward
- Atmosphere via a `Lighting.ClockTime` day/night cycle

## Requirements

- Roblox Studio
- A Roblox account

## How to Open / Run

1. Open Roblox Studio.
2. **File → Open from File...** and select `custom-game-world-npcs.rbxl`.
3. Click **Play** (or **Play Here**) to test — this project is single-player-focused, but also test with **Test tab → 2 Players** to confirm independent coin balances.
4. The place opens fully built — world, NPCs, collectibles, UI, and all scripts are already in place.

## Game Controls

| Input | Action |
|---|---|
| `W A S D` | Move |
| `Space` | Jump |
| `E` (default ProximityPrompt key) | Interact with NPCs |
| Click **Trade (5 coins)** | Spend coins with the Merchant (shown only during Merchant dialogue) |

## Gameplay / Core Mechanics

1. Players explore the world and touch **Crystal** collectibles, each awarding coins, playing a particle+sound reward cue, and respawning 15 seconds later.
2. Walking near the **GuideNPC** shows a `ProximityPrompt`; interacting advances progressive dialogue (3 stages).
3. Walking near the **MerchantNPC** shows a `ProximityPrompt`; interacting greets the player, shows their coin balance, and reveals a **Trade** button.
4. Clicking Trade fires `RequestTrade`; the server independently re-checks the player has ≥5 coins before deducting them and granting the "Lumexa Star Badge" reward — a client cannot fake having enough coins.
5. Completing a trade after talking to both NPCs marks the quest complete.
6. `Lighting.ClockTime` sweeps a full day every 5 real minutes for a living atmosphere.

## Game Structure

```
Workspace
├── Baseplate, SpawnLocation
├── NPCs (Folder)
│   ├── GuideNPC    (Part) → TalkPrompt (ProximityPrompt), GuideNPCHandler (Script)
│   └── MerchantNPC (Part) → TradePrompt (ProximityPrompt), TradeDing (Sound), MerchantNPCHandler (Script)
└── Collectibles (Folder)
    └── Crystal1..6 (Part) → CoinValue (IntValue: 5/5/10/5/10/15), ParticleEmitter,
                              CollectDing (Sound), CollectibleTouch (Script)

ReplicatedStorage
└── Remotes (Folder) → NPCDialogue, UpdateCoins, RequestTrade (RemoteEvents)

ServerScriptService
├── GameManager (Script)              -- leaderstats setup, day/night ClockTime loop
└── Modules (Folder)
    ├── CoinManager (ModuleScript)     -- owns coin balance + server-validated spend
    ├── QuestManager (ModuleScript)    -- owns dialogue-stage + quest-complete progress
    └── SafeCall (ModuleScript)        -- pcall wrapper for cosmetic effects

StarterGui
└── GameUI (ScreenGui)
    ├── CoinsLabel (TextLabel)
    └── DialogueFrame (Frame)
        ├── SpeakerNameLabel, DialogueTextLabel (TextLabel)
        └── TradeButton (TextButton)
```

`CoinManager` and `QuestManager` (server) own all currency and progress truth. The only client-facing Remotes (`NPCDialogue`, `UpdateCoins`) carry read-only display data, and `RequestTrade` is the one client-initiated request, fully re-validated server-side before granting anything.

## Build / Setup Guide (recreating from a blank Baseplate)

1. **NPCs:** In `Workspace`, add a `NPCs` folder with `GuideNPC` (Part, blue) and `MerchantNPC` (Part, gold). Add a `ProximityPrompt` named `TalkPrompt` to `GuideNPC` and `TradePrompt` to `MerchantNPC` (`MaxActivationDistance=10`). Add a `Sound` named `TradeDing` to `MerchantNPC`.
2. **Collectibles:** Add a `Collectibles` folder with `Crystal1..6` (Part, cyan, scattered around the world). Each needs an `IntValue` named `CoinValue` (5/5/10/5/10/15), a `ParticleEmitter` (`Enabled=false`), and a `Sound` named `CollectDing`.
3. **Remotes:** In `ReplicatedStorage`, add a `Folder` named `Remotes` with 3 `RemoteEvent`s: `NPCDialogue`, `UpdateCoins`, `RequestTrade`.
4. **Server logic:** In `ServerScriptService`, add `Modules` (Folder) with `ModuleScript`s `CoinManager`, `QuestManager`, `SafeCall`, then add the `GameManager` `Script`.
5. **Per-instance scripts:** Paste `GuideNPCHandler` into `GuideNPC`, `MerchantNPCHandler` into `MerchantNPC`, and the identical `CollectibleTouch` `Script` into every `Crystal1..6` (behavior differs only via each crystal's own `CoinValue`).
6. **UI:** In `StarterGui`, add `GameUI` (`ScreenGui`) with `CoinsLabel` and a `DialogueFrame` `Frame` containing `SpeakerNameLabel`, `DialogueTextLabel`, and `TradeButton`. Paste the `UIController` `LocalScript` into `GameUI`.
7. **Lighting:** Set `Lighting.ClockTime = 8` initially — `GameManager`'s day-cycle loop animates it automatically once the game runs.

## Testing

- Walk to a Crystal — confirm coins increase, particle/sound feedback plays, and it respawns after ~15 seconds.
- Interact with `GuideNPC` three times — confirm three different dialogue lines appear in sequence, then repeats the final line.
- Collect ≥5 coins, interact with `MerchantNPC`, click Trade — confirm 5 coins are deducted and the reward message shows.
- Try clicking Trade with fewer than 5 coins — confirm the server refuses and shows a "not enough coins" message.
- Watch `Lighting.ClockTime` change gradually over a few minutes.
- Use Test tab → 2 Players to confirm two players collect/trade independently.

## Troubleshooting

- **ProximityPrompt doesn't appear:** confirm it's parented to the NPC Part, `Enabled=true`, and you're within `MaxActivationDistance`.
- **Dialogue never shows:** confirm `NPCDialogue` remote name matches exactly between the NPC handler and `UIController`.
- **Trade always fails:** confirm you actually have ≥5 coins (`Coins` under your `leaderstats`).
- **Crystal never respawns:** confirm `CollectibleTouch` is a `Script` (not `LocalScript`) and `RESPAWN_SECONDS` wasn't changed to something excessive.

## Customization / Extension Ideas

- Add a third NPC with a simple fetch-quest.
- Add a day-only or night-only special collectible tied to the `ClockTime` cycle.
- Persist coins across sessions using `DataStoreService`.
