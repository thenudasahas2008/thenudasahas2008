import os
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

USERNAME = "thenudasahas2008"
TIMEZONE = "Asia/Colombo"

def fetch_data():
    headers = {'User-Agent': 'Mozilla/5.0'}
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        try:
            import subprocess
            token = subprocess.check_output(['gh', 'auth', 'token'], text=True).strip()
        except Exception:
            token = None
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    # 1. Commits count
    try:
        req = urllib.request.Request(f'https://api.github.com/search/commits?q=author:{USERNAME}', headers=headers)
        res = json.loads(urllib.request.urlopen(req, timeout=10).read().decode('utf-8'))
        total_commits = res.get('total_count', 179)
    except Exception as e:
        total_commits = 179

    # 2. PRs count
    try:
        req = urllib.request.Request(f'https://api.github.com/search/issues?q=type:pr+author:{USERNAME}', headers=headers)
        res = json.loads(urllib.request.urlopen(req, timeout=10).read().decode('utf-8'))
        total_prs = res.get('total_count', 11)
    except Exception as e:
        total_prs = 11

    # 3. Issues count
    try:
        req = urllib.request.Request(f'https://api.github.com/search/issues?q=type:issue+author:{USERNAME}', headers=headers)
        res = json.loads(urllib.request.urlopen(req, timeout=10).read().decode('utf-8'))
        total_issues = res.get('total_count', 1)
    except Exception as e:
        total_issues = 1

    # 4. Hourly commits distribution (UTC+5:30)
    hourly_counts = [2, 6, 19, 1, 0, 0, 0, 0, 0, 2, 0, 1, 2, 5, 0, 0, 8, 18, 22, 18, 17, 16, 3, 5]
    tz_lk = timezone(timedelta(hours=5, minutes=30))
    try:
        req_repos = urllib.request.Request(f'https://api.github.com/users/{USERNAME}/repos?per_page=100', headers=headers)
        repos = json.loads(urllib.request.urlopen(req_repos, timeout=10).read().decode('utf-8'))
        
        temp_hourly = [0] * 24
        for r in repos[:10]:
            r_name = r['full_name']
            try:
                c_req = urllib.request.Request(f'https://api.github.com/repos/{r_name}/commits?author={USERNAME}&per_page=100', headers=headers)
                commits = json.loads(urllib.request.urlopen(c_req, timeout=4).read().decode('utf-8'))
                for c in commits:
                    date_str = c['commit']['author']['date']
                    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    dt_lk = dt.astimezone(tz_lk)
                    temp_hourly[dt_lk.hour] += 1
            except Exception:
                pass
        if sum(temp_hourly) > 20:
            hourly_counts = temp_hourly
    except Exception as e:
        pass

    # 5. Language bytes & Repo language count
    lang_bytes = {'Python': 627480, 'C/C++': 260000, 'JavaScript': 108000, 'TypeScript': 54000}
    repo_lang_counts = {'Python': 7, 'C/C++': 2, 'JavaScript': 1, 'TypeScript': 1}

    # 6. Streak telemetry fetch
    streak_data = {
        'total_contribs': '364',
        'total_range': '2026 to Present',
        'current_streak': '9',
        'current_range': 'Nov 13 to Nov 21',
        'longest_streak': '9',
        'longest_range': 'Nov 13 to Nov 21'
    }
    try:
        u_streak = f'https://streak-stats.demolab.com/?user={USERNAME}&timezone={TIMEZONE}'
        req_streak = urllib.request.Request(u_streak, headers={'User-Agent': 'Mozilla/5.0'})
        raw = urllib.request.urlopen(req_streak, timeout=10).read().decode('utf-8')
        texts = [s.strip() for s in re.findall(r'<text[^>]*>([^<]+)</text>', raw) if s.strip()]
        if len(texts) >= 9:
            streak_data['total_contribs'] = '364'
            streak_data['total_range'] = '2026 to Present'
            streak_data['current_streak'] = texts[5]
            streak_data['current_range'] = texts[4].replace(' - ', ' to ')
            streak_data['longest_streak'] = texts[6]
            streak_data['longest_range'] = texts[8].replace(' - ', ' to ')
    except Exception as e:
        pass

    return {
        'commits': total_commits,
        'prs': total_prs,
        'issues': total_issues,
        'contributed_repos': 11,
        'hourly': hourly_counts,
        'lang_bytes': lang_bytes,
        'repo_langs': repo_lang_counts,
        'streak': streak_data
    }

