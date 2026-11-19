import xml.etree.ElementTree as ET

TOTAL_DUR = 18.0

# 14 Real Active Blocks with EXACT Y alignment (diff Y = 0!)
shots = [
    # Phase 1: October Lower Front (Row 5: y=137)
    {"id": 1,  "t_fire": 0.9,  "im_pos": (580, 137), "tx": 735, "ty": 137, "bx": 730, "by": 132, "orig_color": "#006d32"},
    {"id": 2,  "t_fire": 1.8,  "im_pos": (580, 137), "tx": 749, "ty": 137, "bx": 744, "by": 132, "orig_color": "#26a641"},

    # Phase 2: October Midline (Row 2: y=95 & Row 3: y=109)
    # Impostor steps to (630, 95)
    {"id": 3,  "t_fire": 3.2,  "im_pos": (630, 95),  "tx": 749, "ty": 95,  "bx": 744, "by": 90,  "orig_color": "#0e4429"},
    # Impostor steps to (630, 109)
    {"id": 4,  "t_fire": 4.2,  "im_pos": (630, 109), "tx": 749, "ty": 109, "bx": 744, "by": 104, "orig_color": "#39d353"},

    # Phase 3: November Midline (Rows 1, 2, 3)
    # Impostor steps to (675, 81)
    {"id": 5,  "t_fire": 5.6,  "im_pos": (675, 81),  "tx": 777, "ty": 81,  "bx": 772, "by": 76,  "orig_color": "#39d353"},
    # Impostor steps to (675, 95)
    {"id": 6,  "t_fire": 6.6,  "im_pos": (675, 95),  "tx": 777, "ty": 95,  "bx": 772, "by": 90,  "orig_color": "#26a641"},
    # Impostor steps to (675, 109)
    {"id": 7,  "t_fire": 7.6,  "im_pos": (675, 109), "tx": 777, "ty": 109, "bx": 772, "by": 104, "orig_color": "#0e4429"},
    # Impostor steps to (675, 95)
    {"id": 8,  "t_fire": 8.6,  "im_pos": (675, 95),  "tx": 791, "ty": 95,  "bx": 786, "by": 90,  "orig_color": "#0e4429"},

    # Phase 4: November Lower Flank (Row 6: y=151)
    # Impostor steps to (710, 151)
    {"id": 9,  "t_fire": 10.0, "im_pos": (710, 151), "tx": 777, "ty": 151, "bx": 772, "by": 146, "orig_color": "#26a641"},
    {"id": 10, "t_fire": 11.0, "im_pos": (710, 151), "tx": 791, "ty": 151, "bx": 786, "by": 146, "orig_color": "#39d353"},

    # Phase 5: Final Frontline Core (Col 52: Rows 0, 1, 2, 4)
    # Impostor steps to (745, 67)
    {"id": 11, "t_fire": 12.4, "im_pos": (745, 67),  "tx": 805, "ty": 67,  "bx": 800, "by": 62,  "orig_color": "#0e4429"},
    # Impostor steps to (745, 81)
    {"id": 12, "t_fire": 13.3, "im_pos": (745, 81),  "tx": 805, "ty": 81,  "bx": 800, "by": 76,  "orig_color": "#26a641"},
    # Impostor steps to (745, 95)
    {"id": 13, "t_fire": 14.2, "im_pos": (745, 95),  "tx": 805, "ty": 95,  "bx": 800, "by": 90,  "orig_color": "#39d353"},
    # Impostor steps to (745, 123)
    {"id": 14, "t_fire": 15.1, "im_pos": (745, 123), "tx": 805, "ty": 123, "bx": 800, "by": 118, "orig_color": "#39d353"},
]

def pct(t):
    return f"{(t / TOTAL_DUR) * 100:.2f}%"

css_lines = []

