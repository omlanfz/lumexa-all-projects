"""
Lumexa Portfolio Project: Recipe Chatbot with Memory

A command-line chatbot with a "Chef Orbit" recipe-assistant persona that
remembers dietary preferences and restrictions you mention mid-conversation,
using a growing conversation history sent with every API call.

Run with:
    python src/chatbot.py
"""

import os
import sys

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

# ---------------------------------------------------------------------------
# Configuration and setup
# ---------------------------------------------------------------------------

# Load environment variables from a local .env file (never commit this file).
load_dotenv()

# CRITICAL SECURITY RULE: never hardcode your API key in source code.
# Always load it from an environment variable, populated via .env locally
# or via your hosting platform's secrets manager when deployed.
API_KEY = os.environ.get("OPENAI_API_KEY")

if not API_KEY:
    print(
        "ERROR: OPENAI_API_KEY not found.\n"
        "Copy .env.example to .env and add your real OpenAI API key, "
        "then run this script again."
    )
    sys.exit(1)

client = OpenAI(api_key=API_KEY)

MODEL_NAME = "gpt-4o-mini"

# Chef Orbit's persona and purpose (see Lumexa Lesson 5: AI Personality).
SYSTEM_PROMPT = """
You are Chef Orbit, a warm and encouraging AI recipe assistant aboard the
Lumexa space station galley.

PERSONA:
- You speak in a friendly, enthusiastic tone, like an experienced home cook
  who loves helping people in the kitchen.
- You occasionally use light space/cooking metaphors ("let's launch into
  this recipe"), but at most one per response.
- Keep responses focused and practical: ingredients, steps, or substitutions,
  not long unrelated stories.

PURPOSE:
- Help the user find recipes, suggest ingredient substitutions, and answer
  cooking questions.
- Pay close attention to any dietary restrictions, allergies, or preferences
  the user mentions at ANY point in the conversation (e.g., "I'm vegetarian",
  "I'm allergic to peanuts", "I don't eat dairy"). Remember these for the
  rest of the conversation and never suggest a recipe or ingredient that
  conflicts with them. If you're not sure whether something conflicts with
  a stated restriction, ask a clarifying question rather than guessing.

BOUNDARIES:
- If asked something unrelated to food, cooking, or nutrition, gently
  redirect back to the kitchen: "That's outside my galley duties — let's
  get back to cooking!"
- If you don't know something (like a very obscure ingredient), say so
  honestly rather than inventing an answer.

Stay in character as Chef Orbit for the entire conversation.
""".strip()

# ---------------------------------------------------------------------------
# Conversation memory
# ---------------------------------------------------------------------------

# This list IS the bot's memory. Every user message and every assistant
# reply gets appended here, and the FULL list is resent on every API call.
# This is what lets Chef Orbit "remember" dietary preferences stated earlier.
conversation_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]


def get_ai_reply(history: list) -> str:
    """Send the full conversation history to the API and return the reply text.

    Includes basic error handling so network or API issues don't crash
    the whole program.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=history,
            temperature=0.7,
            max_tokens=350,
        )
        return response.choices[0].message.content
    except OpenAIError as error:
        return f"(Chef Orbit's radio crackled with an error: {error})"


def print_history_debug(history: list) -> None:
    """Print the raw conversation history for debugging/teaching purposes."""
    print("\n--- Raw conversation history (sent to the API each turn) ---")
    for i, message in enumerate(history):
        role = message["role"].upper()
        content = message["content"]
        print(f"[{i}] {role}: {content}")
    print("--- end of history ---\n")


def main() -> None:
    print("=" * 60)
    print("  Chef Orbit's Galley — Lumexa Recipe Chatbot with Memory")
    print("=" * 60)
    print("Tell Chef Orbit what you'd like to cook, or mention any dietary")
    print("restrictions and it will remember them for this session.")
    print("Type 'exit' or 'quit' to leave the galley.")
    print("Type '/history' to see the raw conversation memory.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nChef Orbit: Mission log closed. Happy cooking, cadet!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("Chef Orbit: Mission log closed. Happy cooking, cadet!")
            break

        if user_input.lower() == "/history":
            print_history_debug(conversation_history)
            continue

        # 1. Add the user's message to the shared memory list.
        conversation_history.append({"role": "user", "content": user_input})

        # 2. Send the FULL history (this is what makes memory work).
        reply = get_ai_reply(conversation_history)

        # 3. Add the assistant's reply to memory too, so its own past
        #    responses stay part of the context for future turns.
        conversation_history.append({"role": "assistant", "content": reply})

        print(f"Chef Orbit: {reply}\n")


if __name__ == "__main__":
    main()
