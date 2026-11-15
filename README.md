# 🎓 College Bunk Simulator 🏫

A high-octane 2D campus stealth maze runner featuring **5 distinct floors**, **9 academic branches**, and **smooth corner navigation**. Available as both a **Streamlit Web App** and a **Native Pygame Desktop Game**.

---

## 🌟 Key Features

- **🎮 Dual Mode**:
  - **Streamlit Web App (`app.py`)**: Runs at 60 FPS in any modern web browser on PC and mobile phones (includes on-screen virtual touch D-pad & sprint controls).
  - **Pygame Desktop Game (`yash.py`)**: Native desktop window with smooth 60 FPS gameplay, particle systems, and sound effects.
- **🎨 Dynamic Cyber-Faculty Badges**: Integrated across all 9 departments for HODs, teachers, Security, Bouncers, and the Principal (with optional custom local photo support).
- **🏫 9 Academic Departments & 8 Semesters**:
  - `ASH`, `CSE`, `CSIT`, `CSE(AI & ML)`, `CSE(IOT & CS)`, `ECE`, `ECS`, `ME`, `RA`
  - **Semesters 1 & 2 Rule**: 1st-year disciplinary dragnet supervised by HOD Pooja Sharma, Security, and Bouncer.
  - **Semesters 3–8 Rule**: Branch-specific faculty and HODs actively patrol corridors.
- **👑 Principal (Final Boss)**: Stationed at the Main Gate in Level 5 across all departments and semesters.
- **🏃 Thickened Turns & Corner Auto-Assist**:
  - Pac-Man style corridor auto-centering and corner turn alignment prevents sticking or snagging on tight turns on PC keyboard or mobile touch.
- **🏆 Level 5 Completion**:
  - Reaching the college **GROUND** in Level 5 unlocks the victory screen:
    - `🏆 LEVEL 5 COMPLETED! 🏆`
    - `🚀 UPCOMING LEVELS COMING SOON! 🚀`
- **🔊 Web Audio API & Synth SFX**: Responsive, lightweight synthesized sound effects.

---

## 🚀 Quick Start

### 1. Web Version (Streamlit)
```powershell
pip install -r requirements.txt
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

### 2. Desktop Version (Pygame)
```powershell
python yash.py
```

---

## 🕹️ Controls

| Action | PC Keyboard | Mobile |
| :--- | :--- | :--- |
| **Move** | `Arrow Keys` or `W, A, S, D` | Virtual D-Pad / Touch Drag |
| **Sprint** | `Hold Shift` (when boosted) | `⚡ SPRINT` Button |
| **Pause** | `P` or `ESC` | `⏸️ Pause` Button |
| **Mute Sound** | `M` | `🔊 Sound` Button |
| **Restart** | `R` | `🔄 Restart` Button |

---

## ☁️ Deploy to Streamlit Community Cloud (Free)

1. Push this repository to your GitHub account:
   ```powershell
   git init
   git add .
   git commit -m "College Bunk Simulator"
   git branch -M main
   git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO_NAME>.git
   git push -u origin main
   ```
2. Go to [share.streamlit.io](https://share.streamlit.io) and log in with GitHub.
3. Click **"New app"**, select your repository, set the main file path to `app.py`, and click **"Deploy!"**.
