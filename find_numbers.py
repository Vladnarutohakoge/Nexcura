
with open(r'C:\Users\divya\OneDrive\Desktop\NexCura\patient-portal.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
labels = re.findall(r'>\s*([0-9]{1,2}\.\s+[^<]+)<', text)
print('Numbered module labels found:', len(labels))
for l in labels:
    print('  ', l.strip())
