# Teacher Guide — Project 01: Animated Animal Story

## Purpose
This portfolio project is where students see Lessons 1–7 (especially motion/looks/sound, broadcasting, and loops) combined into one polished animated story. Use it as a model BEFORE students build their own story in Lesson 7, and again as an exemplar of "final polish" quality.

## How to Use in Class
1. Open `project.sb3` in the Scratch editor and play it for the class first, without explaining how it works — let them enjoy it as a story.
2. Then open the code for the Pip sprite and walk through one script together, connecting it to what students already know: "See this repeat block? That's making Pip's legs animate while it hops, just like Lesson 5!"
3. Point out the broadcast chain (`fox_intro` → `fox_greeted` → `scene2_river` → `turtle_helped` → `scene3_home`) on the whiteboard as a simple flowchart, connecting to Lesson 4 and Lesson 7.
4. Challenge students to remix ONE part (change Pip's dialogue, add a 4th animal, or add a bonus scene) as a warm-up before starting their own Lesson 7 story.

## Key Teaching Moments
- **Animation trick:** two costumes (idle + hop) switched with `next costume` inside a loop is how simple, charming animation works — no fancy art needed.
- **Broadcast chain:** Show how NO sprite directly commands another — they only broadcast and listen, which is a powerful, flexible pattern.
- **Story pacing:** `say for seconds` blocks give the player time to read — a subtle but important detail for young authors to notice.

## Discussion Questions
- "Why does Pip's costume switch back and forth while walking?"
- "How does the fox know when to appear on stage?"
- "What would happen if the Turtle's `when I receive [scene2_river]` block were deleted?"
