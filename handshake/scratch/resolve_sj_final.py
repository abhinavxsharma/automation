import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome

REASON = (
    "The prompt is fully self-contained and explicitly requests: 'Determine the fully simplified Boolean expression "
    "for the output Q in terms of the independent inputs A, B, and C from the provided circuit image' and 'Return the "
    "final answer as a single Boolean expression for Q, using standard Boolean notation with no units or extra quantities.' "
    "Both the requested output Q and the simplification are completely and unambiguously defined from the prompt and the provided circuit topology."
)


def dismiss_modal_if_present(page):
    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=1000):
        print("Dismissing Start timer modal via Playwright...")
        st_btn.click()
        page.wait_for_timeout(1000)


ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    page.wait_for_selector("text=Project Lumière", timeout=15000)

    # 1. Dismiss modal if visible
    dismiss_modal_if_present(page)

    # 2. Check if Disagree button exists
    disagree_btn = page.locator("button[aria-label='Disagree']").first
    if disagree_btn.is_visible(timeout=2000):
        print("Found Disagree button on Science Judge. Clicking...")
        disagree_btn.click()
        page.wait_for_timeout(1000)
    else:
        print("Disagree button not visible, checking if reason textarea is already open...")

    # Dismiss modal again if it appeared
    dismiss_modal_if_present(page)

    # 3. Locate the Reason textarea
    ta = page.locator("textarea[placeholder='Reason for disagreeing']").first
    if ta.is_visible(timeout=3000):
        print("Found reason textarea. Filling reason...")
        ta.fill(REASON)
        page.wait_for_timeout(500)

        dismiss_modal_if_present(page)

        # 4. Find the submit button inside the reason container and click it
        clicked = page.evaluate("""() => {
            const ta = document.querySelector(\"textarea[placeholder='Reason for disagreeing']\");
            if (!ta) return false;
            let container = ta.parentElement;
            const btns = Array.from(container.querySelectorAll('button'));
            if (btns.length > 0) {
                btns[btns.length - 1].click();
                return true;
            }
            return false;
        }""")
        print("Clicked submit button inside reason container:", clicked)
        page.wait_for_timeout(2000)
    else:
        print("Reason textarea not visible!")

    dismiss_modal_if_present(page)

    # 5. Check sidebar status
    sidebar_text = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const fbIdx = bodyText.indexOf('Feedback');
        return fbIdx !== -1 ? bodyText.slice(fbIdx, fbIdx + 600) : 'None';
    }""")
    print("\n--- FINAL SIDEBAR STATUS ---")
    print(sidebar_text)

    page.screenshot(path="handshake/scratch/after_sj_final_resolve.png")
    print("Saved screenshot to handshake/scratch/after_sj_final_resolve.png")
