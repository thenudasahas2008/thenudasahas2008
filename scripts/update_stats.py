import os
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

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
        total_commits = res.get('total_count', 174)
    except Exception as e:
        print("Commits fetch fallback:", e)
        total_commits = 174

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

    # 4. Streak Stats
    streak_data = {
        'totalContributions': 201,
        'currentStreak': 8,
        'longestStreak': 8,
        'firstContrib': 'Aug 19, 2025',
        'currentDates': 'Nov 13 - Nov 20',
        'longestDates': 'Nov 13 - Nov 20'
    }
    try:
        u_streak = f'https://streak-stats.demolab.com?user={USERNAME}&timezone={TIMEZONE}&type=json'
        req_streak = urllib.request.Request(u_streak, headers=headers)
        raw_streak = json.loads(urllib.request.urlopen(req_streak, timeout=10).read().decode('utf-8'))
        streak_data['totalContributions'] = raw_streak.get('totalContributions', 201)
        
        cs = raw_streak.get('currentStreak', {})
        streak_data['currentStreak'] = cs.get('length', 8)
        if cs.get('start') and cs.get('end'):
            streak_data['currentDates'] = f"{cs['start']} - {cs['end']}"
            
        ls = raw_streak.get('longestStreak', {})
        streak_data['longestStreak'] = ls.get('length', 8)
        if ls.get('start') and ls.get('end'):
            streak_data['longestDates'] = f"{ls['start']} - {ls['end']}"
    except Exception as e:
        print("Streak fetch fallback:", e)

    # 5. Language bytes
    lang_bytes = {'JavaScript': 2187041, 'Python': 47404, 'HTML': 9261}
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

    # Calculate filtered language percentages
    filtered_langs = {k: v for k, v in lang_bytes.items() if k not in ['Procfile', 'Dockerfile', 'Shell']}
    tot = sum(filtered_langs.values()) or 1
    lang_pcts = []
    colors_map = {
        'JavaScript': '#f1e05a',
        'Python': '#3572A5',
        'HTML': '#e34c26',
        'CSS': '#563d7c',
        'TypeScript': '#3178c6',
    }
    for name, cnt in sorted(filtered_langs.items(), key=lambda x: -x[1])[:5]:
        pct = (cnt / tot) * 100
        color = colors_map.get(name, '#58A6FF')
        lang_pcts.append({'name': name, 'pct': pct, 'color': color})

    return {
        'commits': total_commits,
        'prs': total_prs,
        'issues': total_issues,
        'streak': streak_data,
        'langs': lang_pcts
    }