# 1. Impostor Movement: Row-by-Row Stance Transitions
# Smooth repositioning between shots so the Impostor is ALWAYS in the exact row of the shot!
css_lines.append(f"""
@keyframes impostorPatrolPath {{
  0%, {pct(2.3)}      {{ transform: translate(580px, 137px); }}
  {pct(2.7)}, {pct(3.7)}  {{ transform: translate(630px, 95px); }}
  {pct(3.9)}, {pct(4.9)}  {{ transform: translate(630px, 109px); }}
  {pct(5.2)}, {pct(6.1)}  {{ transform: translate(675px, 81px); }}
  {pct(6.3)}, {pct(7.1)}  {{ transform: translate(675px, 95px); }}
  {pct(7.3)}, {pct(8.1)}  {{ transform: translate(675px, 109px); }}
  {pct(8.3)}, {pct(9.2)}  {{ transform: translate(675px, 95px); }}
  {pct(9.6)}, {pct(11.6)} {{ transform: translate(710px, 151px); }}
  {pct(12.0)}, {pct(12.8)} {{ transform: translate(745px, 67px); }}
  {pct(13.0)}, {pct(13.7)} {{ transform: translate(745px, 81px); }}
  {pct(13.9)}, {pct(14.6)} {{ transform: translate(745px, 95px); }}
  {pct(14.8)}, {pct(15.7)} {{ transform: translate(745px, 123px); }}
  {pct(16.0)}              {{ transform: translate(745px, 95px); }}
  {pct(16.4)}              {{ transform: translate(745px, 75px) rotate(-10deg); }}
  {pct(16.8)}              {{ transform: translate(745px, 68px) rotate(360deg); }}
  {pct(17.2)}              {{ transform: translate(745px, 95px); }}
  {pct(17.7)}, 100%        {{ transform: translate(580px, 137px); }}
}}
.impostor-patrol {{ animation: impostorPatrolPath {TOTAL_DUR}s ease-in-out infinite; }}
""")

# 2. Leg Waddling
css_lines.append(f"""
@keyframes impostorWalkLegs {{
  0%, 100% {{ transform: rotate(0deg); }}
  50%      {{ transform: rotate(3deg) translateY(-0.5px); }}
}}
.waddling-legs {{ animation: impostorWalkLegs 0.25s ease-in-out infinite; }}
""")

# 3. Gun Recoil
recoil_keyframes = ["0% { transform: translate(6px, 0px) rotate(0deg); }"]
for s in shots:
    tf = s["t_fire"]
    recoil_keyframes.append(f"{pct(tf - 0.04)} {{ transform: translate(6px, 0px) rotate(0deg); }}")
    recoil_keyframes.append(f"{pct(tf)} {{ transform: translate(2px, 0px) rotate(-6deg); }}")
    recoil_keyframes.append(f"{pct(tf + 0.10)} {{ transform: translate(6px, 0px) rotate(0deg); }}")
recoil_keyframes.append("100% { transform: translate(6px, 0px) rotate(0deg); }")
css_lines.append(f"@keyframes gunRecoilSeq {{ {' '.join(recoil_keyframes)} }}\n.impostor-blaster {{ animation: gunRecoilSeq {TOTAL_DUR}s ease-out infinite; }}")

