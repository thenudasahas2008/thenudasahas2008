import os
import json
import re
import urllib.request
import xml.etree.ElementTree as ET

USERNAME = "thenudasahas2008"
TIMEZONE = "Asia/Colombo"

def fetch_data():
    headers = {'User-Agent': 'Mozilla/5.0'}
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    # 1. Commits count
    try:
        req = urllib.request.Request(f'https://api.github.com/search/commits?q=author:{USERNAME}', headers=headers)
        res = json.loads(urllib.request.urlopen(req, timeout=10).read().decode('utf-8'))
        total_commits = res.get('total_count', 179)
    except Exception as e:
        print("Commits fetch fallback:", e)
        total_commits = 179

    # 2. PRs count
    try:
        req = urllib.request.Request(f'https://api.github.com/search/issues?q=type:pr+author:{USERNAME}', headers=headers)
        res = json.loads(urllib.request.urlopen(req, timeout=10).read().decode('utf-8'))
        total_prs = res.get('total_count', 11)
    except Exception as e:
        print("PRs fetch fallback:", e)
        total_prs = 11

    # 3. Issues count
    try:
        req = urllib.request.Request(f'https://api.github.com/search/issues?q=type:issue+author:{USERNAME}', headers=headers)
        res = json.loads(urllib.request.urlopen(req, timeout=10).read().decode('utf-8'))
        total_issues = res.get('total_count', 1)
    except Exception as e:
        print("Issues fetch fallback:", e)
        total_issues = 1

    # 4. Language bytes
    lang_bytes = {'JavaScript': 2187041, 'Python': 62748, 'HTML': 9261, 'Shell': 1812}
    try:
        req_repos = urllib.request.Request(f'https://api.github.com/users/{USERNAME}/repos?per_page=100', headers=headers)
        repos = json.loads(urllib.request.urlopen(req_repos, timeout=10).read().decode('utf-8'))
        temp_langs = {}
        for r in repos:
            l_url = r.get('languages_url')
            if l_url:
                try:
                    req_l = urllib.request.Request(l_url, headers=headers)
                    l_res = json.loads(urllib.request.urlopen(req_l, timeout=5).read().decode('utf-8'))
                    for name, count in l_res.items():
                        temp_langs[name] = temp_langs.get(name, 0) + count
                except Exception:
                    pass
        if temp_langs:
            lang_bytes = temp_langs
    except Exception as e:
        print("Repos fetch fallback:", e)

    filtered_langs = {k: v for k, v in lang_bytes.items() if k not in ['Procfile', 'Dockerfile']}
    tot = sum(filtered_langs.values()) or 1
    lang_items = []
    colors_map = {
        'JavaScript': '#f1e05a',
        'Python': '#3572A5',
        'HTML': '#e34c26',
        'Shell': '#89e051',
        'CSS': '#563d7c',
        'TypeScript': '#3178c6',
    }
    for name, cnt in sorted(filtered_langs.items(), key=lambda x: -x[1])[:4]:
        pct = (cnt / tot) * 100
        color = colors_map.get(name, '#58A6FF')
        # format bytes
        if cnt >= 1048576:
            size_str = f"{cnt / 1048576:.2f} MB"
        else:
            size_str = f"{cnt / 1024:.1f} KB"
        lang_items.append({'name': name, 'bytes': cnt, 'size_str': size_str, 'pct': pct, 'color': color})

    # 5. Streak telemetry fetch
    streak_data = {
        'total_contribs': '201',
        'total_range': 'Aug 19, 2025 - Present',
        'current_streak': '8',
        'current_range': 'Nov 13 - Nov 20',
        'longest_streak': '8',
        'longest_range': 'Nov 13 - Nov 20'
    }
    try:
        u_streak = f'https://streak-stats.demolab.com/?user={USERNAME}&timezone={TIMEZONE}'
        req_streak = urllib.request.Request(u_streak, headers={'User-Agent': 'Mozilla/5.0'})
        raw = urllib.request.urlopen(req_streak, timeout=10).read().decode('utf-8')
        texts = [s.strip() for s in re.findall(r'<text[^>]*>([^<]+)</text>', raw) if s.strip()]
        if len(texts) >= 9:
            # Demolab typical text array: ['201', 'Total Contributions', 'Aug 19, 2025 - Present', 'Current Streak', 'Nov 13 - Nov 20', '8', '8', 'Longest Streak', 'Nov 13 - Nov 20']
            streak_data['total_contribs'] = texts[0]
            streak_data['total_range'] = texts[2]
            streak_data['current_streak'] = texts[5]
            streak_data['current_range'] = texts[4]
            streak_data['longest_streak'] = texts[6]
            streak_data['longest_range'] = texts[8]
    except Exception as e:
        print("Streak fetch fallback:", e)

    return {
        'commits': total_commits,
        'prs': total_prs,
        'issues': total_issues,
        'contributed_repos': 7,
        'langs': lang_items,
        'streak': streak_data
    }

