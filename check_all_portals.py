import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

portals = ['patient-portal.html', 'clinician-portal.html', 'admin-portal.html', 'staff-portal.html', 'index.html', 'templates/home.html']

for p in portals:
    if not os.path.exists(p):
        continue
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Check numbering
    numbered = re.findall(r'>\s*([0-9]{1,2}\.\s+[A-Za-z][^<]+)<', content)
    
    # Check view buttons without onclick or with href="#"
    dead_buttons = re.findall(r'<button(?![^>]*onclick)[^>]*>[^<]*View[^<]*</button>', content, re.IGNORECASE)
    hash_links = re.findall(r'<a[^>]*href=["\']#["\'][^>]*>[^<]*View[^<]*</a>', content, re.IGNORECASE)
    
    # Check charts / canvas
    canvases = re.findall(r'<canvas[^>]*id="([^"]+)"', content)
    chart_scripts = 'Chart' in content or 'chart.js' in content.lower()
    
    # Check background color in styles
    bg_matches = re.findall(r'body\s*\{[^}]*background[^}]*\}', content)
    
    print(f"=== {p} ===")
    print(f"  Numbered labels: {len(numbered)}")
    if numbered:
        print(f"    Sample: {numbered[:5]}")
    print(f"  Dead View buttons: {len(dead_buttons)}")
    if dead_buttons:
        print(f"    Sample: {dead_buttons[:3]}")
    print(f"  Hash View links: {len(hash_links)}")
    if hash_links:
        print(f"    Sample: {hash_links[:3]}")
    print(f"  Canvases: {canvases}")
    print(f"  Has Chart references: {chart_scripts}")
    print(f"  Body bg: {bg_matches}")
    print()