# 4. Pure Flying Bullets, Muzzle Flash, Shockwaves, and Sparks (ZERO GUIDE LINES!)
for s in shots:
    sid = s["id"]
    tf = s["t_fire"]
    t_impact = tf + 0.10
    
    gx = s["im_pos"][0] + 18
    gy = s["im_pos"][1] # EXACT row center!
    tx = s["tx"]
    ty = s["ty"]         # EXACT row center!

    # Muzzle flash
    css_lines.append(f"""
@keyframes muzzleFlash{sid} {{
  0%, {pct(tf - 0.02)} {{ opacity: 0; transform: translate({gx}px, {gy}px) scale(0); }}
  {pct(tf)} {{ opacity: 1; transform: translate({gx}px, {gy}px) scale(1.4); }}
  {pct(tf + 0.08)} {{ opacity: 0; transform: translate({gx}px, {gy}px) scale(0.2); }}
  100% {{ opacity: 0; }}
}}
.muzzle-flash-{sid} {{ animation: muzzleFlash{sid} {TOTAL_DUR}s ease-out infinite; }}
""")

    # Pure Bullet Tracer (flies completely horizontally inside row!)
    css_lines.append(f"""
@keyframes flyBullet{sid} {{
  0%, {pct(tf - 0.01)} {{ opacity: 0; transform: translate({gx}px, {gy}px) scale(0.4); }}
  {pct(tf)} {{ opacity: 1; transform: translate({gx}px, {gy}px) scale(1); }}
  {pct(t_impact)} {{ opacity: 1; transform: translate({tx}px, {ty}px) scale(1.1); }}
  {pct(t_impact + 0.03)}, 100% {{ opacity: 0; transform: translate({tx}px, {ty}px); }}
}}
.bullet-{sid} {{ animation: flyBullet{sid} {TOTAL_DUR}s linear infinite; }}
""")

    # Expanding Shockwave Ring
    css_lines.append(f"""
@keyframes shockwave{sid} {{
  0%, {pct(t_impact - 0.01)} {{ opacity: 0; transform: translate({tx}px, {ty}px) scale(0.2); }}
  {pct(t_impact)} {{ opacity: 1; transform: translate({tx}px, {ty}px) scale(0.5); }}
  {pct(t_impact + 0.22)} {{ opacity: 0; transform: translate({tx}px, {ty}px) scale(2.2); }}
  100% {{ opacity: 0; }}
}}
.shockwave-{sid} {{ animation: shockwave{sid} {TOTAL_DUR}s ease-out infinite; }}
""")

    # Spark Debris
    css_lines.append(f"""
@keyframes sparkExplosion{sid} {{
  0%, {pct(t_impact - 0.01)} {{ opacity: 0; transform: translate({tx}px, {ty}px) scale(0); }}
  {pct(t_impact)} {{ opacity: 1; transform: translate({tx}px, {ty}px) scale(1); }}
  {pct(t_impact + 0.20)} {{ opacity: 0; transform: translate({tx}px, {ty}px) scale(1.8) rotate(35deg); }}
  100% {{ opacity: 0; }}
}}
.detonation-{sid} {{ animation: sparkExplosion{sid} {TOTAL_DUR}s ease-out infinite; }}
""")

    # CRITICAL POINT 2: BLOCK BURNS AND THEN COMPLETELY DISAPPEARS INTO EMPTY DARK CELL!
    css_lines.append(f"""
@keyframes targetBurn{sid} {{
  0%, {pct(t_impact - 0.01)} {{ fill: {s['orig_color']}; stroke: none; filter: none; opacity: 1; }}
  {pct(t_impact)} {{ fill: #ffffff; filter: drop-shadow(0 0 6px #ffffff); opacity: 1; }}
  {pct(t_impact + 0.05)} {{ fill: #ffea00; filter: drop-shadow(0 0 8px #ff6600); opacity: 1; }}
  {pct(t_impact + 0.15)} {{ fill: #ff4500; filter: drop-shadow(0 0 6px #ff2200); opacity: 1; }}
  {pct(t_impact + 0.35)} {{ fill: #b91c1c; filter: drop-shadow(0 0 2px #ff4500); opacity: 0.8; }}
  /* DISAPPEARS! Becomes empty dark square #161b22, completely wiped out! */
  {pct(t_impact + 0.50)}, 97.0% {{ fill: #161b22; stroke: none; filter: none; opacity: 1; }}
  /* Respawns green at end of loop for fresh cycle */
  98.5%, 100% {{ fill: {s['orig_color']}; stroke: none; filter: none; opacity: 1; }}
}}
.target-block-{sid} {{ animation: targetBurn{sid} {TOTAL_DUR}s ease-in-out infinite; }}
""")

# Radar scanner animation
css_lines.append("""
@keyframes radarSweep {
  0%   { transform: translateX(50px); opacity: 0; }
  10%  { opacity: 0.18; }
  90%  { opacity: 0.18; }
  100% { transform: translateX(810px); opacity: 0; }
}
.radar-scan { animation: radarSweep 9s linear infinite; }
""")

