import sys
sys.stdout.reconfigure(encoding="utf-8")
import time
from pathlib import Path
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

NEW_IMAGE = str(Path("scratch/dag_final_corrected.png").resolve())
PROMPT_TEXT = (
    "The figure shows a task-dependency directed acyclic graph (DAG) representing a parallel computation pipeline. "
    "Tasks are nodes $S, A, B, C, D, E, F, T$, where $S$ is entry and $T$ is terminal. "
    "Directed edges $(u, v)$ represent precedence with latency in milliseconds ($\\text{ms}$). "
    "Assuming each task starts immediately once all predecessors complete, determine the critical path duration (maximum latency from $S$ to $T$). "
    "The answer should be expressed in $\\text{ms}$. Report your final answer as a 2 significant figure number without units. "
    "Any intermediate calculations should be carried out to 6 significant figures. All unstated fundamental constants should be used to 4 significant figures."
)

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Check if Step 7 editor is open
    ta = page.locator("textarea").first
    if not ta.is_visible():
        print("Opening Step 7 editor...")
        edit_btns = page.locator("button[aria-label='Edit this step']").all()
        edit_btns[7].scroll_into_view_if_needed()
        time.sleep(0.5)
        edit_btns[7].click(force=True)
        time.sleep(2)
        ta.wait_for(state="visible", timeout=5000)

    print("Step 7 editor is open. Removing old image...")
    rem_btn = page.locator("button[aria-label='Remove']").first
    if rem_btn.is_visible(timeout=2000):
        rem_btn.click(force=True)
        time.sleep(1.5)
        print("Removed old image.")
    else:
        print("No remove button visible.")

    print(f"Uploading new image: {NEW_IMAGE}")
    upload_btn = page.locator("button[aria-label='Upload files'], button:has-text('+')").first
    with page.expect_file_chooser() as fc_info:
        upload_btn.click(force=True)
    fc = fc_info.value
    fc.set_files(NEW_IMAGE)
    time.sleep(3)
    print("New image uploaded into file chooser.")

    print("Updating prompt text...")
    ta = page.locator("textarea").first
    ta.fill("")
    page.wait_for_timeout(300)
    ta.fill(PROMPT_TEXT)
    page.wait_for_timeout(500)
    # Trigger input event in React
    page.evaluate("""(text) => {
        const t = document.querySelector('textarea');
        if (t) {
            t.value = text;
            t.dispatchEvent(new Event('input', { bubbles: true }));
            t.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }""", PROMPT_TEXT)
    time.sleep(1)

    page.screenshot(path="scratch/before_submitting_step7.png")
    print("Screenshot saved to scratch/before_submitting_step7.png")

    # Now click Submit button inside editor
    submit_btn = page.locator("button[aria-label='Submit']").first
    print("Clicking Submit button...")
    submit_btn.click(force=True)
    time.sleep(3)

    page.screenshot(path="scratch/after_submitting_step7.png")
    print("Screenshot saved to scratch/after_submitting_step7.png")

    # Check for any confirmation modal / dialog
    dialogs = page.locator("div[role='dialog'], [role='alertdialog']").all()
    print(f"Dialogs found: {len(dialogs)}")
    for i, d in enumerate(dialogs):
        print(f"Dialog {i} text: {d.inner_text()[:200]}")
        # Look for Confirm, Continue, Proceed, or Submit button
        confirm_btn = d.locator("button:has-text('Continue'), button:has-text('Confirm'), button:has-text('Delete'), button:has-text('Submit')").first
        if confirm_btn.is_visible(timeout=1000):
            print(f"Clicking confirm button in dialog: {confirm_btn.inner_text()}")
            confirm_btn.click(force=True)
            time.sleep(2)

    page.screenshot(path="scratch/step7_final_state.png")
    print("Screenshot saved to scratch/step7_final_state.png")
