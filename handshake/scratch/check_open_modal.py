import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Find open dialog or modal
    info = page.evaluate("""() => {
        const dialog = document.querySelector("[role='dialog'], [role='alertdialog']");
        const backdrop = document.querySelector("[data-state='open'][class*='fixed inset-0']");
        return {
            hasDialog: !!dialog,
            dialogHTML: dialog ? dialog.outerHTML : null,
            dialogText: dialog ? dialog.innerText : null,
            hasBackdrop: !!backdrop,
            backdropHTML: backdrop ? backdrop.outerHTML : null
        };
    }""")
    print("Dialog text:\n", info["dialogText"])
    print("\nDialog HTML:\n", info["dialogHTML"][:400] if info["dialogHTML"] else "None")
    page.screenshot(path="handshake/scratch/open_modal_debug.png")
    print("Screenshot saved to handshake/scratch/open_modal_debug.png")