def generate_stats_svg(data):
    commits = data['commits']
    prs = data['prs']
    issues = data['issues']
    repos = data['contributed_repos']
    
    svg = f"""<svg width="495" height="195" viewBox="0 0 495 195" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgStats" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0e131f" />
      <stop offset="50%" stop-color="#0d1117" />
      <stop offset="100%" stop-color="#080c14" />
    </linearGradient>
    <linearGradient id="topGlow" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#22D3EE" stop-opacity="0" />
      <stop offset="25%" stop-color="#22D3EE" stop-opacity="0.9" />
      <stop offset="75%" stop-color="#58A6FF" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#58A6FF" stop-opacity="0" />
    </linearGradient>
    <style>
      .header {{ font: 700 16px -apple-system, BlinkMacSystemFont, 'Segoe UI', Ubuntu, sans-serif; fill: #58A6FF; letter-spacing: 0.3px; }}
      .subhead {{ font: 600 9.5px ui-monospace, SFMono-Regular, "Fira Code", monospace; fill: #7d8590; letter-spacing: 0.8px; }}
      .stat-label {{ font: 500 13px -apple-system, BlinkMacSystemFont, 'Segoe UI', Ubuntu, sans-serif; fill: #c9d1d9; }}
      .stat-val {{ font: 700 14px ui-monospace, SFMono-Regular, "Fira Code", monospace; fill: #ffffff; }}
      .octo-ring {{ animation: ringRotate 8s linear infinite; transform-origin: 418px 97px; }}
      .rank-pulse {{ animation: rankPulse 2s ease-in-out infinite; }}
      @keyframes ringRotate {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
      @keyframes rankPulse {{ 0%, 100% {{ opacity: 0.92; }} 50% {{ opacity: 1; filter: drop-shadow(0 0 5px rgba(34, 211, 238, 0.7)); }} }}
    </style>
  </defs>

  <!-- Container Box -->
  <rect x="0.5" y="0.5" width="494" height="194" rx="8" fill="url(#bgStats)" stroke="#30363d" stroke-width="1.2" />
  <!-- Neon Accent Line Top -->
  <line x1="12" y1="1" x2="483" y2="1" stroke="url(#topGlow)" stroke-width="2.2" />

  <!-- Title and Subtitle -->
  <g transform="translate(24, 32)">
    <text x="0" y="0" class="header">Thenuda Sahas' GitHub Stats</text>
    <text x="0" y="16" class="subhead">REAL-TIME TELEMETRY // DFIR and DEV OPS</text>
  </g>

  <!-- Stats Rows -->
  <g transform="translate(24, 76)">
    <!-- Total Commits -->
    <g transform="translate(0, 0)">
      <circle cx="7" cy="7" r="7" fill="#161b22" stroke="#22D3EE" stroke-width="1" />
      <path d="M4.5 7h5M7 4.5v5" stroke="#22D3EE" stroke-width="1.2" stroke-linecap="round" />
      <text x="24" y="11" class="stat-label">Total Commits:</text>
      <text x="220" y="11" class="stat-val" text-anchor="end">{commits}</text>
    </g>

    <!-- Total PRs -->
    <g transform="translate(0, 26)">
      <circle cx="7" cy="7" r="7" fill="#161b22" stroke="#39d353" stroke-width="1" />
      <path d="M4.5 5.5l5 3M9.5 5.5l-5 3" stroke="#39d353" stroke-width="1.2" stroke-linecap="round" />
      <text x="24" y="11" class="stat-label">Total PRs Merged:</text>
      <text x="220" y="11" class="stat-val" text-anchor="end">{prs}</text>
    </g>

    <!-- Total Issues -->
    <g transform="translate(0, 52)">
      <circle cx="7" cy="7" r="7" fill="#161b22" stroke="#e3b341" stroke-width="1" />
      <circle cx="7" cy="7" r="2" fill="#e3b341" />
      <text x="24" y="11" class="stat-label">Total Issues Opened:</text>
      <text x="220" y="11" class="stat-val" text-anchor="end">{issues}</text>
    </g>

    <!-- Contributed Repos -->
    <g transform="translate(0, 78)">
      <circle cx="7" cy="7" r="7" fill="#161b22" stroke="#58A6FF" stroke-width="1" />
      <path d="M4 7l2 2 4-4" stroke="#58A6FF" stroke-width="1.2" stroke-linecap="round" />
      <text x="24" y="11" class="stat-label">Contributed Repos:</text>
      <text x="220" y="11" class="stat-val" text-anchor="end">{repos}</text>
    </g>
  </g>

  <!-- GitHub Octocat Logo and Rank Badge on Right -->
  <g transform="translate(418, 97)">
    <!-- Rotating Dash Ring -->
    <circle cx="0" cy="0" r="42" fill="none" stroke="#21262d" stroke-width="4" />
    <circle cx="0" cy="0" r="42" fill="none" stroke="#22D3EE" stroke-width="4" stroke-dasharray="180 70" class="octo-ring" />
    <!-- Background Circle -->
    <circle cx="0" cy="0" r="37" fill="#161b22" />
    <!-- Octocat Silhouette Vector -->
    <path d="M 0 -24 C -13.2 -24 -24 -13.2 -24 0 C -24 10.6 -17.1 19.6 -7.6 22.8 C -6.4 23 -5.9 22.2 -5.9 21.6 C -5.9 21 -5.9 19 -5.9 17 C -12.5 18.5 -13.9 14.3 -13.9 14.3 C -15 11.5 -16.6 10.8 -16.6 10.8 C -18.7 9.3 -16.4 9.3 -16.4 9.3 C -14.1 9.5 -12.8 11.7 -12.8 11.7 C -10.7 15.3 -7.3 14.3 -5.9 13.6 C -5.7 12.1 -5.1 11 -4.3 10.4 C -9.7 9.8 -15.2 7.7 -15.2 -1.5 C -15.2 -4.1 -14.3 -6.3 -12.7 -7.9 C -13 -8.6 -13.8 -11 -12.4 -14.4 C -12.4 -14.4 -10.4 -15 -5.8 -11.9 C -3.9 -12.4 -1.8 -12.7 0.2 -12.7 C 2.2 -12.7 4.2 -12.4 6.2 -11.9 C 10.8 -15 12.8 -14.4 12.8 -14.4 C 14.2 -11 13.4 -8.6 13.1 -7.9 C 14.7 -6.3 15.6 -4.1 15.6 -1.5 C 15.6 7.7 10.1 9.8 4.7 10.4 C 5.5 11.1 6.3 12.5 6.3 14.6 C 6.3 17.7 6.3 20.2 6.3 21.6 C 6.3 22.2 6.7 23 7.9 22.8 C 17.4 19.6 24.3 10.6 24.3 0 C 24.3 -13.2 13.6 -24 0 -24 Z" fill="#e6edf3" />

    <!-- Cyber Rank Pill at bottom -->
    <g transform="translate(0, 44)" class="rank-pulse">
      <rect x="-34" y="-9" width="68" height="18" rx="9" fill="#0D1117" stroke="#22D3EE" stroke-width="1.2" />
      <text x="0" y="3.5" font-size="9.5" font-weight="700" fill="#22D3EE" font-family="-apple-system, sans-serif" text-anchor="middle" letter-spacing="0.5">RANK S+</text>
    </g>
  </g>
</svg>"""
    return svg

