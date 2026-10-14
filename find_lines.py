
with open(r'C:\Users\divya\OneDrive\Desktop\NexCura\patient-portal.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'View Details' in line or 'View Summary' in line or 'View Results' in line:
        print(f'{idx+1}: {line.strip()}')