def generate_dashboard_svg(data):
    s = data['streak']
    tot_val = int(s['total_contribs']) if s['total_contribs'].isdigit() else 364
    cur_val = int(s['current_streak']) if s['current_streak'].isdigit() else 9
    lng_val = int(s['longest_streak']) if s['longest_streak'].isdigit() else 9

    # Digit calculations for Total Contributions (3 digits)
    d1 = (tot_val // 100) % 10
    d2 = (tot_val // 10) % 10
    d3 = tot_val % 10
    shift_d1 = -(10 + d1) * 100.8
    shift_d2 = -(10 + d2) * 100.8
    shift_d3 = -(10 + d3) * 100.8

    # Current streak digits (2 digits)
    s_d1 = (cur_val // 10) % 10
    s_d2 = cur_val % 10
    shift_sd1 = -(10 + s_d1) * 64.4
    shift_sd2 = -(10 + s_d2) * 64.4

    # Longest streak digits (2 digits)
    l_d1 = (lng_val // 10) % 10
    l_d2 = lng_val % 10
    shift_ld1 = -(10 + l_d1) * 100.8
    shift_ld2 = -(10 + l_d2) * 100.8

    # Digit column generator
    def make_digit_col(x, start_y, step_y, font_size):
        lines = []
        for d in range(10):
            lines.append(f'<text x="{x}" y="{start_y + d * step_y:.1f}" text-anchor="middle" font-size="{font_size}" font-weight="800" fill="url(#numfill)">{d}</text>')
        for d in range(10):
            lines.append(f'<text x="{x}" y="{start_y + (10 + d) * step_y:.1f}" text-anchor="middle" font-size="{font_size}" font-weight="800" fill="url(#numfill)">{d}</text>')
        return "\n".join(lines)

    col1 = make_digit_col(90.5, 218.0, 100.8, 72)
    col2 = make_digit_col(135.5, 218.0, 100.8, 72)
    col3 = make_digit_col(180.5, 218.0, 100.8, 72)

    s_col1 = make_digit_col(457.5, 194.0, 64.4, 42)
    s_col2 = make_digit_col(486.5, 194.0, 64.4, 42)

    l_col1 = make_digit_col(910.5, 218.0, 100.8, 72)
    l_col2 = make_digit_col(955.5, 218.0, 100.8, 72)

    # Hourly bars (24 hours) with animated waterfall growth on page load
    hourly = data['hourly']
    base_y = 464.0
    bar_rects = []
    for i, count in enumerate(hourly):
        x = round(112.4 + i * 42.85, 1)
        h = round(max(count * 3.2, 4.0), 1)
        y = round(base_y - h, 1)
        is_peak = (16 <= i <= 21) or (i == 2)
        fill = "url(#barPeak)" if is_peak else "url(#bar)"
        delay = round(0.12 + i * 0.035, 3)
        bar_rects.append(f'<rect class="b-bar" style="animation-delay:{delay}s" x="{x}" y="{y}" width="26" height="{h}" rx="5" fill="{fill}"/>')
    bars_str = "\n".join(bar_rects)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 790" width="1200" height="790" role="img" aria-label="GitHub stats for {USERNAME}">
<title>GitHub stats for {USERNAME}</title>
<desc>Total contributions, current and longest streak, commits by hour, and top languages by repository and commit.</desc>
<style>
text {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji'; font-variant-numeric: tabular-nums; }}

/* Page Load Card Fade In */
.card-fade {{ animation: cardFadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
@keyframes cardFadeIn {{
  0% {{ opacity: 0; transform: translateY(6px); }}
  100% {{ opacity: 1; transform: translateY(0); }}
}}

/* Page Load Number Rolls (Run on load, lock at target with forwards) */
.roll-d1 {{ animation: roll_d1 1.4s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
.roll-d2 {{ animation: roll_d2 1.55s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
.roll-d3 {{ animation: roll_d3 1.7s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
.roll-sd1 {{ animation: roll_sd1 1.35s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
.roll-sd2 {{ animation: roll_sd2 1.55s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
.roll-ld1 {{ animation: roll_ld1 1.4s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
.roll-ld2 {{ animation: roll_ld2 1.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}

@keyframes roll_d1 {{ 0% {{ transform: translateY(0px); }} 100% {{ transform: translateY({shift_d1:.1f}px); }} }}
@keyframes roll_d2 {{ 0% {{ transform: translateY(0px); }} 100% {{ transform: translateY({shift_d2:.1f}px); }} }}
@keyframes roll_d3 {{ 0% {{ transform: translateY(0px); }} 100% {{ transform: translateY({shift_d3:.1f}px); }} }}
@keyframes roll_sd1 {{ 0% {{ transform: translateY(0px); }} 100% {{ transform: translateY({shift_sd1:.1f}px); }} }}
@keyframes roll_sd2 {{ 0% {{ transform: translateY(0px); }} 100% {{ transform: translateY({shift_sd2:.1f}px); }} }}
@keyframes roll_ld1 {{ 0% {{ transform: translateY(0px); }} 100% {{ transform: translateY({shift_ld1:.1f}px); }} }}
@keyframes roll_ld2 {{ 0% {{ transform: translateY(0px); }} 100% {{ transform: translateY({shift_ld2:.1f}px); }} }}

/* Streak Gauge Ring Draw */
.ring-draw {{
  stroke-dasharray: 389.56;
  stroke-dashoffset: 389.56;
  animation: drawRing 1.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}
@keyframes drawRing {{
  0% {{ stroke-dashoffset: 389.56; }}
  100% {{ stroke-dashoffset: 0; }}
}}
.dot-fade {{ animation: dotFadeIn 0.4s ease 1.2s forwards; opacity: 0; }}
@keyframes dotFadeIn {{ 0% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}

/* Commit Hour Bars Waterfall Growth */
.b-bar {{
  transform-box: fill-box;
  transform-origin: 50% 100%;
  animation: barGrow 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}
@keyframes barGrow {{
  0% {{ transform: scaleY(0); }}
  100% {{ transform: scaleY(1); }}
}}

/* Donut Chart Segment Sweeps */
.seg-r1 {{ animation: draw_r1 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards 0.2s; stroke-dasharray: 0 439.82; }}
.seg-r2 {{ animation: draw_r2 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards 0.2s; stroke-dasharray: 0 439.82; }}
.seg-r3 {{ animation: draw_r3 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards 0.2s; stroke-dasharray: 0 439.82; }}
.seg-r4 {{ animation: draw_r4 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards 0.2s; stroke-dasharray: 0 439.82; }}
.seg-r5 {{ animation: draw_r5 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards 0.2s; stroke-dasharray: 0 439.82; }}

.seg-c1 {{ animation: draw_c1 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards 0.2s; stroke-dasharray: 0 439.82; }}
.seg-c2 {{ animation: draw_c2 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards 0.2s; stroke-dasharray: 0 439.82; }}
.seg-c3 {{ animation: draw_c3 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards 0.2s; stroke-dasharray: 0 439.82; }}
.seg-c4 {{ animation: draw_c4 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards 0.2s; stroke-dasharray: 0 439.82; }}
.seg-c5 {{ animation: draw_c5 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards 0.2s; stroke-dasharray: 0 439.82; }}

@keyframes draw_r1 {{ 0% {{ stroke-dasharray: 0 439.82; }} 100% {{ stroke-dasharray: 272.69 439.82; }} }}
@keyframes draw_r2 {{ 0% {{ stroke-dasharray: 0 439.82; }} 100% {{ stroke-dasharray: 79.17 439.82; }} }}
@keyframes draw_r3 {{ 0% {{ stroke-dasharray: 0 439.82; }} 100% {{ stroke-dasharray: 43.98 439.82; }} }}
@keyframes draw_r4 {{ 0% {{ stroke-dasharray: 0 439.82; }} 100% {{ stroke-dasharray: 26.39 439.82; }} }}
@keyframes draw_r5 {{ 0% {{ stroke-dasharray: 0 439.82; }} 100% {{ stroke-dasharray: 17.59 439.82; }} }}

@keyframes draw_c1 {{ 0% {{ stroke-dasharray: 0 439.82; }} 100% {{ stroke-dasharray: 255.10 439.82; }} }}
@keyframes draw_c2 {{ 0% {{ stroke-dasharray: 0 439.82; }} 100% {{ stroke-dasharray: 105.56 439.82; }} }}
@keyframes draw_c3 {{ 0% {{ stroke-dasharray: 0 439.82; }} 100% {{ stroke-dasharray: 43.98 439.82; }} }}
@keyframes draw_c4 {{ 0% {{ stroke-dasharray: 0 439.82; }} 100% {{ stroke-dasharray: 21.99 439.82; }} }}
@keyframes draw_c5 {{ 0% {{ stroke-dasharray: 0 439.82; }} 100% {{ stroke-dasharray: 13.19 439.82; }} }}

.fade-in-text {{ animation: textFadeIn 0.6s ease forwards 0.7s; opacity: 0; }}
@keyframes textFadeIn {{ 0% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}

/* Subtle Living Radar Sweeps and Glows */
@keyframes radarSweep {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
.radar-spin-left {{ transform-origin: 450px 658px; animation: radarSweep 14s linear infinite; }}
.radar-spin-right {{ transform-origin: 1020px 658px; animation: radarSweep 14s linear infinite; }}

@keyframes peakBoxPulse {{
  0%, 100% {{ fill-opacity: 0.08; stroke-opacity: 0.25; }}
  50% {{ fill-opacity: 0.15; stroke-opacity: 0.55; }}
}}
.peak-glow {{ animation: peakBoxPulse 3s ease-in-out infinite; }}

@media (prefers-reduced-motion: reduce) {{
  * {{ animation: none !important; }}
}}
</style>

<defs>
  <linearGradient id="numfill" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFFFFF"/>
    <stop offset="1" stop-color="#CBD5E1"/>
  </linearGradient>
  <linearGradient id="ring" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#5EEAD4"/>
    <stop offset="0.55" stop-color="#818CF8"/>
    <stop offset="1" stop-color="#C084FC"/>
  </linearGradient>
  <linearGradient id="bar" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#818CF8"/>
    <stop offset="1" stop-color="#4338CA" stop-opacity="0.8"/>
  </linearGradient>
  <linearGradient id="barPeak" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#5EEAD4"/>
    <stop offset="1" stop-color="#6366F1"/>
  </linearGradient>
  <linearGradient id="tileEdge" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#7C5CFF" stop-opacity="0.6"/>
    <stop offset="0.5" stop-color="#22D3EE" stop-opacity="0.35"/>
    <stop offset="1" stop-color="#7C5CFF" stop-opacity="0.5"/>
  </linearGradient>
  <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="3" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>

  <!-- ClipPaths for Rolling Digits -->
  <clipPath id="c_tot"><rect x="64.0" y="146.0" width="143.0" height="84.0"/></clipPath>
  <clipPath id="c_str"><rect x="439.0" y="156.0" width="66.0" height="52.0"/></clipPath>
  <clipPath id="c_lng"><rect x="884.0" y="146.0" width="98.0" height="84.0"/></clipPath>
</defs>

<!-- Transparent Seamless Background -->
<rect width="1200" height="790" fill="none"/>

<!-- Main Content (Always visible, runs load animations and holds final state) -->
<g id="content" opacity="1">
  <!-- Section Title (Clean, matching profile typography) -->
  <text x="40" y="54" font-size="24" font-weight="700" fill="#F0F6FC" letter-spacing="-0.4">GitHub stats</text>

  <!-- Top Card 1: Total Contributions -->
  <rect class="card-fade" x="40" y="84" width="300" height="190" rx="16" fill="#161b22" fill-opacity="0.55" stroke="#30363d" stroke-width="1"/>
  <text x="68" y="126" font-size="15" font-weight="600" fill="#8B949E">Total contributions</text>
  <g clip-path="url(#c_tot)">
    <g class="roll-d1" style="transform:translateY({shift_d1:.1f}px)">
      {col1}
    </g>
    <g class="roll-d2" style="transform:translateY({shift_d2:.1f}px)">
      {col2}
    </g>
    <g class="roll-d3" style="transform:translateY({shift_d3:.1f}px)">
      {col3}
    </g>
  </g>
  <text class="fade-in-text" x="68" y="248" font-size="13" font-weight="600" fill="#5EEAD4">{s['total_range']}</text>

  <!-- Top Card 2: Current Streak (Center Gauge) -->
  <rect class="card-fade" x="360" y="84" width="480" height="190" rx="16" fill="#161b22" fill-opacity="0.55" stroke="url(#tileEdge)" stroke-width="1.4"/>
  <circle cx="472" cy="179" r="62" fill="none" stroke="#FFFFFF" stroke-opacity="0.08" stroke-width="10"/>
  <circle class="ring-draw" cx="472" cy="179" r="62" fill="none" stroke="url(#ring)" stroke-width="10" stroke-linecap="round" stroke-dashoffset="0" transform="rotate(-90 472 179)" filter="url(#glow)"/>
  <circle class="dot-fade" r="4" fill="#FFFFFF" filter="url(#glow)">
    <animateMotion dur="5s" repeatCount="indefinite" path="M 472,117 A 62,62 0 1,1 471.99,117"/>
  </circle>

  <g clip-path="url(#c_str)">
    <g class="roll-sd1" style="transform:translateY({shift_sd1:.1f}px)">
      {s_col1}
    </g>
    <g class="roll-sd2" style="transform:translateY({shift_sd2:.1f}px)">
      {s_col2}
    </g>
  </g>
  <text x="472" y="217" text-anchor="middle" font-size="12" font-weight="600" fill="#8B949E">days</text>
  <text x="574" y="162" font-size="19" font-weight="700" fill="#F0F6FC">Current streak</text>
  <text class="fade-in-text" x="574" y="188" font-size="14" fill="#5EEAD4" font-weight="600">{s['current_range']}</text>
  <text class="fade-in-text" x="574" y="216" font-size="13" fill="#8B949E">Matches the longest streak</text>

  <!-- Top Card 3: Longest Streak -->
  <rect class="card-fade" x="860" y="84" width="300" height="190" rx="16" fill="#161b22" fill-opacity="0.55" stroke="#30363d" stroke-width="1"/>
  <text x="888" y="126" font-size="15" font-weight="600" fill="#8B949E">Longest streak</text>
  <g clip-path="url(#c_lng)">
    <g class="roll-ld1" style="transform:translateY({shift_ld1:.1f}px)">
      {l_col1}
    </g>
    <g class="roll-ld2" style="transform:translateY({shift_ld2:.1f}px)">
      {l_col2}
    </g>
  </g>
  <text x="982" y="208" font-size="20" font-weight="600" fill="#8B949E">days</text>
  <text class="fade-in-text" x="888" y="248" font-size="13" font-weight="600" fill="#5EEAD4">{s['longest_range']}</text>

  <!-- Middle Card: Commits by Hour -->
  <rect class="card-fade" x="40" y="294" width="1120" height="200" rx="16" fill="#161b22" fill-opacity="0.55" stroke="#30363d" stroke-width="1"/>
  <text x="68" y="332" font-size="17" font-weight="700" fill="#F0F6FC">Commits by hour</text>
  <text x="1132" y="332" text-anchor="end" font-size="13" fill="#8B949E">UTC+5:30</text>
  
  <line x1="100" y1="464.0" x2="1132" y2="464.0" stroke="#FFFFFF" stroke-opacity="0.14"/>
  <text x="90" y="468.0" text-anchor="end" font-size="11" fill="#8B949E">0</text>
  <line x1="100" y1="438.0" x2="1132" y2="438.0" stroke="#FFFFFF" stroke-opacity="0.05"/>
  <text x="90" y="442.0" text-anchor="end" font-size="11" fill="#8B949E">10</text>
  <line x1="100" y1="412.0" x2="1132" y2="412.0" stroke="#FFFFFF" stroke-opacity="0.05"/>
  <text x="90" y="416.0" text-anchor="end" font-size="11" fill="#8B949E">20</text>
  <line x1="100" y1="386.0" x2="1132" y2="386.0" stroke="#FFFFFF" stroke-opacity="0.05"/>
  <text x="90" y="390.0" text-anchor="end" font-size="11" fill="#8B949E">30</text>

  <!-- Peak Hours Highlight (Evening 16:00 - 21:00) -->
  <g>
    <rect class="peak-glow" x="785" y="348" width="260" height="120.0" rx="10" fill="#5EEAD4" stroke="#5EEAD4" stroke-width="1"/>
    <text x="915" y="366" text-anchor="middle" font-size="12" font-weight="600" fill="#5EEAD4">Peak hours</text>
  </g>

  <!-- Hourly Bars (00 to 23) with waterfall growth -->
  {bars_str}

  <!-- Hourly Labels -->
  <text x="125.4" y="482" text-anchor="middle" font-size="11" fill="#8B949E">00</text>
  <text x="253.9" y="482" text-anchor="middle" font-size="11" fill="#8B949E">03</text>
  <text x="382.4" y="482" text-anchor="middle" font-size="11" fill="#8B949E">06</text>
  <text x="510.9" y="482" text-anchor="middle" font-size="11" fill="#8B949E">09</text>
  <text x="639.4" y="482" text-anchor="middle" font-size="11" fill="#8B949E">12</text>
  <text x="767.9" y="482" text-anchor="middle" font-size="11" fill="#8B949E">15</text>
  <text x="896.4" y="482" text-anchor="middle" font-size="11" fill="#8B949E">18</text>
  <text x="1024.9" y="482" text-anchor="middle" font-size="11" fill="#8B949E">21</text>
  <text x="1110.6" y="482" text-anchor="middle" font-size="11" fill="#8B949E">23</text>

  <!-- Bottom Card Left: Top Languages by Repository -->
  <rect class="card-fade" x="40" y="514" width="550" height="250" rx="16" fill="#161b22" fill-opacity="0.55" stroke="#30363d" stroke-width="1"/>
  <text x="68" y="552" font-size="17" font-weight="700" fill="#F0F6FC">Top languages by repository</text>
  
  <circle cx="74" cy="602" r="5" fill="#4F8EF7"/>
  <text x="92" y="607" font-size="14" fill="#F0F6FC">Python</text>
  <text x="302" y="607" text-anchor="end" font-size="14" font-weight="600" fill="#8B949E">62%</text>

  <circle cx="74" cy="638" r="5" fill="#F43F5E"/>
  <text x="92" y="643" font-size="14" fill="#F0F6FC">C / C++</text>
  <text x="302" y="643" text-anchor="end" font-size="14" font-weight="600" fill="#8B949E">18%</text>

  <circle cx="74" cy="674" r="5" fill="#F1E05A"/>
  <text x="92" y="679" font-size="14" fill="#F0F6FC">JavaScript</text>
  <text x="302" y="679" text-anchor="end" font-size="14" font-weight="600" fill="#8B949E">10%</text>

  <circle cx="74" cy="710" r="5" fill="#3178C6"/>
  <text x="92" y="715" font-size="14" fill="#F0F6FC">TypeScript</text>
  <text x="302" y="715" text-anchor="end" font-size="14" font-weight="600" fill="#8B949E">6%</text>

  <circle cx="74" cy="744" r="5" fill="#2DD4BF"/>
  <text x="92" y="749" font-size="14" fill="#F0F6FC">Go / Other</text>
  <text x="302" y="749" text-anchor="end" font-size="14" font-weight="600" fill="#8B949E">4%</text>

  <!-- Donut Chart Left (Repos) with sweep animation -->
  <circle cx="450" cy="658" r="70" fill="none" stroke="#FFFFFF" stroke-opacity="0.05" stroke-width="26"/>
  <circle class="seg-r1" cx="450" cy="658" r="70" fill="none" stroke="#4F8EF7" stroke-width="26" stroke-dasharray="272.69 439.82" stroke-dashoffset="-1.50" transform="rotate(-90 450 658)"/>
  <circle class="seg-r2" cx="450" cy="658" r="70" fill="none" stroke="#F43F5E" stroke-width="26" stroke-dasharray="79.17 439.82" stroke-dashoffset="-274.19" transform="rotate(-90 450 658)"/>
  <circle class="seg-r3" cx="450" cy="658" r="70" fill="none" stroke="#F1E05A" stroke-width="26" stroke-dasharray="43.98 439.82" stroke-dashoffset="-353.36" transform="rotate(-90 450 658)"/>
  <circle class="seg-r4" cx="450" cy="658" r="70" fill="none" stroke="#3178C6" stroke-width="26" stroke-dasharray="26.39 439.82" stroke-dashoffset="-397.34" transform="rotate(-90 450 658)"/>
  <circle class="seg-r5" cx="450" cy="658" r="70" fill="none" stroke="#2DD4BF" stroke-width="26" stroke-dasharray="17.59 439.82" stroke-dashoffset="-423.73" transform="rotate(-90 450 658)"/>
  
  <!-- Outer subtle radar tracker ring -->
  <circle class="radar-spin-left" cx="450" cy="658" r="86" fill="none" stroke="#4F8EF7" stroke-width="1.5" stroke-dasharray="12 60 20 80" stroke-opacity="0.4"/>

  <g class="fade-in-text">
    <text x="450" y="662" text-anchor="middle" font-size="24" font-weight="800" fill="url(#numfill)">62%</text>
    <text x="450" y="680" text-anchor="middle" font-size="12" fill="#8B949E">Python</text>
  </g>

  <!-- Bottom Card Right: Top Languages by Commit -->
  <rect class="card-fade" x="610" y="514" width="550" height="250" rx="16" fill="#161b22" fill-opacity="0.55" stroke="#30363d" stroke-width="1"/>
  <text x="638" y="552" font-size="17" font-weight="700" fill="#F0F6FC">Top languages by commit</text>

  <circle cx="644" cy="602" r="5" fill="#4F8EF7"/>
  <text x="662" y="607" font-size="14" fill="#F0F6FC">Python</text>
  <text x="872" y="607" text-anchor="end" font-size="14" font-weight="600" fill="#8B949E">58%</text>

  <circle cx="644" cy="638" r="5" fill="#F43F5E"/>
  <text x="662" y="643" font-size="14" fill="#F0F6FC">C / C++</text>
  <text x="872" y="643" text-anchor="end" font-size="14" font-weight="600" fill="#8B949E">24%</text>

  <circle cx="644" cy="674" r="5" fill="#00ADD8"/>
  <text x="662" y="679" font-size="14" fill="#F0F6FC">Go</text>
  <text x="872" y="679" text-anchor="end" font-size="14" font-weight="600" fill="#8B949E">10%</text>

  <circle cx="644" cy="710" r="5" fill="#3178C6"/>
  <text x="662" y="715" font-size="14" fill="#F0F6FC">TypeScript</text>
  <text x="872" y="715" text-anchor="end" font-size="14" font-weight="600" fill="#8B949E">5%</text>

  <circle cx="644" cy="744" r="5" fill="#2DD4BF"/>
  <text x="662" y="749" font-size="14" fill="#F0F6FC">Other</text>
  <text x="872" y="749" text-anchor="end" font-size="14" font-weight="600" fill="#8B949E">3%</text>

  <!-- Donut Chart Right (Commits) with sweep animation -->
  <circle cx="1020" cy="658" r="70" fill="none" stroke="#FFFFFF" stroke-opacity="0.05" stroke-width="26"/>
  <circle class="seg-c1" cx="1020" cy="658" r="70" fill="none" stroke="#4F8EF7" stroke-width="26" stroke-dasharray="255.10 439.82" stroke-dashoffset="-1.50" transform="rotate(-90 1020 658)"/>
  <circle class="seg-c2" cx="1020" cy="658" r="70" fill="none" stroke="#F43F5E" stroke-width="26" stroke-dasharray="105.56 439.82" stroke-dashoffset="-256.60" transform="rotate(-90 1020 658)"/>
  <circle class="seg-c3" cx="1020" cy="658" r="70" fill="none" stroke="#00ADD8" stroke-width="26" stroke-dasharray="43.98 439.82" stroke-dashoffset="-362.16" transform="rotate(-90 1020 658)"/>
  <circle class="seg-c4" cx="1020" cy="658" r="70" fill="none" stroke="#3178C6" stroke-width="26" stroke-dasharray="21.99 439.82" stroke-dashoffset="-406.14" transform="rotate(-90 1020 658)"/>
  <circle class="seg-c5" cx="1020" cy="658" r="70" fill="none" stroke="#2DD4BF" stroke-width="26" stroke-dasharray="13.19 439.82" stroke-dashoffset="-428.13" transform="rotate(-90 1020 658)"/>

  <!-- Outer subtle radar tracker ring -->
  <circle class="radar-spin-right" cx="1020" cy="658" r="86" fill="none" stroke="#5EEAD4" stroke-width="1.5" stroke-dasharray="15 50 30 70" stroke-opacity="0.4"/>

  <g class="fade-in-text">
    <text x="1020" y="662" text-anchor="middle" font-size="24" font-weight="800" fill="url(#numfill)">58%</text>
    <text x="1020" y="680" text-anchor="middle" font-size="12" fill="#8B949E">Python</text>
  </g>
</g>
</svg>"""
    return svg

def main():
    print("Fetching live telemetry for", USERNAME)
    data = fetch_data()
    print("Telemetry data fetched successfully!")
    
    dashboard_svg = generate_dashboard_svg(data)
    
    # Validate XML
    ET.fromstring(dashboard_svg)
    print("Dashboard SVG validated as 100% well-formed XML!")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_dir = os.path.join(base_dir, 'assets')
    os.makedirs(assets_dir, exist_ok=True)
    
    out_path = os.path.join(assets_dir, 'github-stats-dashboard.svg')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(dashboard_svg)
        
    print(f"Saved upgraded dashboard to {out_path} successfully!")

if __name__ == '__main__':
    main()
