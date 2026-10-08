import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    distractors = pg.evaluate('''() => {
        const divs = Array.from(document.querySelectorAll('div, section, p'))
            .filter(el => el.innerText && /^Distractor #\d+:/.test(el.innerText.trim()));
        return divs.map(d => d.innerText.replace(/\\n/g, ' '));
    }''')
    print("Found distractors:")
    for d in distractors:
        print(" ", d.encode('ascii', 'replace').decode('ascii'))