def generate_streak_svg(data):
    s = data['streak']
    total_contribs = s['total_contribs']
    total_range = s['total_range']
    current_streak = s['current_streak']
    current_range = s['current_range']
    longest_streak = s['longest_streak']
    longest_range = s['longest_range']

    svg = f"""<svg width="495" height="195" viewBox="0 0 495 195" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgStreak" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0e131f" />
      <stop offset="50%" stop-color="#0d1117" />
      <stop offset="100%" stop-color="#080c14" />
    </linearGradient>
    <linearGradient id="topGlowStreak" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#58A6FF" stop-opacity="0" />
      <stop offset="25%" stop-color="#58A6FF" stop-opacity="0.9" />
      <stop offset="75%" stop-color="#22D3EE" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#22D3EE" stop-opacity="0" />
    </linearGradient>
    <style>
      .num {{ font: 700 28px ui-monospace, SFMono-Regular, "Fira Code", monospace; fill: #ffffff; }}
      .lbl {{ font: 600 13px -apple-system, BlinkMacSystemFont, 'Segoe UI', Ubuntu, sans-serif; fill: #58A6FF; }}
      .sub {{ font: 500 11px -apple-system, BlinkMacSystemFont, 'Segoe UI', Ubuntu, sans-serif; fill: #7d8590; }}
      .fire-anim {{ animation: flamePulse 1.8s ease-in-out infinite; }}
      @keyframes flamePulse {{ 0%, 100% {{ transform: scale(1); filter: drop-shadow(0 0 3px #22D3EE); }} 50% {{ transform: scale(1.08); filter: drop-shadow(0 0 8px #22D3EE); }} }}
    </style>
  </defs>

  <!-- Container Box -->
  <rect x="0.5" y="0.5" width="494" height="194" rx="8" fill="url(#bgStreak)" stroke="#30363d" stroke-width="1.2" />
  <!-- Neon Accent Line Top -->
  <line x1="12" y1="1" x2="483" y2="1" stroke="url(#topGlowStreak)" stroke-width="2.2" />

  <!-- Dividers between columns -->
  <line x1="165" y1="35" x2="165" y2="165" stroke="#21262d" stroke-width="1" />
  <line x1="330" y1="35" x2="330" y2="165" stroke="#21262d" stroke-width="1" />

  <!-- Column 1: Total Contributions -->
  <g transform="translate(82, 0)">
    <text x="0" y="82" class="num" text-anchor="middle">{total_contribs}</text>
    <text x="0" y="112" class="lbl" text-anchor="middle">Total Contributions</text>
    <text x="0" y="132" class="sub" text-anchor="middle">{total_range}</text>
  </g>

  <!-- Column 2: Current Streak (Center Featured Gauge) -->
  <g transform="translate(247, 0)">
    <!-- Ring Gauge -->
    <g transform="translate(0, 68)">
      <circle cx="0" cy="0" r="32" fill="none" stroke="#21262d" stroke-width="4.5" />
      <circle cx="0" cy="0" r="32" fill="none" stroke="#22D3EE" stroke-width="4.5" stroke-dasharray="160 50" stroke-linecap="round" />
      
      <!-- Flame Icon Top of Ring (Safe from clipping) -->
      <g transform="translate(0, -32) translate(0, -2)" class="fire-anim">
        <path d="M0 -8 C2 -5 5 -3 5 1 C5 4 2 7 0 7 C-2 7 -5 4 -5 1 C-5 -3 -2 -5 0 -8 Z" fill="#22D3EE" />
        <path d="M0 -4 C1 -2 2.5 -1 2.5 1.5 C2.5 3 1 4.5 0 4.5 C-1 4.5 -2.5 3 -2.5 1.5 C-2.5 -1 -1 -2 0 -4 Z" fill="#ffffff" />
      </g>
      
      <text x="0" y="9" class="num" text-anchor="middle">{current_streak}</text>
    </g>
    <text x="0" y="122" class="lbl" text-anchor="middle" fill="#22D3EE" font-weight="700">Current Streak</text>
    <text x="0" y="142" class="sub" text-anchor="middle">{current_range}</text>
  </g>

  <!-- Column 3: Longest Streak -->
  <g transform="translate(412, 0)">
    <text x="0" y="82" class="num" text-anchor="middle">{longest_streak}</text>
    <text x="0" y="112" class="lbl" text-anchor="middle">Longest Streak</text>
    <text x="0" y="132" class="sub" text-anchor="middle">{longest_range}</text>
  </g>
</svg>"""
    return svg