# Status LED Pulse
css_lines.append("""
@keyframes ledPulse {
  0%, 100% { opacity: 0.6; filter: drop-shadow(0 0 2px #22d3ee); }
  50%      { opacity: 1.0; filter: drop-shadow(0 0 6px #22d3ee); }
}
.status-led { animation: ledPulse 1.8s ease-in-out infinite; }
""")

# Visor sparkle
css_lines.append(f"""
@keyframes visorSparkle {{
  0%, 91.0% {{ opacity: 0; transform: scale(0); }}
  92.0%, 94.5% {{ opacity: 1; transform: scale(1.3) rotate(45deg); filter: drop-shadow(0 0 4px #22d3ee); }}
  95.5%, 100% {{ opacity: 0; transform: scale(0); }}
}}
.visor-sparkle {{ animation: visorSparkle {TOTAL_DUR}s ease-in-out infinite; }}
""")

# Victory prompt banner (Displays ONLY after all 14 targets have completely disappeared!)
css_lines.append(f"""
@keyframes victoryPrompt {{
  0%, 88.0% {{ opacity: 0; transform: translateY(4px); }}
  89.5%, 96.0% {{ opacity: 1; transform: translateY(0px); filter: drop-shadow(0 0 6px #39d353); }}
  97.5%, 100% {{ opacity: 0; transform: translateY(-4px); }}
}}
.victory-hud {{ animation: victoryPrompt {TOTAL_DUR}s ease-in-out infinite; }}
""")

css_str = "\n".join(css_lines)

# Grid cells: 53 cols x 7 rows
# ONLY the 14 real active blocks are green initially; all other cells are #161b22!
target_dict = { (s["bx"], s["by"]): s["id"] for s in shots }

grid_cells = []
for c in range(53):
    x = 72 + c * 14
    for r in range(7):
        y = 62 + r * 14
        if (x, y) in target_dict:
            sid = target_dict[(x, y)]
            orig_c = shots[sid - 1]["orig_color"]
            grid_cells.append(f'<rect class="target-block-{sid}" x="{x}" y="{y}" width="10" height="10" rx="2" fill="{orig_c}"/>')
        else:
            grid_cells.append(f'<rect x="{x}" y="{y}" width="10" height="10" rx="2" fill="#161b22"/>')

grid_markup = "\n    ".join(grid_cells)

# Pure bullets, shockwaves, and spark debris (ABSOLUTELY ZERO GUIDE LINES!)
bullets = []
shockwaves = []
explosions = []

for s in shots:
    sid = s["id"]

    # Bullet tracer (glowing plasma bolt)
    bullets.append(f"""
    <!-- Plasma Bullet {sid} -->
    <g class="bullet-{sid}" filter="url(#bulletGlow)">
      <ellipse cx="0" cy="0" rx="6" ry="2.2" fill="#ffffff" />
      <ellipse cx="-4" cy="0" rx="8" ry="1.8" fill="#22d3ee" opacity="0.8" />
      <ellipse cx="-10" cy="0" rx="6" ry="1.2" fill="#ff4500" opacity="0.6" />
    </g>""")

    # Expanding shockwave
    shockwaves.append(f"""
    <!-- Shockwave Ring {sid} -->
    <circle class="shockwave-{sid}" cx="0" cy="0" r="10" fill="none" stroke="#22d3ee" stroke-width="2" />""")

    # Sparks explosion
    explosions.append(f"""
    <!-- Debris Sparks {sid} -->
    <g class="detonation-{sid}" filter="url(#bulletGlow)">
      <polygon points="0,-12 3,-3 12,0 3,3 0,12 -3,3 -12,0 -3,-3" fill="#ffffff"/>
      <polygon points="-7,-7 0,-2 7,-7 2,0 7,7 0,2 -7,7 -2,0" fill="#ffea00"/>
      <circle cx="-6" cy="-6" r="1.8" fill="#ff4500"/>
      <circle cx="6" cy="-6" r="1.8" fill="#ff4500"/>
      <circle cx="-6" cy="6" r="1.8" fill="#ff4500"/>
      <circle cx="6" cy="6" r="1.8" fill="#ff4500"/>
    </g>""")

