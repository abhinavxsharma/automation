import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
import time
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    # Let's find the button for Model Failure Justification
    res = pg.evaluate('''() => {
        // Find heading 'Model Failure Justification'
        const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, div, span'))
            .filter(el => el.innerText && el.innerText.trim() === 'Model Failure Justification');
            
        if (headings.length === 0) return { error: "No heading found" };
        const h = headings[0];
        
        // Find container and edit button within or near container
        let parent = h.parentElement;
        let btn = null;
        for (let i = 0; i < 5; i++) {
            if (!parent) break;
            btn = parent.querySelector('button[aria-label="Edit this step"]');
            if (btn) break;
            parent = parent.parentElement;
        }
        
        if (!btn) return { error: "No edit button near Model Failure Justification", parentText: parent ? parent.innerText.slice(0, 100) : '' };
        
        btn.scrollIntoView({ behavior: 'instant', block: 'center' });
        btn.click();
        return { success: true };
    }''')
    print("Click edit on Model Failure Justification:", res)
    time.sleep(2)
    
    pg.screenshot(path="scratch/step15_opened_inspect.png")
    
    # Inspect all visible textareas, inputs, buttons after clicking edit
    state = pg.evaluate('''() => {
        const textareas = Array.from(document.querySelectorAll('textarea')).map(t => ({
            placeholder: t.placeholder,
            value: t.value.slice(0, 100),
            visible: t.getBoundingClientRect().height > 0
        }));
        const buttons = Array.from(document.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label') || '',
            visible: b.getBoundingClientRect().height > 0
        })).filter(b => b.text || b.aria);
        
        return { textareas, buttons: buttons.slice(0, 20) };
    }''')
    print("Textareas after click:", state["textareas"])
    print("Buttons after click:", state["buttons"])
