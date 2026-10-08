import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_steps_dump.txt', 'r', encoding='utf-8') as f:
    text = f.read()

sections = text.split('='*30)
step_map = {}
for i in range(1, len(sections), 2):
    step_num = int(sections[i].replace('STEP', '').strip())
    step_body = sections[i+1].strip() if i+1 < len(sections) else ''
    step_map[step_num] = step_body

for num in [7, 11, 15, 16, 23]:
    print(f"\n{'#'*30} FULL CONTENT OF STEP {num} {'#'*30}\n")
    print(step_map.get(num, 'NOT FOUND'))
