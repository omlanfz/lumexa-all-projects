"""
Build script for Project 02 — Interactive Quiz Game.
A host sprite (Quizzy the Robot) asks 5 real space/coding-themed questions
via ask-and-wait, checks each answer, tracks a Score variable, gives
celebratory or encouraging feedback with sound, and shows a results screen.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "_sb3lib"))
from sb3_builder import Project, Sprite, make_svg_costume, make_wav_tone

HERE = os.path.dirname(__file__)
PROJ_DIR = os.path.join(HERE, "..")
ASSETS = os.path.join(PROJ_DIR, "assets")
os.makedirs(ASSETS, exist_ok=True)
assets = []

def svg_asset(fname, **kw):
    path = os.path.join(ASSETS, fname)
    make_svg_costume(path, **kw)
    assets.append((fname, path))
    return fname

def wav_asset(fname, **kw):
    path = os.path.join(ASSETS, fname)
    make_wav_tone(path, **kw)
    assets.append((fname, path))
    return fname

proj = Project()

bg = svg_asset("bg_space.svg", fill="#1B1B3A", shape="rect", label="Lumexa Quiz", w=480, h=360)
proj.stage["costumes"] = [{"assetId": "bg_space", "name": "space", "md5ext": bg, "dataFormat": "svg",
                           "rotationCenterX": 240, "rotationCenterY": 180}]

quizzy = Sprite("Quizzy", x=0, y=0)
c1 = svg_asset("quizzy_idle.svg", fill="#4C97FF", shape="rect", label="Quizzy", w=180, h=180)
c2 = svg_asset("quizzy_happy.svg", fill="#4CD964", shape="rect", label="Yay!", w=180, h=180)
c3 = svg_asset("quizzy_oops.svg", fill="#FF6B6B", shape="rect", label="Oops!", w=180, h=180)
quizzy.add_costume("quizzy-idle", c1, rotation_center=(90, 90))
quizzy.add_costume("quizzy-happy", c2, rotation_center=(90, 90))
quizzy.add_costume("quizzy-oops", c3, rotation_center=(90, 90))

s_correct = wav_asset("correct.wav", freq=880, duration=0.2)
s_wrong = wav_asset("wrong.wav", freq=220, duration=0.3)
s_fanfare = wav_asset("fanfare.wav", freq=1046, duration=0.5)
quizzy.add_sound("correct", s_correct)
quizzy.add_sound("wrong", s_wrong)
quizzy.add_sound("fanfare", s_fanfare)

quizzy.add_variable("Score", 0)
quizzy.add_variable("QuestionNum", 0)

questions = [
    ("What color is the planet Mars usually called?", "red"),
    ("In Scratch, what do we call the characters we code?", "sprite"),
    ("What shape has 3 sides?", "triangle"),
    ("What do we call a block that repeats code many times?", "loop"),
    ("What is 2 + 2?", "4"),
]

def question_block(qtext, answer):
    return [
        ("looks_switchcostumeto", {}, {"COSTUME": "quizzy-idle"}),
        ("data_changevariableby", {"VARIABLE": "QuestionNum"}, {"VALUE": 1}),
        ("sensing_askandwait", {}, {"QUESTION": qtext}),
        ("control_if_else", {}, {
            "CONDITION": ("block", ("operators_equals", {}, {
                "OPERAND1": ("block", ("sensing_answer", {}, {})),
                "OPERAND2": answer,
            })),
            "SUBSTACK": ("stack", [
                ("looks_switchcostumeto", {}, {"COSTUME": "quizzy-happy"}),
                ("sound_play", {}, {"SOUND_MENU": "correct"}),
                ("looks_sayforsecs", {}, {"MESSAGE": "Correct! Great job! ⭐", "SECS": 2}),
                ("data_changevariableby", {"VARIABLE": "Score"}, {"VALUE": 1}),
            ]),
            "SUBSTACK2": ("stack", [
                ("looks_switchcostumeto", {}, {"COSTUME": "quizzy-oops"}),
                ("sound_play", {}, {"SOUND_MENU": "wrong"}),
                ("looks_sayforsecs", {}, {"MESSAGE": ("join_answer", answer), "SECS": 2}),
            ]),
        }),
    ]

# Because looks_say MESSAGE needs a plain literal in this DSL, build the "wrong" message per question directly.
def wrong_message(answer):
    return f"Good try! The answer was: {answer}"

script = [("event_whenflagclicked", {}, {})]
script.append(("data_setvariableto", {"VARIABLE": "Score"}, {"VALUE": 0}))
script.append(("data_setvariableto", {"VARIABLE": "QuestionNum"}, {"VALUE": 0}))
script.append(("data_showvariable", {"VARIABLE": "Score"}, {}))
script.append(("looks_switchcostumeto", {}, {"COSTUME": "quizzy-idle"}))
script.append(("looks_sayforsecs", {}, {"MESSAGE": "Hi! I'm Quizzy the Robot. Let's play a space quiz!", "SECS": 3}))

for qtext, answer in questions:
    script.append(("looks_switchcostumeto", {}, {"COSTUME": "quizzy-idle"}))
    script.append(("data_changevariableby", {"VARIABLE": "QuestionNum"}, {"VALUE": 1}))
    script.append(("sensing_askandwait", {}, {"QUESTION": qtext}))
    script.append(("control_if_else", {}, {
        "CONDITION": ("block", ("operators_equals", {}, {
            "OPERAND1": ("block", ("sensing_answer", {}, {})),
            "OPERAND2": answer,
        })),
        "SUBSTACK": ("stack", [
            ("looks_switchcostumeto", {}, {"COSTUME": "quizzy-happy"}),
            ("sound_play", {}, {"SOUND_MENU": "correct"}),
            ("looks_sayforsecs", {}, {"MESSAGE": "Correct! Great job! Nice work, space coder!", "SECS": 2}),
            ("data_changevariableby", {"VARIABLE": "Score"}, {"VALUE": 1}),
        ]),
        "SUBSTACK2": ("stack", [
            ("looks_switchcostumeto", {}, {"COSTUME": "quizzy-oops"}),
            ("sound_play", {}, {"SOUND_MENU": "wrong"}),
            ("looks_sayforsecs", {}, {"MESSAGE": wrong_message(answer), "SECS": 2}),
        ]),
    }))

# Results screen
script.append(("looks_switchcostumeto", {}, {"COSTUME": "quizzy-idle"}))
script.append(("sound_play", {}, {"SOUND_MENU": "fanfare"}))
script.append(("looks_sayforsecs", {}, {"MESSAGE": "Quiz complete! Let's see how you did...", "SECS": 2}))
script.append(("looks_say", {}, {"MESSAGE": ("block", ("operators_join", {}, {
    "STRING1": ("block", ("operators_join", {}, {
        "STRING1": "You got ",
        "STRING2": ("var", "Score"),
    })),
    "STRING2": " out of 5! 🏆",
}))}))
script.append(("control_wait", {}, {"DURATION": 4}))

quizzy.add_script(script)
proj.add_sprite(quizzy)

out_path = os.path.join(PROJ_DIR, "project.sb3")
proj.save(out_path, assets)
print("Saved:", out_path, os.path.getsize(out_path), "bytes")
