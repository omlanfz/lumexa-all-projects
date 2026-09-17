"""
Lumexa Portfolio Project: Study Assistant Bot

A Streamlit web app featuring Orbit, an AI study companion that guides
students toward answers with hints and questions rather than simply
handing over solutions.

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

SUBJECTS = ["Math", "Science", "English", "History", "Coding", "Custom subject"]
LEVELS = ["Beginner", "Intermediate", "Advanced"]

st.set_page_config(page_title="Lumexa Study Assistant", page_icon="🪐")
st.title("🪐 Orbit — Your Lumexa Study Assistant")

if not API_KEY:
    st.error(
        "OPENAI_API_KEY not found. Copy .env.example to .env and add your "
        "real OpenAI API key, then restart the app."
    )
    st.stop()

client = OpenAI(api_key=API_KEY)


def build_system_prompt(subject: str, level: str) -> str:
    """Build Orbit's system prompt, tailored to the chosen subject/level.

    The prompt enforces a 'guide, don't just give answers' tutoring style
    as an explicit behavioral rule, not just a tone instruction.
    """
    return f"""
You are Orbit, a friendly AI study companion aboard the Lumexa space station.

PERSONA:
- Warm, encouraging tone, like a patient older sibling.
- At most one light space metaphor per response.
- Keep responses concise: 3-5 sentences unless asked for more detail.

CURRENT SESSION:
- Subject: {subject}
- Explanation level: {level}
- Tailor vocabulary, pacing, and depth of explanation to this level.

PURPOSE (VERY IMPORTANT — TUTORING RULES):
- Your job is to help the student understand {subject} by guiding their
  thinking, NOT by doing their work for them.
- When the student asks a question, first respond with a guiding question
  or a helpful hint, rather than the direct final answer.
- Only give a direct, complete answer if the student has clearly made a
  genuine attempt AND explicitly asks for the answer (e.g., "just tell me
  the answer" or "I've tried and I'm stuck, please explain it").
- If asked, you can generate a practice question at the current subject
  and level. After the student answers, tell them if they're right, and
  if not, guide them toward the correct answer with hints rather than
  immediately stating it.

BOUNDARIES:
- Never write full graded assignments or essays for the student.
- If asked about something unrelated to schoolwork or study skills, gently
  redirect: "That's outside my mission here in the study lab — let's get
  back to your studies!"
- If you're not confident about a fact, say so honestly rather than guessing.

Stay in character as Orbit for the entire conversation.
""".strip()


# ---------------------------------------------------------------------------
# Sidebar: subject/level controls
# ---------------------------------------------------------------------------

with st.sidebar:
    st.header("Mission Controls")
    subject = st.selectbox("Subject", SUBJECTS, index=0)
    if subject == "Custom subject":
        subject = st.text_input("Enter your subject", value="General studies")
    level = st.selectbox("Explanation level", LEVELS, index=0)

    st.divider()
    give_practice = st.button("🎯 Give me a practice question")

    st.divider()
    if st.button("🧹 Clear conversation"):
        st.session_state.messages = [
            {"role": "system", "content": build_system_prompt(subject, level)}
        ]
        st.rerun()

    st.caption(f"Messages this session: {len(st.session_state.get('messages', []))}")


# ---------------------------------------------------------------------------
# Persistent conversation state
# ---------------------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": build_system_prompt(subject, level)}
    ]

# Keep the system prompt in sync with the latest sidebar selections, without
# wiping the rest of the conversation history.
st.session_state.messages[0] = {
    "role": "system",
    "content": build_system_prompt(subject, level),
}


def get_ai_reply(history: list) -> str:
    """Send the full conversation history to the API and return the reply text."""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=history,
            temperature=0.6,
            max_tokens=350,
        )
        return response.choices[0].message.content
    except OpenAIError as error:
        return f"Mission control, we hit an error: {error}"


# ---------------------------------------------------------------------------
# Render existing conversation
# ---------------------------------------------------------------------------

for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------------------------------------------
# Handle the "practice question" button
# ---------------------------------------------------------------------------

if give_practice:
    practice_request = (
        f"Please generate one practice question about {subject} at a "
        f"{level} level. Do not include the answer yet — wait for me to try."
    )
    st.session_state.messages.append({"role": "user", "content": practice_request})
    with st.chat_message("user"):
        st.markdown(practice_request)

    with st.chat_message("assistant"):
        with st.spinner("Orbit is preparing a question..."):
            reply = get_ai_reply(st.session_state.messages)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

# ---------------------------------------------------------------------------
# Chat input
# ---------------------------------------------------------------------------

user_input = st.chat_input("Ask Orbit a question, or answer a practice question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Orbit is thinking..."):
            reply = get_ai_reply(st.session_state.messages)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
