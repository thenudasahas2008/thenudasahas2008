import xml.etree.ElementTree as ET

TOTAL_DUR = 18.0

# 14 Real Active Blocks from GitHub 2026 Calendar (EXACT pixel match to Image 2!)
# Formulas: bx = 72 + week * 14, by = 62 + weekday * 14
# Centers: tx = bx + 5, ty = by + 5
shots = [
    # Phase 1: Oct 16 (Week 41, Fri: by=132, ty=137) & Oct 23 (Week 42, Fri: by=132, ty=137)
    {"id": 1,  "t_fire": 0.9,  "im_pos": (530, 137), "tx": 651, "ty": 137, "bx": 646, "by": 132, "orig_color": "#40c463"},
    {"id": 2,  "t_fire": 1.8,  "im_pos": (530, 137), "tx": 665, "ty": 137, "bx": 660, "by": 132, "orig_color": "#9be9a8"},

    # Phase 2: Oct 21 (Week 42, Wed: by=104, ty=109)
    {"id": 3,  "t_fire": 3.0,  "im_pos": (560, 109), "tx": 665, "ty": 109, "bx": 660, "by": 104, "orig_color": "#216e39"},

    # Phase 3: Nov 2-4 (Week 44: Mon by=76, Tue by=90, Wed by=104) & Nov 7 (Sat: by=146, ty=151)
    {"id": 4,  "t_fire": 4.2,  "im_pos": (590, 81),  "tx": 693, "ty": 81,  "bx": 688, "by": 76,  "orig_color": "#40c463"},
    {"id": 5,  "t_fire": 5.2,  "im_pos": (590, 95),  "tx": 693, "ty": 95,  "bx": 688, "by": 90,  "orig_color": "#9be9a8"},
    {"id": 6,  "t_fire": 6.2,  "im_pos": (590, 109), "tx": 693, "ty": 109, "bx": 688, "by": 104, "orig_color": "#9be9a8"},
    {"id": 7,  "t_fire": 7.2,  "im_pos": (590, 151), "tx": 693, "ty": 151, "bx": 688, "by": 146, "orig_color": "#9be9a8"},

    # Phase 4: Nov 10 (Week 45, Tue: by=90, ty=95) & Nov 14 (Week 45, Sat: by=146, ty=151)
    {"id": 8,  "t_fire": 8.4,  "im_pos": (620, 95),  "tx": 707, "ty": 95,  "bx": 702, "by": 90,  "orig_color": "#9be9a8"},
    {"id": 9,  "t_fire": 9.4,  "im_pos": (620, 151), "tx": 707, "ty": 151, "bx": 702, "by": 146, "orig_color": "#216e39"},

    # Phase 5: Nov 15-20 (Week 46: Sun by=62, Mon by=76, Tue by=90, Thu by=118, Fri by=132)
    {"id": 10, "t_fire": 10.6, "im_pos": (640, 67),  "tx": 721, "ty": 67,  "bx": 716, "by": 62,  "orig_color": "#9be9a8"},
    {"id": 11, "t_fire": 11.5, "im_pos": (640, 81),  "tx": 721, "ty": 81,  "bx": 716, "by": 76,  "orig_color": "#9be9a8"},
    {"id": 12, "t_fire": 12.4, "im_pos": (640, 95),  "tx": 721, "ty": 95,  "bx": 716, "by": 90,  "orig_color": "#40c463"},
    {"id": 13, "t_fire": 13.3, "im_pos": (640, 123), "tx": 721, "ty": 123, "bx": 716, "by": 118, "orig_color": "#216e39"},
    {"id": 14, "t_fire": 14.2, "im_pos": (640, 137), "tx": 721, "ty": 137, "bx": 716, "by": 132, "orig_color": "#216e39"},
]

def pct(t):
    return f"{(t / TOTAL_DUR) * 100:.2f}%"

css_lines = []

