import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_steps_dump.txt', 'r', encoding='utf-8') as f:
    text = f.read()

sections = text.split('='*30)
for i in range(1, len(sections), 2):
    step_title = sections[i].strip()
    step_body = sections[i+1].strip() if i+1 < len(sections) else ''
    first_few_lines = [l for l in step_body.splitlines() if l.strip()][:3]
    print(f"{step_title}: " + ' | '.join(first_few_lines))
