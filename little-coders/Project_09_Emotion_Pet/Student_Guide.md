# Student Guide — Project 09: Emotion-Recognition Virtual Pet

Meet your very own virtual pet! Take care of its feelings. 🚀

## How to play
1. Open `project.sb3` and click the green flag.
2. Press **H** for Happy, **S** for Sad, **W** for Surprised (Wow!).
3. Watch the pet's costume and sound change, and watch the **Happiness** number change too.
4. Happiness slowly goes down over time if you don't interact — keep checking in on your pet!
5. Try to get Happiness all the way up to 100 for a special surprise!

## Explore the code
Open the Pet sprite's scripts. Find the block that checks for each key, and the block that changes Happiness. Find the part that keeps Happiness from ever going above 100 or below 0.

🤖 **Robot Tip:** Pressing H/S/W stands in for a REAL camera looking at your actual face! Check `AI_Training_Guide.md` if you want to try training that for real.

## New words
- **Mood/emotion class:** one category of expression the AI could learn to recognize (happy, sad, surprised).
- **Clamp:** keeping a number from going above or below certain limits (like Happiness never going past 100 or below 0).