# 1. Impostor Movement: Stance Transitions
css_lines.append(f"""
@keyframes impostorPatrolPath {{
  0%, {pct(2.3)}      {{ transform: translate(530px, 137px); }}
  {pct(2.6)}, {pct(3.6)}  {{ transform: translate(560px, 109px); }}
  {pct(3.9)}, {pct(4.7)}  {{ transform: translate(590px, 81px); }}
  {pct(4.9)}, {pct(5.7)}  {{ transform: translate(590px, 95px); }}
  {pct(5.9)}, {pct(6.7)}  {{ transform: translate(590px, 109px); }}
  {pct(6.9)}, {pct(7.8)}  {{ transform: translate(590px, 151px); }}
  {pct(8.0)}, {pct(8.9)}  {{ transform: translate(620px, 95px); }}
  {pct(9.1)}, {pct(10.0)} {{ transform: translate(620px, 151px); }}
  {pct(10.2)}, {pct(11.0)} {{ transform: translate(640px, 67px); }}
  {pct(11.2)}, {pct(12.0)} {{ transform: translate(640px, 81px); }}
  {pct(12.1)}, {pct(12.9)} {{ transform: translate(640px, 95px); }}
  {pct(13.0)}, {pct(13.8)} {{ transform: translate(640px, 123px); }}
  {pct(13.9)}, {pct(14.8)} {{ transform: translate(640px, 137px); }}
  {pct(15.2)}              {{ transform: translate(640px, 95px); }}
  {pct(15.6)}              {{ transform: translate(640px, 75px) rotate(-10deg); }}
  {pct(16.0)}              {{ transform: translate(640px, 68px) rotate(360deg); }}
  {pct(16.6)}              {{ transform: translate(640px, 95px); }}
  {pct(17.5)}, 100%        {{ transform: translate(530px, 137px); }}
}}
.impostor-patrol {{ animation: impostorPatrolPath {TOTAL_DUR}s ease-in-out infinite; }}
""")

# 2. Waddling legs
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

# 4. Bullets, Muzzle Flash, Shockwaves, and Sparks
for s in shots:
    sid = s["id"]
    tf = s["t_fire"]
    t_impact = tf + 0.10
    gx = s["im_pos"][0] + 18
    gy = s["im_pos"][1]
    tx = s["tx"]
    ty = s["ty"]

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

    # Plasma bullet
    css_lines.append(f"""
@keyframes flyBullet{sid} {{
  0%, {pct(tf - 0.01)} {{ opacity: 0; transform: translate({gx}px, {gy}px) scale(0.4); }}
  {pct(tf)} {{ opacity: 1; transform: translate({gx}px, {gy}px) scale(1.0); }}
  {pct(t_impact)} {{ opacity: 1; transform: translate({tx}px, {ty}px) scale(1.1); }}
  {pct(t_impact + 0.03)}, 100% {{ opacity: 0; transform: translate({tx}px, {ty}px); }}
}}
.bullet-{sid} {{ animation: flyBullet{sid} {TOTAL_DUR}s linear infinite; }}
""")

    # Shockwave
    css_lines.append(f"""
@keyframes shockwave{sid} {{
  0%, {pct(t_impact - 0.01)} {{ opacity: 0; transform: translate({tx}px, {ty}px) scale(0.2); }}
  {pct(t_impact)} {{ opacity: 1; transform: translate({tx}px, {ty}px) scale(0.5); }}
  {pct(t_impact + 0.22)} {{ opacity: 0; transform: translate({tx}px, {ty}px) scale(2.2); }}
  100% {{ opacity: 0; }}
}}
.shockwave-{sid} {{ animation: shockwave{sid} {TOTAL_DUR}s ease-out infinite; }}
""")

    # Spark explosion
    css_lines.append(f"""
@keyframes sparkExplosion{sid} {{
  0%, {pct(t_impact - 0.01)} {{ opacity: 0; transform: translate({tx}px, {ty}px) scale(0); }}
  {pct(t_impact)} {{ opacity: 1; transform: translate({tx}px, {ty}px) scale(1.0); }}
  {pct(t_impact + 0.20)} {{ opacity: 0; transform: translate({tx}px, {ty}px) scale(1.8) rotate(35deg); }}
  100% {{ opacity: 0; }}
}}
.detonation-{sid} {{ animation: sparkExplosion{sid} {TOTAL_DUR}s ease-out infinite; }}
""")

    # Target block vaporize & burn dissipation
    t_end = 17.5
    orig_c = s["orig_color"]
    css_lines.append(f"""
@keyframes targetBurn{sid} {{
  0%, {pct(t_impact)} {{ fill: {orig_c}; stroke: none; }}
  {pct(t_impact + 0.02)} {{ fill: #ffffff; stroke: #ffea00; stroke-width: 1.5; }}
  {pct(t_impact + 0.08)} {{ fill: #ff4500; stroke: #ff8c00; stroke-width: 1.0; }}
  {pct(t_impact + 0.35)} {{ fill: #7f1d1d; stroke: none; }}
  {pct(t_impact + 0.55)}, {pct(t_end)} {{ fill: #161b22; stroke: none; }}
  {pct(t_end + 0.2)}, 100% {{ fill: {orig_c}; stroke: none; }}
}}
.target-block-{sid} {{ animation: targetBurn{sid} {TOTAL_DUR}s ease-out infinite; }}
""")

