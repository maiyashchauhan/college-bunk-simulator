"""
🎓 COLLEGE BUNK SIMULATOR - STREAMLIT EDITION
High-Octane Campus Stealth Maze Runner with Real Faculty Photos & Smooth Navigation!
"""

import streamlit as st
import streamlit.components.v1 as components
import os
import json
import base64
import subprocess
import sys

# ==============================================================================
# 🎨 STREAMLIT PAGE SETUP & CUSTOM THEMING
# ==============================================================================

st.set_page_config(
    page_title="College Bunk Simulator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Cyber-Campus CSS
st.markdown("""
<style>
    /* Dark cyber theme */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    
    /* Main banner styling */
    .hero-banner {
        background: linear-gradient(135deg, rgba(16, 26, 48, 0.95), rgba(24, 42, 77, 0.95));
        border: 2px solid #00e5ff;
        border-radius: 14px;
        padding: 18px 24px;
        margin-bottom: 20px;
        box-shadow: 0 0 25px rgba(0, 229, 255, 0.25);
        text-align: center;
    }
    
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffd700;
        letter-spacing: 2px;
        margin-bottom: 6px;
        text-shadow: 0 0 12px rgba(255, 215, 0, 0.5);
    }
    
    .hero-sub {
        font-size: 1.05rem;
        color: #00e5ff;
        font-weight: 500;
    }
    
    .badge-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 2px 4px;
        background: rgba(0, 229, 255, 0.15);
        border: 1px solid #00e5ff;
        color: #ffffff;
    }
    
    .badge-gold {
        background: rgba(255, 215, 0, 0.15);
        border: 1px solid #ffd700;
        color: #ffd700;
    }

    .badge-green {
        background: rgba(46, 213, 115, 0.15);
        border: 1px solid #2ed573;
        color: #2ed573;
    }

    /* Faculty card in sidebar */
    .faculty-card {
        background: rgba(18, 24, 38, 0.9);
        border: 1px solid #2a3b5c;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 8px;
        text-align: center;
    }

    /* Streamlit components container */
    iframe {
        border-radius: 12px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(0, 229, 255, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 🏫 CORE ACADEMIC ROSTER & FACULTY RULES
# ==============================================================================

DEPARTMENTS = [
    "ASH",
    "CSE",
    "CSIT",
    "CSE(AI & ML)",
    "CSE(IOT & CS)",
    "ECE",
    "ECS",
    "ME",
    "RA"
]

SEMESTERS = [1, 2, 3, 4, 5, 6, 7, 8]

PRINCIPAL_NAME = "Isha Malhotra (Principal)"

DEPARTMENT_FACULTY = {
    "ASH": {
        "hod": "Pooja Sharma (HOD)",
        "teachers": ["Vaishali Dixit", "Ashok Kumar", "Pooja Jain"]
    },
    "CSE": {
        "hod": "Ashima Mehta (HOD)",
        "teachers": ["Hansraj Yadav", "Manoj Kumar", "Vimmi Malhotra"]
    },
    "CSIT": {
        "hod": "Aswani Kumar (HOD)",
        "teachers": ["Yashwardhan Soni", "Anita Chaudhary", "Sarita"]
    },
    "CSE(AI & ML)": {
        "hod": "Yashwardhan Soni (HOD)",
        "teachers": ["Manoj Kumar", "Ashok Kumar", "Naveen Rathi"]
    },
    "CSE(IOT & CS)": {
        "hod": "Aswani Kumar (HOD)",
        "teachers": ["Yashwardhan Soni", "Anita Chaudhary", "Sarita"]
    },
    "ECE": {
        "hod": "Isha Malhotra (Principal)",
        "teachers": ["Monika Rani", "Amninder Kaur", "Neha Mathur"]
    },
    "ECS": {
        "hod": "Monika Rani (HOD)",
        "teachers": ["Manoj Kumar", "Amninder Kaur", "Neha Mathur"]
    },
    "ME": {
        "hod": "Neha Chauhan (HOD)",
        "teachers": ["Rajesh Mattoo", "Ankit Aggarwal", "Yudhveer Kumar Verma"]
    },
    "RA": {
        "hod": "Neha Chauhan (HOD)",
        "teachers": ["Monika Rani", "Pooja Sharma", "Rajesh Mattoo"]
    }
}

PHOTO_MAP = {
    'isha malhotra': 'isha malhotra.jpeg',
    'pooja sharma': 'pooja sharma.jpeg',
    'vaishali dixit': 'vaishali dixit.jpeg',
    'ashok kumar': 'ashok kumar.jpeg',
    'pooja jain': 'pooja jain.jpeg',
    'ashima mehta': 'ashima mehta.jpeg',
    'hansraj yadav': 'hansraj yadav.jpeg',
    'manoj kumar': 'manoj kumar.jpeg',
    'vimmi malhotra': 'vimmi malhotra.jpeg',
    'ashwani kumar': 'aswani kumar.jpeg',
    'aswani kumar': 'aswani kumar.jpeg',
    'yashwardhan soni': 'yashwardhan soni.jpeg',
    'yashvardhan soni': 'yashwardhan soni.jpeg',
    'anita choudhary': 'anita chaudhary.jpeg',
    'anita chaudhary': 'anita chaudhary.jpeg',
    'sarita': 'sarita.jpeg',
    'naveen rathi': 'naveen rathi.jpeg',
    'monika rani': 'monika rani.jpeg',
    'amninder kaur': 'amninder kaur.jpeg',
    'neha mathur': 'neha mathur.jpeg',
    'neha chauhan': 'neha chauhan.jpeg',
    'rajesh mattoo': 'rajesh mattoo.jpeg',
    'ankit aggarwal': 'ankit aggarwal.jpeg',
    'yudhveer kumar verma': 'yudhveer kumar verma.jpeg'
}

# ==============================================================================
# 📸 PHOTO LOADING & BASE64 ENCODING
# ==============================================================================

@st.cache_data
def get_photo_data_uris():
    """Load all jpeg photos in current directory as base64 data URIs."""
    photos = {}
    for f in os.listdir('.'):
        if f.lower().endswith(('.jpeg', '.jpg', '.png')):
            try:
                with open(f, 'rb') as img_f:
                    b64 = base64.b64encode(img_f.read()).decode('utf-8')
                    photos[f.lower()] = f"data:image/jpeg;base64,{b64}"
            except Exception:
                pass
    return photos

ALL_PHOTOS = get_photo_data_uris()

def get_photo_uri_for_name(name):
    norm = name.lower()
    for clean in ['(hod)', '(principal)', 'principal', 'hod']:
        norm = norm.replace(clean, '')
    norm = norm.strip()
    target_file = PHOTO_MAP.get(norm)
    if target_file and target_file in ALL_PHOTOS:
        return ALL_PHOTOS[target_file]
    # Fallback search
    for k in ALL_PHOTOS:
        if norm in k:
            return ALL_PHOTOS[k]
    return None

# ==============================================================================
# 🗺️ 5 HAND-CRAFTED VERIFIED MAZE LEVELS (Exact same data as yash.py)
# ==============================================================================

LEVEL_DATA = [
    {
        "num": 1,
        "name": "Ground Floor: Corridors of Doom",
        "desc": "Bell rang! Slip past the faculty hunters and sprint to the college GROUND!",
        "theme": {
            "wall_fill": "#19263e",
            "wall_edge": "#375f9b",
            "wall_glow": "#508ce6"
        },
        "maze": [
            "111111111111111111111111111111",
            "100000000011000000000000000001",
            "101111110011011111111110111101",
            "101000010000000000010010000101",
            "101011011111111111010010110101",
            "100010000000010000010000000001",
            "101110111101110111011111111101",
            "100000100000000001000000100001",
            "111010111111011111111110101111",
            "100010000000010000000010001001",
            "101011111111010111111010101001",
            "100000000000010000000000001001",
            "111111101111111111111011111011",
            "100000001000000000001000000001",
            "101111101011111111011111011101",
            "101000000000010000000001010001",
            "101011111111010111111101010111",
            "100000000000000000000000000001",
            "111111111111111111111111111111"
        ],
        "items": [
            {"name": "Bunk Pass", "type": "score", "pts": 150, "pos": [13, 3], "icon": "P"},
            {"name": "Bunk Pass", "type": "score", "pts": 150, "pos": [7, 13], "icon": "P"}
        ]
    },
    {
        "num": 2,
        "name": "First Floor: Science Lab Wing",
        "desc": "Faculty patrolling the science wing! Evade them and advance toward the GROUND!",
        "theme": {
            "wall_fill": "#143226",
            "wall_edge": "#286e50",
            "wall_glow": "#41b987"
        },
        "maze": [
            "111111111111111111111111111111",
            "100000010000001000000100000001",
            "101111010111101011110101111101",
            "101001000100100010010001000101",
            "101001110100111010011101010101",
            "100000000000000000000000010001",
            "111101111111011111110111110111",
            "100001000000010000000100000001",
            "101101011111010111110101111101",
            "101100010000000000010001000101",
            "101101110111111111011101010101",
            "100000000100000001000000010001",
            "111011110101111010111101110111",
            "100010000001001000100001000001",
            "101110111111001111101101011101",
            "100010100000000000100100010101",
            "111010101111111101101111010101",
            "100000001000000000000000000001",
            "111111111111111111111111111111"
        ],
        "items": [
            {"name": "Lab Manual", "type": "score", "pts": 200, "pos": [14, 3], "icon": "M"},
            {"name": "Lab Manual", "type": "score", "pts": 200, "pos": [9, 9], "icon": "M"},
            {"name": "Hot Coffee", "type": "boost", "pts": 100, "pos": [16, 15], "icon": "C"}
        ]
    },
    {
        "num": 3,
        "name": "Second Floor: Central Library",
        "desc": "HOD and teachers checking bookshelf aisles! Navigate out toward the GROUND!",
        "theme": {
            "wall_fill": "#3a2614",
            "wall_edge": "#825023",
            "wall_glow": "#dc913c"
        },
        "maze": [
            "111111111111111111111111111111",
            "100000000000110000000000000001",
            "101110111110110111110111111101",
            "101000100010000100010100000101",
            "101010101011110101010101110101",
            "100010001000000001000001000001",
            "111011101110111101110111011111",
            "100000000010100101000000000001",
            "101111111010100101011111111101",
            "100000001000000000010000000101",
            "111111011011111111011011110101",
            "100000010000010000001000010001",
            "101111011110010011101111011101",
            "101000000010110010000001000101",
            "101011111010111110111101110101",
            "100010000010000000100000010001",
            "111010111111110111101111010111",
            "100000000000000100000000000001",
            "111111111111111111111111111111"
        ],
        "items": [
            {"name": "Hall Ticket", "type": "score", "pts": 250, "pos": [14, 5], "icon": "T"},
            {"name": "Hall Ticket", "type": "score", "pts": 250, "pos": [6, 15], "icon": "T"},
            {"name": "Sneakers", "type": "boost", "pts": 100, "pos": [24, 7], "icon": "S"}
        ]
    },
    {
        "num": 4,
        "name": "Grounds: Canteen & Sports Complex",
        "desc": "Heavy faculty reinforcement! Weave around the canteen to break into the GROUND!",
        "theme": {
            "wall_fill": "#3c161c",
            "wall_edge": "#8c2d37",
            "wall_glow": "#f0505f"
        },
        "maze": [
            "111111111111111111111111111111",
            "100000000000000000000000000001",
            "101111011110111101111011111101",
            "101001010010100101001010000101",
            "101001010010100101001010110101",
            "100000000000000000000000110001",
            "111011111101111110111111110111",
            "100010000000000000000000010001",
            "101010111111001111110111010101",
            "101000100001001000010101000101",
            "101110101101001011010101011101",
            "100000001100000011000000000001",
            "111011111101111110111111110111",
            "100010000000000000000000010001",
            "101010111111111111111111010101",
            "101000000000000000000000000101",
            "101111110111111111110111111101",
            "100000000100000000000000000001",
            "111111111111111111111111111111"
        ],
        "items": [
            {"name": "Canteen Samosa", "type": "score", "pts": 300, "pos": [14, 7], "icon": "S"},
            {"name": "Canteen Samosa", "type": "score", "pts": 300, "pos": [7, 15], "icon": "S"},
            {"name": "Energy Drink", "type": "boost", "pts": 150, "pos": [22, 7], "icon": "E"}
        ]
    },
    {
        "num": 5,
        "name": "The Perimeter: The Grand Main Gate",
        "desc": "FINAL BOSS GAUNTLET! Principal Isha Malhotra & Faculty guard the gate! Break through to the GROUND!",
        "theme": {
            "wall_fill": "#2d1944",
            "wall_edge": "#6e3ca0",
            "wall_glow": "#ffd700"
        },
        "maze": [
            "111111111111111111111111111111",
            "100000000011000000110000000001",
            "101111110011011110110011111101",
            "101000010000010010000010000101",
            "101011011111010010111110110101",
            "100011000001000000100000110001",
            "111011111001110011100111110111",
            "100000001000000000000010000001",
            "101111101111011110111110111101",
            "101000000000010010000000000101",
            "101011111111010010111111110101",
            "100010000001000000100000010001",
            "111110010111111111110101001111",
            "100000000100000000010000000001",
            "101111110101111110101011111101",
            "101000000001000010000000000101",
            "101011111111011011111111110101",
            "100000000000000000000000000001",
            "111111111111111111111111111111"
        ],
        "items": [
            {"name": "Gate Pass", "type": "score", "pts": 500, "pos": [14, 5], "icon": "K"},
            {"name": "Gate Pass", "type": "score", "pts": 500, "pos": [4, 15], "icon": "K"},
            {"name": "Bunk Trophy", "type": "boost", "pts": 1000, "pos": [14, 11], "icon": "🏆"}
        ]
    }
]

# ==============================================================================
# 🎮 SIDEBAR: REGISTRATION & FACULTY PREVIEW
# ==============================================================================

with st.sidebar:
    st.markdown("### 🎓 Student Profile")
    student_name = st.text_input("Student Name", value="", placeholder="Enter Student Name...", help="Starts empty. Falls back to 'Student' if left blank.")
    student_roll = st.text_input("Roll Number", value="", placeholder="Enter Roll Number...", help="Starts empty. Falls back to 'Roll 01' if left blank.")

    st.markdown("---")
    st.markdown("### 🏫 Branch & Semester")
    student_dept = st.selectbox("Department", DEPARTMENTS, index=1)
    student_sem = st.selectbox("Semester", SEMESTERS, index=3)

    st.markdown("---")
    st.markdown("### 🎯 Active Hunters Deployment")

    # Determine Active Hunters for selected Branch & Sem
    if student_sem in (1, 2):
        active_hunters = ["Pooja Sharma (HOD)", "BOUNCER", "SECURITY", PRINCIPAL_NAME]
        st.info("📌 **Sem 1 & 2 Rule:** First-year disciplinary dragnet led by HOD Pooja Sharma, Security & Bouncers!")
    else:
        d_info = DEPARTMENT_FACULTY[student_dept]
        active_hunters = [d_info["hod"]] + d_info["teachers"] + ["BOUNCER", "SECURITY", PRINCIPAL_NAME]
        st.success(f"📌 **Sem {student_sem} Rule:** Specialized {student_dept} departmental faculty deployed!")

    # Display faculty cards with photos
    for h in active_hunters:
        photo_uri = get_photo_uri_for_name(h)
        col_img, col_txt = st.columns([1, 2])
        with col_img:
            if photo_uri:
                st.markdown(f'<img src="{photo_uri}" style="width: 44px; height: 44px; border-radius: 50%; border: 2px solid #00e5ff; object-fit: cover;">', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="width: 44px; height: 44px; border-radius: 50%; background: #1a2a44; border: 2px solid #ffd700; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #ffd700;">{h[:2].upper()}</div>', unsafe_allow_html=True)
        with col_txt:
            if "Principal" in h:
                r_tag = '<span style="color: #ffd700; font-size: 0.75rem; font-weight: bold;">PRINCIPAL</span>'
            elif "HOD" in h:
                r_tag = '<span style="color: #ff4757; font-size: 0.75rem; font-weight: bold;">HOD</span>'
            elif h in ("BOUNCER", "SECURITY"):
                r_tag = '<span style="color: #ffa502; font-size: 0.75rem; font-weight: bold;">CAMPUS GUARD</span>'
            else:
                r_tag = '<span style="color: #2ed573; font-size: 0.75rem; font-weight: bold;">FACULTY</span>'
            st.markdown(f"**{h}**<br>{r_tag}", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🕹️ Controls Guide")
    st.markdown("""
    - **PC Navigation**: `[W A S D]` or `[Arrow Keys]`
    - **Speed Sprint**: `[Hold SHIFT]` (requires coffee/drink boost)
    - **Pause / Resume**: `[P]` or `[ESC]`
    - **Mute Audio**: `[M]`
    - **Mobile**: Use on-screen virtual touch controls below the screen!
    """)

    st.markdown("---")
    if st.button("🖥️ Launch Native Pygame (Local PC)", use_container_width=True):
        try:
            subprocess.Popen([sys.executable, "yash.py"])
            st.toast("Launched Pygame desktop window on your local machine!")
        except Exception as err:
            st.error(f"Could not launch native window: {err}")

# ==============================================================================
# 🎮 MAIN VIEW: BANNER & WEB GAME ENGINE
# ==============================================================================

# Header Banner
final_student_name = student_name.strip() if student_name.strip() else "Student"
final_student_roll = student_roll.strip() if student_roll.strip() else "Roll 01"

st.markdown(f"""
<div class="hero-banner">
    <div class="hero-title">🏃 COLLEGE BUNK SIMULATOR 🏫</div>
    <div class="hero-sub">The Ultimate Campus Stealth & Speed Escape Run</div>
    <div style="margin-top: 10px;">
        <span class="badge-pill">🎓 {final_student_name}</span>
        <span class="badge-pill">🆔 {final_student_roll}</span>
        <span class="badge-pill badge-gold">🏫 {student_dept}</span>
        <span class="badge-pill badge-green">📅 Semester {student_sem}</span>
        <span class="badge-pill">⚡ 5 Dynamic Mazes</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Build JSON configuration for the embedded Web Engine
game_config = {
    "student_name": final_student_name,
    "student_roll": final_student_roll,
    "student_dept": student_dept,
    "student_sem": student_sem,
    "departments": DEPARTMENTS,
    "semesters": SEMESTERS,
    "levels": LEVEL_DATA,
    "faculty_roster": DEPARTMENT_FACULTY,
    "principal_name": PRINCIPAL_NAME,
    "photos": ALL_PHOTOS,
    "photo_map": PHOTO_MAP
}

game_config_json = json.dumps(game_config)

# ==============================================================================
# 🕹️ HTML5 + JAVASCRIPT GAME ENGINE TEMPLATE
# ==============================================================================

game_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        user-select: none;
        -webkit-user-select: none;
    }}
    body {{
        background: #090d16;
        color: #fff;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        overflow-x: hidden;
        padding: 8px 4px;
    }}
    #game-container {{
        position: relative;
        width: 100%;
        max-width: 900px;
        background: #0b1120;
        border-radius: 12px;
        box-shadow: 0 0 30px rgba(0, 229, 255, 0.35);
        border: 2px solid #00e5ff;
        overflow: hidden;
    }}
    canvas {{
        display: block;
        width: 100%;
        height: auto;
        background: #0e1424;
    }}
    /* Mobile Controls Bar */
    #touch-controls {{
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        max-width: 900px;
        background: rgba(14, 20, 36, 0.95);
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 10px 16px;
        margin-top: 10px;
        gap: 10px;
    }}
    .dpad-grid {{
        display: grid;
        grid-template-columns: repeat(3, 48px);
        grid-template-rows: repeat(3, 44px);
        gap: 4px;
        justify-content: center;
    }}
    .touch-btn {{
        background: #1e293b;
        border: 1px solid #00e5ff;
        border-radius: 8px;
        color: #00e5ff;
        font-size: 1.2rem;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        touch-action: manipulation;
        transition: all 0.1s;
    }}
    .touch-btn:active {{
        background: #00e5ff;
        color: #090d16;
        transform: scale(0.94);
    }}
    .btn-action {{
        background: linear-gradient(135deg, #ff4757, #ff6b81);
        border: none;
        color: white;
        padding: 12px 24px;
        font-size: 1rem;
        font-weight: bold;
        border-radius: 8px;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(255, 71, 87, 0.4);
    }}
    .btn-action:active {{
        transform: scale(0.95);
    }}
    .btn-util {{
        background: #152238;
        border: 1px solid #4a69bd;
        color: #82ccdd;
        padding: 8px 14px;
        border-radius: 6px;
        font-size: 0.85rem;
        cursor: pointer;
    }}
</style>
</head>
<body>

<div id="game-container">
    <canvas id="gameCanvas" width="900" height="630"></canvas>
</div>

<!-- Mobile & Responsive Touch Controls -->
<div id="touch-controls">
    <div class="dpad-grid">
        <div></div>
        <button class="touch-btn" id="btn-up">▲</button>
        <div></div>
        <button class="touch-btn" id="btn-left">◀</button>
        <button class="touch-btn" id="btn-center" style="font-size: 0.8rem;">●</button>
        <button class="touch-btn" id="btn-right">▶</button>
        <div></div>
        <button class="touch-btn" id="btn-down">▼</button>
        <div></div>
    </div>
    
    <div style="display: flex; flex-direction: column; gap: 8px; align-items: center;">
        <button class="btn-action" id="btn-sprint">⚡ SPRINT [SHIFT]</button>
        <span style="font-size: 0.75rem; color: #94a3b8;">Hold while Coffee/Boost active</span>
    </div>

    <div style="display: flex; flex-direction: column; gap: 6px;">
        <button class="btn-util" id="btn-sound">🔊 Sound: ON</button>
        <button class="btn-util" id="btn-pause">⏸️ Pause [P]</button>
        <button class="btn-util" id="btn-restart">🔄 Restart Level</button>
    </div>
</div>

<script>
// ==============================================================================
// 📦 GAME CONFIG & INITIALIZATION
// ==============================================================================
const CONFIG = {game_config_json};

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const WIDTH = 900;
const HEIGHT = 630;
const HUD_HEIGHT = 60;
const TILE = 30;
const COLS = 30;
const ROWS = 19;

// Colors
const COLOR_CYAN = "#00e5ff";
const COLOR_GOLD = "#ffd700";
const COLOR_GREEN = "#2ed573";
const COLOR_RED = "#ff4757";
const COLOR_WHITE = "#ffffff";
const COLOR_DARK = "#090d16";

// Audio Synth via Web Audio API
let audioCtx = null;
let soundEnabled = true;

function initAudio() {{
    if (!audioCtx) {{
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        audioCtx = new AudioContext();
    }}
}}

function playTone(freq, type, duration, gainVal=0.1) {{
    if (!soundEnabled || !audioCtx) return;
    try {{
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(gainVal, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
    }} catch(e) {{}}
}}

function playPickupSound() {{ playTone(880, "sine", 0.12, 0.15); }}
function playBoostSound() {{ playTone(540, "triangle", 0.35, 0.2); }}
function playAlertSound() {{ playTone(660, "sawtooth", 0.25, 0.18); }}
function playCaughtSound() {{ playTone(140, "square", 0.45, 0.25); }}
function playWinSound() {{
    playTone(523, "sine", 0.1, 0.15);
    setTimeout(() => playTone(659, "sine", 0.1, 0.15), 100);
    setTimeout(() => playTone(784, "sine", 0.15, 0.2), 200);
    setTimeout(() => playTone(1046, "triangle", 0.4, 0.25), 350);
}}

// ==============================================================================
// 🖼️ PRE-RENDERED AVATARS (21 REAL TEACHER PHOTOS + STUDENT BADGE)
// ==============================================================================
const avatarCache = {{}};
const loadedImages = {{}};

// Preload base64 images into HTML Image elements
for (const [key, uri] of Object.entries(CONFIG.photos)) {{
    const img = new Image();
    img.src = uri;
    loadedImages[key] = img;
}}

function getPhotoForName(name) {{
    let norm = name.toLowerCase();
    for (const clean of ['(hod)', '(principal)', 'principal', 'hod']) {{
        norm = norm.replace(clean, '');
    }}
    norm = norm.trim();
    const targetFile = CONFIG.photo_map[norm];
    if (targetFile && loadedImages[targetFile]) {{
        return loadedImages[targetFile];
    }}
    for (const k of Object.keys(loadedImages)) {{
        if (k.includes(norm)) return loadedImages[k];
    }}
    return null;
}}

function createHunterAvatar(name, size=28) {{
    const off = document.createElement("canvas");
    off.width = size + 4;
    off.height = size + 4;
    const octx = off.getContext("2d");
    const center = off.width / 2;
    const radius = size / 2;

    const img = getPhotoForName(name);
    let borderCol = COLOR_CYAN;
    let fallbackBg = "#223355";
    let inits = "FC";

    const norm = name.toLowerCase();
    if (norm.includes("principal") || norm.includes("isha malhotra")) {{
        borderCol = COLOR_GOLD;
        fallbackBg = "#8c6b12";
        inits = "IM";
    }} else if (norm.includes("hod")) {{
        borderCol = COLOR_RED;
        fallbackBg = "#8c1e28";
        const parts = name.split(" ");
        inits = parts[0][0] + (parts[1] ? parts[1][0] : "");
    }} else if (norm.includes("security")) {{
        borderCol = "#f1c40f";
        fallbackBg = "#2c3e50";
        inits = "SC";
    }} else if (norm.includes("bouncer")) {{
        borderCol = "#e67e22";
        fallbackBg = "#d35400";
        inits = "BC";
    }} else {{
        borderCol = COLOR_CYAN;
        const parts = name.split(" ");
        inits = parts[0][0] + (parts[1] ? parts[1][0] : "");
    }}

    octx.save();
    octx.beginPath();
    octx.arc(center, center, radius, 0, Math.PI * 2);
    octx.clip();

    if (img && img.complete && img.naturalWidth > 0) {{
        octx.drawImage(img, center - radius, center - radius, size, size);
    }} else {{
        octx.fillStyle = fallbackBg;
        octx.fill();
        octx.fillStyle = "#ffffff";
        octx.font = "bold " + Math.floor(size * 0.45) + "px sans-serif";
        octx.textAlign = "center";
        octx.textBaseline = "middle";
        octx.fillText(inits.toUpperCase(), center, center);
    }}
    octx.restore();

    // Border ring
    octx.beginPath();
    octx.arc(center, center, radius, 0, Math.PI * 2);
    octx.lineWidth = 2.5;
    octx.strokeStyle = borderCol;
    octx.stroke();

    return off;
}}

function createStudentAvatar(name, size=28) {{
    const off = document.createElement("canvas");
    off.width = size + 4;
    off.height = size + 4;
    const octx = off.getContext("2d");
    const center = off.width / 2;
    const radius = size / 2;

    const parts = name.replace(/[()]/g, ' ').trim().split(/\\s+/);
    let inits = "ST";
    if (parts.length >= 2) {{
        inits = (parts[0][0] + parts[1][0]).toUpperCase();
    }} else if (parts.length === 1 && parts[0].length >= 2) {{
        inits = parts[0].substring(0, 2).toUpperCase();
    }} else if (parts.length === 1 && parts[0].length === 1) {{
        inits = parts[0].toUpperCase();
    }}

    // Layered cyber-navy circle
    octx.beginPath();
    octx.arc(center, center, radius, 0, Math.PI * 2);
    octx.fillStyle = "#0f1e36";
    octx.fill();

    octx.beginPath();
    octx.arc(center, center, radius - 2, 0, Math.PI * 2);
    octx.fillStyle = "#163c6e";
    octx.fill();

    // Initials in bright cyan
    octx.fillStyle = COLOR_CYAN;
    octx.font = "bold " + Math.floor(size * 0.45) + "px sans-serif";
    octx.textAlign = "center";
    octx.textBaseline = "middle";
    octx.fillText(inits, center, center);

    // Glowing Cyan border
    octx.beginPath();
    octx.arc(center, center, radius, 0, Math.PI * 2);
    octx.lineWidth = 2;
    octx.strokeStyle = COLOR_CYAN;
    octx.stroke();

    return off;
}}

// ==============================================================================
// 📐 COORDINATES & CORNER ASSIST COLLISION ENGINE
// ==============================================================================
function gridToPixel(gx, gy) {{
    return [gx * TILE + TILE / 2, HUD_HEIGHT + gy * TILE + TILE / 2];
}}

function canMoveTo(x, y, radius, maze) {{
    if (x - radius < 0 || x + radius >= WIDTH) return false;
    if (y - radius < HUD_HEIGHT || y + radius >= HEIGHT) return false;

    const minGx = Math.max(0, Math.floor((x - radius) / TILE));
    const maxGx = Math.min(COLS - 1, Math.floor((x + radius) / TILE));
    const minGy = Math.max(0, Math.floor(((y - radius) - HUD_HEIGHT) / TILE));
    const maxGy = Math.min(ROWS - 1, Math.floor(((y + radius) - HUD_HEIGHT) / TILE));

    for (let gy = minGy; gy <= maxGy; gy++) {{
        for (let gx = minGx; gx <= maxGx; gx++) {{
            if (maze[gy][gx] === '1') {{
                const tileL = gx * TILE;
                const tileR = (gx + 1) * TILE;
                const tileT = HUD_HEIGHT + gy * TILE;
                const tileB = HUD_HEIGHT + (gy + 1) * TILE;

                const closestX = Math.max(tileL, Math.min(x, tileR));
                const closestY = Math.max(tileT, Math.min(y, tileB));

                if ((x - closestX)**2 + (y - closestY)**2 < radius * radius) {{
                    return false;
                }}
            }}
        }}
    }}
    return true;
}}

function lineOfSight(x1, y1, x2, y2, maze, steps=12) {{
    for (let s = 1; s < steps; s++) {{
        const t = s / steps;
        const tx = x1 + (x2 - x1) * t;
        const ty = y1 + (y2 - y1) * t;
        const gx = Math.floor(tx / TILE);
        const gy = Math.floor((ty - HUD_HEIGHT) / TILE);
        if (gx >= 0 && gx < COLS && gy >= 0 && gy < ROWS) {{
            if (maze[gy][gx] === '1') return false;
        }} else {{
            return false;
        }}
    }}
    return true;
}}

// Pac-Man style corner auto-alignment & smooth corridor centering
function movePlayer(px, py, dx, dy, speed, radius, maze) {{
    if (dx === 0 && dy === 0) return [px, py];

    let stepX = dx * speed;
    let stepY = dy * speed;
    if (dx !== 0 && dy !== 0) {{
        stepX *= 0.7071;
        stepY *= 0.7071;
    }}

    const gx = Math.floor(px / TILE);
    const gy = Math.floor((py - HUD_HEIGHT) / TILE);
    const colCx = gx * TILE + TILE / 2;
    const rowCy = HUD_HEIGHT + gy * TILE + TILE / 2;

    // Vertical Turn Assist (Aligning X)
    if (stepY !== 0 && stepX === 0) {{
        if (!canMoveTo(px, py + stepY, radius, maze)) {{
            for (const testGx of [gx, gx - 1, gx + 1]) {{
                if (testGx >= 0 && testGx < COLS) {{
                    const tcx = testGx * TILE + TILE / 2;
                    if (Math.abs(tcx - px) <= 14) {{
                        const nudge = Math.sign(tcx - px) * Math.min(Math.abs(tcx - px), speed);
                        if (canMoveTo(px + nudge, py, radius, maze)) {{
                            px += nudge;
                            break;
                        }}
                    }}
                }}
            }}
        }} else {{
            const diffX = colCx - px;
            if (Math.abs(diffX) > 0.3 && Math.abs(diffX) <= 12.0) {{
                const nudge = Math.sign(diffX) * Math.min(Math.abs(diffX), 1.5);
                if (canMoveTo(px + nudge, py, radius, maze)) px += nudge;
            }}
        }}
    }}

    // Horizontal Turn Assist (Aligning Y)
    if (stepX !== 0 && stepY === 0) {{
        if (!canMoveTo(px + stepX, py, radius, maze)) {{
            for (const testGy of [gy, gy - 1, gy + 1]) {{
                if (testGy >= 0 && testGy < ROWS) {{
                    const tcy = HUD_HEIGHT + testGy * TILE + TILE / 2;
                    if (Math.abs(tcy - py) <= 14) {{
                        const nudge = Math.sign(tcy - py) * Math.min(Math.abs(tcy - py), speed);
                        if (canMoveTo(px, py + nudge, radius, maze)) {{
                            py += nudge;
                            break;
                        }}
                    }}
                }}
            }}
        }} else {{
            const diffY = rowCy - py;
            if (Math.abs(diffY) > 0.3 && Math.abs(diffY) <= 12.0) {{
                const nudge = Math.sign(diffY) * Math.min(Math.abs(diffY), 1.5);
                if (canMoveTo(px, py + nudge, radius, maze)) py += nudge;
            }}
        }}
    }}

    // Axis-independent sliding
    if (canMoveTo(px + stepX, py + stepY, radius, maze)) {{
        px += stepX;
        py += stepY;
    }} else {{
        if (stepX !== 0 && canMoveTo(px + stepX, py, radius, maze)) px += stepX;
        if (stepY !== 0 && canMoveTo(px, py + stepY, radius, maze)) py += stepY;
    }}

    return [px, py];
}}

// ==============================================================================
// 🎯 GUARD GENERATION BY DEPARTMENT & SEMESTER
// ==============================================================================
function getGuardsForLevel(dept, sem, lvlIdx) {{
    const levelSlots = [
        [15, 9], [7, 5], [21, 5], [9, 13], [20, 13],
        [4, 9], [25, 9], [15, 3], [15, 15]
    ];
    const spd = 1.9 + lvlIdx * 0.18;
    let roster = [];

    if (sem === 1 || sem === 2) {{
        if (lvlIdx === 0) roster = [["SECURITY", "Security", spd]];
        else if (lvlIdx === 1) roster = [["SECURITY", "Security", spd], ["BOUNCER", "Bouncer", spd + 0.08]];
        else if (lvlIdx === 2) roster = [["SECURITY", "Security", spd], ["Pooja Sharma (HOD)", "HOD", spd + 0.1]];
        else if (lvlIdx === 3) roster = [["SECURITY", "Security", spd], ["BOUNCER", "Bouncer", spd + 0.08], ["Pooja Sharma (HOD)", "HOD", spd + 0.12]];
        else roster = [
            ["SECURITY", "Security", spd],
            ["BOUNCER", "Bouncer", spd + 0.08],
            ["Pooja Sharma (HOD)", "HOD", spd + 0.14],
            [CONFIG.principal_name, "Principal", spd + 0.2]
        ];
    }} else {{
        const d = CONFIG.faculty_roster[dept] || CONFIG.faculty_roster["CSE"];
        const hod = d.hod;
        const [t1, t2, t3] = d.teachers;
        if (lvlIdx === 0) roster = [["SECURITY", "Security", spd], [t1, "Faculty", spd + 0.06]];
        else if (lvlIdx === 1) roster = [["SECURITY", "Security", spd], ["BOUNCER", "Bouncer", spd + 0.06], [t2, "Faculty", spd + 0.08]];
        else if (lvlIdx === 2) roster = [["SECURITY", "Security", spd], ["BOUNCER", "Bouncer", spd + 0.06], [t3, "Faculty", spd + 0.08]];
        else if (lvlIdx === 3) roster = [["SECURITY", "Security", spd], ["BOUNCER", "Bouncer", spd + 0.06], [t1, "Faculty", spd + 0.06], [hod, "HOD", spd + 0.12]];
        else roster = [
            ["SECURITY", "Security", spd],
            ["BOUNCER", "Bouncer", spd + 0.06],
            [hod, "HOD", spd + 0.14],
            [t3, "Faculty", spd + 0.12],
            [CONFIG.principal_name, "Principal", spd + 0.2]
        ];
    }}

    return roster.map((item, i) => {{
        const [name, role, gSpd] = item;
        const slot = levelSlots[i % levelSlots.length];
        const [gPx, gPy] = gridToPixel(slot[0], slot[1]);
        return {{
            name: name,
            role: role,
            x: gPx,
            y: gPy,
            startX: gPx,
            startY: gPy,
            speed: gSpd,
            dir: ["up", "down", "left", "right"][Math.floor(Math.random() * 4)],
            changeCd: Math.floor(Math.random() * 40 + 30),
            alert: false,
            alertTimer: 0,
            radius: 11,
            avatar: createHunterAvatar(name, 28)
        }};
    }});
}}

// ==============================================================================
// 🏃 GAME STATE & MAIN LOOP
// ==============================================================================
let currentLevel = 0;
let lives = 3;
let totalScore = 0;
let gameState = "PLAYING"; // PLAYING, PAUSED, LEVEL_CLEAR, GAME_OVER, VICTORY
let gameStartTime = Date.now();
let levelStartTime = Date.now();

let px = 45, py = 105;
const playerRadius = 8.5;
const baseSpeed = 3.8;
let boostTimer = 0;
let invulnerableTimer = 1.8;
let facingDir = "right";

let guards = [];
let items = [];
let particles = [];
let floatingTexts = [];
let bannerTimer = 2.5;

let caughtByTeacher = "Faculty";
let winData = null;

const studentAvatar = createStudentAvatar(CONFIG.student_name, 28);

function initLevel(lvlIdx) {{
    const lvl = CONFIG.levels[lvlIdx];
    const [spx, spy] = gridToPixel(1, 1);
    px = spx;
    py = spy;
    boostTimer = 0;
    invulnerableTimer = 1.8;
    facingDir = "right";
    bannerTimer = 2.5;
    levelStartTime = Date.now();

    guards = getGuardsForLevel(CONFIG.student_dept, CONFIG.student_sem, lvlIdx);

    items = lvl.items.map(it => {{
        const [ix, iy] = gridToPixel(it.pos[0], it.pos[1]);
        return {{
            name: it.name,
            type: it.type,
            pts: it.pts,
            icon: it.icon,
            x: ix,
            y: iy,
            collected: false
        }};
    }});
}}

initLevel(0);

// Input Handling
const keys = {{}};
window.addEventListener("keydown", (e) => {{
    initAudio();
    keys[e.key.toLowerCase()] = true;
    if (e.key === "p" || e.key === "P" || e.key === "Escape") {{
        if (gameState === "PLAYING") gameState = "PAUSED";
        else if (gameState === "PAUSED") gameState = "PLAYING";
    }}
    if (e.key === "m" || e.key === "M") {{
        soundEnabled = !soundEnabled;
        document.getElementById("btn-sound").innerText = soundEnabled ? "🔊 Sound: ON" : "🔇 Sound: OFF";
    }}
    if (e.key === " " || e.key === "Enter") {{
        if (gameState === "LEVEL_CLEAR") nextLevel();
        else if (gameState === "VICTORY") resetGame();
    }}
    if ((e.key === "r" || e.key === "R") && (gameState === "PAUSED" || gameState === "GAME_OVER")) {{
        retryLevel();
    }}
}});

window.addEventListener("keyup", (e) => {{
    keys[e.key.toLowerCase()] = false;
}});

// Touch Controls Bindings
function bindTouch(btnId, keyName) {{
    const el = document.getElementById(btnId);
    if (!el) return;
    const start = (e) => {{ e.preventDefault(); initAudio(); keys[keyName] = true; }};
    const end = (e) => {{ e.preventDefault(); keys[keyName] = false; }};
    el.addEventListener("mousedown", start);
    el.addEventListener("mouseup", end);
    el.addEventListener("touchstart", start);
    el.addEventListener("touchend", end);
}}

bindTouch("btn-up", "arrowup");
bindTouch("btn-down", "arrowdown");
bindTouch("btn-left", "arrowleft");
bindTouch("btn-right", "arrowright");
bindTouch("btn-sprint", "shift");

document.getElementById("btn-sound").addEventListener("click", () => {{
    soundEnabled = !soundEnabled;
    document.getElementById("btn-sound").innerText = soundEnabled ? "🔊 Sound: ON" : "🔇 Sound: OFF";
}});

document.getElementById("btn-pause").addEventListener("click", () => {{
    if (gameState === "PLAYING") gameState = "PAUSED";
    else if (gameState === "PAUSED") gameState = "PLAYING";
}});

document.getElementById("btn-restart").addEventListener("click", () => {{
    retryLevel();
}});

function spawnParticles(x, y, count=25, colors=[COLOR_CYAN, COLOR_GOLD, COLOR_GREEN]) {{
    for (let i = 0; i < count; i++) {{
        const angle = Math.random() * Math.PI * 2;
        const spd = Math.random() * 3 + 1;
        particles.push({{
            x: x,
            y: y,
            vx: Math.cos(angle) * spd,
            vy: Math.sin(angle) * spd,
            life: 1.0,
            color: colors[Math.floor(Math.random() * colors.length)],
            size: Math.random() * 3.5 + 2
        }});
    }}
}}

function addFloatingText(text, x, y, color=COLOR_GOLD) {{
    floatingTexts.push({{ text, x, y, life: 1.0, color }});
}}

function nextLevel() {{
    if (currentLevel + 1 < CONFIG.levels.length) {{
        currentLevel++;
        gameState = "PLAYING";
        initLevel(currentLevel);
    }} else {{
        gameState = "VICTORY";
    }}
}}

function retryLevel() {{
    lives = 3;
    gameState = "PLAYING";
    initLevel(currentLevel);
}}

function resetGame() {{
    currentLevel = 0;
    lives = 3;
    totalScore = 0;
    gameState = "PLAYING";
    gameStartTime = Date.now();
    initLevel(0);
}}

// ==============================================================================
// 🔄 GAME LOOP
// ==============================================================================
let lastTime = performance.now();

function gameLoop(now) {{
    const dt = Math.min((now - lastTime) / 1000, 0.1);
    lastTime = now;

    update(dt);
    render();

    requestAnimationFrame(gameLoop);
}}
requestAnimationFrame(gameLoop);

function update(dt) {{
    if (gameState !== "PLAYING") return;

    if (bannerTimer > 0) bannerTimer -= dt;
    if (invulnerableTimer > 0) invulnerableTimer -= dt;
    if (boostTimer > 0) boostTimer -= dt;

    // Movement input
    let dx = 0, dy = 0;
    if (keys["arrowleft"] || keys["a"]) {{ dx -= 1; facingDir = "left"; }}
    if (keys["arrowright"] || keys["d"]) {{ dx += 1; facingDir = "right"; }}
    if (keys["arrowup"] || keys["w"]) {{ dy -= 1; facingDir = "up"; }}
    if (keys["arrowdown"] || keys["s"]) {{ dy += 1; facingDir = "down"; }}

    const isSprinting = (keys["shift"]) && (boostTimer > 0);
    const curSpeed = baseSpeed * (isSprinting ? 1.6 : 1.0);

    const lvl = CONFIG.levels[currentLevel];
    [px, py] = movePlayer(px, py, dx, dy, curSpeed, playerRadius, lvl.maze);

    if (isSprinting && (dx !== 0 || dy !== 0) && Math.random() < 0.4) {{
        particles.push({{
            x: px - dx * 8,
            y: py - dy * 8,
            vx: (Math.random() - 0.5) * 1.5,
            vy: (Math.random() - 0.5) * 1.5,
            life: 0.35,
            color: COLOR_CYAN,
            size: 3
        }});
    }}

    // Guard Patrol & AI
    const dirMap = {{
        up: [0, -1, -Math.PI / 2],
        down: [0, 1, Math.PI / 2],
        left: [-1, 0, Math.PI],
        right: [1, 0, 0]
    }};

    for (const g of guards) {{
        const distToPlayer = Math.hypot(px - g.x, py - g.y);
        let gSpeed = g.speed;

        const angleToPlayer = Math.atan2(py - g.y, px - g.x);
        const facingAngle = dirMap[g.dir][2];
        const angleDiff = Math.abs(((angleToPlayer - facingAngle + Math.PI) % (Math.PI * 2)) - Math.PI);

        const inView = (distToPlayer < 120) && (angleDiff < 0.8);
        if (inView && lineOfSight(g.x, g.y, px, py, lvl.maze)) {{
            if (!g.alert) {{
                playAlertSound();
                addFloatingText("!", g.x, g.y - 22, COLOR_RED);
            }}
            g.alert = true;
            g.alertTimer = 2.0;
        }}

        if (g.alertTimer > 0) {{
            g.alertTimer -= dt;
            if (g.alertTimer <= 0) g.alert = false;
        }}

        if (g.alert) {{
            gSpeed *= 1.25;
            const desired = [];
            if (Math.abs(px - g.x) > Math.abs(py - g.y)) {{
                desired.push(px > g.x ? "right" : "left");
                desired.push(py > g.y ? "down" : "up");
            }} else {{
                desired.push(py > g.y ? "down" : "up");
                desired.push(px > g.x ? "right" : "left");
            }}
            let moved = false;
            for (const d of desired) {{
                const [vx, vy] = dirMap[d];
                if (canMoveTo(g.x + vx * gSpeed, g.y + vy * gSpeed, g.radius, lvl.maze)) {{
                    g.x += vx * gSpeed;
                    g.y += vy * gSpeed;
                    g.dir = d;
                    moved = true;
                    break;
                }}
            }}
        }} else {{
            const [vx, vy] = dirMap[g.dir];
            if (canMoveTo(g.x + vx * gSpeed, g.y + vy * gSpeed, g.radius, lvl.maze)) {{
                g.x += vx * gSpeed;
                g.y += vy * gSpeed;
            }} else {{
                const open = Object.keys(dirMap).filter(d => {{
                    const [tvx, tvy] = dirMap[d];
                    return canMoveTo(g.x + tvx * gSpeed, g.y + tvy * gSpeed, g.radius, lvl.maze);
                }});
                g.dir = open.length > 0 ? open[Math.floor(Math.random() * open.length)] : "right";
            }}
            g.changeCd--;
            if (g.changeCd <= 0) {{
                g.changeCd = Math.floor(Math.random() * 50 + 30);
                const open = Object.keys(dirMap).filter(d => {{
                    const [tvx, tvy] = dirMap[d];
                    return canMoveTo(g.x + tvx * gSpeed, g.y + tvy * gSpeed, g.radius, lvl.maze);
                }});
                if (open.length > 0) g.dir = open[Math.floor(Math.random() * open.length)];
            }}
        }}

        // Guard Collision
        if (invulnerableTimer <= 0) {{
            if (Math.hypot(px - g.x, py - g.y) < (playerRadius + g.radius)) {{
                lives--;
                playCaughtSound();
                invulnerableTimer = 2.0;
                addFloatingText("CAUGHT BY " + g.name + "! -1 LIFE", WIDTH / 2, HEIGHT / 2 - 30, COLOR_RED);
                spawnParticles(px, py, 30, [COLOR_RED, "#ffa502", COLOR_WHITE]);

                const [spx, spy] = gridToPixel(1, 1);
                px = spx;
                py = spy;
                for (const grd of guards) {{
                    grd.x = grd.startX;
                    grd.y = grd.startY;
                    grd.alert = false;
                }}

                if (lives <= 0) {{
                    caughtByTeacher = g.name;
                    gameState = "GAME_OVER";
                }}
                break;
            }}
        }}
    }}

    // Item Pickups
    for (const it of items) {{
        if (!it.collected && Math.hypot(px - it.x, py - it.y) < 20) {{
            it.collected = true;
            totalScore += it.pts;
            playPickupSound();
            spawnParticles(it.x, it.y, 16, [COLOR_GOLD, COLOR_WHITE]);
            if (it.type === "boost") {{
                boostTimer = 6.0;
                playBoostSound();
                addFloatingText(it.name + "! SPRINT READY! +" + it.pts, it.x, it.y - 15, COLOR_CYAN);
            }} else {{
                addFloatingText("+" + it.pts + " PTS!", it.x, it.y - 15, COLOR_GOLD);
            }}
        }}
    }}

    // Destination / GROUND reached
    const [exitPx, exitPy] = gridToPixel(COLS - 2, ROWS - 2);
    if (Math.hypot(px - exitPx, py - exitPy) < 22) {{
        const timeSpent = Math.round((Date.now() - levelStartTime) / 100) / 10;
        const timeBonus = Math.max(0, Math.floor((45 - timeSpent) * 20));
        totalScore += timeBonus;
        playWinSound();
        spawnParticles(exitPx, exitPy, 45, [COLOR_GREEN, COLOR_GOLD, COLOR_CYAN]);
        addFloatingText("GROUND REACHED! BUNKED!", px, py - 20, COLOR_GOLD);

        winData = {{
            level: currentLevel + 1,
            time: timeSpent,
            bonus: timeBonus,
            itemsCollected: items.filter(it => it.collected).length,
            itemsTotal: items.length
        }};

        if (currentLevel + 1 < CONFIG.levels.length) {{
            gameState = "LEVEL_CLEAR";
        }} else {{
            gameState = "VICTORY";
        }}
    }}

    // Update Particles
    for (let i = particles.length - 1; i >= 0; i--) {{
        const p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.life -= dt;
        if (p.life <= 0) particles.splice(i, 1);
    }}

    // Update Floating Text
    for (let i = floatingTexts.length - 1; i >= 0; i--) {{
        const ft = floatingTexts[i];
        ft.y -= 25 * dt;
        ft.life -= dt;
        if (ft.life <= 0) floatingTexts.splice(i, 1);
    }}
}}

// ==============================================================================
// 🎨 RENDERING PIPELINE
// ==============================================================================
function render() {{
    const lvl = CONFIG.levels[currentLevel];

    // Background Canvas
    ctx.fillStyle = "#0c1322";
    ctx.fillRect(0, 0, WIDTH, HEIGHT);

    // Corridor Grid Lines
    ctx.strokeStyle = "#141e33";
    ctx.lineWidth = 1;
    for (let x = 0; x < WIDTH; x += 30) {{
        ctx.beginPath();
        ctx.moveTo(x, HUD_HEIGHT);
        ctx.lineTo(x, HEIGHT);
        ctx.stroke();
    }}
    for (let y = HUD_HEIGHT; y < HEIGHT; y += 30) {{
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(WIDTH, y);
        ctx.stroke();
    }}

    // Maze Walls with Theme Colors
    const theme = lvl.theme;
    ctx.fillStyle = theme.wall_fill;
    for (let gy = 0; gy < ROWS; gy++) {{
        for (let gx = 0; gx < COLS; gx++) {{
            if (lvl.maze[gy][gx] === '1') {{
                const tx = gx * TILE;
                const ty = HUD_HEIGHT + gy * TILE;
                ctx.fillStyle = theme.wall_fill;
                ctx.fillRect(tx, ty, TILE, TILE);

                ctx.strokeStyle = theme.wall_edge;
                ctx.lineWidth = 1.5;
                ctx.strokeRect(tx + 1, ty + 1, TILE - 2, TILE - 2);

                ctx.strokeStyle = theme.wall_glow;
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(tx, ty);
                ctx.lineTo(tx + TILE, ty);
                ctx.stroke();
            }}
        }}
    }}

    // Start Zone
    const [startPx, startPy] = gridToPixel(1, 1);
    ctx.fillStyle = "rgba(46, 213, 115, 0.25)";
    ctx.fillRect(TILE, HUD_HEIGHT + TILE, TILE, TILE);
    ctx.strokeStyle = COLOR_GREEN;
    ctx.lineWidth = 2;
    ctx.strokeRect(TILE, HUD_HEIGHT + TILE, TILE, TILE);

    // Campus GROUND Destination Gate
    const [exitPx, exitPy] = gridToPixel(COLS - 2, ROWS - 2);
    const pulseR = 12 + Math.sin(Date.now() / 150) * 3;
    ctx.fillStyle = "#1e4d2b";
    ctx.fillRect((COLS - 2) * TILE, HUD_HEIGHT + (ROWS - 2) * TILE, TILE, TILE);
    ctx.strokeStyle = COLOR_GREEN;
    ctx.lineWidth = 2;
    ctx.strokeRect((COLS - 2) * TILE + 2, HUD_HEIGHT + (ROWS - 2) * TILE + 2, TILE - 4, TILE - 4);

    ctx.beginPath();
    ctx.arc(exitPx, exitPy, pulseR, 0, Math.PI * 2);
    ctx.strokeStyle = COLOR_GOLD;
    ctx.lineWidth = 2;
    ctx.stroke();

    ctx.fillStyle = COLOR_GOLD;
    ctx.font = "bold 9px sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText("GROUND", exitPx, exitPy);

    // Guide Indicator to GROUND if far
    const distToGround = Math.hypot(px - exitPx, py - exitPy);
    if (distToGround > 200) {{
        const guideAng = Math.atan2(exitPy - py, exitPx - px);
        const arrX = px + Math.cos(guideAng) * 26;
        const arrY = py + Math.sin(guideAng) * 26;
        ctx.beginPath();
        ctx.arc(arrX, arrY, 3.5, 0, Math.PI * 2);
        ctx.fillStyle = COLOR_GOLD;
        ctx.fill();

        ctx.fillStyle = COLOR_GOLD;
        ctx.font = "bold 9px sans-serif";
        ctx.fillText("GROUND ➔", arrX + Math.cos(guideAng) * 12, arrY + Math.sin(guideAng) * 12);
    }}

    // Collectibles / Items
    for (const it of items) {{
        if (!it.collected) {{
            const bob = Math.sin(Date.now() / 200 + it.x) * 3;
            ctx.beginPath();
            ctx.arc(it.x, it.y + bob, 10, 0, Math.PI * 2);
            ctx.fillStyle = it.type === "boost" ? "rgba(0, 229, 255, 0.3)" : "rgba(255, 215, 0, 0.3)";
            ctx.fill();

            ctx.fillStyle = it.type === "boost" ? COLOR_CYAN : COLOR_GOLD;
            ctx.font = "bold 13px sans-serif";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillText(it.icon.substring(0, 1), it.x, it.y + bob);
        }}
    }}

    // Guard Vision Cones & Sprites
    const dirMap = {{
        up: -Math.PI / 2,
        down: Math.PI / 2,
        left: Math.PI,
        right: 0
    }};

    for (const g of guards) {{
        // Vision Cone
        const ang = dirMap[g.dir];
        const fov = 0.9;
        const dist = 115;
        ctx.save();
        ctx.beginPath();
        ctx.moveTo(g.x, g.y);
        ctx.arc(g.x, g.y, dist, ang - fov / 2, ang + fov / 2);
        ctx.closePath();
        ctx.fillStyle = g.alert ? "rgba(255, 71, 87, 0.22)" : "rgba(255, 235, 120, 0.12)";
        ctx.fill();
        ctx.restore();

        // Draw Avatar Sprite
        ctx.drawImage(g.avatar, g.x - g.avatar.width / 2, g.y - g.avatar.height / 2);

        // Nameplate
        ctx.fillStyle = "rgba(15, 23, 42, 0.85)";
        ctx.strokeStyle = g.alert ? COLOR_RED : "#475569";
        ctx.lineWidth = 1;
        const nameW = ctx.measureText(g.name).width + 8;
        ctx.fillRect(g.x - nameW / 2, g.y - 24, nameW, 13);
        ctx.strokeRect(g.x - nameW / 2, g.y - 24, nameW, 13);

        ctx.fillStyle = g.alert ? COLOR_RED : COLOR_WHITE;
        ctx.font = "bold 9px sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(g.name, g.x, g.y - 18);
    }}

    // Draw Player (with dynamic initials student badge)
    if (invulnerableTimer <= 0 || Math.floor(Date.now() / 100) % 2 === 0) {{
        if (boostTimer > 0) {{
            ctx.beginPath();
            ctx.arc(px, py, 16, 0, Math.PI * 2);
            ctx.strokeStyle = COLOR_CYAN;
            ctx.lineWidth = 2;
            ctx.stroke();
        }}
        ctx.drawImage(studentAvatar, px - studentAvatar.width / 2, py - studentAvatar.height / 2);

        // Direction Indicator
        const noseAng = dirMap[facingDir];
        const nx = px + Math.cos(noseAng) * 14;
        const ny = py + Math.sin(noseAng) * 14;
        ctx.beginPath();
        ctx.arc(nx, ny, 3, 0, Math.PI * 2);
        ctx.fillStyle = COLOR_WHITE;
        ctx.fill();

        // Student Nameplate
        ctx.fillStyle = "rgba(15, 23, 42, 0.85)";
        ctx.strokeStyle = COLOR_CYAN;
        ctx.lineWidth = 1;
        const sNameW = ctx.measureText(CONFIG.student_name).width + 8;
        ctx.fillRect(px - sNameW / 2, py - 24, sNameW, 13);
        ctx.strokeRect(px - sNameW / 2, py - 24, sNameW, 13);

        ctx.fillStyle = COLOR_CYAN;
        ctx.font = "bold 9px sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(CONFIG.student_name, px, py - 18);
    }}

    // Particles
    for (const p of particles) {{
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size * (p.life), 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.life;
        ctx.fill();
        ctx.globalAlpha = 1.0;
    }}

    // Floating Text Notifications
    for (const ft of floatingTexts) {{
        ctx.fillStyle = ft.color;
        ctx.font = "bold 13px sans-serif";
        ctx.textAlign = "center";
        ctx.globalAlpha = ft.life;
        ctx.fillText(ft.text, ft.x, ft.y);
        ctx.globalAlpha = 1.0;
    }}

    // ==========================================================================
    // 👑 TOP HUD (Displays Branch, Sem, Roll, Score & Lives)
    // ==========================================================================
    ctx.fillStyle = "rgba(10, 16, 28, 0.95)";
    ctx.fillRect(0, 0, WIDTH, HUD_HEIGHT);
    ctx.strokeStyle = "#00e5ff";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(0, HUD_HEIGHT);
    ctx.lineTo(WIDTH, HUD_HEIGHT);
    ctx.stroke();

    ctx.textAlign = "left";
    ctx.fillStyle = COLOR_CYAN;
    ctx.font = "bold 13px sans-serif";
    ctx.fillText("LVL " + (lvl.num) + "/5", 14, 20);
    ctx.fillStyle = COLOR_GOLD;
    ctx.font = "bold 11px sans-serif";
    ctx.fillText(CONFIG.student_dept + " • SEM " + CONFIG.student_sem, 14, 40);

    ctx.fillStyle = COLOR_WHITE;
    ctx.font = "bold 14px sans-serif";
    ctx.fillText(lvl.name, 110, 30);

    // Center Lives & Info
    ctx.textAlign = "center";
    ctx.fillStyle = "#cbd5e1";
    ctx.font = "11px sans-serif";
    ctx.fillText(CONFIG.student_name + " (" + CONFIG.student_roll + ")", WIDTH / 2, 18);

    const hearts = "❤️ ".repeat(lives) + "🖤 ".repeat(Math.max(0, 3 - lives));
    ctx.fillStyle = COLOR_RED;
    ctx.font = "14px sans-serif";
    ctx.fillText("LIVES: " + hearts, WIDTH / 2, 38);

    if (boostTimer > 0) {{
        ctx.fillStyle = COLOR_CYAN;
        ctx.font = "bold 11px sans-serif";
        ctx.fillText("⚡ SPRINT READY! [HOLD SHIFT] (" + boostTimer.toFixed(1) + "s)", WIDTH / 2, 54);
    }}

    // Timer & Score
    ctx.textAlign = "right";
    const elapsed = Math.round((Date.now() - levelStartTime) / 100) / 10;
    ctx.fillStyle = COLOR_GOLD;
    ctx.font = "bold 14px sans-serif";
    ctx.fillText("⏱️ " + elapsed.toFixed(1) + "s", WIDTH - 120, 24);
    ctx.fillText("⭐ " + totalScore + " PTS", WIDTH - 120, 44);

    // Intro Splash Banner with Mini Photos
    if (bannerTimer > 0) {{
        ctx.fillStyle = "rgba(10, 16, 28, 0.9)";
        ctx.fillRect(0, HEIGHT / 2 - 45, WIDTH, 90);
        ctx.strokeStyle = COLOR_CYAN;
        ctx.lineWidth = 2;
        ctx.strokeRect(0, HEIGHT / 2 - 45, WIDTH, 90);

        ctx.textAlign = "center";
        ctx.fillStyle = COLOR_GOLD;
        ctx.font = "bold 18px sans-serif";
        ctx.fillText("LEVEL " + lvl.num + ": " + lvl.name, WIDTH / 2, HEIGHT / 2 - 15);

        ctx.fillStyle = COLOR_WHITE;
        ctx.font = "13px sans-serif";
        ctx.fillText(lvl.desc, WIDTH / 2, HEIGHT / 2 + 15);
    }}

    // Modals: Pause, Level Clear, Game Over, Victory
    if (gameState === "PAUSED") {{
        drawModalCard("GAME PAUSED", [
            "[ESC / P] Resume Bunk",
            "[R] Restart Current Level",
            "[M] Toggle Sound Effects"
        ], COLOR_GOLD);
    }} else if (gameState === "LEVEL_CLEAR" && winData) {{
        drawModalCard("🎉 LEVEL " + winData.level + " CLEARED! 🎉", [
            "Ground Path Reached, " + CONFIG.student_name + "!",
            "Time Taken: " + winData.time + "s  |  Bonus: +" + winData.bonus + " PTS",
            "Items Collected: " + winData.itemsCollected + " / " + winData.itemsTotal,
            "Total Score: " + totalScore + " PTS",
            "",
            "➔ CLICK TO ADVANCE TO NEXT LEVEL"
        ], COLOR_GREEN, () => nextLevel());
    }} else if (gameState === "GAME_OVER") {{
        drawModalCard("BUSTED! ZERO ATTENDANCE 🎓❌", [
            "Caught by " + caughtByTeacher + "!",
            "Final Score: " + totalScore + " PTS",
            "",
            "➔ CLICK TO RETRY LEVEL"
        ], COLOR_RED, () => retryLevel());
    }} else if (gameState === "VICTORY") {{
        const totalTime = Math.round((Date.now() - gameStartTime) / 100) / 10;
        const rank = totalScore > 3000 ? "Master Bunk King (S-Rank)" : "Elite Bunk Specialist (A-Rank)";
        drawModalCard("🏆 LEVEL 5 COMPLETED! 🏆", [
            "🚀 UPCOMING LEVELS COMING SOON! 🚀",
            "Congratulations " + CONFIG.student_name + "! You reached the College Ground!",
            "Profile: " + CONFIG.student_dept + " Sem " + CONFIG.student_sem + " (" + CONFIG.student_roll + ")",
            "Evaded Principal " + CONFIG.principal_name + " across all 5 Floors!",
            "Total Time: " + totalTime + "s  |  Final Score: " + totalScore + " PTS",
            "Awarded Title: " + rank,
            "",
            "➔ CLICK TO PLAY AGAIN ↻"
        ], COLOR_GOLD, () => resetGame());
    }}
}}

function drawModalCard(title, lines, borderColor, onClickHandler=null) {{
    ctx.fillStyle = "rgba(8, 12, 22, 0.94)";
    ctx.fillRect(0, 0, WIDTH, HEIGHT);

    const cardW = 620;
    const cardH = 380;
    const cardX = WIDTH / 2 - cardW / 2;
    const cardY = HEIGHT / 2 - cardH / 2;

    ctx.fillStyle = "#0f172a";
    ctx.fillRect(cardX, cardY, cardW, cardH);
    ctx.strokeStyle = borderColor;
    ctx.lineWidth = 3;
    ctx.strokeRect(cardX, cardY, cardW, cardH);

    ctx.textAlign = "center";
    ctx.fillStyle = borderColor;
    ctx.font = "bold 22px sans-serif";
    ctx.fillText(title, WIDTH / 2, cardY + 40);

    ctx.font = "14px sans-serif";
    for (let i = 0; i < lines.length; i++) {{
        const line = lines[i];
        if (line.includes("UPCOMING LEVELS")) {{
            ctx.fillStyle = COLOR_CYAN;
            ctx.font = "bold 16px sans-serif";
        }} else if (line.includes("CLICK TO")) {{
            ctx.fillStyle = COLOR_GOLD;
            ctx.font = "bold 15px sans-serif";
        }} else {{
            ctx.fillStyle = COLOR_WHITE;
            ctx.font = "14px sans-serif";
        }}
        ctx.fillText(line, WIDTH / 2, cardY + 95 + i * 28);
    }}

    if (onClickHandler) {{
        canvas.onclick = () => {{
            canvas.onclick = null;
            onClickHandler();
        }};
    }}
}}

</script>
</body>
</html>
"""

# Embed the responsive web game component directly into Streamlit
components.html(game_html, height=760, scrolling=False)

# ==============================================================================
# 🏆 ACADEMIC GALLERY & FACULTY DIRECTORY
# ==============================================================================
st.markdown("---")
tab1, tab2, tab3 = st.tabs(["👥 Faculty Directory (21 Photos)", "📜 Mission Briefing & Lore", "🚀 Deployment Guide"])

with tab1:
    st.markdown("### 🎓 Full Faculty & Disciplinary Hunters Directory")
    st.caption("All 21 faculty photos loaded dynamically into both Streamlit and the Web Game Engine:")

    dept_cols = st.columns(3)
    for idx, d_name in enumerate(DEPARTMENTS):
        col = dept_cols[idx % 3]
        with col:
            with st.container():
                st.markdown(f"#### 🏛️ {d_name} Department")
                info = DEPARTMENT_FACULTY[d_name]
                
                # HOD
                hod_name = info["hod"]
                hod_img = get_photo_uri_for_name(hod_name)
                c1, c2 = st.columns([1, 3])
                with c1:
                    if hod_img:
                        st.markdown(f'<img src="{hod_img}" style="width: 48px; height: 48px; border-radius: 50%; border: 2px solid #ff4757; object-fit: cover;">', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div style="width: 48px; height: 48px; border-radius: 50%; background: #1a2a44; border: 2px solid #ff4757; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #ff4757;">{hod_name[:2].upper()}</div>', unsafe_allow_html=True)
                with c2:
                    st.markdown(f"**{hod_name}**<br><span style='color: #ff4757; font-size: 0.8rem;'>Department HOD</span>", unsafe_allow_html=True)

                # Teachers
                for t in info["teachers"]:
                    t_img = get_photo_uri_for_name(t)
                    tc1, tc2 = st.columns([1, 3])
                    with tc1:
                        if t_img:
                            st.markdown(f'<img src="{t_img}" style="width: 42px; height: 42px; border-radius: 50%; border: 2px solid #00e5ff; object-fit: cover;">', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div style="width: 42px; height: 42px; border-radius: 50%; background: #1a2a44; border: 2px solid #00e5ff; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #00e5ff;">{t[:2].upper()}</div>', unsafe_allow_html=True)
                    with tc2:
                        st.markdown(f"**{t}**<br><span style='color: #2ed573; font-size: 0.75rem;'>Faculty</span>", unsafe_allow_html=True)
                st.markdown("---")

with tab2:
    st.markdown("""
    ### 🏫 The Legend of the College Bunk
    
    1. **Semester 1 & 2 Disciplinary Dragnet**:
       - First and second semester students face strict campus discipline supervised by **Pooja Sharma (HOD)** alongside **Security** and **Bouncers**.
    2. **Semester 3 to 8 Branch Specialization**:
       - From Semester 3 onwards, departmental HODs and respective subject teachers take over hallway surveillance.
    3. **Universal Campus Guards**:
       - **Security** and **Bouncers** patrol every department, guarding corridors and stairwells.
    4. **Level 5 Main Gate Showdown**:
       - **Principal Isha Malhotra** locks down the main perimeter gate across all 9 departments and all semesters.
    5. **Mission Target - THE GROUND**:
       - Evade faculty vision cones, collect gate passes and coffee speed boosts, make smooth corner turns, and sprint safely to the **College GROUND**!
    """)

with tab3:
    st.markdown("""
    ### 🚀 How to Post / Host this on Streamlit Community Cloud (100% Free)
    
    You can deploy this Streamlit game so anyone on PC or mobile can play via a public web URL:
    
    1. **Create GitHub Repository**:
       - Initialize a Git repo in this folder:
         ```bash
         git init
         git add .
         git commit -m "College Bunk Simulator Streamlit App"
         ```
       - Push to your GitHub account (e.g., `https://github.com/your-username/college-bunk-simulator`).
       
    2. **Deploy on Streamlit Community Cloud**:
       - Go to [share.streamlit.io](https://share.streamlit.io).
       - Sign in with your GitHub account.
       - Click **"New app"**.
       - Select your repository, branch (`main`), and set **Main file path** to `app.py`.
       - Click **"Deploy!"**.
       
    3. **Run Locally**:
       ```powershell
       streamlit run app.py
       ```
    """)