def generate_langs_svg(data):
    langs = data['langs']
    
    bar_width = 550
    bar_rects = []
    accum_x = 0
    for l in langs:
        w = round((l['pct'] / 100) * bar_width, 1)
        if w > 0:
            bar_rects.append(f'<rect x="{accum_x}" y="0" width="{w}" height="9" fill="{l["color"]}" />')
            accum_x += w

    bars_markup = "\n      ".join(bar_rects)

    # Render language items with byte sizes
    items_markup = []
    col_xs = [0, 180, 360, 470]
    for idx, item in enumerate(langs):
        if idx >= len(col_xs):
            break
        x = col_xs[idx]
        items_markup.append(f"""<g transform="translate({x}, 0)">
      <circle cx="6" cy="6" r="5" fill="{item['color']}" />
      <text x="18" y="10" font-size="13" font-weight="600" fill="#c9d1d9" font-family="-apple-system, sans-serif">{item['name']} <tspan fill="#ffffff" font-weight="700">{item['pct']:.1f}%</tspan> <tspan fill="#7d8590" font-size="11">({item['size_str']})</tspan></text>
    </g>""")

    lang_items_str = "\n    ".join(items_markup)

    svg = f"""<svg width="600" height="145" viewBox="0 0 600 145" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgLangs" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0e131f" />
      <stop offset="50%" stop-color="#0d1117" />
      <stop offset="100%" stop-color="#080c14" />
    </linearGradient>
    <linearGradient id="topGlowLangs" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#22D3EE" stop-opacity="0" />
      <stop offset="30%" stop-color="#22D3EE" stop-opacity="0.8" />
      <stop offset="70%" stop-color="#58A6FF" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#58A6FF" stop-opacity="0" />
    </linearGradient>
    <mask id="barMask">
      <rect x="0" y="0" width="{bar_width}" height="9" rx="4.5" fill="white" />
    </mask>
  </defs>

  <!-- Container Box -->
  <rect x="0.5" y="0.5" width="599" height="144" rx="8" fill="url(#bgLangs)" stroke="#30363d" stroke-width="1.2" />
  <!-- Neon Accent Line Top -->
  <line x1="12" y1="1" x2="587" y2="1" stroke="url(#topGlowLangs)" stroke-width="2.2" />

  <!-- Title and Ecosystem Tag -->
  <text x="25" y="32" font-size="16" font-weight="700" fill="#58A6FF" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Ubuntu, sans-serif">Most Used Languages</text>
  <text x="575" y="32" text-anchor="end" font-size="10" font-weight="600" fill="#7d8590" font-family="ui-monospace, monospace">PRIMARY STACK // JAVASCRIPT and PYTHON</text>

  <!-- Progress Bar ({bar_width}px wide) -->
  <g transform="translate(25, 48)" mask="url(#barMask)">
    <rect x="0" y="0" width="{bar_width}" height="9" fill="#161b22" />
    <g>
      {bars_markup}
    </g>
  </g>

  <!-- Language Items Grid -->
  <g transform="translate(25, 82)">
    {lang_items_str}
  </g>
</svg>"""
    return svg

def main():
    print("Fetching live telemetry for", USERNAME)
    data = fetch_data()
    print("Telemetry data fetched:", data)
    
    stats_svg = generate_stats_svg(data)
    streak_svg = generate_streak_svg(data)
    langs_svg = generate_langs_svg(data)
    
    # Validate XML
    ET.fromstring(stats_svg)
    ET.fromstring(streak_svg)
    ET.fromstring(langs_svg)
    print("All SVGs validated as 100% well-formed XML!")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_dir = os.path.join(base_dir, 'assets')
    os.makedirs(assets_dir, exist_ok=True)
    
    with open(os.path.join(assets_dir, 'github-stats.svg'), 'w', encoding='utf-8') as f:
        f.write(stats_svg)
    with open(os.path.join(assets_dir, 'github-streak.svg'), 'w', encoding='utf-8') as f:
        f.write(streak_svg)
    with open(os.path.join(assets_dir, 'github-langs.svg'), 'w', encoding='utf-8') as f:
        f.write(langs_svg)
        
    print("Saved upgraded stats, streak, and langs SVGs successfully!")

if __name__ == '__main__':
    main()
