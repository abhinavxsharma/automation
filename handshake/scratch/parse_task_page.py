import re
from html.parser import HTMLParser

with open('scratch/task_page.html', 'r', encoding='utf-8') as f:
    content = f.read()

keywords = ['login', 'sign in', 'stage', 'justification', 'critical', 'latency', 'reviewer', 'feedback', 'jimson', '1520c7f4']
for kw in keywords:
    matches = len(re.findall(re.escape(kw), content, re.IGNORECASE))
    print(f'Keyword "{kw}": {matches}')

# Find titles and button tags using regex
title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
print('Title:', title_match.group(1) if title_match else 'None')

buttons = re.findall(r'<button[^>]*>(.*?)</button>', content, re.IGNORECASE | re.DOTALL)
print(f'Buttons count: {len(buttons)}')
clean_buttons = [re.sub(r'<[^>]+>', '', b).strip() for b in buttons if re.sub(r'<[^>]+>', '', b).strip()]
print('Sample buttons:', clean_buttons[:20])

headings = re.findall(r'<h[1-5][^>]*>(.*?)</h[1-5]>', content, re.IGNORECASE | re.DOTALL)
print(f'Headings count: {len(headings)}')
clean_headings = [re.sub(r'<[^>]+>', '', h).strip() for h in headings if re.sub(r'<[^>]+>', '', h).strip()]
print('Sample headings:', clean_headings[:20])
