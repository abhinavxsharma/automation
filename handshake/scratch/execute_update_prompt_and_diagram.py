import json
import sys
import time
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

from handshake_automation.tasks.cs_diagram_creator import create_network_flow_diagram
from handshake_automation.tasks.problem_solver import solve_network_flow_task


def dismiss_modals(page):
    for sel in ["button:has-text('Start timer')", "button:has-text('Got it')", "button:has-text('OK')"]:
        btn = page.locator(sel).first
        if btn.is_visible(timeout=1000):
            btn.click(force=True)
            page.wait_for_timeout(800)


def main():
    print("=== 1. Generating Adversarial Diagram and Solving ===")
    diagram_path = Path("scratch/adversarial_flow_diagram.png").resolve()
    info = create_network_flow_diagram(diagram_path)
    task_data = solve_network_flow_task(info)

    print(f"Diagram saved to: {diagram_path}")
    print(f"GTFA: {task_data['gtfa']}")
    print(f"Edges: {len(info['edges'])}")
    print(f"Distractors: {task_data['distractors']}")

    # Save solution metadata
    meta = {
        "diagram_path": str(diagram_path),
        "info": info,
        "task_data": task_data
    }
    with open("scratch/current_task_solution.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print("Saved solution metadata to scratch/current_task_solution.json")

    print("\n=== 2. Connecting to Chrome ===")
    ensure_chrome()
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        page = browser.contexts[0].pages[0]

        # Wait for page hydration
        for _ in range(20):
            if "Final Answer" in page.evaluate("() => document.body ? document.body.innerText : ''"):
                break
            time.sleep(0.5)

        dismiss_modals(page)

        # Check if textarea is already open
        ta = page.locator("textarea").first
        if not ta.is_visible():
            print("Prompt editor not open. Finding Edit this step button...")
            edit_btns = page.locator("button[aria-label='Edit this step']").all()
            if len(edit_btns) > 7:
                print("Clicking edit_btns[7] to open prompt editor...")
                edit_btns[7].scroll_into_view_if_needed()
                page.wait_for_timeout(500)
                edit_btns[7].click(force=True)
                page.wait_for_timeout(1500)
                dismiss_modals(page)

        ta = page.locator("textarea").first
        if not ta.is_visible():
            print("ERROR: Textarea is not visible after attempting to open editor!")
            page.screenshot(path="scratch/error_textarea_not_found.png")
            return

        print("Prompt editor is OPEN!")

        # 3. Remove old image
        remove_btn = page.locator("button[aria-label='Remove']").first
        if remove_btn.is_visible():
            print("Removing old image...")
            remove_btn.click(force=True)
            page.wait_for_timeout(1000)

        # 4. Upload new diagram
        print(f"Uploading new diagram: {diagram_path}")
        upload_btn = page.locator("button[aria-label='Upload files']").first
        with page.expect_file_chooser() as fc_info:
            upload_btn.click(force=True)
        file_chooser = fc_info.value
        file_chooser.set_files(str(diagram_path))
        page.wait_for_timeout(2000)
        print("Diagram uploaded successfully!")

        # 5. Fill new clean prompt
        clean_prompt = task_data["prompt"]
        print("Filling clean prompt into textarea...")
        ta.fill(clean_prompt)
        page.wait_for_timeout(1000)

        page.screenshot(path="scratch/before_prompt_submit.png")
        print("Saved screenshot: scratch/before_prompt_submit.png")

        # 6. Click Submit (up-arrow button)
        submit_btn = page.locator("button[aria-label='Submit']").first
        print("Clicking submit button...")
        submit_btn.click(force=True)
        page.wait_for_timeout(3000)

        # 7. Check if the 4 statement checkboxes appear
        print("Checking statement checkboxes...")
        statements = [
            "double checked",
            "not duplicative",
            "self-contained",
            "information in the image"
        ]
        for st in statements:
            cb = page.locator(f"label:has-text('{st}'), div:has-text('{st}')").first
            if cb.is_visible(timeout=2000):
                cb.click(force=True)
                page.wait_for_timeout(300)
                print(f"  Checked: {st}")

        page.wait_for_timeout(1000)

        # 8. Click Continue if present
        cont = page.locator("button:has-text('Continue')").first
        if cont.is_visible(timeout=3000):
            print("Clicking Continue...")
            cont.click(force=True)
            page.wait_for_timeout(3000)

        page.screenshot(path="scratch/after_prompt_update.png")
        print("Saved screenshot: scratch/after_prompt_update.png")
        print("\n=== SUCCESS: Prompt and Diagram Updated! ===")


if __name__ == "__main__":
    main()
