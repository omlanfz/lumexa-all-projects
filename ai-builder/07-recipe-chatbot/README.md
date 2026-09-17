# Recipe Chatbot with Memory

A Lumexa portfolio project: a command-line AI chatbot with a friendly recipe-assistant personality that remembers your stated preferences (like dietary restrictions) throughout a conversation.

## Overview

This project is a Python command-line chatbot powered by the OpenAI API. It's designed to act like a friendly, knowledgeable recipe assistant named **Chef Orbit** who helps you find recipes, suggests ingredient substitutions, and adapts its suggestions based on preferences you mention during the conversation — for example, if you say "I'm vegetarian" or "I'm allergic to peanuts" early on, it will remember that for the rest of the session and avoid suggesting conflicting recipes, without you needing to repeat yourself.

This project directly applies the concepts from Lumexa's Language Models lessons: secure API key handling (Lesson 2), a carefully engineered system prompt (Lesson 3), conversation memory via a growing message history (Lesson 4), and a defined persona and purpose (Lesson 5).

## Learning Objectives

- Understand how conversational memory works by maintaining a list of role/content messages across turns.
- Practice designing a system prompt that gives an assistant both a persona and a clear purpose.
- Practice secure API key handling using `.env` and `python-dotenv`.
- Understand how an LLM can "remember" user-stated facts (like dietary restrictions) purely through resent conversation history.

## Features

- Friendly, in-character "Chef Orbit" recipe assistant persona.
- Remembers dietary restrictions, allergies, and preferences mentioned mid-conversation.
- Suggests recipes, ingredient substitutions, and cooking tips.
- Maintains full conversation history for context-aware, coherent multi-turn conversations.
- Simple `/history` debug command to inspect the raw conversation memory.
- Graceful error handling for a missing or invalid API key.

## Structure

```
07-recipe-chatbot/
├── README.md
├── requirements.txt
├── .env.example
└── src/
    └── chatbot.py
```

## Requirements

- Python 3.9 or later
- An OpenAI API account and API key
- Packages listed in `requirements.txt`: `openai`, `python-dotenv`

## Installation

1. Clone or download this project folder.
2. (Recommended) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate      # on Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration (API Key Setup)

This project **never** hardcodes your API key. Instead:

1. Copy the example environment file to a real one:

   ```bash
   cp .env.example .env
   ```

2. Open `.env` in a text editor and paste your real OpenAI API key:

   ```
   OPENAI_API_KEY=sk-your-real-secret-key-here
   ```

3. `.env` is excluded from version control (see `.gitignore` in a real project repo) — never commit or share this file. `.env.example` contains only a placeholder and is safe to share.

## Running

From the project root, run:

```bash
python src/chatbot.py
```

Chat with Chef Orbit in your terminal. Type `exit` or `quit` to end the conversation. Type `/history` at any time to print the raw conversation memory list currently being sent to the API.

## How It Works

1. **Startup**: The script loads your API key via `python-dotenv`, checks it exists, and initializes the OpenAI client. It also creates a `conversation_history` list starting with a single system message defining Chef Orbit's persona (friendly, encouraging cooking mentor) and purpose (help find/adapt recipes, remember dietary needs).
2. **Each turn**: Your typed message is appended to `conversation_history` as a `user` message. The *entire* history — not just your latest message — is sent to `client.chat.completions.create()`.
3. **Memory**: Because the whole history is resent every turn, anything you mention earlier (like "I'm vegan") remains visible to the model on every later turn, so it naturally adjusts future suggestions — no separate database needed for this session-based memory.
4. **Response**: Chef Orbit's reply is printed and also appended to `conversation_history` as an `assistant` message, so its own past replies stay part of the context too.
5. **Error handling**: If the API key is missing, a clear error is raised before any API call is attempted. If a request fails (network issue, invalid key, rate limit), the error is caught and shown as a friendly in-character message rather than crashing.

## Common Problems

- **`ValueError: Missing OPENAI_API_KEY`** — you haven't created `.env` from `.env.example`, or forgot to paste in a real key. Double check the file exists in the project root and contains a valid key.
- **`AuthenticationError` from the API** — your key is invalid, expired, or was revoked. Generate a new key in your OpenAI account dashboard and update `.env`.
- **Bot "forgets" something you said** — check that you didn't restart the script (memory only lasts for one running session; it is not saved between runs in this version).
- **Slow or no response** — check your internet connection, and confirm you have available API credits/quota on your OpenAI account.

## Extensions

- Persist conversation history to a local JSON file so memory survives across separate runs of the script.
- Add a `/save` command that exports the current conversation as a text file of "saved recipes discussed."
- Rebuild the chatbot as a Streamlit web app (see Lumexa Lesson 7) for a browser-based chat interface.
- Add grounding (Lumexa Lesson 6) by loading a local file of curated recipes and instructing the bot to prefer suggestions from that list.
