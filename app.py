"""
🎓 COLLEGE BUNK SIMULATOR - MOBILE & FULLSCREEN WEB APP
Pure 60 FPS Landscape Fullscreen Experience with Corner Assist & In-Game Controls
"""

import streamlit as st
import streamlit.components.v1 as components
import os
import json
import base64

# ==============================================================================
# 🎨 STREAMLIT PAGE SETUP - 100% CLEAN FULLSCREEN (NO CLUTTER / BANNERS)
# ==============================================================================

st.set_page_config(
    page_title="College Bunk Simulator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Completely remove Streamlit UI padding, margins, headers, and footers for pure full screen
st.markdown("""
<style>
    /* Hide Streamlit header, footer, decoration, deploy button, and toolbars */
    #MainMenu, header, footer, .stDeployButton, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"], [data-testid="stHeader"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Zero padding and fixed full viewport */
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main {
        background-color: #060911 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
        width: 100vw !important;
        height: 100vh !important;
    }
    
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100vw !important;
        height: 100vh !important;
        overflow: hidden !important;
    }
    
    /* Full viewport iframe container */
    iframe, [data-testid="stCustomComponentV1"], .element-container {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
        margin: 0 !important;
        padding: 0 !important;
        z-index: 9999 !important;
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
    'yudhveer kumar verma': 'yudhveer kumar verma.jpeg',
    'security': 'security.jpeg',
    'security guard': 'security.jpeg',
    'bouncer': 'sonu_bouncer.jpeg',
    'sonu bouncer': 'sonu_bouncer.jpeg',
    'campus bouncer': 'sonu_bouncer.jpeg',
    'counu bouncer': 'sonu_bouncer.jpeg'
}

# ==============================================================================
# 📸 EMBEDDED FACULTY & CAMPUS PHOTO ASSETS & DYNAMIC LOADER
# ==============================================================================

try:
    from faculty_assets import FACULTY_PHOTOS, GAME_BACKGROUND
except Exception:
    FACULTY_PHOTOS = {}
    GAME_BACKGROUND = ""

def get_all_faculty_photos():
    # Start with all embedded base64 assets (guaranteed to be available on Streamlit Cloud)
    photos = dict(FACULTY_PHOTOS)
    # Also scan current directory if local image files exist
    for f in os.listdir('.'):
        if f.lower().endswith(('.jpeg', '.jpg', '.png')):
            try:
                with open(f, 'rb') as img_f:
                    b64 = base64.b64encode(img_f.read()).decode('utf-8')
                    photos[f.lower()] = f"data:image/jpeg;base64,{b64}"
            except Exception:
                pass
    return photos

ALL_PHOTOS = get_all_faculty_photos()

def get_game_background():
    if GAME_BACKGROUND:
        return GAME_BACKGROUND
    for f in ["Snapchat-893693281.jpg", "snapchat.jpg", "college_bg.jpg"]:
        if os.path.exists(f):
            try:
                with open(f, "rb") as img_f:
                    b64 = base64.b64encode(img_f.read()).decode("utf-8")
                    return f"data:image/jpeg;base64,{b64}"
            except Exception:
                pass
    return ""

GAME_BG_DATA = get_game_background()

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
            "101100110111100111100110011101",
            "100000000000000000000000000001",
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

# Build JSON configuration for client-side JavaScript engine
game_config = {
    "student_name": "Student",
    "student_roll": "Roll 01",
    "student_dept": "CSE",
    "student_sem": 4,
    "departments": DEPARTMENTS,
    "semesters": SEMESTERS,
    "levels": LEVEL_DATA,
    "faculty_roster": DEPARTMENT_FACULTY,
    "principal_name": PRINCIPAL_NAME,
    "photos": ALL_PHOTOS,
    "photo_map": PHOTO_MAP,
    "background": GAME_BG_DATA
}

game_config_json = json.dumps(game_config)

# ==============================================================================
# 🕹️ HTML5 + JAVASCRIPT FULLSCREEN LANDSCAPE ENGINE
# ==============================================================================

game_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<title>College Bunk Simulator</title>
<style>
    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }}
    html, body {{
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        background: #060911;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #fff;
        position: fixed;
        margin: 0;
        padding: 0;
    }}

    /* =========================================================================
       📱 AUTOMATIC FULLSCREEN HORIZONTAL LAYOUT (NO ASKING / NO POPUP)
       ========================================================================= */
    #game-container {{
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background: #060911 !important;
        overflow: hidden !important;
        transform-origin: center center !important;
        user-select: none;
        -webkit-user-select: none;
        touch-action: none;
    }}

    /* Automatic 90-degree Horizontal Rotation in Portrait (Zero popups / dont ask) */
    @media screen and (orientation: portrait) {{
        #game-container {{
            top: 50% !important;
            left: 50% !important;
            width: 100vh !important;
            height: 100vw !important;
            transform: translate(-50%, -50%) rotate(90deg) !important;
        }}
    }}

    /* Dynamic JS class fallback for 100% reliable auto-rotation */
    #game-container.mode-portrait {{
        top: 50% !important;
        left: 50% !important;
        width: 100vh !important;
        height: 100vw !important;
        transform: translate(-50%, -50%) rotate(90deg) !important;
    }}
    #game-container.mode-landscape {{
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        transform: none !important;
    }}

    canvas {{
        display: block;
        max-width: 70%;
        max-height: 68%;
        aspect-ratio: 900 / 630;
        object-fit: contain;
        background: #090e1a;
        box-shadow: 0 0 25px rgba(0, 229, 255, 0.3), 0 0 10px rgba(0, 0, 0, 0.9);
        border: 2px solid rgba(0, 229, 255, 0.45);
        border-radius: 10px;
        z-index: 10;
        position: relative;
    }}

    /* =========================================================================
       👑 UPPER RIGHT CORNER CONTROLS (Pause in one, Settings in other)
       ========================================================================= */
    #corner-controls {{
        position: absolute;
        top: 10px;
        right: 14px;
        z-index: 500;
        display: flex;
        gap: 8px;
    }}
    .corner-btn {{
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: rgba(15, 23, 42, 0.88);
        border: 2px solid #00e5ff;
        color: #00e5ff;
        font-size: 1.15rem;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        transition: transform 0.1s, background 0.1s;
    }}
    .corner-btn:active {{
        transform: scale(0.9);
        background: #00e5ff;
        color: #070b12;
    }}

    /* =========================================================================
       ⚙️ SETTINGS MODAL (Sound & Restart Level in One Option)
       ========================================================================= */
    #settings-modal {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100% !important;
        height: 100% !important;
        background: rgba(6, 9, 17, 0.92);
        backdrop-filter: blur(10px);
        z-index: 1100;
        display: none;
        align-items: center;
        justify-content: center;
    }}
    .settings-card {{
        width: 90%;
        max-width: 420px;
        background: #0f172a;
        border: 2px solid #00e5ff;
        border-radius: 16px;
        padding: 22px 18px;
        box-shadow: 0 0 40px rgba(0, 229, 255, 0.4);
        display: flex;
        flex-direction: column;
        gap: 12px;
        text-align: center;
    }}
    .settings-title {{
        font-size: 1.4rem;
        font-weight: 800;
        color: #ffd700;
        letter-spacing: 1.5px;
    }}
    .settings-btn {{
        padding: 12px 14px;
        border-radius: 10px;
        font-size: 1rem;
        font-weight: bold;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        transition: all 0.15s;
    }}
    .btn-sound {{
        background: #1e293b;
        border: 2px solid #2ed573;
        color: #2ed573;
    }}
    .btn-sound.muted {{
        border-color: #ff4757;
        color: #ff4757;
    }}
    .btn-restart {{
        background: #1e293b;
        border: 2px solid #ffd700;
        color: #ffd700;
    }}
    .btn-profile {{
        background: #1e293b;
        border: 2px solid #00e5ff;
        color: #00e5ff;
    }}
    .btn-close {{
        background: linear-gradient(135deg, #00e5ff, #0077b6);
        border: none;
        color: #060911;
        font-weight: 900;
        margin-top: 4px;
    }}
    .settings-btn:active {{
        transform: scale(0.96);
    }}

    /* =========================================================================
       🎓 IN-GAME STUDENT REGISTRATION MODAL (Upright, matches device orientation)
       ========================================================================= */
    #registration-modal {{
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        background: rgba(6, 9, 17, 0.96) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        z-index: 99999 !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: flex-start !important;
        padding: 16px 12px;
        overflow-y: auto !important;
        touch-action: pan-y !important;
        -webkit-overflow-scrolling: touch !important;
    }}
    .reg-card {{
        width: 100%;
        max-width: 500px;
        margin: auto 0;
        background: #0f172a;
        border: 2px solid #00e5ff;
        border-radius: 16px;
        padding: 16px 18px;
        box-shadow: 0 0 35px rgba(0, 229, 255, 0.35), 0 0 80px rgba(0, 0, 0, 0.9);
        display: flex;
        flex-direction: column;
        gap: 10px;
        touch-action: pan-y !important;
    }}
    @media screen and (min-width: 640px) and (orientation: landscape) {{
        .reg-card {{
            max-width: 660px;
            padding: 14px 18px;
            gap: 8px;
        }}
        .reg-body {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            align-items: stretch;
        }}
    }}
    @media screen and (max-width: 639px), screen and (orientation: portrait) {{
        .reg-card {{
            max-width: 440px;
            padding: 14px;
            gap: 8px;
        }}
        .reg-body {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
    }}
    .reg-header {{
        text-align: center;
    }}
    .reg-badge {{
        display: inline-block;
        font-size: 0.65rem;
        font-weight: 800;
        background: rgba(0, 229, 255, 0.15);
        color: #00e5ff;
        border: 1px solid #00e5ff;
        padding: 2px 8px;
        border-radius: 12px;
        letter-spacing: 1px;
    }}
    .reg-title {{
        font-size: 1.25rem;
        font-weight: 900;
        color: #ffd700;
        letter-spacing: 1.2px;
        margin-top: 2px;
    }}
    .reg-sub {{
        font-size: 0.72rem;
        color: #94a3b8;
    }}
    .reg-col {{
        display: flex;
        flex-direction: column;
        gap: 6px;
    }}
    .reg-roster-col {{
        display: flex;
        flex-direction: column;
        gap: 8px;
        justify-content: space-between;
    }}
    .reg-field {{
        display: flex;
        flex-direction: column;
        gap: 2px;
        text-align: left;
    }}
    .reg-field label {{
        font-size: 0.72rem;
        font-weight: bold;
        color: #00e5ff;
        letter-spacing: 0.5px;
    }}
    .reg-field input, .reg-field select {{
        background: #1e293b;
        border: 1.5px solid rgba(0, 229, 255, 0.4);
        border-radius: 8px;
        padding: 9px 12px;
        color: #fff;
        font-size: 1rem;
        outline: none;
        user-select: text !important;
        -webkit-user-select: text !important;
        touch-action: manipulation !important;
        transition: border-color 0.15s, box-shadow 0.15s;
    }}
    .reg-field input:focus, .reg-field select:focus {{
        border-color: #00e5ff;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.4);
    }}
    .reg-field input::placeholder {{
        color: #64748b;
        font-style: italic;
    }}
    .reg-roster-box {{
        background: rgba(15, 23, 42, 0.9);
        border: 1px dashed rgba(255, 215, 0, 0.5);
        border-radius: 8px;
        padding: 8px 10px;
        font-size: 0.75rem;
        line-height: 1.35;
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 3px;
        text-align: left;
    }}
    .btn-start-mission {{
        position: sticky;
        bottom: 0;
        z-index: 10;
        background: linear-gradient(135deg, #00e5ff, #00b4d8);
        border: none;
        border-radius: 10px;
        color: #060911;
        font-size: 1.05rem;
        font-weight: 900;
        padding: 12px 14px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        box-shadow: 0 4px 18px rgba(0, 229, 255, 0.5);
        touch-action: manipulation !important;
        user-select: none;
        -webkit-user-select: none;
        transition: transform 0.1s, box-shadow 0.1s, background 0.15s;
        margin-top: 4px;
    }}
    .btn-start-mission:active {{
        transform: scale(0.96);
        background: #ffd700;
    }}

    /* =========================================================================
       🎮 FLOATING ERGONOMIC MOBILE TOUCH CONTROLS (Horizontal Landscape)
       Positioned completely in side margins outside the puzzle canvas
       ========================================================================= */
    #mobile-controls {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100% !important;
        height: 100% !important;
        pointer-events: none;
        z-index: 300;
    }}
    .touch-dpad {{
        position: absolute;
        left: 14px;
        bottom: 16px;
        pointer-events: auto;
        display: grid;
        grid-template-columns: repeat(3, 36px);
        grid-template-rows: repeat(3, 34px);
        gap: 2px;
        background: rgba(6, 9, 17, 0.45);
        border: 1px solid rgba(0, 229, 255, 0.35);
        border-radius: 12px;
        padding: 4px;
        backdrop-filter: blur(6px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }}
    .dpad-key {{
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(0, 229, 255, 0.35);
        border-radius: 6px;
        color: #00e5ff;
        font-size: 1.05rem;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }}
    .dpad-key:active {{
        background: rgba(0, 229, 255, 0.75);
        color: #060911;
        transform: scale(0.92);
    }}
    .sprint-touch-container {{
        position: absolute;
        right: 18px;
        bottom: 20px;
        pointer-events: auto;
        display: flex;
        flex-direction: column;
        align-items: center;
    }}
    .touch-sprint-btn {{
        width: 62px;
        height: 62px;
        border-radius: 50%;
        background: linear-gradient(135deg, rgba(255, 71, 87, 0.75), rgba(255, 107, 129, 0.75));
        border: 2px solid rgba(255, 71, 87, 0.9);
        color: white;
        font-size: 0.8rem;
        font-weight: 900;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 18px rgba(255, 71, 87, 0.4);
        cursor: pointer;
        backdrop-filter: blur(6px);
        transition: transform 0.1s ease;
    }}
    .touch-sprint-btn:active {{
        transform: scale(0.92);
        background: #ff4757;
    }}
</style>
</head>
<body>

<div id="game-container">
    <!-- Main Scaled Game Canvas (Roomy margins, no congestion) -->
    <canvas id="gameCanvas" width="900" height="630"></canvas>

    <!-- Upper Right Corner Controls: Pause in one, Settings in other -->
    <div id="corner-controls">
        <button class="corner-btn" id="btn-pause" title="Pause / Resume">⏸️</button>
        <button class="corner-btn" id="btn-settings" title="Settings (Sound & Restart Level)">⚙️</button>
    </div>

    <!-- Ergonomic On-Screen Touch Controls (Mobile Horizontal in Side Margins) -->
    <div id="mobile-controls">
        <!-- Left Margin: D-Pad -->
        <div class="touch-dpad">
            <div></div>
            <div class="dpad-key" id="k-up">▲</div>
            <div></div>
            <div class="dpad-key" id="k-left">◀</div>
            <div class="dpad-key" id="k-center" style="font-size: 0.75rem;">●</div>
            <div class="dpad-key" id="k-right">▶</div>
            <div></div>
            <div class="dpad-key" id="k-down">▼</div>
            <div></div>
        </div>

        <!-- Right Margin: Sprint Button -->
        <div class="sprint-touch-container">
            <button class="touch-sprint-btn" id="k-sprint">
                <span>⚡</span>
                <span style="font-size: 0.72rem; letter-spacing: 0.5px;">SPRINT</span>
            </button>
        </div>
    </div>

    <!-- ⚙️ SETTINGS MODAL: Sound, Restart & Change Profile in One Place -->
    <div id="settings-modal">
        <div class="settings-card">
            <div class="settings-title">⚙️ GAME SETTINGS</div>
            <button class="settings-btn btn-sound" id="modal-sound">
                <span id="sound-icon">🔊</span>
                <span id="sound-text">SOUND: ON</span>
            </button>
            <button class="settings-btn btn-restart" id="modal-restart">
                <span>🔄</span>
                <span>RESTART CURRENT LEVEL</span>
            </button>
            <button class="settings-btn btn-profile" id="modal-profile">
                <span>🎓</span>
                <span>CHANGE PROFILE / BRANCH</span>
            </button>
            <button class="settings-btn btn-close" id="modal-close">
                <span>✕ RESUME GAME</span>
            </button>
        </div>
    </div>
</div>

<!-- 🎓 STUDENT ADMISSION & BUNK PROFILE MODAL (Upright, matches device orientation) -->
<div id="registration-modal">
    <div class="reg-card">
        <div class="reg-header">
            <div class="reg-badge">🎓 ADMISSION FORM</div>
            <div class="reg-title">COLLEGE BUNK SIMULATOR</div>
            <div class="reg-sub">Configure your student profile & deploy departmental faculty</div>
        </div>

        <div class="reg-body">
            <div class="reg-col">
                <div class="reg-field">
                    <label for="reg-name">👤 STUDENT NAME</label>
                    <input type="text" id="reg-name" value="" placeholder="Enter your name..." maxlength="25" autocomplete="off">
                </div>
                <div class="reg-field">
                    <label for="reg-roll">🔢 ROLL NUMBER</label>
                    <input type="text" id="reg-roll" value="" placeholder="Enter roll number..." maxlength="20" autocomplete="off">
                </div>
                <div class="reg-field">
                    <label for="reg-dept">🏢 DEPARTMENT / BRANCH</label>
                    <select id="reg-dept">
                        <option value="CSE" selected>CSE - Computer Science & Engg</option>
                        <option value="CSIT">CSIT - Computer Science & Info Tech</option>
                        <option value="CSE(AI & ML)">CSE (AI & Machine Learning)</option>
                        <option value="CSE(IOT & CS)">CSE (IoT & Cyber Security)</option>
                        <option value="ECE">ECE - Electronics & Comm</option>
                        <option value="ECS">ECS - Electronics & Computer Sci</option>
                        <option value="ME">ME - Mechanical Engineering</option>
                        <option value="RA">RA - Robotics & Automation</option>
                        <option value="ASH">ASH - Applied Sciences & Humanities</option>
                    </select>
                </div>
                <div class="reg-field">
                    <label for="reg-sem">📅 SEMESTER</label>
                    <select id="reg-sem">
                        <option value="1">Semester 1 (1st Year)</option>
                        <option value="2">Semester 2 (1st Year)</option>
                        <option value="3">Semester 3 (2nd Year)</option>
                        <option value="4" selected>Semester 4 (2nd Year)</option>
                        <option value="5">Semester 5 (3rd Year)</option>
                        <option value="6">Semester 6 (3rd Year)</option>
                        <option value="7">Semester 7 (4th Year)</option>
                        <option value="8">Semester 8 (4th Year)</option>
                    </select>
                </div>
            </div>

            <div class="reg-col reg-roster-col">
                <div id="reg-roster-preview" class="reg-roster-box">
                    <!-- Filled dynamically by updateRosterPreview() -->
                </div>
                <button class="btn-start-mission" id="btn-start-game">
                    <span>🚀 START BUNK MISSION</span>
                </button>
            </div>
        </div>
    </div>
</div>

<script>
// ==============================================================================
// 📦 CONFIG & ENGINE INITIALIZATION
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

// Audio Synthesis (Web Audio API)
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
// 📱 SCREEN AUTO-ROTATION (Automatic Horizontal, No Popups / No Asking)
// ==============================================================================
const gameContainer = document.getElementById("game-container");

function updateOrientation() {{
    if (!gameContainer) return;
    const isPortrait = window.innerHeight > window.innerWidth;
    if (isPortrait) {{
        gameContainer.classList.add("mode-portrait");
        gameContainer.classList.remove("mode-landscape");
    }} else {{
        gameContainer.classList.add("mode-landscape");
        gameContainer.classList.remove("mode-portrait");
    }}
}}
window.addEventListener("resize", updateOrientation);
window.addEventListener("orientationchange", updateOrientation);
updateOrientation();

// Apply college Snapchat background to #game-container with cyber vignette
if (CONFIG.background) {{
    gameContainer.style.backgroundImage = `radial-gradient(circle at center, rgba(6, 9, 17, 0.68) 0%, rgba(6, 9, 17, 0.94) 100%), url("${{CONFIG.background}}")`;
    gameContainer.style.backgroundPosition = "center center";
    gameContainer.style.backgroundSize = "cover";
    gameContainer.style.backgroundRepeat = "no-repeat";
}}

// ==============================================================================
// 👑 UPPER RIGHT CORNER & SETTINGS MODAL (Pause in one, Settings in other)
// ==============================================================================
const btnPause = document.getElementById("btn-pause");
const btnSettings = document.getElementById("btn-settings");
const settingsModal = document.getElementById("settings-modal");
const modalSound = document.getElementById("modal-sound");
const soundIcon = document.getElementById("sound-icon");
const soundText = document.getElementById("sound-text");
const modalRestart = document.getElementById("modal-restart");
const modalProfile = document.getElementById("modal-profile");
const modalClose = document.getElementById("modal-close");

// Registration Modal Elements
const regModal = document.getElementById("registration-modal");
const regNameInput = document.getElementById("reg-name");
const regRollInput = document.getElementById("reg-roll");
const regDeptSelect = document.getElementById("reg-dept");
const regSemSelect = document.getElementById("reg-sem");
const btnStartGame = document.getElementById("btn-start-game");

function updateRosterPreview() {{
    if (!regDeptSelect || !regSemSelect) return;
    const dept = regDeptSelect.value;
    const sem = parseInt(regSemSelect.value, 10);
    let hodName = "";
    let teachers = [];
    let notice = "";

    if (sem === 1 || sem === 2) {{
        hodName = "Pooja Sharma (ASH HOD)";
        teachers = (CONFIG.faculty_roster && CONFIG.faculty_roster["ASH"]) ? CONFIG.faculty_roster["ASH"].teachers : ["Vaishali Dixit", "Ashok Kumar", "Pooja Jain"];
        notice = "⚡ 1st Year: Common Applied Sciences Wing under Pooja Sharma (HOD)!";
    }} else {{
        const d = (CONFIG.faculty_roster && CONFIG.faculty_roster[dept]) ? CONFIG.faculty_roster[dept] : CONFIG.faculty_roster["CSE"];
        hodName = d.hod;
        teachers = d.teachers;
        notice = `⚡ Core Branch: Patrolled by ${{dept}} Department Faculty!`;
    }}

    const previewEl = document.getElementById("reg-roster-preview");
    if (previewEl) {{
        previewEl.innerHTML = `
            <div style="font-weight: 800; color: #ffd700; font-size: 0.82rem; letter-spacing: 0.5px;">🚨 CAMPUS HUNTER DEPLOYMENT</div>
            <div style="font-size: 0.72rem; color: #a5b4fc; margin-bottom: 2px;">${{notice}}</div>
            <div style="color: #ff6b81; font-size: 0.78rem;"><strong>👑 HOD:</strong> <span style="color:#fff;">${{hodName}}</span></div>
            <div style="color: #00e5ff; font-size: 0.78rem;"><strong>📚 Faculty:</strong> <span style="color:#fff;">${{teachers.join(", ")}}</span></div>
            <div style="color: #f1c40f; font-size: 0.74rem;"><strong>🛡️ Gates:</strong> Campus Security & Sonu Bouncer | <strong>Boss:</strong> Principal Isha Malhotra</div>
        `;
    }}
}}

if (regDeptSelect) regDeptSelect.addEventListener("change", updateRosterPreview);
if (regSemSelect) regSemSelect.addEventListener("change", updateRosterPreview);
updateRosterPreview();

// Ensure clean empty fields on startup (no autofill)
if (regNameInput) regNameInput.value = "";
if (regRollInput) regRollInput.value = "";

function openRegistrationModal() {{
    gameState = "REGISTRATION";
    btnPause.innerText = "▶️";
    if (regNameInput) regNameInput.value = (CONFIG.student_name && CONFIG.student_name !== "Student") ? CONFIG.student_name : "";
    if (regRollInput) regRollInput.value = (CONFIG.student_roll && CONFIG.student_roll !== "Roll 01") ? CONFIG.student_roll : "";
    if (regDeptSelect) regDeptSelect.value = CONFIG.student_dept;
    if (regSemSelect) regSemSelect.value = CONFIG.student_sem;
    updateRosterPreview();
    if (regModal) regModal.style.display = "flex";
}}

if (btnStartGame) {{
    const startAction = (e) => {{
        if (e) {{ e.preventDefault(); e.stopPropagation(); }}
        initAudio();
        const enteredName = (regNameInput && regNameInput.value.trim()) ? regNameInput.value.trim() : "Student";
        const enteredRoll = (regRollInput && regRollInput.value.trim()) ? regRollInput.value.trim() : "Roll 01";
        const enteredDept = regDeptSelect ? regDeptSelect.value : "CSE";
        const enteredSem = regSemSelect ? parseInt(regSemSelect.value, 10) : 4;

        CONFIG.student_name = enteredName;
        CONFIG.student_roll = enteredRoll;
        CONFIG.student_dept = enteredDept;
        CONFIG.student_sem = enteredSem;

        studentAvatar = createStudentAvatar(CONFIG.student_name, 28);
        currentLevel = 0;
        lives = 3;
        totalScore = 0;
        gameStartTime = Date.now();
        levelStartTime = Date.now();
        initLevel(0);

        if (regModal) regModal.style.display = "none";
        gameState = "PLAYING";
        btnPause.innerText = "⏸️";

        // Attempt mobile fullscreen and landscape orientation lock upon game start
        try {{
            if (document.documentElement.requestFullscreen) {{
                document.documentElement.requestFullscreen().then(() => {{
                    if (screen.orientation && screen.orientation.lock) {{
                        screen.orientation.lock("landscape").catch(() => {{}});
                    }}
                }}).catch(() => {{}});
            }}
        }} catch(err) {{}}
    }};
    btnStartGame.addEventListener("click", startAction);
    btnStartGame.addEventListener("touchend", startAction);
}}

const handleEnter = (e) => {{
    if (e.key === "Enter") {{
        e.preventDefault();
        if (btnStartGame) btnStartGame.click();
    }}
}};
if (regNameInput) regNameInput.addEventListener("keydown", handleEnter);
if (regRollInput) regRollInput.addEventListener("keydown", handleEnter);

btnPause.addEventListener("click", () => {{
    initAudio();
    if (gameState === "PLAYING") {{
        gameState = "PAUSED";
        btnPause.innerText = "▶️";
    }} else if (gameState === "PAUSED") {{
        gameState = "PLAYING";
        btnPause.innerText = "⏸️";
    }}
}});

btnSettings.addEventListener("click", () => {{
    initAudio();
    if (gameState === "PLAYING") {{
        gameState = "PAUSED";
        btnPause.innerText = "▶️";
    }}
    settingsModal.style.display = "flex";
}});

modalSound.addEventListener("click", () => {{
    soundEnabled = !soundEnabled;
    if (soundEnabled) {{
        modalSound.classList.remove("muted");
        soundIcon.innerText = "🔊";
        soundText.innerText = "SOUND: ON";
    }} else {{
        modalSound.classList.add("muted");
        soundIcon.innerText = "🔇";
        soundText.innerText = "SOUND: OFF";
    }}
}});

modalRestart.addEventListener("click", () => {{
    settingsModal.style.display = "none";
    retryLevel();
    btnPause.innerText = "⏸️";
}});

if (modalProfile) {{
    modalProfile.addEventListener("click", () => {{
        settingsModal.style.display = "none";
        openRegistrationModal();
    }});
}}

modalClose.addEventListener("click", () => {{
    settingsModal.style.display = "none";
    gameState = "PLAYING";
    btnPause.innerText = "⏸️";
}});

// ==============================================================================
// 🖼️ FACULTY PHOTO ASSETS & HIGH-RES AVATAR SYSTEM
// ==============================================================================
const loadedImages = {{}};
const photoEntries = Object.entries(CONFIG.photos || {{}});
let loadedPhotosCount = 0;

function preloadAllPhotos(onDone) {{
    if (photoEntries.length === 0) {{
        if (onDone) onDone();
        return;
    }}
    let doneCalled = false;
    const finish = () => {{
        if (!doneCalled) {{
            doneCalled = true;
            if (onDone) onDone();
        }}
    }};
    // Maximum 800ms wait
    const timer = setTimeout(finish, 800);

    photoEntries.forEach(([key, uri]) => {{
        const img = new Image();
        img.onload = img.onerror = () => {{
            loadedPhotosCount++;
            if (loadedPhotosCount >= photoEntries.length) {{
                clearTimeout(timer);
                finish();
            }}
        }};
        img.src = uri;
        loadedImages[key.toLowerCase()] = img;
    }});
}}

// College Snapchat Game Background Loader
const bgImg = new Image();
let bgImgLoaded = false;
if (CONFIG.background) {{
    bgImg.onload = () => {{ bgImgLoaded = true; }};
    bgImg.src = CONFIG.background;
}}

function getPhotoForName(name) {{
    if (!name) return null;
    let norm = name.toLowerCase();
    for (const clean of ['(hod)', '(principal)', 'principal', 'hod', 'faculty', 'guard', 'campus']) {{
        norm = norm.replace(clean, '');
    }}
    norm = norm.trim();

    // 1. Direct match in photo_map
    const mapped = CONFIG.photo_map[norm];
    if (mapped && loadedImages[mapped.toLowerCase()]) {{
        return loadedImages[mapped.toLowerCase()];
    }}

    // 2. Direct key in loadedImages
    const jpegName = norm + ".jpeg";
    if (loadedImages[jpegName]) {{
        return loadedImages[jpegName];
    }}
    const jpgName = norm + ".jpg";
    if (loadedImages[jpgName]) {{
        return loadedImages[jpgName];
    }}

    // Special checks for security and bouncer
    if (norm.includes("security") && loadedImages["security.jpeg"]) {{
        return loadedImages["security.jpeg"];
    }}
    if ((norm.includes("bouncer") || norm.includes("sonu") || norm.includes("counu")) && loadedImages["sonu_bouncer.jpeg"]) {{
        return loadedImages["sonu_bouncer.jpeg"];
    }}

    // 3. Substring matching
    for (const k of Object.keys(loadedImages)) {{
        const base = k.replace(/\\.(jpeg|jpg|png)$/i, '');
        if (base === norm || base.includes(norm) || norm.includes(base)) {{
            return loadedImages[k];
        }}
    }}
    return null;
}}

function createHunterAvatar(name, size=30) {{
    const off = document.createElement("canvas");
    off.width = size + 6;
    off.height = size + 6;
    const octx = off.getContext("2d");
    const center = off.width / 2;
    const radius = size / 2;

    const img = getPhotoForName(name);
    let borderCol = COLOR_CYAN;
    let fallbackBg = "#1a2a44";
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
    }} else if (norm.includes("bouncer") || norm.includes("sonu") || norm.includes("counu")) {{
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

    let hasPhoto = false;
    if (img && img.complete && img.naturalWidth > 0) {{
        octx.drawImage(img, center - radius, center - radius, size, size);
        hasPhoto = true;
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

    // Glowing outer ring
    octx.beginPath();
    octx.arc(center, center, radius, 0, Math.PI * 2);
    octx.lineWidth = 2.5;
    octx.strokeStyle = borderCol;
    octx.shadowColor = borderCol;
    octx.shadowBlur = 6;
    octx.stroke();

    off.hasPhoto = hasPhoto;
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

    octx.beginPath();
    octx.arc(center, center, radius, 0, Math.PI * 2);
    octx.fillStyle = "#0f1e36";
    octx.fill();

    octx.beginPath();
    octx.arc(center, center, radius - 2, 0, Math.PI * 2);
    octx.fillStyle = "#163c6e";
    octx.fill();

    octx.fillStyle = COLOR_CYAN;
    octx.font = "bold " + Math.floor(size * 0.45) + "px sans-serif";
    octx.textAlign = "center";
    octx.textBaseline = "middle";
    octx.fillText(inits, center, center);

    octx.beginPath();
    octx.arc(center, center, radius, 0, Math.PI * 2);
    octx.lineWidth = 2;
    octx.strokeStyle = COLOR_CYAN;
    octx.stroke();

    return off;
}}

// ==============================================================================
// 📐 CORNER TURN ASSIST COLLISION ENGINE
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
            avatar: createHunterAvatar(name, 30)
        }};
    }});
}}

// ==============================================================================
// 🏃 GAME STATE
// ==============================================================================
let currentLevel = 0;
let lives = 3;
let totalScore = 0;
let gameState = "REGISTRATION"; // REGISTRATION on startup, PLAYING, PAUSED, LEVEL_CLEAR, GAME_OVER, VICTORY
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
let bannerTimer = 1.0;

let caughtByTeacher = "Faculty";
let winData = null;

let studentAvatar = createStudentAvatar(CONFIG.student_name, 28);

function initLevel(lvlIdx) {{
    const lvl = CONFIG.levels[lvlIdx];
    const [spx, spy] = gridToPixel(1, 1);
    px = spx;
    py = spy;
    boostTimer = 0;
    invulnerableTimer = 1.8;
    facingDir = "right";
    bannerTimer = 1.0;
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

// Preload faculty photo assets and dynamically upgrade guard avatars once decoded
preloadAllPhotos(() => {{
    if (guards && guards.length > 0) {{
        guards.forEach(g => {{
            g.avatar = createHunterAvatar(g.name, 30);
        }});
    }}
}});

// Keyboard bindings
const keys = {{}};
window.addEventListener("keydown", (e) => {{
    if (e.target && (e.target.tagName === "INPUT" || e.target.tagName === "SELECT")) {{
        return;
    }}
    initAudio();
    keys[e.key.toLowerCase()] = true;
    if (e.key === "p" || e.key === "P" || e.key === "Escape") {{
        if (gameState === "PLAYING") {{
            gameState = "PAUSED";
            btnPause.innerText = "▶️";
        }} else if (gameState === "PAUSED") {{
            gameState = "PLAYING";
            btnPause.innerText = "⏸️";
        }}
    }}
    if (e.key === "m" || e.key === "M") {{
        soundEnabled = !soundEnabled;
        if (soundEnabled) {{
            modalSound.classList.remove("muted");
            soundIcon.innerText = "🔊";
            soundText.innerText = "SOUND: ON";
        }} else {{
            modalSound.classList.add("muted");
            soundIcon.innerText = "🔇";
            soundText.innerText = "SOUND: OFF";
        }}
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

// Touch controls bindings with multi-touch & slide off protection
function bindTouch(btnId, keyName) {{
    const el = document.getElementById(btnId);
    if (!el) return;
    const start = (e) => {{ e.preventDefault(); e.stopPropagation(); initAudio(); keys[keyName] = true; }};
    const end = (e) => {{ e.preventDefault(); e.stopPropagation(); keys[keyName] = false; }};
    el.addEventListener("mousedown", start);
    el.addEventListener("mouseup", end);
    el.addEventListener("mouseleave", end);
    el.addEventListener("touchstart", start, {{ passive: false }});
    el.addEventListener("touchend", end, {{ passive: false }});
    el.addEventListener("touchcancel", end, {{ passive: false }});
}}

bindTouch("k-up", "arrowup");
bindTouch("k-down", "arrowdown");
bindTouch("k-left", "arrowleft");
bindTouch("k-right", "arrowright");
bindTouch("k-sprint", "shift");

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
    openRegistrationModal();
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
            for (const d of desired) {{
                const [vx, vy] = dirMap[d];
                if (canMoveTo(g.x + vx * gSpeed, g.y + vy * gSpeed, g.radius, lvl.maze)) {{
                    g.x += vx * gSpeed;
                    g.y += vy * gSpeed;
                    g.dir = d;
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
// 🎨 RENDERING PIPELINE (Full Landscape Canvas)
// ==============================================================================
function render() {{
    const lvl = CONFIG.levels[currentLevel];

    // 1. College Snapchat Campus Game Background
    if (bgImg && (bgImgLoaded || (bgImg.complete && bgImg.naturalWidth > 0))) {{
        ctx.drawImage(bgImg, 0, HUD_HEIGHT, WIDTH, HEIGHT - HUD_HEIGHT);
        // Semi-transparent dark atmospheric cyber tint to keep maze walls & paths sharp
        ctx.fillStyle = "rgba(6, 9, 17, 0.72)";
        ctx.fillRect(0, HUD_HEIGHT, WIDTH, HEIGHT - HUD_HEIGHT);
    }} else {{
        ctx.fillStyle = "#090e1a";
        ctx.fillRect(0, 0, WIDTH, HEIGHT);
    }}

    // Grid lines
    ctx.strokeStyle = "rgba(18, 27, 47, 0.6)";
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

        // Dynamic Photo Upgrade: ensure real faculty photo renders on sprite
        if (!g.avatar || !g.avatar.hasPhoto) {{
            const photoImg = getPhotoForName(g.name);
            if (photoImg && photoImg.complete && photoImg.naturalWidth > 0) {{
                g.avatar = createHunterAvatar(g.name, 30);
            }}
        }}
        ctx.drawImage(g.avatar, g.x - g.avatar.width / 2, g.y - g.avatar.height / 2);

        // Guard Nameplate
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

    // Draw Player
    if (invulnerableTimer <= 0 || Math.floor(Date.now() / 100) % 2 === 0) {{
        if (boostTimer > 0) {{
            ctx.beginPath();
            ctx.arc(px, py, 16, 0, Math.PI * 2);
            ctx.strokeStyle = COLOR_CYAN;
            ctx.lineWidth = 2;
            ctx.stroke();
        }}
        ctx.drawImage(studentAvatar, px - studentAvatar.width / 2, py - studentAvatar.height / 2);

        const noseAng = dirMap[facingDir];
        const nx = px + Math.cos(noseAng) * 14;
        const ny = py + Math.sin(noseAng) * 14;
        ctx.beginPath();
        ctx.arc(nx, ny, 3, 0, Math.PI * 2);
        ctx.fillStyle = COLOR_WHITE;
        ctx.fill();

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

    // Floating Texts
    for (const ft of floatingTexts) {{
        ctx.fillStyle = ft.color;
        ctx.font = "bold 13px sans-serif";
        ctx.textAlign = "center";
        ctx.globalAlpha = ft.life;
        ctx.fillText(ft.text, ft.x, ft.y);
        ctx.globalAlpha = 1.0;
    }}

    // ==========================================================================
    // 👑 TOP HUD (Level, Lives, Timer, Score)
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

    // Lives & Info
    ctx.textAlign = "center";
    ctx.fillStyle = "#cbd5e1";
    ctx.font = "11px sans-serif";
    ctx.fillText(CONFIG.student_name + " (" + CONFIG.student_roll + ")", WIDTH / 2 - 30, 18);

    const hearts = "❤️ ".repeat(lives) + "🖤 ".repeat(Math.max(0, 3 - lives));
    ctx.fillStyle = COLOR_RED;
    ctx.font = "14px sans-serif";
    ctx.fillText("LIVES: " + hearts, WIDTH / 2 - 30, 38);

    if (boostTimer > 0) {{
        ctx.fillStyle = COLOR_CYAN;
        ctx.font = "bold 11px sans-serif";
        ctx.fillText("⚡ SPRINT READY! [HOLD SPRINT] (" + boostTimer.toFixed(1) + "s)", WIDTH / 2 - 30, 54);
    }}

    // Timer & Score
    ctx.textAlign = "right";
    const elapsed = Math.round((Date.now() - levelStartTime) / 100) / 10;
    ctx.fillStyle = COLOR_GOLD;
    ctx.font = "bold 14px sans-serif";
    ctx.fillText("⏱️ " + elapsed.toFixed(1) + "s", WIDTH - 120, 24);
    ctx.fillText("⭐ " + totalScore + " PTS", WIDTH - 120, 44);

    // Intro Splash Banner
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

    // In-game Modals (Pause, Clear, Game Over, Level 5 Victory)
    if (gameState === "PAUSED") {{
        drawModalCard("GAME PAUSED", [
            "Game is paused.",
            "Tap [⚙️] in upper right to toggle Sound or Restart.",
            "Tap [▶️] to resume."
        ], COLOR_GOLD);
    }} else if (gameState === "LEVEL_CLEAR" && winData) {{
        drawModalCard("🎉 LEVEL " + winData.level + " CLEARED! 🎉", [
            "Ground Path Reached, " + CONFIG.student_name + "!",
            "Time Taken: " + winData.time + "s  |  Bonus: +" + winData.bonus + " PTS",
            "Items Collected: " + winData.itemsCollected + " / " + winData.itemsTotal,
            "Total Score: " + totalScore + " PTS",
            "",
            "➔ TAP SCREEN TO ADVANCE TO NEXT LEVEL"
        ], COLOR_GREEN, () => nextLevel());
    }} else if (gameState === "GAME_OVER") {{
        drawModalCard("BUSTED! ZERO ATTENDANCE 🎓❌", [
            "Caught by " + caughtByTeacher + "!",
            "Final Score: " + totalScore + " PTS",
            "",
            "➔ TAP SCREEN TO RETRY LEVEL"
        ], COLOR_RED, () => retryLevel(), caughtByTeacher);
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
            "➔ TAP SCREEN TO PLAY AGAIN ↻"
        ], COLOR_GOLD, () => resetGame(), CONFIG.principal_name);
    }}
}}

function drawModalCard(title, lines, borderColor, onClickHandler=null, featuredTeacher=null) {{
    ctx.fillStyle = "rgba(6, 9, 17, 0.94)";
    ctx.fillRect(0, 0, WIDTH, HEIGHT);

    const cardW = 620;
    const cardH = 390;
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
    ctx.fillText(title, WIDTH / 2, cardY + 36);

    let textStartY = cardY + 95;

    // Featured Faculty Photo Badge (e.g. Caught by Teacher or Principal Boss)
    if (featuredTeacher) {{
        const featImg = getPhotoForName(featuredTeacher);
        if (featImg && featImg.complete && featImg.naturalWidth > 0) {{
            const pSize = 64;
            const pxCenter = WIDTH / 2;
            const pyCenter = cardY + 76;

            ctx.save();
            ctx.beginPath();
            ctx.arc(pxCenter, pyCenter, pSize / 2, 0, Math.PI * 2);
            ctx.clip();
            ctx.drawImage(featImg, pxCenter - pSize / 2, pyCenter - pSize / 2, pSize, pSize);
            ctx.restore();

            // Glow border around photo
            ctx.beginPath();
            ctx.arc(pxCenter, pyCenter, pSize / 2, 0, Math.PI * 2);
            ctx.lineWidth = 3;
            ctx.strokeStyle = borderColor;
            ctx.shadowColor = borderColor;
            ctx.shadowBlur = 8;
            ctx.stroke();

            textStartY = pyCenter + pSize / 2 + 24;
        }}
    }}

    ctx.font = "14px sans-serif";
    for (let i = 0; i < lines.length; i++) {{
        const line = lines[i];
        if (line.includes("UPCOMING LEVELS")) {{
            ctx.fillStyle = COLOR_CYAN;
            ctx.font = "bold 16px sans-serif";
        }} else if (line.includes("TAP SCREEN")) {{
            ctx.fillStyle = COLOR_GOLD;
            ctx.font = "bold 15px sans-serif";
        }} else {{
            ctx.fillStyle = COLOR_WHITE;
            ctx.font = "14px sans-serif";
        }}
        ctx.fillText(line, WIDTH / 2, textStartY + i * 26);
    }}

    if (onClickHandler) {{
        const trigger = () => {{
            canvas.onclick = null;
            canvas.ontouchend = null;
            onClickHandler();
        }};
        canvas.onclick = trigger;
        canvas.ontouchend = (e) => {{
            e.preventDefault();
            trigger();
        }};
    }}
}}
</script>
</body>
</html>
"""

# Render the edge-to-edge fullscreen web application
components.html(game_html, height=850, scrolling=False)