# Radar scan animation
css_lines.append(f"""
@keyframes radarSweep {{
  0%   {{ transform: translateX(0px); opacity: 0.1; }}
  50%  {{ opacity: 0.6; }}
  100% {{ transform: translateX(810px); opacity: 0.1; }}
}}
.radar-scan {{ animation: radarSweep 7.0s linear infinite; }}
""")

css_str = "\n".join(css_lines)

# Generate grid cells (53 weeks x 7 weekdays)
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

# Pure bullets, shockwaves, and spark debris
bullets = []
shockwaves = []
explosions = []

for s in shots:
    sid = s["id"]
    bullets.append(f"""
    <!-- Plasma Bullet {sid} -->
    <g class="bullet-{sid}" filter="url(#bulletGlow)">
      <ellipse cx="0" cy="0" rx="6" ry="2.2" fill="#ffffff" />
      <ellipse cx="-4" cy="0" rx="8" ry="1.8" fill="#22d3ee" opacity="0.8" />
      <ellipse cx="-10" cy="0" rx="6" ry="1.2" fill="#ff4500" opacity="0.6" />
    </g>""")

    shockwaves.append(f"""
    <!-- Shockwave Ring {sid} -->
    <circle class="shockwave-{sid}" cx="0" cy="0" r="10" fill="none" stroke="#22d3ee" stroke-width="2" />""")

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

  <!-- Month Headers (Calendar Year 2026: Jan to Dec matching Image 2!) -->
  <g transform="translate(0, 48)" font-size="10" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" fill="#7d8590">
    <text x="72" y="0">Jan</text>
    <text x="128" y="0">Feb</text>
    <text x="184" y="0">Mar</text>
    <text x="254" y="0">Apr</text>
    <text x="310" y="0">May</text>
    <text x="366" y="0">Jun</text>
    <text x="436" y="0">Jul</text>
    <text x="492" y="0">Aug</text>
    <text x="562" y="0">Sep</text>
    <text x="618" y="0">Oct</text>
    <text x="688" y="0">Nov</text>
    <text x="758" y="0">Dec</text>
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

# Validate SVG XML
ET.fromstring(svg)
print("SVG is 100% valid XML!")

with open(r"C:\Users\sahas\.gemini\antigravity\scratch\thenudasahas2008\assets\among-us-sentry-fire.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print("Saved perfectly synchronized among-us-sentry-fire.svg!")
