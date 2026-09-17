# Project Overview — Animated Animal Story

## Theme
An animated, multi-scene animal adventure story, designed as the Course 10 portfolio piece that shows off motion, looks, sound, broadcasting, and simple animation together.

## Story Summary
"Pip the Bunny's Big Adventure": Pip wakes up curious, hops out into the meadow, meets Fox, and the pair reach a river they can't cross alone. A wise Turtle appears, offers a ride across its shell, and everyone arrives safely home as new friends. THE END.

## Sprites
| Sprite | Role | Costumes | Sounds |
|---|---|---|---|
| Pip | Main character, the bunny | pip-idle, pip-hop | hop, splash, yay |
| Fox | Friend met in the meadow | fox-idle, fox-step | yip |
| Turtle | Helper who crosses the river | turtle-idle, turtle-swim | plop |

## Backdrops (Stage)
1. `meadow` — story start
2. `river` — the crossing challenge
3. `home` — happy ending

## Scene Flow (Broadcasts)
1. `fox_intro` — Pip meets Fox
2. `fox_greeted` — Fox and Pip start walking together
3. `scene2_river` — backdrop switches to the river; Fox and Turtle both react
4. `turtle_helped` — Turtle finishes helping; Pip celebrates
5. `scene3_home` — backdrop switches to home; story wraps up

## Learning Concepts Demonstrated
- Multiple costumes animated via `next costume` inside a `repeat` loop (walking/hopping motion)
- `say for seconds` dialogue driving a real narrative
- Broadcast-and-receive coordinating 3 independent sprites and the Stage
- Sound effects tied to key story beats
