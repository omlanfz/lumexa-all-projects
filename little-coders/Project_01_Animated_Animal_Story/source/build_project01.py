"""
Build script for Project 01 — Animated Animal Story.
Story: "Pip the Bunny's Big Adventure" — a small bunny who leaves home,
meets a friendly fox, gets scared of a river, and is helped across by
a wise turtle, ending happily back home with new friends.

Sprites: Pip (bunny), Fox, Turtle. Backdrop: Stage with 3 scenes via broadcasts.
Each animal has 2 costumes (idle / hop or step) to animate with next-costume in a loop.
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

# ---- Stage backdrops (3 scenes) ----
bg1 = svg_asset("bg_meadow.svg", fill="#8FE38F", shape="rect", label="Meadow", w=480, h=360)
bg2 = svg_asset("bg_river.svg", fill="#6FC3F7", shape="rect", label="River", w=480, h=360)
bg3 = svg_asset("bg_home.svg", fill="#FFE066", shape="rect", label="Home Sweet Home", w=480, h=360)
proj.stage["costumes"] = [
    {"assetId": "bg_meadow", "name": "meadow", "md5ext": bg1, "dataFormat": "svg", "rotationCenterX": 240, "rotationCenterY": 180},
    {"assetId": "bg_river", "name": "river", "md5ext": bg2, "dataFormat": "svg", "rotationCenterX": 240, "rotationCenterY": 180},
    {"assetId": "bg_home", "name": "home", "md5ext": bg3, "dataFormat": "svg", "rotationCenterX": 240, "rotationCenterY": 180},
]

# Stage script: switch backdrop on each scene broadcast
stage_sprite_stub = None  # stage isn't a Sprite object, so we compile its blocks manually via a helper

def add_stage_script(stack):
    from sb3_builder import _compile_stack
    class _StageProxy:
        pass
    proxy = _StageProxy()
    proxy.name = "Stage"
    proxy._project = proj
    proxy._block_counter = 0
    def _new_id(prefix="b"):
        proxy._block_counter += 1
        return f"{prefix}_stage_{proxy._block_counter}_{os.urandom(3).hex()}"
    proxy._new_id = _new_id
    blocks = proj.stage["blocks"]
    _compile_stack(proxy, stack, blocks, parent=None)

add_stage_script([
    ("event_whenbroadcastreceived", {"BROADCAST_OPTION": "scene2_river"}, {}),
    ("looks_switchbackdropto", {}, {"BACKDROP": "river"}),
])
add_stage_script([
    ("event_whenbroadcastreceived", {"BROADCAST_OPTION": "scene3_home"}, {}),
    ("looks_switchbackdropto", {}, {"BACKDROP": "home"}),
])
add_stage_script([
    ("event_whenflagclicked", {}, {}),
    ("looks_switchbackdropto", {}, {"BACKDROP": "meadow"}),
])

# ---- Pip the Bunny ----
pip = Sprite("Pip", x=-150, y=-50)
c1 = svg_asset("pip_idle.svg", fill="#FFFFFF", shape="circle", label="Pip", w=150, h=150)
c2 = svg_asset("pip_hop.svg", fill="#FFEEEE", shape="circle", label="Pip", w=150, h=150)
pip.add_costume("pip-idle", c1, rotation_center=(75, 75))
pip.add_costume("pip-hop", c2, rotation_center=(75, 75))
s_hop = wav_asset("hop.wav", freq=520, duration=0.15)
pip.add_sound("hop", s_hop)
s_splash = wav_asset("splash.wav", freq=300, duration=0.3)
pip.add_sound("splash", s_splash)
s_yay = wav_asset("yay.wav", freq=700, duration=0.35)
pip.add_sound("yay", s_yay)

pip.add_script([
    ("event_whenflagclicked", {}, {}),
    ("motion_gotoxy", {}, {"X": -150, "Y": -50}),
    ("looks_switchcostumeto", {}, {"COSTUME": "pip-idle"}),
    ("looks_sayforsecs", {}, {"MESSAGE": "One sunny morning, Pip the bunny woke up feeling very curious.", "SECS": 3}),
    ("looks_sayforsecs", {}, {"MESSAGE": "\"I wonder what's past the meadow,\" said Pip.", "SECS": 3}),
    ("control_repeat", {}, {"TIMES": 6, "SUBSTACK": ("stack", [
        ("motion_changexby", {}, {"DX": 15}),
        ("looks_nextcostume", {}, {}),
        ("sound_play", {}, {"SOUND_MENU": "hop"}),
        ("control_wait", {}, {"DURATION": 0.2}),
    ])}),
    ("looks_sayforsecs", {}, {"MESSAGE": "Pip hopped along until a fox appeared from the bushes!", "SECS": 3}),
    ("event_broadcast", {}, {"BROADCAST_INPUT": ("broadcast", "fox_intro")}),
])

pip.add_script([
    ("event_whenbroadcastreceived", {"BROADCAST_OPTION": "fox_greeted"}, {}),
    ("looks_sayforsecs", {}, {"MESSAGE": "\"Nice to meet you, Fox! I'm exploring today,\" said Pip.", "SECS": 3}),
    ("looks_sayforsecs", {}, {"MESSAGE": "Pip and Fox walked together until they reached a big river.", "SECS": 3}),
    ("event_broadcast", {}, {"BROADCAST_INPUT": ("broadcast", "scene2_river")}),
    ("control_wait", {}, {"DURATION": 0.5}),
    ("motion_gotoxy", {}, {"X": -180, "Y": -30}),
    ("looks_sayforsecs", {}, {"MESSAGE": "\"Oh no, the river is too wide! How will we cross?\" worried Pip.", "SECS": 3}),
    ("sound_play", {}, {"SOUND_MENU": "splash"}),
])

pip.add_script([
    ("event_whenbroadcastreceived", {"BROADCAST_OPTION": "turtle_helped"}, {}),
    ("looks_sayforsecs", {}, {"MESSAGE": "\"Thank you, Turtle! You're a hero!\" cheered Pip.", "SECS": 3}),
    ("control_repeat", {}, {"TIMES": 5, "SUBSTACK": ("stack", [
        ("motion_changexby", {}, {"DX": 20}),
        ("looks_nextcostume", {}, {}),
        ("control_wait", {}, {"DURATION": 0.2}),
    ])}),
    ("event_broadcast", {}, {"BROADCAST_INPUT": ("broadcast", "scene3_home")}),
    ("control_wait", {}, {"DURATION": 0.5}),
    ("motion_gotoxy", {}, {"X": -60, "Y": -40}),
    ("sound_play", {}, {"SOUND_MENU": "yay"}),
    ("looks_sayforsecs", {}, {"MESSAGE": "Pip made it home with two brand-new friends. What a wonderful adventure!", "SECS": 4}),
    ("looks_sayforsecs", {}, {"MESSAGE": "THE END", "SECS": 2}),
])

proj.add_sprite(pip)

# ---- Fox ----
fox = Sprite("Fox", x=250, y=-60, visible=False)
fc1 = svg_asset("fox_idle.svg", fill="#FF8C42", shape="triangle", label="Fox", w=150, h=150)
fc2 = svg_asset("fox_step.svg", fill="#FFA85C", shape="triangle", label="Fox", w=150, h=150)
fox.add_costume("fox-idle", fc1, rotation_center=(75, 75))
fox.add_costume("fox-step", fc2, rotation_center=(75, 75))
s_yip = wav_asset("yip.wav", freq=900, duration=0.15)
fox.add_sound("yip", s_yip)

fox.add_script([
    ("event_whenflagclicked", {}, {}),
    ("looks_hide", {}, {}),
    ("motion_gotoxy", {}, {"X": 250, "Y": -60}),
])
fox.add_script([
    ("event_whenbroadcastreceived", {"BROADCAST_OPTION": "fox_intro"}, {}),
    ("looks_show", {}, {}),
    ("sound_play", {}, {"SOUND_MENU": "yip"}),
    ("looks_sayforsecs", {}, {"MESSAGE": "\"Yip! Hello little bunny, where are you headed?\" asked Fox.", "SECS": 3}),
    ("control_repeat", {}, {"TIMES": 6, "SUBSTACK": ("stack", [
        ("motion_changexby", {}, {"DX": -15}),
        ("looks_nextcostume", {}, {}),
        ("control_wait", {}, {"DURATION": 0.2}),
    ])}),
    ("event_broadcast", {}, {"BROADCAST_INPUT": ("broadcast", "fox_greeted")}),
])
fox.add_script([
    ("event_whenbroadcastreceived", {"BROADCAST_OPTION": "scene2_river"}, {}),
    ("motion_gotoxy", {}, {"X": -120, "Y": -60}),
    ("looks_sayforsecs", {}, {"MESSAGE": "\"Hmm, I can't swim either,\" said Fox, scratching its head.", "SECS": 3}),
])
proj.add_sprite(fox)

# ---- Turtle ----
turtle = Sprite("Turtle", x=0, y=-120, visible=False)
tc1 = svg_asset("turtle_idle.svg", fill="#4CAF50", shape="circle", label="Turtle", w=140, h=140)
tc2 = svg_asset("turtle_swim.svg", fill="#66BB6A", shape="circle", label="Turtle", w=140, h=140)
turtle.add_costume("turtle-idle", tc1, rotation_center=(70, 70))
turtle.add_costume("turtle-swim", tc2, rotation_center=(70, 70))
s_splash2 = wav_asset("turtle_splash.wav", freq=250, duration=0.25)
turtle.add_sound("plop", s_splash2)

turtle.add_script([
    ("event_whenflagclicked", {}, {}),
    ("looks_hide", {}, {}),
])
turtle.add_script([
    ("event_whenbroadcastreceived", {"BROADCAST_OPTION": "scene2_river"}, {}),
    ("control_wait", {}, {"DURATION": 1.5}),
    ("motion_gotoxy", {}, {"X": -40, "Y": -100}),
    ("looks_show", {}, {}),
    ("sound_play", {}, {"SOUND_MENU": "plop"}),
    ("looks_sayforsecs", {}, {"MESSAGE": "\"Need a ride? Hop on my shell!\" said the wise old Turtle.", "SECS": 3}),
    ("control_repeat", {}, {"TIMES": 5, "SUBSTACK": ("stack", [
        ("motion_changexby", {}, {"DX": 25}),
        ("looks_nextcostume", {}, {}),
        ("control_wait", {}, {"DURATION": 0.25}),
    ])}),
    ("looks_sayforsecs", {}, {"MESSAGE": "\"There we go, safe and sound!\" said Turtle proudly.", "SECS": 2}),
    ("event_broadcast", {}, {"BROADCAST_INPUT": ("broadcast", "turtle_helped")}),
])
proj.add_sprite(turtle)

out_path = os.path.join(PROJ_DIR, "project.sb3")
proj.save(out_path, assets)
print("Saved:", out_path, os.path.getsize(out_path), "bytes")
