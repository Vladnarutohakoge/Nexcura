
with open(r'C:\Users\divya\OneDrive\Desktop\NexCura\patient-portal.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
titles = re.findall(r'<h[1-3][^>]*>[0-9]{1,2}\.\s+[^<]+</h[1-3]>', text)
print('Numbered headings found:', len(titles))
for t in titles:
    print('  ', t)