bullet_str = "\n".join(bullets)
shockwave_str = "\n".join(shockwaves)
explosion_str = "\n".join(explosions)

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 230" width="100%" height="230" fill="none">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0f1d"/>
      <stop offset="50%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#060911"/>
    </linearGradient>
    <linearGradient id="topCyberGlow" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ef4444" stop-opacity="0"/>
      <stop offset="25%" stop-color="#ef4444" stop-opacity="0.9"/>
      <stop offset="70%" stop-color="#f97316" stop-opacity="0.9"/>
      <stop offset="90%" stop-color="#22d3ee" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#22d3ee" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="radarGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#22d3ee" stop-opacity="0"/>
      <stop offset="50%" stop-color="#22d3ee" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#39d353" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="impostorRedGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ef4444"/>
      <stop offset="70%" stop-color="#dc2626"/>
      <stop offset="100%" stop-color="#991b1b"/>
    </linearGradient>
    <linearGradient id="visorGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#cffafe"/>
      <stop offset="35%" stop-color="#67e8f9"/>
      <stop offset="100%" stop-color="#0891b2"/>
    </linearGradient>
    <filter id="bulletGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="3.5" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <style>
      {css_str}
    </style>
  </defs>

  <!-- Container Box -->
  <rect x="0.5" y="0.5" width="879" height="229" rx="14" fill="url(#bgGrad)" stroke="#30363d" stroke-width="1.2"/>
  <!-- Top Neon Cyber Accent Line -->
  <line x1="15" y1="1" x2="865" y2="1" stroke="url(#topCyberGlow)" stroke-width="2.2"/>

  <!-- Top HUD Header -->
  <g transform="translate(24, 26)">
    <!-- Title -->
    <text x="0" y="0" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="12" font-weight="700" fill="#e6edf3" letter-spacing="0.4px">
      <tspan fill="#ef4444">&#9888; AMONG US</tspan> // TACTICAL GRID PURGE PROTOCOL
    </text>

    <!-- Center Victory Banner Prompt (Shows after ALL 14 are destroyed!) -->
    <g transform="translate(360, -3)" class="victory-hud">
      <rect x="-10" y="-10" width="180" height="18" rx="9" fill="#064e3b" stroke="#39d353" stroke-width="1"/>
      <text x="80" y="3" text-anchor="middle" font-size="9" font-weight="700" fill="#39d353" font-family="ui-monospace, monospace">&#10004; ALL 14 TARGETS PURGED [100%]</text>
    </g>

    <!-- Live Telemetry Badges Right -->
    <g transform="translate(710, 0)">
      <circle cx="0" cy="-3.5" r="3.5" fill="#22d3ee" class="status-led"/>
      <text x="8" y="0" font-family="ui-monospace, monospace" font-size="9.5" font-weight="600" fill="#22d3ee">PURGE: 14/14</text>
      <text x="120" y="0" text-anchor="end" font-family="ui-monospace, monospace" font-size="9" fill="#7d8590">ACCURACY: 100%</text>
    </g>
  </g>

  <!-- Month Headers -->
  <g transform="translate(0, 48)" font-size="10" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" fill="#7d8590">
    <text x="72" y="0">Nov</text>
    <text x="142" y="0">Dec</text>
    <text x="212" y="0">Jan</text>
    <text x="282" y="0">Feb</text>
    <text x="352" y="0">Mar</text>
    <text x="422" y="0">Apr</text>
    <text x="492" y="0">May</text>
    <text x="562" y="0">Jun</text>
    <text x="632" y="0">Jul</text>
    <text x="702" y="0">Aug</text>
    <text x="772" y="0">Sep</text>
    <text x="825" y="0">Oct</text>
    <text x="856" y="0">Nov</text>
  </g>

  <!-- Weekday Labels -->
  <g transform="translate(56, 0)" font-size="9" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" fill="#7d8590">
    <text x="0" y="70" text-anchor="end">Mon</text>
    <text x="0" y="98" text-anchor="end">Wed</text>
    <text x="0" y="126" text-anchor="end">Fri</text>
  </g>

  <!-- Radar Scanning Beam (Sweeps across the grid) -->
  <rect class="radar-scan" x="0" y="58" width="70" height="102" rx="4" fill="url(#radarGrad)"/>

  <!-- Contribution Grid Cells (ALL 14 Active Cells Targeted!) -->
  <g>
    {grid_markup}
  </g>

  <!-- Shockwaves -->
  {shockwave_str}

  <!-- Flying Plasma Bullets (Pure bullets, ZERO guide lines) -->
  {bullet_str}

  <!-- Debris Spark Explosions -->
  {explosion_str}

  <!-- Animated Impostor Sentry Character -->
  <g class="impostor-patrol">
    <g class="waddling-legs">
      <!-- Backpack -->
      <rect x="-9" y="-6" width="4.5" height="13" rx="2" fill="#991b1b" stroke="#450a0a" stroke-width="1.5"/>
      <!-- Body -->
      <path d="M -5 -9 C -5 -13, 5 -13, 5 -9 L 5 6 C 5 8, 4 8.5, 3 8.5 L 3 11 C 3 12.5, 1 12.5, 1 11 L 1 8 L -1 8 L -1 11 C -1 12.5, -3 12.5, -3 11 L -3 8.5 C -4 8.5, -5 8, -5 6 Z" fill="url(#impostorRedGrad)" stroke="#450a0a" stroke-width="1.8" stroke-linejoin="round"/>
      <!-- Visor -->
      <rect x="-1" y="-7.5" width="8.5" height="6.5" rx="3.2" fill="url(#visorGrad)" stroke="#450a0a" stroke-width="1.4"/>
      <ellipse cx="3.2" cy="-5.5" rx="2.2" ry="1.1" fill="#ffffff" opacity="0.85" transform="rotate(-10 3.2 -5.5)"/>
      <!-- Sparkle Star on Visor at Victory -->
      <g transform="translate(6, -6)" class="visor-sparkle">
        <polygon points="0,-4 1,-1 4,0 1,1 0,4 -1,1 -4,0 -1,-1" fill="#cffafe"/>
      </g>
      
      <!-- Blaster Plasma Cannon (Mounted on EXACT ROW CENTER y=0!) -->
      <g class="impostor-blaster">
        <rect x="0" y="-3.5" width="13" height="7" rx="1.5" fill="#1e293b" stroke="#0f172a" stroke-width="1.4"/>
        <rect x="13" y="-4" width="5" height="8" rx="1" fill="#475569" stroke="#0f172a" stroke-width="1.2"/>
        <line x1="8" y1="-3.5" x2="8" y2="3.5" stroke="#f97316" stroke-width="2"/>
        <circle cx="5" cy="0" r="1.8" fill="#22d3ee"/>
      </g>
    </g>
  </g>

  <!-- Bottom Footer Telemetry Bar -->
  <g transform="translate(72, 196)">
    <!-- Legend -->
    <g transform="translate(630, 0)">
      <text x="-26" y="8" fill="#7d8590" font-size="8.5" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif">Less</text>
      <rect x="0" y="0" width="9" height="9" rx="2" fill="#161b22"/>
      <rect x="13" y="0" width="9" height="9" rx="2" fill="#0e4429"/>
      <rect x="26" y="0" width="9" height="9" rx="2" fill="#006d32"/>
      <rect x="39" y="0" width="9" height="9" rx="2" fill="#26a641"/>
      <rect x="52" y="0" width="9" height="9" rx="2" fill="#39d353"/>
      <rect x="68" y="0" width="9" height="9" rx="2" fill="#ff4500" stroke="#ff8c00" stroke-width="0.8"/>
      <text x="82" y="8" fill="#ff4500" font-size="8.5" font-weight="700" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif">VAPORIZED &#128293;</text>
    </g>
  </g>
</svg>"""

ET.fromstring(svg)
print("PERFECTLY ROW-ALIGNED & VAPORIZING SENTRY VALIDATED AS 100% WELL-FORMED XML!")

with open("C:/Users/sahas/.gemini/antigravity/scratch/thenudasahas2008/assets/among-us-sentry-fire.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print("Saved to assets/among-us-sentry-fire.svg successfully!")
