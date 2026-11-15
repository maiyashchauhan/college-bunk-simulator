import pygame
import random
import sys
import time
import math
import os
import io
import wave
import struct

# ==============================================================================
# 🎮 COLLEGE BUNK SIMULATOR - BIG LEVEL & MULTI-DEPARTMENT EDITION
# ==============================================================================

# ---------- Window & Grid Settings ----------
WIDTH, HEIGHT = 900, 630
HUD_HEIGHT = 60
TILE = 30
ROWS = (HEIGHT - HUD_HEIGHT) // TILE  # exactly 19 rows
COLS = WIDTH // TILE                  # exactly 30 columns
FPS = 60

# ---------- Colors & Aesthetics ----------
BLACK       = (10, 12, 16)
WHITE       = (255, 255, 255)
GOLD        = (255, 205, 40)
YELLOW      = (255, 235, 75)
CYAN        = (0, 230, 255)
GREEN       = (46, 213, 115)
RED         = (255, 71, 87)
ORANGE      = (255, 127, 80)
PURPLE      = (165, 94, 234)
DARK_BLUE   = (20, 28, 48)
HUD_BG      = (15, 20, 32)
HUD_BORDER  = (40, 55, 85)

# Initialize Pygame & Mixer
pygame.init()
pygame.font.init()
try:
    pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
    mixer_available = True
except Exception:
    mixer_available = False

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("College Bunk Simulator - Faculty Photo Edition")
clock = pygame.time.Clock()

# Fonts
FONT_TINY   = pygame.font.Font(None, 19)
FONT_SMALL  = pygame.font.Font(None, 23)
FONT_MED    = pygame.font.Font(None, 28)
FONT_BIG    = pygame.font.Font(None, 40)
FONT_TITLE  = pygame.font.Font(None, 52)

# ---------- Procedural Sound Generator ----------
sound_enabled = True

def generate_tone(freqs, duration=0.2, volume=0.4, waveform="sine"):
    if not mixer_available:
        return None
    try:
        sample_rate = 22050
        total_samples = int(duration * sample_rate)
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sample_rate)
            samples = []
            for i in range(total_samples):
                t = i / sample_rate
                env = 1.0
                attack = int(0.015 * sample_rate)
                decay = int(0.05 * sample_rate)
                if i < attack:
                    env = i / attack
                elif i > total_samples - decay:
                    env = max(0.0, (total_samples - i) / decay)

                val = 0.0
                for f in freqs:
                    phase = 2 * math.pi * f * t
                    if waveform == "sine":
                        val += math.sin(phase)
                    elif waveform == "square":
                        val += 0.6 if math.sin(phase) > 0 else -0.6
                val = (val / len(freqs)) * 32767 * volume * env
                samples.append(int(max(-32767, min(32767, val))))
            w.writeframes(struct.pack(f'<{len(samples)}h', *samples))
        buf.seek(0)
        return pygame.mixer.Sound(buf)
    except Exception:
        return None

# In-game audio cues
snd_pickup = generate_tone([523, 659, 784, 1046], duration=0.22, volume=0.4)
snd_caught = generate_tone([240, 160], duration=0.35, volume=0.5, waveform="square")
snd_alert  = generate_tone([880, 1200], duration=0.18, volume=0.35)
snd_win    = generate_tone([523, 659, 784, 1046, 1318], duration=0.45, volume=0.45)
snd_boost  = generate_tone([440, 587, 880], duration=0.25, volume=0.4)

def play_sound(snd):
    if sound_enabled and snd and mixer_available:
        try:
            snd.play()
        except Exception:
            pass

# ---------- Image Loading & Background ----------
COLLEGE_BG_PATH = "college_bg.jpg"

def safe_load_image(filepath, size=None):
    candidates = [
        filepath,
        os.path.basename(filepath),
        os.path.join(".", os.path.basename(filepath)),
        os.path.join("assets", os.path.basename(filepath))
    ]
    for path in candidates:
        try:
            img = pygame.image.load(path)
            if size:
                img = pygame.transform.scale(img, size)
            return img
        except Exception:
            pass
    return None

