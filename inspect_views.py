
with open(r'C:\Users\divya\OneDrive\Desktop\NexCura\patient-portal.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
view_buttons = re.findall(r'<button[^>]*>[^<]*View[^<]*</button>', text, re.IGNORECASE)
print('View buttons found:', len(view_buttons))
for b in view_buttons:
    print('  ', b)

view_links = re.findall(r'<a[^>]*>[^<]*View[^<]*</a>', text, re.IGNORECASE)
print('View links found:', len(view_links))
for l in view_links:
    print('  ', l)