def generate_stats_svg(data):
    commits = data['commits']
    prs = data['prs']
    issues = data['issues']
    
    svg = f"""<svg width="467" height="170" viewBox="0 0 467 170" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117" />
      <stop offset="100%" stop-color="#090d16" />
    </linearGradient>
    <filter id="octoGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <style>
      .header {{ font: 600 17px -apple-system, BlinkMacSystemFont, 'Segoe UI', Ubuntu, sans-serif; fill: #58A6FF; }}
      .stat-label {{ font: 400 13px -apple-system, BlinkMacSystemFont, 'Segoe UI', Ubuntu, sans-serif; fill: #c9d1d9; }}
      .stat-val {{ font: 700 13.5px -apple-system, BlinkMacSystemFont, 'Segoe UI', Ubuntu, sans-serif; fill: #ffffff; }}
      .octo-ring {{ animation: ringRotate 10s linear infinite; transform-origin: 395px 95px; }}
      @keyframes ringRotate {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
    </style>
  </defs>

  <!-- Container Box -->
  <rect x="0.5" y="0.5" width="466" height="169" rx="6" fill="url(#bg)" stroke="#30363d" />

  <!-- Title -->
  <g transform="translate(25, 32)">
    <text x="0" y="0" class="header">Thenuda Sahas' GitHub Stats</text>
  </g>

  <!-- Stats Rows -->
  <g transform="translate(25, 62)">
    <!-- Total Commits -->
    <g transform="translate(0, 0)">
      <path d="M1.5 8a6.5 6.5 0 1 1 13 0 6.5 6.5 0 0 1-13 0zM8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0zm.5 4.75a.75.75 0 0 0-1.5 0v3.5a.75.75 0 0 0 .37.65l2.5 1.5a.75.75 0 0 0 .76-1.3L8.5 7.92V4.75z" fill="#22D3EE" />
      <text x="25" y="12" class="stat-label">Total Commits:</text>
      <text x="210" y="12" class="stat-val" text-anchor="end">{commits}</text>
    </g>

    <!-- Total PRs -->
    <g transform="translate(0, 28)">
      <path d="M7.177 3.073L4.405.5a.75.75 0 00-1.01.037L.64 3.292a.75.75 0 001.06 1.06l1.55-1.55V9a2.5 2.5 0 002.5 2.5h1a.75.75 0 000-1.5h-1A1 1 0 014.75 9V2.803l1.366 1.367a.75.75 0 001.06-1.06l-.001-.001zM11.75 1.5a2.5 2.5 0 00-2.5 2.5v6.197l-1.366-1.367a.75.75 0 00-1.06 1.06l2.75 2.75a.75.75 0 001.06 0l2.75-2.75a.75.75 0 00-1.06-1.06l-1.574 1.574V4a1 1 0 011-1h1a.75.75 0 000-1.5h-1z" fill="#22D3EE" />
      <text x="25" y="12" class="stat-label">Total PRs:</text>
      <text x="210" y="12" class="stat-val" text-anchor="end">{prs}</text>
    </g>

    <!-- Total Issues -->
    <g transform="translate(0, 56)">
      <path d="M8 9.5a1.5 1.5 0 100-3 1.5 1.5 0 000 3z M8 0a8 8 0 100 16A8 8 0 008 0zM1.5 8a6.5 6.5 0 1113 0 6.5 6.5 0 01-13 0z" fill="#22D3EE" />
      <text x="25" y="12" class="stat-label">Total Issues:</text>
      <text x="210" y="12" class="stat-val" text-anchor="end">{issues}</text>
    </g>
  </g>

  <!-- GitHub Octocat Logo on Right -->
  <g transform="translate(395, 95)">
    <!-- Cyan Ring -->
    <circle cx="0" cy="0" r="42" fill="none" stroke="#21262d" stroke-width="4.5" />
    <circle cx="0" cy="0" r="42" fill="none" stroke="#22D3EE" stroke-width="4.5" stroke-dasharray="190 75" class="octo-ring" />
    <!-- Background Circle -->
    <circle cx="0" cy="0" r="38" fill="#161b22" />
    <!-- Octocat Silhouette Vector -->
    <path d="M 0 -26 C -14.4 -26 -26 -14.4 -26 0 C -26 11.5 -18.5 21.3 -8.2 24.7 C -6.9 25 -6.4 24.1 -6.4 23.4 C -6.4 22.8 -6.4 20.6 -6.4 18.5 C -13.6 20.1 -15.1 15.5 -15.1 15.5 C -16.3 12.5 -18 11.7 -18 11.7 C -20.3 10.1 -17.8 10.1 -17.8 10.1 C -15.3 10.3 -13.9 12.7 -13.9 12.7 C -11.6 16.6 -7.9 15.5 -6.4 14.8 C -6.2 13.1 -5.5 12 -4.7 11.3 C -10.5 10.6 -16.5 8.4 -16.5 -1.6 C -16.5 -4.5 -15.5 -6.8 -13.8 -8.6 C -14.1 -9.3 -15 -12 -13.5 -15.6 C -13.5 -15.6 -11.3 -16.3 -6.3 -12.9 C -4.2 -13.5 -2 -13.8 0.2 -13.8 C 2.4 -13.8 4.6 -13.5 6.7 -12.9 C 11.7 -16.3 13.9 -15.6 13.9 -15.6 C 15.4 -12 14.5 -9.3 14.2 -8.6 C 15.9 -6.8 16.9 -4.5 16.9 -1.6 C 16.9 8.4 10.9 10.6 5.1 11.3 C 6 12.1 6.8 13.6 6.8 15.9 C 6.8 19.2 6.8 21.9 6.8 23.4 C 6.8 24.1 7.3 25 8.6 24.7 C 18.9 21.3 26.4 11.5 26.4 0 C 26.4 -14.4 14.8 -26 0 -26 Z" fill="#e6edf3" />
  </g>
</svg>"""
    return svg