def load_college_background():
    for bg_file in ["Snapchat-893693281.jpg", COLLEGE_BG_PATH, "college_bg.jpg"]:
        img = safe_load_image(bg_file, (WIDTH, HEIGHT))
        if img:
            # Apply dark atmospheric cyber tint so maze corridors stay 100% visible
            tint = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            tint.fill((8, 12, 22, 175))
            img.blit(tint, (0, 0))
            return img
    fallback = pygame.Surface((WIDTH, HEIGHT))
    fallback.fill((22, 28, 42))
    for x in range(0, WIDTH, 40):
        pygame.draw.line(fallback, (30, 38, 56), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(fallback, (30, 38, 56), (0, y), (WIDTH, y))
    return fallback

background = load_college_background()

# ---------- Circular Avatar Generator ----------
def create_circular_avatar(img_surface, size=26, border_color=(0, 230, 255), border_width=2, fallback_initial="P", fallback_bg=(50, 60, 80)):
    total_size = size + border_width * 2
    avatar = pygame.Surface((total_size, total_size), pygame.SRCALPHA)

    if img_surface:
        scaled = pygame.transform.smoothscale(img_surface, (size, size))
        mask_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(mask_surf, (255, 255, 255, 255), (size // 2, size // 2), size // 2)
        masked_img = pygame.Surface((size, size), pygame.SRCALPHA)
        masked_img.blit(scaled, (0, 0))
        masked_img.blit(mask_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        avatar.blit(masked_img, (border_width, border_width))
    else:
        pygame.draw.circle(avatar, fallback_bg, (total_size // 2, total_size // 2), size // 2)
        init_txt = FONT_TINY.render(fallback_initial[:2], True, WHITE)
        avatar.blit(init_txt, (total_size // 2 - init_txt.get_width() // 2, total_size // 2 - init_txt.get_height() // 2))

    pygame.draw.circle(avatar, border_color, (total_size // 2, total_size // 2), size // 2 + border_width - 1, border_width)
    return avatar

# ---------- Photo Resolution & Cache for All Faculty & Roles ----------
PHOTO_MAP = {
    'bouncer': ['SONU_BOUNCER.jpeg', 'sonu_bouncer.jpeg', 'bouncer.jpeg', 'bouncer.jpg'],
    'sonu bouncer': ['SONU_BOUNCER.jpeg', 'sonu_bouncer.jpeg'],
    'campus bouncer': ['SONU_BOUNCER.jpeg', 'sonu_bouncer.jpeg'],
    'counu bouncer': ['SONU_BOUNCER.jpeg', 'sonu_bouncer.jpeg'],
    'security': ['SECURITY.jpeg', 'security.jpeg', 'security.jpg'],
    'security guard': ['SECURITY.jpeg', 'security.jpeg', 'security.jpg'],
    'isha malhotra': ['isha malhotra.jpeg'],
    'pooja sharma': ['pooja sharma.jpeg', 'hod_pooja.jpeg'],
    'vaishali dixit': ['vaishali dixit.jpeg'],
    'ashok kumar': ['ashok kumar.jpeg'],
    'pooja jain': ['pooja jain.jpeg'],
    'ashima mehta': ['ashima mehta.jpeg'],
    'hansraj yadav': ['hansraj yadav.jpeg'],
    'manoj kumar': ['manoj kumar.jpeg'],
    'vimmi malhotra': ['vimmi malhotra.jpeg'],
    'ashwani kumar': ['aswani kumar.jpeg', 'ashwani kumar.jpeg'],
    'aswani kumar': ['aswani kumar.jpeg'],
    'yashwardhan soni': ['yashwardhan soni.jpeg'],
    'yashvardhan soni': ['yashwardhan soni.jpeg'],
    'anita choudhary': ['anita chaudhary.jpeg', 'anita choudhary.jpeg'],
    'anita chaudhary': ['anita chaudhary.jpeg'],
    'sarita': ['sarita.jpeg'],
    'naveen rathi': ['naveen rathi.jpeg'],
    'monika rani': ['monika rani.jpeg'],
    'amninder kaur': ['amninder kaur.jpeg'],
    'neha mathur': ['neha mathur.jpeg'],
    'neha chauhan': ['neha chauhan.jpeg'],
    'rajesh mattoo': ['rajesh mattoo.jpeg'],
    'ankit aggarwal': ['ankit aggarwal.jpeg'],
    'yudhveer kumar verma': ['yudhveer kumar verma.jpeg']
}

def load_photo_for_name(name):
    norm = name.lower()
    for clean in ['(hod)', '(principal)', 'principal', 'hod']:
        norm = norm.replace(clean, '')
    norm = norm.strip()

    candidates = PHOTO_MAP.get(norm, [f"{norm}.jpeg", f"{norm}.jpg", f"{norm}.png"])
    for c in candidates:
        img = safe_load_image(c)
        if img:
            return img
    # Search directory for partial match
    try:
        for f in os.listdir('.'):
            if f.lower().endswith(('.jpeg', '.jpg', '.png')):
                base = os.path.splitext(f.lower())[0]
                if base in norm or norm in base:
                    img = safe_load_image(f)
                    if img:
                        return img
    except Exception:
        pass
    return None

avatar_cache = {}

def get_hunter_avatar(name, role="Faculty", size=26):
    cache_key = f"{name}_{size}"
    if cache_key in avatar_cache:
        return avatar_cache[cache_key]

    raw_img = load_photo_for_name(name)
    norm = name.lower()

    if "principal" in norm or "isha malhotra" in norm:
        border_col = GOLD
        bg_col = (180, 140, 20)
        inits = "IM"
    elif "hod" in norm or "(hod)" in norm:
        border_col = RED
        bg_col = (160, 30, 45)
        inits = "".join([p[0] for p in name.replace("(", " ").split() if p[0].isalpha()][:2]).upper()
    elif "security" in norm:
        border_col = YELLOW
        bg_col = (50, 80, 130)
        inits = "SC"
    elif "bouncer" in norm:
        border_col = ORANGE
        bg_col = (180, 80, 20)
        inits = "BC"
    else:
        palette = [CYAN, PURPLE, GREEN, ORANGE, YELLOW]
        border_col = palette[abs(hash(name)) % len(palette)]
        bg_col = (40, 50, 70)
        inits = "".join([p[0] for p in name.replace("(", " ").split() if p[0].isalpha()][:2]).upper()

    av = create_circular_avatar(raw_img, size=size, border_color=border_col, border_width=2, fallback_initial=inits, fallback_bg=bg_col)
    avatar_cache[cache_key] = av
    return av

# Universal dynamic student badge avatar (no static student photo)
def create_student_avatar(name="Student", size=26):
    parts = [p for p in name.replace("(", " ").replace(")", " ").split() if p and p[0].isalnum()]
    if len(parts) >= 2:
        inits = (parts[0][0] + parts[1][0]).upper()
    elif len(parts) == 1 and len(parts[0]) >= 2:
        inits = parts[0][:2].upper()
    elif len(parts) == 1:
        inits = parts[0][0].upper()
    else:
        inits = "ST"

    total_size = size + 4
    surf = pygame.Surface((total_size, total_size), pygame.SRCALPHA)
    center = total_size // 2

    # Circular background badge with dark-navy tone
    pygame.draw.circle(surf, (15, 30, 55), (center, center), size // 2)
    pygame.draw.circle(surf, (22, 60, 110), (center, center), size // 2 - 2)

    # Render dynamic student initials
    font_to_use = FONT_TINY if size <= 28 else FONT_SMALL
    txt = font_to_use.render(inits, True, CYAN)
    surf.blit(txt, (center - txt.get_width() // 2, center - txt.get_height() // 2))

    # Glowing Cyan student ring
    pygame.draw.circle(surf, CYAN, (center, center), size // 2 + 1, 2)
    return surf

player_avatar = create_student_avatar("Student", size=26)

# ==============================================================================
# 🏫 DEPARTMENTS, FACULTY ROSTER & PRINCIPAL RULES
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
        "hod": "Ashwani Kumar (HOD)",
        "teachers": ["Yashwardhan Soni", "Anita Choudhary", "Sarita"]
    },
    "CSE(AI & ML)": {
        "hod": "Yashwardhan Soni (HOD)",
        "teachers": ["Manoj Kumar", "Ashok Kumar", "Naveen Rathi"]
    },
    "CSE(IOT & CS)": {
        "hod": "Ashwani Kumar (HOD)",
        "teachers": ["Yashvardhan Soni", "Anita Choudhary", "Sarita"]
    },
    "ECE": {
        "hod": "Monika Rani (HOD)",
        "teachers": ["Amninder Kaur", "Neha Mathur", "Isha Malhotra (Principal)"]
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

# ==============================================================================
# 🗺️ 5 DISTINCT, HAND-CRAFTED & VERIFIED MAZE LEVELS (19 rows x 30 cols)
# ==============================================================================

LEVEL_DATA = [
    # ---------- LEVEL 1: GROUND FLOOR ----------
    {
        "num": 1,
        "name": "Ground Floor: Corridors of Doom",
        "desc": "Bell rang! Slip past the faculty hunters and sprint to the college GROUND!",
        "theme": {
            "wall_fill": (25, 38, 62),
            "wall_edge": (55, 95, 155),
            "wall_glow": (80, 140, 230)
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
            {"name": "Bunk Pass", "type": "score", "pts": 150, "pos": (13, 3), "icon": "P"},
            {"name": "Bunk Pass", "type": "score", "pts": 150, "pos": (7, 13), "icon": "P"}
        ]
    },

    # ---------- LEVEL 2: FIRST FLOOR ----------
    {
        "num": 2,
        "name": "First Floor: Science Lab Wing",
        "desc": "Faculty patrolling the science wing! Evade them and advance toward the GROUND!",
        "theme": {
            "wall_fill": (20, 50, 38),
            "wall_edge": (40, 110, 80),
            "wall_glow": (65, 185, 135)
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
            {"name": "Lab Manual", "type": "score", "pts": 200, "pos": (14, 3), "icon": "M"},
            {"name": "Lab Manual", "type": "score", "pts": 200, "pos": (9, 9), "icon": "M"},
            {"name": "Hot Coffee", "type": "boost", "pts": 100, "pos": (16, 15), "icon": "C"}
        ]
    },

    # ---------- LEVEL 3: SECOND FLOOR ----------
    {
        "num": 3,
        "name": "Second Floor: Central Library",
        "desc": "HOD and teachers checking bookshelf aisles! Navigate out toward the GROUND!",
        "theme": {
            "wall_fill": (58, 38, 20),
            "wall_edge": (130, 80, 35),
            "wall_glow": (220, 145, 60)
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
            {"name": "Hall Ticket", "type": "score", "pts": 250, "pos": (14, 5), "icon": "T"},
            {"name": "Hall Ticket", "type": "score", "pts": 250, "pos": (6, 15), "icon": "T"},
            {"name": "Sneakers", "type": "boost", "pts": 100, "pos": (24, 7), "icon": "S"}
        ]
    },

    # ---------- LEVEL 4: GROUNDS & CANTEEN ----------
    {
        "num": 4,
        "name": "Grounds: Canteen & Sports Complex",
        "desc": "Heavy faculty reinforcement! Weave around the canteen to break into the GROUND!",
        "theme": {
            "wall_fill": (60, 22, 28),
            "wall_edge": (140, 45, 55),
            "wall_glow": (240, 80, 95)
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
            {"name": "Canteen Samosa", "type": "score", "pts": 300, "pos": (14, 7), "icon": "S"},
            {"name": "Canteen Samosa", "type": "score", "pts": 300, "pos": (7, 15), "icon": "S"},
            {"name": "Energy Drink", "type": "boost", "pts": 150, "pos": (22, 7), "icon": "E"}
        ]
    },

    # ---------- LEVEL 5: THE GRAND MAIN GATE ----------
    {
        "num": 5,
        "name": "The Perimeter: The Grand Main Gate",
        "desc": "FINAL BOSS GAUNTLET! Principal Isha Malhotra & Faculty guard the gate! Break through to the GROUND!",
        "theme": {
            "wall_fill": (45, 25, 68),
            "wall_edge": (110, 60, 160),
            "wall_glow": (255, 215, 60)
        },
        "maze": [
            "111111111111111111111111111111",
            "100000000011000000110000000001",
            "101111110011011110110011111101",
            "101000010000010010000010000101",
            "101011011111010010111110110101",
            "100011000001000000100000110001",
            "111011111001110011100111110111",
            "100000001000010010000100000001",
            "101111001110010010011100111101",
            "100001000010000000010000100001",
            "101001110011110011110011100101",
            "101000010000000000000001000101",
            "111110010111111111110101001111",
            "100000000100000000010000000001",
            "101111110101111110101011111101",
            "101000000001000010000000000101",
            "101011111111011011111111110101",
            "100000000000000000000000000001",
            "111111111111111111111111111111"
        ],
        "items": [
            {"name": "Gate Pass", "type": "score", "pts": 500, "pos": (14, 5), "icon": "K"},
            {"name": "Gate Pass", "type": "score", "pts": 500, "pos": (4, 15), "icon": "K"},
            {"name": "Bunk Trophy", "type": "boost", "pts": 1000, "pos": (14, 11), "icon": "🏆"}
        ]
    }
]

# ---------- Helper Coordinates & Geometry ----------
def grid_to_pixel(gx, gy):
    return gx * TILE + TILE // 2, HUD_HEIGHT + gy * TILE + TILE // 2

def pixel_to_grid(px, py):
    return int(px // TILE), int((py - HUD_HEIGHT) // TILE)

def can_move_to(x, y, radius, maze_data):
    if x - radius < 0 or x + radius >= WIDTH:
        return False
    if y - radius < HUD_HEIGHT or y + radius >= HEIGHT:
        return False

    min_gx = max(0, int((x - radius) // TILE))
    max_gx = min(COLS - 1, int((x + radius) // TILE))
    min_gy = max(0, int(((y - radius) - HUD_HEIGHT) // TILE))
    max_gy = min(ROWS - 1, int(((y + radius) - HUD_HEIGHT) // TILE))

    for gy in range(min_gy, max_gy + 1):
        for gx in range(min_gx, max_gx + 1):
            if maze_data[gy][gx] == "1":
                tile_l = gx * TILE
                tile_r = (gx + 1) * TILE
                tile_t = HUD_HEIGHT + gy * TILE
                tile_b = HUD_HEIGHT + (gy + 1) * TILE

                closest_x = max(tile_l, min(x, tile_r))
                closest_y = max(tile_t, min(y, tile_b))

                if (x - closest_x)**2 + (y - closest_y)**2 < (radius * radius):
                    return False
    return True

def line_of_sight(x1, y1, x2, y2, maze_data, steps=12):
    for s in range(1, steps):
        t = s / steps
        tx = x1 + (x2 - x1) * t
        ty = y1 + (y2 - y1) * t
        gx, gy = pixel_to_grid(tx, ty)
        if 0 <= gx < COLS and 0 <= gy < ROWS:
            if maze_data[gy][gx] == "1":
                return False
        else:
            return False
    return True

def move_player(px, py, dx, dy, speed, radius, maze_data):
    if dx == 0 and dy == 0:
        return px, py

    if dx != 0 and dy != 0:
        step_x = dx * speed * 0.7071
        step_y = dy * speed * 0.7071
    else:
        step_x = dx * speed
        step_y = dy * speed

    # Corner Turn Assist & Corridor Alignment (thickens turns & prevents sticking)
    gx = int(px // TILE)
    gy = int((py - HUD_HEIGHT) // TILE)
    col_cx = gx * TILE + TILE // 2
    row_cy = HUD_HEIGHT + gy * TILE + TILE // 2

    # If turning/moving vertically: assist X corridor centering
    if step_y != 0 and step_x == 0:
        if not can_move_to(px, py + step_y, radius, maze_data):
            for test_gx in [gx, gx - 1, gx + 1]:
                if 0 <= test_gx < COLS:
                    tcx = test_gx * TILE + TILE // 2
                    if abs(tcx - px) <= 14:
                        nudge = math.copysign(min(abs(tcx - px), speed), tcx - px)
                        if can_move_to(px + nudge, py, radius, maze_data):
                            px += nudge
                            break
        else:
            diff_x = col_cx - px
            if 0.3 < abs(diff_x) <= 12.0:
                nudge = math.copysign(min(abs(diff_x), 1.5), diff_x)
                if can_move_to(px + nudge, py, radius, maze_data):
                    px += nudge

    # If turning/moving horizontally: assist Y corridor centering
    if step_x != 0 and step_y == 0:
        if not can_move_to(px + step_x, py, radius, maze_data):
            for test_gy in [gy, gy - 1, gy + 1]:
                if 0 <= test_gy < ROWS:
                    tcy = HUD_HEIGHT + test_gy * TILE + TILE // 2
                    if abs(tcy - py) <= 14:
                        nudge = math.copysign(min(abs(tcy - py), speed), tcy - py)
                        if can_move_to(px, py + nudge, radius, maze_data):
                            py += nudge
                            break
        else:
            diff_y = row_cy - py
            if 0.3 < abs(diff_y) <= 12.0:
                nudge = math.copysign(min(abs(diff_y), 1.5), diff_y)
                if can_move_to(px, py + nudge, radius, maze_data):
                    py += nudge

    # Apply final position with axis-independent sliding
    if can_move_to(px + step_x, py + step_y, radius, maze_data):
        px += step_x
        py += step_y
    else:
        if step_x != 0 and can_move_to(px + step_x, py, radius, maze_data):
            px += step_x
        if step_y != 0 and can_move_to(px, py + step_y, radius, maze_data):
            py += step_y

    return px, py

def draw_nameplate(surface, text, font, cx, cy, bg=(15, 20, 32, 225), border=(90, 110, 150), text_color=WHITE):
    txt_surf = font.render(text, True, text_color)
    pw = txt_surf.get_width() + 10
    ph = txt_surf.get_height() + 4
    pill = pygame.Surface((pw, ph), pygame.SRCALPHA)
    pygame.draw.rect(pill, bg, (0, 0, pw, ph), border_radius=6)
    pygame.draw.rect(pill, border, (0, 0, pw, ph), width=1, border_radius=6)
    rx = cx - pw // 2
    ry = cy - ph // 2
    surface.blit(pill, (rx, ry))
    surface.blit(txt_surf, (rx + 5, ry + 2))

# ==============================================================================
# 🎯 DYNAMIC GUARD ROSTER GENERATOR (WITH ALL 21 FACULTY PHOTOS)
# ==============================================================================

def get_level_guards(dept, sem, level_idx):
    guards = []
    level_speeds = [1.6, 1.74, 1.88, 2.02, 2.16]
    spd = level_speeds[level_idx]

    slots = [
        [(15, 9), (7, 5)],
        [(11, 7), (22, 13), (7, 13)],
        [(7, 5), (19, 7), (14, 13), (11, 11)],
        [(11, 5), (18, 5), (6, 11), (22, 13), (7, 9)],
        [(7, 5), (22, 5), (14, 9), (6, 13), (20, 15)]
    ]
    level_slots = slots[level_idx]

    if sem in (1, 2):
        # 1st & 2nd Semester: Basic faculty Pooja (HOD), Bouncer, Security
        if level_idx == 0:
            roster = [("SECURITY", "Security", spd)]
        elif level_idx == 1:
            roster = [("SECURITY", "Security", spd), ("BOUNCER", "Bouncer", spd + 0.08)]
        elif level_idx == 2:
            roster = [("SECURITY", "Security", spd), ("Pooja Sharma (HOD)", "HOD", spd + 0.1)]
        elif level_idx == 3:
            roster = [("SECURITY", "Security", spd), ("BOUNCER", "Bouncer", spd + 0.08), ("Pooja Sharma (HOD)", "HOD", spd + 0.12)]
        else:
            roster = [
                ("SECURITY", "Security", spd),
                ("BOUNCER", "Bouncer", spd + 0.08),
                ("Pooja Sharma (HOD)", "HOD", spd + 0.12),
                (PRINCIPAL_NAME, "Principal", spd + 0.18)
            ]
    else:
        # Semesters 3 to 8: Department specific faculty!
        dept_info = DEPARTMENT_FACULTY.get(dept, DEPARTMENT_FACULTY["CSE"])
        hod = dept_info["hod"]
        t1, t2, t3 = dept_info["teachers"][0], dept_info["teachers"][1], dept_info["teachers"][2]

        if level_idx == 0:
            roster = [("SECURITY", "Security", spd), (t1, "Faculty", spd + 0.06)]
        elif level_idx == 1:
            roster = [("SECURITY", "Security", spd), ("BOUNCER", "Bouncer", spd + 0.06), (t2, "Faculty", spd + 0.1)]
        elif level_idx == 2:
            roster = [("SECURITY", "Security", spd), ("BOUNCER", "Bouncer", spd + 0.06), (t3, "Faculty", spd + 0.1), (hod, "HOD", spd + 0.14)]
        elif level_idx == 3:
            roster = [("SECURITY", "Security", spd), ("BOUNCER", "Bouncer", spd + 0.06), (t1, "Faculty", spd + 0.1), (t2, "Faculty", spd + 0.12), (hod, "HOD", spd + 0.16)]
        else:
            roster = [
                ("SECURITY", "Security", spd),
                ("BOUNCER", "Bouncer", spd + 0.06),
                (hod, "HOD", spd + 0.14),
                (t3, "Faculty", spd + 0.12),
                (PRINCIPAL_NAME, "Principal", spd + 0.2)
            ]

    for i, (name, role, g_spd) in enumerate(roster):
        slot = level_slots[i % len(level_slots)]
        gx, gy = slot
        g_px, g_py = grid_to_pixel(gx, gy)
        guards.append({
            "name": name,
            "role": role,
            "avatar": get_hunter_avatar(name, role, size=26),
            "x": float(g_px),
            "y": float(g_py),
            "speed": g_spd,
            "dir": random.choice(["up", "down", "left", "right"]),
            "change_cd": random.randint(25, 60),
            "alert": False,
            "alert_timer": 0.0,
            "radius": 11,
            "start": (gx, gy)
        })

    return guards

# ==============================================================================
# 📋 INTERACTIVE STUDENT REGISTRATION SCREEN WITH LIVE PHOTO PREVIEWS
# ==============================================================================

def student_registration_screen():
    student_name = ""
    student_roll = ""
    active_field = "NAME"

    dept_idx = 1  # default "CSE"
    sem_idx = 3   # default "Sem 4"

    cursor_timer = 0.0

    card_w, card_h = 820, 580
    card_x = WIDTH // 2 - card_w // 2
    card_y = HEIGHT // 2 - card_h // 2

    name_box_rect = pygame.Rect(card_x + 50, card_y + 115, 340, 42)
    roll_box_rect = pygame.Rect(card_x + 430, card_y + 115, 340, 42)

    # Department buttons (2 rows)
    dept_rects = []
    r1_depts = DEPARTMENTS[:5]
    r1_w = [80, 80, 85, 150, 150]
    total_w1 = sum(r1_w) + (len(r1_w) - 1) * 10
    start_x1 = WIDTH // 2 - total_w1 // 2
    cur_x = start_x1
    for i, d in enumerate(r1_depts):
        rect = pygame.Rect(cur_x, card_y + 195, r1_w[i], 32)
        dept_rects.append((i, rect, d))
        cur_x += r1_w[i] + 10

    r2_depts = DEPARTMENTS[5:]
    r2_w = [90, 90, 90, 90]
    total_w2 = sum(r2_w) + (len(r2_w) - 1) * 14
    start_x2 = WIDTH // 2 - total_w2 // 2
    cur_x = start_x2
    for j, d in enumerate(r2_depts, 5):
        rect = pygame.Rect(cur_x, card_y + 235, 90, 32)
        dept_rects.append((j, rect, d))
        cur_x += 90 + 14

    # Semester buttons (8 in a row)
    sem_rects = []
    total_sem_w = 8 * 84 + 7 * 8
    sem_start_x = WIDTH // 2 - total_sem_w // 2
    for s_i, sem in enumerate(SEMESTERS):
        rect = pygame.Rect(sem_start_x + s_i * 92, card_y + 302, 84, 32)
        sem_rects.append((s_i, rect, f"Sem {sem}"))

    # Start button
    start_btn_rect = pygame.Rect(WIDTH // 2 - 180, card_y + 518, 360, 46)

    while True:
        dt = clock.tick(FPS) / 1000.0
        cursor_timer += dt
        mouse_pos = pygame.mouse.get_pos()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if name_box_rect.collidepoint(mouse_pos):
                    active_field = "NAME"
                elif roll_box_rect.collidepoint(mouse_pos):
                    active_field = "ROLL"
                for d_i, r, _ in dept_rects:
                    if r.collidepoint(mouse_pos):
                        dept_idx = d_i
                        play_sound(snd_pickup)
                for s_i, r, _ in sem_rects:
                    if r.collidepoint(mouse_pos):
                        sem_idx = s_i
                        play_sound(snd_pickup)
                if start_btn_rect.collidepoint(mouse_pos):
                    final_name = student_name.strip() if student_name.strip() else "Student"
                    final_roll = student_roll.strip() if student_roll.strip() else "Roll 01"
                    return (
                        final_name,
                        final_roll,
                        DEPARTMENTS[dept_idx],
                        SEMESTERS[sem_idx]
                    )

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    final_name = student_name.strip() if student_name.strip() else "Student"
                    final_roll = student_roll.strip() if student_roll.strip() else "Roll 01"
                    return (
                        final_name,
                        final_roll,
                        DEPARTMENTS[dept_idx],
                        SEMESTERS[sem_idx]
                    )
                elif e.key == pygame.K_TAB:
                    active_field = "ROLL" if active_field == "NAME" else "NAME"
                elif e.key == pygame.K_BACKSPACE:
                    if active_field == "NAME":
                        student_name = student_name[:-1]
                    else:
                        student_roll = student_roll[:-1]
                else:
                    if active_field == "NAME" and len(student_name) < 18 and (e.unicode.isalnum() or e.unicode in " _-"):
                        student_name += e.unicode
                    elif active_field == "ROLL" and len(student_roll) < 14 and (e.unicode.isalnum() or e.unicode in "_-"):
                        student_roll += e.unicode.upper()

        # Render background
        screen.blit(background, (0, 0))

        # Main modal card
        card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        pygame.draw.rect(card_surf, (15, 20, 32, 248), (0, 0, card_w, card_h), border_radius=18)
        pygame.draw.rect(card_surf, (0, 230, 255, 140), (0, 0, card_w, card_h), width=2, border_radius=18)
        screen.blit(card_surf, (card_x, card_y))

        # Title Header
        title = FONT_TITLE.render("COLLEGE BUNK SIMULATOR", True, GOLD)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, card_y + 16))

        sub = FONT_SMALL.render("Student Profile & Faculty Deployment System", True, CYAN)
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, card_y + 62))

        # Row 1: Student Name & Roll No
        lbl_name = FONT_SMALL.render("Student Name:", True, WHITE)
        screen.blit(lbl_name, (name_box_rect.x, card_y + 92))
        pygame.draw.rect(screen, (24, 32, 48), name_box_rect, border_radius=8)
        pygame.draw.rect(screen, CYAN if active_field == "NAME" else (60, 80, 110), name_box_rect, width=2, border_radius=8)
        cursor1 = "|" if active_field == "NAME" and int(cursor_timer * 2) % 2 == 0 else ""
        if student_name:
            txt1 = FONT_MED.render(student_name + cursor1, True, YELLOW)
            screen.blit(txt1, (name_box_rect.x + 12, name_box_rect.y + 10))
        else:
            ph1 = FONT_MED.render("Enter Student Name...", True, (105, 125, 155))
            screen.blit(ph1, (name_box_rect.x + 12, name_box_rect.y + 10))
            if active_field == "NAME" and cursor1:
                cur_s = FONT_MED.render(cursor1, True, CYAN)
                screen.blit(cur_s, (name_box_rect.x + 12, name_box_rect.y + 10))

        lbl_roll = FONT_SMALL.render("Roll Number:", True, WHITE)
        screen.blit(lbl_roll, (roll_box_rect.x, card_y + 92))
        pygame.draw.rect(screen, (24, 32, 48), roll_box_rect, border_radius=8)
        pygame.draw.rect(screen, CYAN if active_field == "ROLL" else (60, 80, 110), roll_box_rect, width=2, border_radius=8)
        cursor2 = "|" if active_field == "ROLL" and int(cursor_timer * 2) % 2 == 0 else ""
        if student_roll:
            txt2 = FONT_MED.render(student_roll + cursor2, True, YELLOW)
            screen.blit(txt2, (roll_box_rect.x + 12, roll_box_rect.y + 10))
        else:
            ph2 = FONT_MED.render("Enter Roll Number...", True, (105, 125, 155))
            screen.blit(ph2, (roll_box_rect.x + 12, roll_box_rect.y + 10))
            if active_field == "ROLL" and cursor2:
                cur_s2 = FONT_MED.render(cursor2, True, CYAN)
                screen.blit(cur_s2, (roll_box_rect.x + 12, roll_box_rect.y + 10))

        # Row 2: Department Selection
        lbl_dept = FONT_SMALL.render("Select Department (9 Academic Branches):", True, WHITE)
        screen.blit(lbl_dept, (card_x + 50, card_y + 172))
        for d_i, r, d_name in dept_rects:
            is_sel = (d_i == dept_idx)
            is_hov = r.collidepoint(mouse_pos)
            bg_col = (0, 120, 160) if is_sel else ((35, 45, 65) if is_hov else (22, 28, 42))
            border_col = CYAN if is_sel else ((100, 130, 170) if is_hov else (50, 65, 90))
            pygame.draw.rect(screen, bg_col, r, border_radius=6)
            pygame.draw.rect(screen, border_col, r, width=2 if is_sel else 1, border_radius=6)
            t_col = GOLD if is_sel else WHITE
            d_txt = FONT_TINY.render(d_name, True, t_col)
            screen.blit(d_txt, (r.centerx - d_txt.get_width() // 2, r.centery - d_txt.get_height() // 2))

        # Row 3: Semester Selection
        lbl_sem = FONT_SMALL.render("Select Semester (1 to 8):", True, WHITE)
        screen.blit(lbl_sem, (card_x + 50, card_y + 278))
        for s_i, r, s_name in sem_rects:
            is_sel = (s_i == sem_idx)
            is_hov = r.collidepoint(mouse_pos)
            bg_col = (40, 110, 60) if is_sel else ((35, 45, 65) if is_hov else (22, 28, 42))
            border_col = GREEN if is_sel else ((100, 130, 170) if is_hov else (50, 65, 90))
            pygame.draw.rect(screen, bg_col, r, border_radius=6)
            pygame.draw.rect(screen, border_col, r, width=2 if is_sel else 1, border_radius=6)
            t_col = GOLD if is_sel else WHITE
            s_txt = FONT_SMALL.render(s_name, True, t_col)
            screen.blit(s_txt, (r.centerx - s_txt.get_width() // 2, r.centery - s_txt.get_height() // 2))

        # Row 4: LIVE HUNTER ROSTER PREVIEW WITH ACTUAL TEACHER PHOTOS!
        cur_dept = DEPARTMENTS[dept_idx]
        cur_sem = SEMESTERS[sem_idx]
        preview_rect = pygame.Rect(card_x + 40, card_y + 350, card_w - 80, 150)
        pygame.draw.rect(screen, (20, 26, 40), preview_rect, border_radius=10)
        pygame.draw.rect(screen, (60, 80, 120), preview_rect, width=1, border_radius=10)

        badge_txt = FONT_MED.render(f"🎯 DEPLOYMENT: {cur_dept} • SEMESTER {cur_sem}  |  ACTIVE FACULTY HUNTERS:", True, GOLD)
        screen.blit(badge_txt, (preview_rect.x + 16, preview_rect.y + 10))

        # Get list of hunters for this branch and sem
        if cur_sem in (1, 2):
            active_hunters = ["Pooja Sharma (HOD)", "BOUNCER", "SECURITY", PRINCIPAL_NAME]
        else:
            d_data = DEPARTMENT_FACULTY[cur_dept]
            active_hunters = [d_data["hod"]] + d_data["teachers"] + ["BOUNCER", "SECURITY", PRINCIPAL_NAME]

        # Render row of actual circular photos!
        n_h = len(active_hunters)
        col_w = preview_rect.width // n_h
        for hi, h_name in enumerate(active_hunters):
            hx = preview_rect.x + int((hi + 0.5) * col_w)
            # 32px circular photo avatar
            av = get_hunter_avatar(h_name, size=32)
            screen.blit(av, (hx - av.get_width() // 2, preview_rect.y + 40))

            # Short display label under photo
            if h_name == PRINCIPAL_NAME:
                lbl_str = "Principal"
            elif "(HOD)" in h_name:
                lbl_str = h_name.split()[0] + " (HOD)"
            elif h_name in ("BOUNCER", "SECURITY"):
                lbl_str = h_name.capitalize()
            else:
                parts = h_name.split()
                lbl_str = parts[0] + (" " + parts[1][0] + "." if len(parts) > 1 else "")

            h_lbl = FONT_TINY.render(lbl_str, True, WHITE)
            screen.blit(h_lbl, (hx - h_lbl.get_width() // 2, preview_rect.y + 82))

        note_str = "✓ Real faculty photos loaded! Security & Bouncer stationed in every branch | Principal Isha Malhotra at Main Gate"
        rule_note = FONT_TINY.render(note_str, True, (160, 200, 235))
        screen.blit(rule_note, (preview_rect.centerx - rule_note.get_width() // 2, preview_rect.y + 118))

        # Row 5: Start Button
        is_btn_hover = start_btn_rect.collidepoint(mouse_pos)
        btn_bg = (30, 140, 80) if is_btn_hover else (20, 110, 60)
        pygame.draw.rect(screen, btn_bg, start_btn_rect, border_radius=10)
        pygame.draw.rect(screen, GREEN, start_btn_rect, width=2, border_radius=10)
        btn_txt = FONT_BIG.render("START BUNK MISSION ➔", True, WHITE)
        screen.blit(btn_txt, (start_btn_rect.centerx - btn_txt.get_width() // 2, start_btn_rect.centery - btn_txt.get_height() // 2))

        hint = FONT_TINY.render("Click options or press TAB to switch fields | Press ENTER to start", True, (180, 200, 230))
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, card_y + 564))

        pygame.display.flip()

# ==============================================================================
# 🏃 CORE GAMEPLAY LOOP (PER LEVEL)
# ==============================================================================

student_name = "Student"
student_roll = "Roll 01"
student_dept = "CSE"
student_sem  = 4
current_level_idx = 0
total_score = 0
lives = 3
max_lives = 3
game_start_timestamp = time.time()

floating_texts = []
particles = []

def add_floating_text(text, x, y, color=GOLD):
    floating_texts.append({"text": text, "x": x, "y": y, "timer": 1.2, "color": color})

def spawn_particles(x, y, count=15, colors=[GOLD, CYAN, WHITE]):
    for _ in range(count):
        ang = random.uniform(0, math.pi * 2)
        spd = random.uniform(1.5, 4.5)
        particles.append({
            "x": x, "y": y,
            "vx": math.cos(ang) * spd,
            "vy": math.sin(ang) * spd,
            "life": random.uniform(0.4, 1.0),
            "max_life": 1.0,
            "color": random.choice(colors),
            "size": random.randint(2, 4)
        })

def run_level(level_idx):
    global total_score, lives, sound_enabled

    lvl = LEVEL_DATA[level_idx]
    maze = lvl["maze"]
    theme = lvl["theme"]

    start_gx, start_gy = 1, 1
    exit_gx, exit_gy = COLS - 2, ROWS - 2

    start_px, start_py = grid_to_pixel(start_gx, start_gy)
    exit_px, exit_py = grid_to_pixel(exit_gx, exit_gy)

    # Player state
    px, py = float(start_px), float(start_py)
    player_radius = 8.5
    base_speed = 3.8
    sprint_multiplier = 1.6
    boost_timer = 0.0
    invulnerable_timer = 1.8
    facing_dir = "right"

    # Dynamic Guards with actual photos!
    guards = get_level_guards(student_dept, student_sem, level_idx)

    # Collectibles
    items = []
    for it in lvl["items"]:
        ix, iy = grid_to_pixel(it["pos"][0], it["pos"][1])
        items.append({
            "name": it["name"],
            "type": it["type"],
            "pts": it["pts"],
            "x": ix,
            "y": iy,
            "icon": it["icon"],
            "collected": False
        })

    level_start_time = time.time()
    banner_timer = 2.5
    paused = False
    flash_red_timer = 0.0

    dir_vectors = {
        "up": (0, -1),
        "down": (0, 1),
        "left": (-1, 0),
        "right": (1, 0)
    }

    angle_map = {
        "up": -math.pi / 2,
        "down": math.pi / 2,
        "left": math.pi,
        "right": 0
    }

    while True:
        dt = clock.tick(FPS) / 1000.0
        now = time.time()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_p, pygame.K_ESCAPE):
                    paused = not paused
                    play_sound(snd_pickup)
                elif e.key == pygame.K_m:
                    sound_enabled = not sound_enabled
                    add_floating_text("Sound " + ("ON" if sound_enabled else "OFF"), WIDTH // 2, 80, CYAN)
                elif paused:
                    if e.key == pygame.K_r:
                        return "RETRY"
                    elif e.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

        if paused:
            pause_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pause_overlay.fill((10, 14, 24, 210))
            screen.blit(pause_overlay, (0, 0))

            card_w, card_h = 440, 270
            card_rect = pygame.Rect(WIDTH//2 - card_w//2, HEIGHT//2 - card_h//2, card_w, card_h)
            pygame.draw.rect(screen, (20, 26, 40), card_rect, border_radius=14)
            pygame.draw.rect(screen, CYAN, card_rect, width=2, border_radius=14)

            p_title = FONT_BIG.render("GAME PAUSED", True, GOLD)
            screen.blit(p_title, (WIDTH // 2 - p_title.get_width() // 2, card_rect.y + 25))

            lines = [
                "[ESC / P] Resume Game",
                "[R] Restart Current Level",
                "[M] Toggle Sound Effects",
                "[Q] Quit to Desktop"
            ]
            for i, l in enumerate(lines):
                ls = FONT_MED.render(l, True, WHITE)
                screen.blit(ls, (WIDTH // 2 - ls.get_width() // 2, card_rect.y + 90 + i * 36))

            pygame.display.flip()
            continue

        if banner_timer > 0:
            banner_timer -= dt
        if invulnerable_timer > 0:
            invulnerable_timer -= dt
        if boost_timer > 0:
            boost_timer -= dt
        if flash_red_timer > 0:
            flash_red_timer -= dt

        # Player Movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
            facing_dir = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
            facing_dir = "right"
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
            facing_dir = "up"
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1
            facing_dir = "down"

        is_sprinting = (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and boost_timer > 0
        cur_speed = base_speed * (sprint_multiplier if is_sprinting else 1.0)

        px, py = move_player(px, py, dx, dy, cur_speed, player_radius, maze)

        if is_sprinting and (dx != 0 or dy != 0) and random.random() < 0.4:
            particles.append({
                "x": px - dx * 8, "y": py - dy * 8,
                "vx": random.uniform(-0.5, 0.5), "vy": random.uniform(-0.5, 0.5),
                "life": 0.3, "max_life": 0.3, "color": CYAN, "size": 3
            })

        # Guard AI & Patrol
        for g in guards:
            dist_to_player = math.hypot(px - g["x"], py - g["y"])
            guard_spd = g["speed"]

            angle_to_player = math.atan2(py - g["y"], px - g["x"])
            facing_angle = angle_map[g["dir"]]
            angle_diff = abs((angle_to_player - facing_angle + math.pi) % (2 * math.pi) - math.pi)

            in_view = (dist_to_player < 125) and (angle_diff < math.radians(45))
            if in_view and line_of_sight(g["x"], g["y"], px, py, maze):
                if not g["alert"]:
                    play_sound(snd_alert)
                    add_floating_text("!", g["x"], g["y"] - 22, RED)
                g["alert"] = True
                g["alert_timer"] = 2.0

            if g["alert_timer"] > 0:
                g["alert_timer"] -= dt
                if g["alert_timer"] <= 0:
                    g["alert"] = False

            if g["alert"]:
                guard_spd *= 1.25
                desired_dirs = []
                if abs(px - g["x"]) > abs(py - g["y"]):
                    desired_dirs.append("right" if px > g["x"] else "left")
                    desired_dirs.append("down" if py > g["y"] else "up")
                else:
                    desired_dirs.append("down" if py > g["y"] else "up")
                    desired_dirs.append("right" if px > g["x"] else "left")

                moved = False
                for d in desired_dirs:
                    vx, vy = dir_vectors[d]
                    if can_move_to(g["x"] + vx * guard_spd, g["y"] + vy * guard_spd, g["radius"], maze):
                        g["x"] += vx * guard_spd
                        g["y"] += vy * guard_spd
                        g["dir"] = d
                        moved = True
                        break
                if not moved:
                    g["dir"] = random.choice(["up", "down", "left", "right"])
            else:
                vx, vy = dir_vectors[g["dir"]]
                if can_move_to(g["x"] + vx * guard_spd, g["y"] + vy * guard_spd, g["radius"], maze):
                    g["x"] += vx * guard_spd
                    g["y"] += vy * guard_spd
                else:
                    open_dirs = [d for d, (tvx, tvy) in dir_vectors.items() if can_move_to(g["x"] + tvx * guard_spd, g["y"] + tvy * guard_spd, g["radius"], maze)]
                    g["dir"] = random.choice(open_dirs) if open_dirs else random.choice(["up", "down", "left", "right"])

                g["change_cd"] -= 1
                if g["change_cd"] <= 0:
                    g["change_cd"] = random.randint(30, 80)
                    open_dirs = [d for d, (tvx, tvy) in dir_vectors.items() if can_move_to(g["x"] + tvx * guard_spd, g["y"] + tvy * guard_spd, g["radius"], maze)]
                    if open_dirs:
                        g["dir"] = random.choice(open_dirs)

        # Collision with Guard
        if invulnerable_timer <= 0:
            for g in guards:
                if math.hypot(px - g["x"], py - g["y"]) < (player_radius + g["radius"]):
                    lives -= 1
                    play_sound(snd_caught)
                    flash_red_timer = 0.5
                    invulnerable_timer = 2.0
                    add_floating_text(f"CAUGHT BY {g['name']}! -1 LIFE", WIDTH // 2, HEIGHT // 2 - 30, RED)
                    spawn_particles(px, py, count=25, colors=[RED, ORANGE, WHITE])

                    px, py = float(start_px), float(start_py)
                    for guard in guards:
                        guard["x"], guard["y"] = grid_to_pixel(guard["start"][0], guard["start"][1])
                        guard["alert"] = False

                    if lives <= 0:
                        return {"status": "GAME_OVER", "caught_by": g["name"]}
                    break

        # Item Pickups
        for it in items:
            if not it["collected"] and math.hypot(px - it["x"], py - it["y"]) < 20:
                it["collected"] = True
                total_score += it["pts"]
                play_sound(snd_pickup)
                spawn_particles(it["x"], it["y"], count=15, colors=[GOLD, YELLOW, WHITE])
                if it["type"] == "boost":
                    boost_timer = 6.0
                    play_sound(snd_boost)
                    add_floating_text(f"{it['name']}! SPRINT READY! +{it['pts']}", it["x"], it["y"] - 15, CYAN)
                else:
                    add_floating_text(f"+{it['pts']} PTS!", it["x"], it["y"] - 15, GOLD)

        # Level Win (College Ground Reached)
        if math.hypot(px - exit_px, py - exit_py) < 22:
            time_spent = round(now - level_start_time, 1)
            time_bonus = max(0, int((45 - time_spent) * 20))
            total_score += time_bonus
            play_sound(snd_win)
            spawn_particles(exit_px, exit_py, count=40, colors=[GREEN, GOLD, CYAN])
            add_floating_text("GROUND REACHED! BUNKED!", px, py - 20, GOLD)
            return {
                "status": "WIN",
                "time": time_spent,
                "bonus": time_bonus,
                "items_collected": sum(1 for it in items if it["collected"]),
                "items_total": len(items)
            }

        for p in particles[:]:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["life"] -= dt
            if p["life"] <= 0:
                particles.remove(p)

        for ft in floating_texts[:]:
            ft["y"] -= 28 * dt
            ft["timer"] -= dt
            if ft["timer"] <= 0:
                floating_texts.remove(ft)

        # ======================================================================
        # 🎨 DRAWING PIPELINE
        # ======================================================================

        # 1. College Background Image (100% visible and bright!)
        screen.blit(background, (0, 0))

        # 2. Draw Maze Walls with Theme Colors (Corridors show college photo directly!)
        wall_fill = theme["wall_fill"]
        wall_edge = theme["wall_edge"]
        wall_glow = theme["wall_glow"]

        for gy in range(ROWS):
            for gx in range(COLS):
                tx = gx * TILE
                ty = HUD_HEIGHT + gy * TILE
                ch = maze[gy][gx]

                if ch == "1":
                    pygame.draw.rect(screen, wall_fill, (tx, ty, TILE, TILE))
                    pygame.draw.line(screen, wall_glow, (tx, ty), (tx + TILE - 1, ty), 1)
                    pygame.draw.line(screen, wall_glow, (tx, ty), (tx, ty + TILE - 1), 1)
                    pygame.draw.line(screen, (10, 14, 20), (tx, ty + TILE - 1), (tx + TILE - 1, ty + TILE - 1), 1)
                    pygame.draw.line(screen, (10, 14, 20), (tx + TILE - 1, ty), (tx + TILE - 1, ty + TILE - 1), 1)
                    pygame.draw.rect(screen, wall_edge, (tx + 1, ty + 1, TILE - 2, TILE - 2), 1)

        # 3. Start Zone Pad
        pygame.draw.rect(screen, (20, 60, 40), (start_gx * TILE, HUD_HEIGHT + start_gy * TILE, TILE, TILE), border_radius=4)
        pygame.draw.rect(screen, GREEN, (start_gx * TILE, HUD_HEIGHT + start_gy * TILE, TILE, TILE), width=2, border_radius=4)
        c_lbl = FONT_TINY.render("START", True, GREEN)
        screen.blit(c_lbl, (start_px - c_lbl.get_width() // 2, start_py - c_lbl.get_height() // 2))

        # 4. Campus Ground Destination Gate
        pulse_r = 12 + int(3 * math.sin(now * 6))
        pygame.draw.rect(screen, (20, 65, 30), (exit_gx * TILE, HUD_HEIGHT + exit_gy * TILE, TILE, TILE), border_radius=4)
        pygame.draw.rect(screen, (40, 180, 70), (exit_gx * TILE + 2, HUD_HEIGHT + exit_gy * TILE + 2, TILE - 4, TILE - 4), width=1, border_radius=3)
        pygame.draw.circle(screen, GOLD, (exit_px, exit_py), pulse_r, width=2)
        grd_lbl = FONT_TINY.render("GROUND", True, GOLD)
        screen.blit(grd_lbl, (exit_px - grd_lbl.get_width() // 2, exit_py - grd_lbl.get_height() // 2))

        # 5. Objective Guide Indicator (pointing to GROUND)
        dist_to_ground = math.hypot(px - exit_px, py - exit_py)
        if dist_to_ground > 200:
            guide_ang = math.atan2(exit_py - py, exit_px - px)
            arrow_x = px + math.cos(guide_ang) * 26
            arrow_y = py + math.sin(guide_ang) * 26
            pygame.draw.circle(screen, GOLD, (int(arrow_x), int(arrow_y)), 4)
            gtxt = FONT_TINY.render("GROUND ➔", True, GOLD)
            screen.blit(gtxt, (int(arrow_x + math.cos(guide_ang) * 12 - gtxt.get_width() // 2), int(arrow_y + math.sin(guide_ang) * 12 - gtxt.get_height() // 2)))

        # 6. Items / Collectibles
        for it in items:
            if not it["collected"]:
                bob = int(math.sin(now * 5 + it["x"]) * 3)
                iy = it["y"] + bob
                aura_col = (0, 230, 255, 90) if it["type"] == "boost" else (255, 215, 0, 90)
                aura_surf = pygame.Surface((28, 28), pygame.SRCALPHA)
                pygame.draw.circle(aura_surf, aura_col, (14, 14), 11)
                screen.blit(aura_surf, (it["x"] - 14, iy - 14))

                icon_surf = FONT_MED.render(it["icon"][:1], True, GOLD if it["type"] == "score" else CYAN)
                screen.blit(icon_surf, (it["x"] - icon_surf.get_width() // 2, iy - icon_surf.get_height() // 2))

        # 7. Guard Vision Cones
        vision_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for g in guards:
            ang = angle_map[g["dir"]]
            fov = math.radians(52)
            dist = 115
            points = [(g["x"], g["y"])]
            beam_color = (255, 60, 60, 65) if g["alert"] else (255, 235, 120, 45)
            for a in [ang - fov/2, ang - fov/4, ang, ang + fov/4, ang + fov/2]:
                tx = g["x"] + math.cos(a) * dist
                ty = g["y"] + math.sin(a) * dist
                for s in range(5, int(dist), 8):
                    cx = g["x"] + math.cos(a) * s
                    cy = g["y"] + math.sin(a) * s
                    cgx, cgy = pixel_to_grid(cx, cy)
                    if 0 <= cgx < COLS and 0 <= cgy < ROWS and maze[cgy][cgx] == "1":
                        tx, ty = cx, cy
                        break
                points.append((tx, ty))
            pygame.draw.polygon(vision_surf, beam_color, points)
        screen.blit(vision_surf, (0, 0))

        # 8. Draw Guards with Real Photo Circular Avatars!
        for g in guards:
            av_w = g["avatar"].get_width()
            av_h = g["avatar"].get_height()
            screen.blit(g["avatar"], (g["x"] - av_w // 2, g["y"] - av_h // 2))
            if g["alert"]:
                alert_txt = FONT_BIG.render("!", True, RED)
                screen.blit(alert_txt, (g["x"] - alert_txt.get_width() // 2, g["y"] - 38))
            draw_nameplate(screen, g["name"], FONT_TINY, g["x"], g["y"] - 22, border=RED if g["alert"] else (90, 110, 140))

        # 9. Draw Player with Circular Avatar
        if invulnerable_timer <= 0 or int(now * 12) % 2 == 0:
            if is_sprinting:
                pygame.draw.circle(screen, CYAN, (int(px), int(py)), 17, width=2)
            p_w = player_avatar.get_width()
            p_h = player_avatar.get_height()
            screen.blit(player_avatar, (px - p_w // 2, py - p_h // 2))

            nose_ang = angle_map[facing_dir]
            nx = px + math.cos(nose_ang) * 14
            ny = py + math.sin(nose_ang) * 14
            pygame.draw.circle(screen, WHITE, (int(nx), int(ny)), 3)

            draw_nameplate(screen, student_name, FONT_TINY, px, py - 24, border=CYAN)

        # 10. Particles & Text
        for p in particles:
            alpha = int(255 * (p["life"] / p["max_life"]))
            p_surf = pygame.Surface((p["size"] * 2, p["size"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(p_surf, (*p["color"][:3], alpha), (p["size"], p["size"]), p["size"])
            screen.blit(p_surf, (p["x"] - p["size"], p["y"] - p["size"]))

        for ft in floating_texts:
            f_surf = FONT_SMALL.render(ft["text"], True, ft["color"])
            screen.blit(f_surf, (ft["x"] - f_surf.get_width() // 2, ft["y"]))

        if flash_red_timer > 0:
            flash_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash_surf.fill((255, 0, 0, int(90 * (flash_red_timer / 0.5))))
            screen.blit(flash_surf, (0, 0))

        # ======================================================================
        # 👑 TOP HUD (Displays Branch, Sem, Roll, Score & Lives)
        # ======================================================================
        hud = pygame.Surface((WIDTH, HUD_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(hud, (*HUD_BG, 245), (0, 0, WIDTH, HUD_HEIGHT))
        pygame.draw.line(hud, HUD_BORDER, (0, HUD_HEIGHT - 1), (WIDTH, HUD_HEIGHT - 1), 2)
        screen.blit(hud, (0, 0))

        lvl_num_txt = FONT_SMALL.render(f"LVL {lvl['num']}/5", True, CYAN)
        screen.blit(lvl_num_txt, (14, 12))
        sub_tag = FONT_TINY.render(f"{student_dept} • SEM {student_sem}", True, GOLD)
        screen.blit(sub_tag, (14, 34))

        lvl_title_txt = FONT_MED.render(lvl["name"], True, WHITE)
        screen.blit(lvl_title_txt, (95, 18))

        student_info = FONT_TINY.render(f"{student_name} ({student_roll})", True, (210, 225, 245))
        screen.blit(student_info, (WIDTH // 2 - student_info.get_width() // 2, 10))

        hearts_str = "❤️ " * lives + "🖤 " * (max_lives - lives)
        lives_txt = FONT_MED.render(f"LIVES: {hearts_str}", True, RED)
        screen.blit(lives_txt, (WIDTH // 2 - lives_txt.get_width() // 2, 28))

        if boost_timer > 0:
            boost_txt = FONT_TINY.render(f"⚡ SPRINT READY! [HOLD SHIFT] ({boost_timer:.1f}s)", True, CYAN)
            screen.blit(boost_txt, (WIDTH // 2 - boost_txt.get_width() // 2, 46))

        elapsed = round(now - level_start_time, 1)
        timer_txt = FONT_MED.render(f"⏱️ {elapsed:.1f}s", True, YELLOW)
        screen.blit(timer_txt, (WIDTH - 230, 20))

        score_txt = FONT_MED.render(f"⭐ {total_score}", True, GOLD)
        screen.blit(score_txt, (WIDTH - 115, 20))

        # Level Intro Splash Banner with Mini Photos of Hunters!
        if banner_timer > 0:
            banner_alpha = min(255, int(banner_timer * 220))
            banner_h = 100
            banner_surf = pygame.Surface((WIDTH, banner_h), pygame.SRCALPHA)
            banner_surf.fill((15, 22, 36, min(240, banner_alpha)))
            pygame.draw.line(banner_surf, CYAN, (0, 0), (WIDTH, 0), 2)
            pygame.draw.line(banner_surf, CYAN, (0, banner_h - 2), (WIDTH, banner_h - 2), 2)

            t1 = FONT_BIG.render(f"LEVEL {lvl['num']}: {lvl['name']}", True, GOLD)
            banner_surf.blit(t1, (WIDTH // 2 - t1.get_width() // 2, 8))

            # Render photos and names of active guards in this level
            total_g = len(guards)
            col_g_w = min(150, WIDTH // (total_g + 1))
            start_gx_pos = WIDTH // 2 - ((total_g - 1) * col_g_w) // 2

            for gi, g in enumerate(guards):
                pos_x = start_gx_pos + gi * col_g_w
                # Mini avatar
                banner_surf.blit(g["avatar"], (pos_x - g["avatar"].get_width() // 2, 42))
                g_lbl = FONT_TINY.render(g["name"], True, WHITE)
                banner_surf.blit(g_lbl, (pos_x - g_lbl.get_width() // 2, 74))

            screen.blit(banner_surf, (0, HEIGHT // 2 - banner_h // 2))

        pygame.display.flip()

# ==============================================================================
# 🏆 LEVEL CLEARED & GAME OVER & VICTORY SCREENS
# ==============================================================================

def level_cleared_screen(lvl_num, win_data):
    particles.clear()
    confetti_timer = 0
    while True:
        dt = clock.tick(FPS) / 1000.0
        confetti_timer += dt

        if random.random() < 0.6:
            spawn_particles(random.randint(50, WIDTH - 50), random.randint(40, 200), count=4, colors=[GOLD, GREEN, CYAN, PURPLE])

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_SPACE, pygame.K_RETURN):
                    return

        screen.blit(background, (0, 0))

        card_w, card_h = 580, 370
        card_x = WIDTH // 2 - card_w // 2
        card_y = HEIGHT // 2 - card_h // 2
        card = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        pygame.draw.rect(card, (15, 22, 34, 248), (0, 0, card_w, card_h), border_radius=16)
        pygame.draw.rect(card, GREEN, (0, 0, card_w, card_h), width=2, border_radius=16)
        screen.blit(card, (card_x, card_y))

        t = FONT_TITLE.render(f"🎉 LEVEL {lvl_num} CLEARED! 🎉", True, GREEN)
        screen.blit(t, (WIDTH // 2 - t.get_width() // 2, card_y + 25))

        sub = FONT_MED.render(f"Ground Path Reached, {student_name}! ({student_dept} Sem {student_sem})", True, WHITE)
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, card_y + 80))

        time_str = f"Time Taken: {win_data['time']} seconds"
        t_surf = FONT_MED.render(time_str, True, YELLOW)
        screen.blit(t_surf, (WIDTH // 2 - t_surf.get_width() // 2, card_y + 125))

        items_str = f"Items Collected: {win_data['items_collected']} / {win_data['items_total']}"
        i_surf = FONT_MED.render(items_str, True, CYAN)
        screen.blit(i_surf, (WIDTH // 2 - i_surf.get_width() // 2, card_y + 165))

        score_str = f"Total Score: {total_score} PTS (+{win_data['bonus']} Speed Bonus)"
        s_surf = FONT_MED.render(score_str, True, GOLD)
        screen.blit(s_surf, (WIDTH // 2 - s_surf.get_width() // 2, card_y + 205))

        p_txt = FONT_BIG.render("PRESS SPACE FOR NEXT LEVEL ➔", True, WHITE)
        pulse = abs(math.sin(confetti_timer * 4))
        p_surf = pygame.Surface(p_txt.get_size(), pygame.SRCALPHA)
        p_surf.blit(p_txt, (0, 0))
        p_surf.set_alpha(int(180 + 75 * pulse))
        screen.blit(p_surf, (WIDTH // 2 - p_txt.get_width() // 2, card_y + 285))

        for p in particles[:]:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["life"] -= dt
            if p["life"] <= 0:
                particles.remove(p)
            else:
                pygame.draw.circle(screen, p["color"], (int(p["x"]), int(p["y"])), p["size"])

        pygame.display.flip()

def game_over_screen(caught_by="Faculty"):
    global lives, total_score
    while True:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    lives = max_lives
                    return "RETRY"
                elif e.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        screen.blit(background, (0, 0))

        card_w, card_h = 580, 390
        card_x = WIDTH // 2 - card_w // 2
        card_y = HEIGHT // 2 - card_h // 2
        card = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        pygame.draw.rect(card, (20, 15, 20, 248), (0, 0, card_w, card_h), border_radius=16)
        pygame.draw.rect(card, RED, (0, 0, card_w, card_h), width=2, border_radius=16)
        screen.blit(card, (card_x, card_y))

        title = FONT_TITLE.render("BUSTED! ZERO ATTENDANCE 🎓❌", True, RED)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, card_y + 22))

        # Display actual face photo of the teacher who caught you!
        caught_avatar = get_hunter_avatar(caught_by, size=46)
        screen.blit(caught_avatar, (WIDTH // 2 - caught_avatar.get_width() // 2, card_y + 70))

        sub = FONT_MED.render(f"Caught by {caught_by}!", True, YELLOW)
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, card_y + 128))

        info = FONT_SMALL.render(f"Student: {student_name} ({student_roll}) | {student_dept} Sem {student_sem}", True, WHITE)
        screen.blit(info, (WIDTH // 2 - info.get_width() // 2, card_y + 162))

        s_txt = FONT_MED.render(f"Final Score: {total_score} PTS", True, GOLD)
        screen.blit(s_txt, (WIDTH // 2 - s_txt.get_width() // 2, card_y + 200))

        prompt_r = FONT_BIG.render("[R] Retry Level", True, GREEN)
        screen.blit(prompt_r, (WIDTH // 2 - prompt_r.get_width() // 2, card_y + 255))

        prompt_q = FONT_SMALL.render("Press [Q] to Quit Game", True, (180, 180, 180))
        screen.blit(prompt_q, (WIDTH // 2 - prompt_q.get_width() // 2, card_y + 320))

        pygame.display.flip()

def grand_victory_screen():
    confetti_timer = 0
    total_time = round(time.time() - game_start_timestamp, 1)

    while True:
        dt = clock.tick(FPS) / 1000.0
        confetti_timer += dt

        for _ in range(4):
            spawn_particles(random.randint(20, WIDTH - 20), 0, count=2, colors=[GOLD, CYAN, GREEN, YELLOW, PURPLE])

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_SPACE, pygame.K_RETURN):
                    return
                elif e.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit()
                    sys.exit()

        screen.blit(background, (0, 0))

        card_w, card_h = 720, 480
        card_x = WIDTH // 2 - card_w // 2
        card_y = HEIGHT // 2 - card_h // 2
        card = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        pygame.draw.rect(card, (15, 20, 36, 252), (0, 0, card_w, card_h), border_radius=18)
        pygame.draw.rect(card, GOLD, (0, 0, card_w, card_h), width=3, border_radius=18)
        screen.blit(card, (card_x, card_y))

        t = FONT_TITLE.render("🏆 LEVEL 5 COMPLETED! 🏆", True, GOLD)
        screen.blit(t, (WIDTH // 2 - t.get_width() // 2, card_y + 20))

        # UPCOMING LEVELS COMING SOON BANNER
        soon_pill = pygame.Surface((540, 38), pygame.SRCALPHA)
        pygame.draw.rect(soon_pill, (25, 60, 110, 230), (0, 0, 540, 38), border_radius=10)
        pygame.draw.rect(soon_pill, CYAN, (0, 0, 540, 38), width=2, border_radius=10)
        screen.blit(soon_pill, (WIDTH // 2 - 270, card_y + 70))
        soon_txt = FONT_BIG.render("🚀 UPCOMING LEVELS COMING SOON! 🚀", True, CYAN)
        screen.blit(soon_txt, (WIDTH // 2 - soon_txt.get_width() // 2, card_y + 74))

        sub = FONT_MED.render(f"Congratulations {student_name}! You reached the College Ground!", True, GREEN)
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, card_y + 124))

        d0 = FONT_MED.render(f"Roll No: {student_roll}  |  {student_dept}  |  Semester {student_sem}", True, WHITE)
        screen.blit(d0, (WIDTH // 2 - d0.get_width() // 2, card_y + 162))

        d1 = FONT_SMALL.render(f"Bunk Mission Complete! Evaded Principal {PRINCIPAL_NAME} & all faculty hunters!", True, (190, 215, 245))
        screen.blit(d1, (WIDTH // 2 - d1.get_width() // 2, card_y + 200))

        d2 = FONT_MED.render(f"Total Bunk Time: {total_time}s   |   Final Score: {total_score} PTS", True, YELLOW)
        screen.blit(d2, (WIDTH // 2 - d2.get_width() // 2, card_y + 238))

        rank_str = f"Master Bunk King of {student_dept} (S-Rank)" if total_score > 3000 else f"Elite Bunk Specialist of {student_dept} (A-Rank)"
        rank_txt = FONT_MED.render(f"Awarded Title: {rank_str}", True, GOLD)
        screen.blit(rank_txt, (WIDTH // 2 - rank_txt.get_width() // 2, card_y + 280))

        pulse = abs(math.sin(confetti_timer * 4))
        p_txt = FONT_BIG.render("PRESS [SPACE / ENTER] TO PLAY AGAIN ↻", True, GOLD)
        p_surf = pygame.Surface(p_txt.get_size(), pygame.SRCALPHA)
        p_surf.blit(p_txt, (0, 0))
        p_surf.set_alpha(int(180 + 75 * pulse))
        screen.blit(p_surf, (WIDTH // 2 - p_txt.get_width() // 2, card_y + 350))

        q_txt = FONT_TINY.render("Press [Q / ESC] to Quit Game", True, (160, 180, 210))
        screen.blit(q_txt, (WIDTH // 2 - q_txt.get_width() // 2, card_y + 420))

        for p in particles[:]:
            p["x"] += p["vx"]
            p["y"] += p["vy"] + 1.5
            p["life"] -= dt * 0.7
            if p["life"] <= 0 or p["y"] > HEIGHT:
                particles.remove(p)
            else:
                pygame.draw.circle(screen, p["color"], (int(p["x"]), int(p["y"])), p["size"])

        pygame.display.flip()

# ==============================================================================
# 🚀 MAIN CONTROLLER
# ==============================================================================

def main():
    global current_level_idx, total_score, lives, student_name, student_roll, student_dept, student_sem, game_start_timestamp, player_avatar

    student_name, student_roll, student_dept, student_sem = student_registration_screen()
    player_avatar = create_student_avatar(student_name, size=26)
    game_start_timestamp = time.time()
    current_level_idx = 0
    total_score = 0
    lives = max_lives

    while True:
        res = run_level(current_level_idx)

        if isinstance(res, dict) and res.get("status") == "GAME_OVER":
            action = game_over_screen(res.get("caught_by", "Faculty"))
            if action == "RETRY":
                continue

        elif res == "RETRY":
            continue

        elif isinstance(res, dict) and res.get("status") == "WIN":
            if current_level_idx + 1 < len(LEVEL_DATA):
                level_cleared_screen(current_level_idx + 1, res)
                current_level_idx += 1
            else:
                grand_victory_screen()
                student_name, student_roll, student_dept, student_sem = student_registration_screen()
                player_avatar = create_student_avatar(student_name, size=26)
                current_level_idx = 0
                total_score = 0
                lives = max_lives
                game_start_timestamp = time.time()

if __name__ == "__main__":
    main()
