"""
Build script for Project 03 — Creative Music Maker.
5 instrument sprites, each with a different pitched tone (or short rhythmic
sequence), triggered by click or key-press, with a visual pulse (size change)
synced to the sound so clicking around feels like composing music.
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
bg = svg_asset("bg_studio.svg", fill="#2E2E48", shape="rect", label="Lumexa Music Maker", w=480, h=360)
proj.stage["costumes"] = [{"assetId": "bg_studio", "name": "studio", "md5ext": bg, "dataFormat": "svg",
                           "rotationCenterX": 240, "rotationCenterY": 180}]

# Instrument definitions: name, position, shape, color, key, note freq(s) (list -> short sequence), pulse color
instruments = [
    ("Drum",    (-160, 60),  "circle",   "#FF5C5C", "1", [220]),
    ("Bell",    (-60, 60),   "star",     "#FFD34D", "2", [880]),
    ("Xylo",    (60, 60),    "rect",     "#4CD9C0", "3", [523, 659, 784]),
    ("Bass",    (160, 60),   "triangle", "#5C7CFF", "4", [110]),
    ("Chime",   (0, -80),    "star",     "#C77DFF", "5", [1046, 1318]),
]

for name, (x, y), shape, color, key, freqs in instruments:
    spr = Sprite(name, x=x, y=y)
    c_idle = svg_asset(f"{name.lower()}_idle.svg", fill=color, shape=shape, label=name, w=140, h=140)
    c_pulse = svg_asset(f"{name.lower()}_pulse.svg", fill="#FFFFFF", shape=shape, label=name, w=140, h=140)
    spr.add_costume(f"{name.lower()}-idle", c_idle, rotation_center=(70, 70))
    spr.add_costume(f"{name.lower()}-pulse", c_pulse, rotation_center=(70, 70))
    for i, f in enumerate(freqs):
        sfile = wav_asset(f"{name.lower()}_note{i}.wav", freq=f, duration=0.22)
        spr.add_sound(f"{name.lower()}-note{i}", sfile)

    def play_sequence_blocks():
        blocks = [
            ("looks_switchcostumeto", {}, {"COSTUME": f"{name.lower()}-pulse"}),
            ("looks_changesizeby", {}, {"CHANGE": 25}),
        ]
        for i in range(len(freqs)):
            blocks.append(("sound_playuntildone", {}, {"SOUND_MENU": f"{name.lower()}-note{i}"}))
        blocks.append(("looks_setsizeto", {}, {"SIZE": 100}))
        blocks.append(("looks_switchcostumeto", {}, {"COSTUME": f"{name.lower()}-idle"}))
        return blocks

    spr.add_script([
        ("event_whenflagclicked", {}, {}),
        ("motion_gotoxy", {}, {"X": x, "Y": y}),
        ("looks_switchcostumeto", {}, {"COSTUME": f"{name.lower()}-idle"}),
        ("looks_setsizeto", {}, {"SIZE": 100}),
    ])
    spr.add_script([
        ("event_whenthisspriteclicked", {}, {}),
    ] + play_sequence_blocks())
    spr.add_script([
        ("event_whenkeypressed", {"KEY_OPTION": key}, {}),
    ] + play_sequence_blocks())

    proj.add_sprite(spr)

out_path = os.path.join(PROJ_DIR, "project.sb3")
proj.save(out_path, assets)
print("Saved:", out_path, os.path.getsize(out_path), "bytes")