def generate_streak_svg(data):
    s = data['streak']
    tot = s['totalContributions']
    cur = s['currentStreak']
    long = s['longestStreak']
    cur_dates = s['currentDates']
    long_dates = s['longestDates']
    
    svg = f"""<svg width="495" height="170" viewBox="0 0 495 170" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgStreak" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117" />
      <stop offset="100%" stop-color="#090d16" />
    </linearGradient>
    <filter id="fireGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3.5" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <style>
      .num-val {{ font: 700 28px -apple-system, BlinkMacSystemFont, 'Segoe UI', Ubuntu, sans-serif; fill: #ffffff; text-anchor: middle; }}
      .title-mid {{ font: 700 13px -apple-system, BlinkMacSystemFont, 'Segoe UI', Ubuntu, sans-serif; fill: #22D3EE; text-anchor: middle; }}
      .title-side {{ font: 600 12px -apple-system, BlinkMacSystemFont, 'Segoe UI', Ubuntu, sans-serif; fill: #58A6FF; text-anchor: middle; }}
      .sub-date {{ font: 400 10px -apple-system, BlinkMacSystemFont, 'Segoe UI', Ubuntu, sans-serif; fill: #7d8590; text-anchor: middle; }}
      .fire-pulse {{ animation: flamePulse 1.8s ease-in-out infinite; transform-origin: 247px 62px; }}
      @keyframes flamePulse {{ 0%, 100% {{ transform: scale(1); filter: drop-shadow(0 0 3px rgba(34, 211, 238, 0.4)); }} 50% {{ transform: scale(1.08); filter: drop-shadow(0 0 8px rgba(34, 211, 238, 0.8)); }} }}
    </style>
  </defs>

  <!-- Container Box -->
  <rect x="0.5" y="0.5" width="494" height="169" rx="6" fill="url(#bgStreak)" stroke="#30363d" />

  <!-- Separator Dividers -->
  <line x1="165" y1="25" x2="165" y2="145" stroke="#21262d" stroke-width="1.2" />
  <line x1="330" y1="25" x2="330" y2="145" stroke="#21262d" stroke-width="1.2" />

  <!-- Left: Total Contributions -->
  <g transform="translate(82, 0)">
    <text x="0" y="70" class="num-val">{tot}</text>
    <text x="0" y="98" class="title-side">Total Contributions</text>
    <text x="0" y="118" class="sub-date">Aug 19, 2025 - Present</text>
  </g>

  <!-- Center: Current Streak -->
  <g transform="translate(247, 0)">
    <!-- Fire Ring -->
    <circle cx="0" cy="58" r="32" fill="none" stroke="#21262d" stroke-width="4" />
    <circle cx="0" cy="58" r="32" fill="none" stroke="#22D3EE" stroke-width="4" stroke-dasharray="150 50" />
    <!-- Flame Icon Top of Ring -->
    <g transform="translate(0, 24)" class="fire-pulse">
      <path d="M 0 -8 C 2 -4 4 -3 5 0 C 6 3 4 7 0 9 C -4 7 -6 3 -5 0 C -4 -3 -2 -4 0 -8 Z" fill="#22D3EE" />
      <path d="M 0 -4 C 1 -2 2 -1 2.5 0.5 C 3 2 2 4.5 0 5.5 C -2 4.5 -3 2 -2.5 0.5 C -2 -1 -1 -2 0 -4 Z" fill="#ffffff" />
    </g>
    <!-- Streak Number -->
    <text x="0" y="68" class="num-val">{cur}</text>
    <!-- Labels -->
    <text x="0" y="114" class="title-mid">Current Streak</text>
    <text x="0" y="132" class="sub-date">{cur_dates}</text>
  </g>

  <!-- Right: Longest Streak -->
  <g transform="translate(412, 0)">
    <text x="0" y="70" class="num-val">{long}</text>
    <text x="0" y="98" class="title-side">Longest Streak</text>
    <text x="0" y="118" class="sub-date">{long_dates}</text>
  </g>
</svg>"""
    return svg

