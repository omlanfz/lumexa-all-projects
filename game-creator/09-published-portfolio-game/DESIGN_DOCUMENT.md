# Nova Drift — Design Document

**Project:** Lumexa Game Creator Path, Course 03: Advanced Game Design — Project 09 (Capstone Portfolio Game)
**Genre:** Side-scrolling platformer
**Engine:** Python + Pygame

This document captures the core design thinking behind Nova Drift, applying the vocabulary taught across Course 03: core loop, player goal, challenge, feedback, progression, failure, and replayability (Lesson 01), together with level design pacing (Lesson 02) and playtesting-informed balance (Lesson 06).

## 1. Core Loop

The core loop of Nova Drift, stated in one sentence: **run and jump across platforms → collect shards while avoiding hazards and enemies → reach a checkpoint or the goal → repeat with rising challenge.**

This loop repeats at multiple scales: moment-to-moment (jump to jump), section-to-section (checkpoint to checkpoint), and level-to-level (Level 1 → 2 → 3 → victory). Every element in the game exists to serve this loop — there are no mechanics that don't feed directly into "move skillfully through space, be rewarded for precision, be punished for carelessness."

## 2. Player Goal

The player's goal is explicit and always visible: **reach the goal flag at the far end of each level while collecting as many star shards as possible, without running out of lives.** Secondary goals emerge naturally from this: mastering timing on moving platforms, learning enemy patrol patterns, and deciding whether a risky shard is worth pursuing given current health.

## 3. Challenge

Challenge is introduced using the **teach, test, twist** pattern from Lesson 02:

- **Level 1 ("Launch Pad") teaches** the basics: jumping over static ground hazards and collecting shards on solid, unmoving platforms, in a forgiving layout with wide platforms and generous gaps.
- **Level 2 ("Drifting Platforms") tests** the player on the new mechanics introduced by the game: moving platforms (requiring timed jumps) and patrolling enemies (requiring either avoidance or careful timing), layered onto wider hazard pits.
- **Level 3 ("Nova's Edge") twists** everything together: five moving platforms of mixed axes and speeds, three enemies with tighter patrol ranges, and hazard pits that punish mistimed jumps — while still remaining fair, since every hazard and enemy is clearly visible and telegraphed before the player reaches it (never an off-screen surprise hit).

Difficulty escalates as a staircase, not a straight line: each level opens with an easier introductory stretch (a "breather") before its hardest sections, so players are never asked to perform at their peak skill for the entire level in one unbroken stretch.

## 4. Feedback

Every player action produces immediate, readable feedback:

- **Positive feedback:** collecting a shard triggers an instant floating "+1" popup and updates the HUD shard counter; reaching a checkpoint visibly changes its flag color from gray to green.
- **Negative feedback:** taking damage triggers a screen shake, a floating "-1 HP" popup, a color-coded health bar shift toward red, and a visible invincibility flicker on the player sprite so the player always understands exactly when and why they were hit.
- **State feedback:** the HUD constantly shows health, lives, shard count, and the current level name, so the player is never confused about their current standing.

None of this feedback is guesswork by the player — it is instantaneous and specific, directly following the "feedback loops" principle from Lesson 01 and the "juice" concept from Lesson 08.

## 5. Progression

Progression happens on three timescales:
1. **Within a level:** checkpoints mark real progress, so a death never erases more than the current section's effort.
2. **Across levels:** completing a level unlocks the next and carries the player's total shard count forward, visible on the final victory screen.
3. **Across the whole game:** the three levels form a clear difficulty arc from "Launch Pad" (introductory) to "Nova's Edge" (a genuine test of everything learned), giving the player a satisfying sense of growing mastery that mirrors their own growing skill as they played through Course 03's lessons.

## 6. Failure

Failure is meaningful but never punishing beyond what's fair:
- Taking damage costs 1 of 3 HP and grants brief invincibility frames, preventing "death by mashing into the same hazard repeatedly" frustration.
- Reaching 0 HP costs 1 of 3 lives and respawns the player at their most recent checkpoint (not the level start), keeping failure proportionate to the mistake.
- Running out of all 3 lives triggers a clear Game Over screen with a one-click "Retry Level" option — failure is always recoverable and never a dead end requiring the whole game to be relaunched.

This directly follows Lesson 01's distinction between a game being *hard* (which is good — it requires skill) and being *unfair* (which is bad — for instance, losing all your progress from one single mistake would be unfair, so checkpoints exist specifically to prevent that).

## 7. Replayability

Replayability comes from two sources: **shard-collection completionism** (a player who finished the game with a partial shard count has a clear, visible reason to replay a level and try to collect every shard) and **skill mastery** (a player who died several times to a moving-platform timing puzzle can replay for a cleaner, faster run once they've learned the pattern). The level-select-free, linear structure keeps the initial experience focused and simple for this scope, while the shard counter and per-level attempt awareness (visible via lives/health state) still give committed players something to chase.

## Summary

Nova Drift was designed, from its first core-loop sketch to its final polish pass, using the exact vocabulary and techniques taught across Course 03: a tight, escalating core loop; data-driven, teach-test-twist level design; clean OOP architecture; a deliberate, tuned difficulty curve; instant and specific feedback; forgiving-but-meaningful failure; and multiple angles of replayability — making it a genuine, complete demonstration of everything the course set out to teach.
