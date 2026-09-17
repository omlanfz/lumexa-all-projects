# Study Assistant Bot

A Lumexa portfolio project: a Streamlit web app named **Orbit**, a study companion that helps students learn by guiding their thinking with hints and questions instead of just handing over answers.

## Overview

This project is a full Streamlit application powered by the OpenAI API. Students pick a subject and a difficulty/explanation level, then chat with Orbit, an AI tutor whose system prompt enforces a strict "guide, don't just give answers" tutoring style: it asks guiding questions, gives hints, and only provides a direct answer if the student has genuinely tried and asks for it explicitly. It also supports a practice question mode.

This project applies concepts from Lumexa's Language Models lessons: secure API key handling (Lesson 2), careful prompt engineering with explicit behavioral rules (Lesson 3), conversation memory (Lesson 4), a defined tutoring persona and purpose with guardrails (Lesson 5), and a real Streamlit chat UI using `st.session_state` (Lesson 7).

## Learning Objectives

- Build a real, runnable Streamlit chat application using `st.chat_message` and `st.chat_input`.
- Understand how `st.session_state` persists conversation memory across Streamlit's rerun model.
- Design a system prompt that enforces a specific pedagogical behavior (hints before answers) rather than just a tone.
- Practice secure API key handling in a Streamlit context.

## Features

- Subject picker (Math, Science, English, History, Coding, or a custom subject).
- Difficulty/explanation level selector (Beginner, Intermediate, Advanced).
- "Guide, don't just give answers" tutoring persona: Orbit asks questions and gives hints before revealing direct answers.
- Practice question mode: Orbit can generate a practice question on the selected subject/level.
- Full chat history maintained via `st.session_state` across the session.
- Sidebar controls: subject/level selection and a "Clear conversation" button.
- Graceful handling of a missing API key.

## Structure

```
08-study-assistant/
├── README.md
├── requirements.txt
├── .env.example
└── src/
    └── app.py
```

## Requirements

- Python 3.9 or later
- An OpenAI API account and API key
- Packages listed in `requirements.txt`: `openai`, `python-dotenv`, `streamlit`

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

2. Open `.env` and paste your real OpenAI API key:

   ```
   OPENAI_API_KEY=sk-your-real-secret-key-here
   ```

3. `.env` should never be committed to version control; only `.env.example` (with a placeholder) is safe to share.

## Running

From the project root, run:

```bash
streamlit run src/app.py
```

This opens the app in your browser (usually at `http://localhost:8501`). Pick a subject and level in the sidebar, then start chatting with Orbit, or click "Give me a practice question" to get a question generated for you.

## How It Works

1. **Startup**: The app loads the API key via `python-dotenv`. If missing, it shows a clear error message using `st.error()` and halts with `st.stop()`.
2. **Sidebar controls**: The student selects a subject and a difficulty level using `st.selectbox()`. These choices are inserted into the system prompt so Orbit tailors its language and depth accordingly.
3. **Session state**: `st.session_state.messages` holds the full conversation (system + user + assistant messages), initialized once with a guard clause so it survives Streamlit's rerun-on-every-interaction behavior (see Lumexa Lesson 7).
4. **Tutoring behavior**: The system prompt explicitly instructs the model to respond with a guiding question or a hint first, and only give a direct answer if the student has made a genuine attempt and explicitly asks for it. This is prompt engineering (Lesson 3) enforcing pedagogy, not just tone.
5. **Practice questions**: A sidebar button sends a special hidden user-style request asking Orbit to generate one practice question at the selected subject/level, which then appears in the chat like a normal message.
6. **Clearing conversation**: A "Clear conversation" button resets `st.session_state.messages` back to just the system prompt and calls `st.rerun()` to refresh the display immediately.

## Common Problems

- **App won't start / `OPENAI_API_KEY not found` error banner** — you haven't created `.env` from `.env.example`, or the key is missing/invalid. Confirm the file exists in the project root.
- **`ModuleNotFoundError: No module named 'streamlit'`** — dependencies weren't installed; run `pip install -r requirements.txt` again inside your active virtual environment.
- **Changing subject/level mid-conversation doesn't seem to apply** — the system prompt is set when the conversation starts; use "Clear conversation" after changing subject/level to start a fresh session with the new settings applied.
- **Orbit just gives the answer immediately** — try being explicit in your message that you want a hint first (e.g., "Can you give me a hint instead of the answer?"); the system prompt strongly encourages hint-first behavior but is not an absolute guarantee against a very direct request.

## Extensions

- Add a difficulty auto-adjustment feature that gets slightly easier or harder based on how many hints the student needed.
- Add a "progress log" sidebar section tracking topics covered during the session.
- Persist chat history to a file so a student can resume a previous study session.
- Add grounding (Lumexa Lesson 6) by loading the student's actual class notes from a local file and having Orbit reference them directly.
