# Creative Story Generator

A Lumexa portfolio project: a polished Streamlit web app that generates original short stories from structured student input — genre, characters, setting, tone, length, and theme.

## Overview

This project is a Streamlit application powered by the OpenAI API. Students fill out a form specifying the genre, main characters, setting, tone, desired length, and theme of a story they want. The app builds a carefully structured prompt from these inputs and generates a complete, original short story, displayed in a polished reading layout.

This project applies concepts from Lumexa's Language Models lessons: secure API key handling (Lesson 2), structured prompt engineering with explicit constraints (Lesson 3), a creative-writing persona (Lesson 5), and a real Streamlit UI using `st.form` and layout tools (Lesson 7).

## Learning Objectives

- Practice building a structured prompt from multiple distinct user inputs.
- Understand how `temperature` affects creative writing output.
- Build a polished Streamlit UI using `st.form`, sidebar/columns, and text display.
- Practice secure API key handling in a creative-generation context.

## Features

- Form inputs for genre, main character(s), setting, tone, desired length, and theme.
- Structured prompt construction that combines all inputs into one clear creative brief.
- Adjustable creativity via a `temperature` slider.
- Generated story displayed in a clean, readable format with a title.
- "Generate another version" support without losing your form inputs.
- Graceful handling of a missing API key.

## Structure

```
09-creative-story-generator/
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

This opens the app in your browser (usually at `http://localhost:8501`). Fill out the story form in the sidebar and click "Generate Story."

## How It Works

1. **Startup**: The app loads the API key via `python-dotenv`. If missing, it shows a clear error and halts with `st.stop()`.
2. **Form input**: A sidebar `st.form()` collects genre, characters, setting, tone, length, and theme in one batch submission (so the app doesn't regenerate on every keystroke, thanks to Streamlit's rerun model).
3. **Prompt construction**: A dedicated function (`build_story_prompt()`) combines all form fields into one structured, explicit user prompt, paired with a system prompt establishing a creative-writing persona and quality guidelines.
4. **Generation**: The structured prompt is sent to `client.chat.completions.create()` with a student-adjustable `temperature` (higher = more creative/unpredictable, lower = more focused/coherent), reflecting the tradeoff taught in Lumexa Lesson 3.
5. **Display**: The generated story is shown in the main panel using Markdown formatting for a clean reading experience, along with the story's inferred title if the model includes one.

## Common Problems

- **App won't start / API key error banner** — you haven't created `.env` from `.env.example`, or the key is missing/invalid.
- **`ModuleNotFoundError: No module named 'streamlit'`** — run `pip install -r requirements.txt` again inside your active virtual environment.
- **Story doesn't match requested length** — token-based length requests are approximate; try adjusting the `max_tokens` value in `app.py` or explicitly stating a paragraph/word count in the theme/tone fields.
- **Repetitive or generic-feeling stories** — try raising the `temperature` slider, or add more specific details in the characters/setting/theme fields (Lumexa Lesson 3: specificity improves output).

## Extensions

- Add a genre-specific system prompt variant (e.g., mystery stories get a "clue-planting" instruction, sci-fi stories get a "explain the tech briefly" instruction).
- Add a "continue this story" button that appends the next chapter using conversation history (Lumexa Lesson 4).
- Add a download/export view using `st.text_area()` so students can copy their finished story.
- Add illustration prompts: have the model also generate a short image-generation-style description of a key scene, for future extension into image generation.
