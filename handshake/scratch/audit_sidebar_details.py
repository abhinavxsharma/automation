import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    sidebar = pg.evaluate('''() => {
        // Find sidebar container
        const tabs = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.trim() === 'All' || b.innerText.trim() === 'Needs attention');
        const counter = document.body.innerText.match(/\\d+ \\/ \\d+ items addressed/)?.[0] || 'No counter';
        
        // Find all cards under sidebar
        const cards = Array.from(document.querySelectorAll('div, section, li'))
            .filter(el => {
                const t = el.innerText || '';
                return (t.includes('Jimson') || t.includes('Science Judge')) && (t.includes('edited') || t.includes('Oct 1') || t.includes('Finding'));
            })
            .map((el, idx) => ({
                idx,
                text: el.innerText.slice(0, 300).replace(/\\n/g, ' -- '),
                hasResolve: !!el.querySelector('button[aria-label="Resolve"]') || el.innerText.includes('Resolve')
            }));

        const resolveBtns = Array.from(document.querySelectorAll('button[aria-label="Resolve"]')).map((b, idx) => ({
            idx,
            parentText: b.parentElement ? b.parentElement.innerText.slice(0, 100).replace(/\\n/g, ' ') : ''
        }));

        return { counter, cardsCount: cards.length, cards: cards.slice(0, 10), resolveBtns };
    }''')
    
    print("Counter:", sidebar["counter"])
    print("Resolve buttons count:", len(sidebar["resolveBtns"]))
    for rb in sidebar["resolveBtns"]:
        print(f"  Resolve btn {rb['idx']}: {rb['parentText'].encode('ascii', 'replace').decode('ascii')}")
    print("\nCards:")
    for c in sidebar["cards"]:
        print(f"  Card {c['idx']}: {c['text'][:150].encode('ascii', 'replace').decode('ascii')} (hasResolve={c['hasResolve']})")
