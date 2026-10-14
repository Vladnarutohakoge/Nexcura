import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('patient-portal.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

print("=== Search for Condition ===")
for i, l in enumerate(lines):
    if 'condition' in l.lower() and ('button' in l.lower() or 'modal' in l.lower() or 'add' in l.lower()):
        print(f"Line {i+1}: {l.strip()[:100]}")
        for j in range(max(0, i-2), min(len(lines), i+3)):
            print(f"  {j+1}: {lines[j].rstrip()}")
        print("-" * 40)

print("\n=== Search for Request buttons ===")
for i, l in enumerate(lines):
    if '<button' in l and 'request' in l.lower():
        print(f"Line {i+1}: {l.strip()[:100]}")
        for j in range(max(0, i-2), min(len(lines), i+3)):
            print(f"  {j+1}: {lines[j].rstrip()}")
        print("-" * 40)

print("\n=== Search for View Summary ===")
for i, l in enumerate(lines):
    if 'view summary' in l.lower():
        print(f"Line {i+1}: {l.strip()[:100]}")
        for j in range(max(0, i-2), min(len(lines), i+3)):
            print(f"  {j+1}: {lines[j].rstrip()}")
        print("-" * 40)
