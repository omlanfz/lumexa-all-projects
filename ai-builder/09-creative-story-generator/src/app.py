"""
Lumexa Portfolio Project: Creative Story Generator

A Streamlit web app that builds a structured creative-writing prompt from
form inputs (genre, characters, setting, tone, length, theme) and generates
an original short story using the OpenAI API.

Run with:
    streamlit run src/app.py
"""

import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

# ---------------------------------------------------------------------------
# Configuration and setup
# ---------------------------------------------------------------------------

load_dotenv()

# CRITICAL SECURITY RULE: never hardcode your API key. Always load it from
# an environment variable, populated via .env locally or via your hosting
# platform's secrets manager when deployed.
API_KEY = os.environ.get("OPENAI_API_KEY")

MODEL_NAME = "gpt-4o-mini"

GENRES = [
    "Science Fiction", "Fantasy", "Mystery", "Adventure",
    "Comedy", "Horror (mild/age-appropriate)", "Slice of Life",
]
TONES = ["Lighthearted", "Serious", "Suspenseful", "Whimsical", "Inspirational"]
LENGTHS = {
    "Short (about 300 words)": 450,
    "Medium (about 600 words)": 900,
    "Long (about 1000 words)": 1500,
}

st.set_page_config(page_title="Lumexa Story Generator", page_icon="📖", layout="wide")
st.title("📖 Lumexa Creative Story Generator")
st.caption("Build a story brief, and let the AI launch your imagination into orbit.")

if not API_KEY:
    st.error(
        "OPENAI_API_KEY not found. Copy .env.example to .env and add your "
        "real OpenAI API key, then restart the app."
    )
    st.stop()

client = OpenAI(api_key=API_KEY)

SYSTEM_PROMPT = """
You are Nova, a creative writing assistant aboard the Lumexa space station.
You write original, engaging short stories for young readers (ages 12-17)
based on a structured story brief provided by the user.

RULES:
- Write a complete, self-contained story with a clear beginning, middle,
  and end — never leave it obviously unfinished mid-scene.
- Start your response with a short, original title on its own line,
  formatted as "# Title", followed by the story itself.
- Match the requested genre, tone, and approximate length as closely as
  possible.
- Keep content appropriate for a general audience of young teens: avoid
  graphic violence, explicit content, or excessive gore, even for
  horror-genre requests — keep any scares mild and suspense-driven rather
  than graphic.
- Make creative, specific use of the provided characters, setting, and
  theme rather than generic filler description.
""".strip()


def build_story_prompt(
    genre: str,
    characters: str,
    setting: str,
    tone: str,
    length_label: str,
    theme: str,
) -> str:
    """Combine all form inputs into one structured, explicit story brief."""
    return f"""
Write an original short story with the following brief:

GENRE: {genre}
MAIN CHARACTER(S): {characters}
SETTING: {setting}
TONE: {tone}
APPROXIMATE LENGTH: {length_label}
CENTRAL THEME OR MESSAGE: {theme}

Follow all system instructions: begin with a title line, write a complete
story with a real ending, and match the genre, tone, and length as closely
as possible.
""".strip()


def generate_story(prompt: str, temperature: float, max_tokens: int) -> str:
    """Call the OpenAI API with the structured prompt and return the story text."""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except OpenAIError as error:
        return f"Mission control, we hit an error generating your story: {error}"


# ---------------------------------------------------------------------------
# Sidebar: story brief form
# ---------------------------------------------------------------------------

with st.sidebar:
    st.header("Story Brief")
    with st.form("story_form"):
        genre = st.selectbox("Genre", GENRES, index=0)
        characters = st.text_area(
            "Main character(s)",
            placeholder="e.g., Mira, a 14-year-old engineer, and her robot Blip",
        )
        setting = st.text_input(
            "Setting",
            placeholder="e.g., an abandoned space station orbiting Jupiter",
        )
        tone = st.selectbox("Tone", TONES, index=0)
        length_label = st.selectbox("Length", list(LENGTHS.keys()), index=1)
        theme = st.text_input(
            "Central theme or message",
            placeholder="e.g., courage in the face of the unknown",
        )
        temperature = st.slider(
            "Creativity level (temperature)", min_value=0.2, max_value=1.4,
            value=0.9, step=0.1,
            help="Lower = more focused and predictable. Higher = more varied and unexpected.",
        )
        submitted = st.form_submit_button("🚀 Generate Story")

# ---------------------------------------------------------------------------
# Persistent state so the story stays visible across reruns
# ---------------------------------------------------------------------------

if "story_text" not in st.session_state:
    st.session_state.story_text = ""
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""

if submitted:
    if not characters.strip() or not setting.strip():
        st.warning("Please fill in at least the main character(s) and setting.")
    else:
        prompt = build_story_prompt(
            genre, characters, setting, tone, length_label, theme or "a personal challenge"
        )
        st.session_state.last_prompt = prompt
        max_tokens = LENGTHS[length_label]
        with st.spinner("Nova is writing your story..."):
            st.session_state.story_text = generate_story(prompt, temperature, max_tokens)

# ---------------------------------------------------------------------------
# Main panel: display the generated story
# ---------------------------------------------------------------------------

col1, col2 = st.columns([3, 1])

with col1:
    if st.session_state.story_text:
        st.markdown(st.session_state.story_text)
    else:
        st.info("Fill out the story brief in the sidebar and click **Generate Story** to begin.")

with col2:
    if st.session_state.story_text:
        st.subheader("Brief Used")
        st.text(st.session_state.last_prompt)
        if st.button("🔁 Generate another version"):
            with st.spinner("Nova is writing a new version..."):
                max_tokens = LENGTHS[length_label] if "length_label" in dir() else 900
                st.session_state.story_text = generate_story(
                    st.session_state.last_prompt, temperature, max_tokens
                )
            st.rerun()
