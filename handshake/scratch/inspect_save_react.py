import json
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Check the top-level Save button
    save_info = page.evaluate("""() => {
        const topSave = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save');
        if (!topSave) return { error: 'No top Save button' };
        
        // Find onClick handler or React props on topSave
        const propKeys = Object.keys(topSave);
        const fiberKey = propKeys.find(k => k.startsWith('__reactFiber') || k.startsWith('__reactInternalInstance'));
        const propsKey = propKeys.find(k => k.startsWith('__reactProps'));
        
        return {
            hasFiber: !!fiberKey,
            hasProps: !!propsKey,
            disabled: topSave.disabled,
            classes: topSave.className
        };
    }""")
    print("Top Save info:\n", save_info)