def generate_langs_svg(data):
    langs = data['langs']
    
    # Generate progress bar rects
    bar_width = 300
    bar_rects = []
    accum_x = 0
    for l in langs:
        w = round((l['pct'] / 100) * bar_width, 1)
        if w > 0:
            bar_rects.append(f'<rect x="{accum_x}" y="0" width="{w}" height="8" fill="{l["color"]}" />')
            accum_x += w

    bars_markup = "\n        ".join(bar_rects)

    # Generate language list text
    # Column 1 (x=0), Column 2 (x=160)
    col1 = langs[:2]
    col2 = langs[2:]

    def render_col(items, start_x):
        res = []
        for idx, item in enumerate(items):
            y = idx * 24
            res.append(f"""<g transform="translate({start_x}, {y})">
        <circle cx="5" cy="5" r="4.5" fill="{item['color']}" />
        <text x="16" y="9" font-size="12" fill="#c9d1d9" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif">{item['name']} <tspan fill="#7d8590" font-size="11">{item['pct']:.2f}%</tspan></text>
      </g>""")
        return "\n      ".join(res)

    col1_markup = render_col(col1, 0)
    col2_markup = render_col(col2, 160)

    svg = f"""<svg width="360" height="150" viewBox="0 0 360 150" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgLangs" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117" />
      <stop offset="100%" stop-color="#090d16" />
    </linearGradient>
    <mask id="barMask">
      <rect x="0" y="0" width="{bar_width}" height="8" rx="4" fill="white" />
    </mask>
  </defs>

  <!-- Container Box -->
  <rect x="0.5" y="0.5" width="359" height="149" rx="6" fill="url(#bgLangs)" stroke="#30363d" />

  <!-- Title -->
  <text x="25" y="32" font-size="17" font-weight="600" fill="#58A6FF" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Ubuntu, sans-serif">Most Used Languages</text>

  <!-- Progress Bar -->
  <g transform="translate(25, 48)" mask="url(#barMask)">
    <rect x="0" y="0" width="{bar_width}" height="8" fill="#161b22" />
    <g>
      {bars_markup}
    </g>
  </g>

  <!-- Language Items -->
  <g transform="translate(25, 75)">
    <g>
      {col1_markup}
    </g>
    <g>
      {col2_markup}
    </g>
  </g>
</svg>"""
    return svg

def main():
    print("Fetching live data for", USERNAME)
    data = fetch_data()
    print("Data fetched:", data)
    
    stats_svg = generate_stats_svg(data)
    streak_svg = generate_streak_svg(data)
    langs_svg = generate_langs_svg(data)
    
    # Validate XML
    ET.fromstring(stats_svg)
    ET.fromstring(streak_svg)
    ET.fromstring(langs_svg)
    print("All SVGs validated as well-formed XML!")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_dir = os.path.join(base_dir, 'assets')
    os.makedirs(assets_dir, exist_ok=True)
    
    with open(os.path.join(assets_dir, 'github-stats.svg'), 'w', encoding='utf-8') as f:
        f.write(stats_svg)
    with open(os.path.join(assets_dir, 'github-streak.svg'), 'w', encoding='utf-8') as f:
        f.write(streak_svg)
    with open(os.path.join(assets_dir, 'github-langs.svg'), 'w', encoding='utf-8') as f:
        f.write(langs_svg)
        
    print("Saved all 3 SVGs to", assets_dir)

if __name__ == '__main__':
    main()
