import sys

sys.path.insert(0, ".")

from playwright.sync_api import sync_playwright

from handshake_automation.tasks.problem_solver import solve_network_flow_task

with sync_playwright() as p:
    b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    pg = next(t for t in b.contexts[0].pages if "/task/" in t.url)
    
    # 1. Dismiss toast if visible
    if (got_it := pg.locator('button:has-text("Got it")').first).is_visible():
        got_it.click()
        pg.wait_for_timeout(500)
        
    # 2. Get clean prompt
    task_data = solve_network_flow_task({})
    clean_prompt = task_data["prompt"]
    
    # 3. Fill clean prompt into textarea
    ta = pg.locator("textarea").first
    if ta.is_visible():
        ta.fill(clean_prompt)
        print("Updated textarea with clean prompt (no placeholders)!")
        pg.wait_for_timeout(1000)
        
    # 4. Check all 4 statement checkboxes
    statements = [
        "double checked",
        "not duplicative",
        "self-contained",
        "information in the image",
    ]
    for st in statements:
        cb = pg.locator(f"label:has-text('{st}'), div:has-text('{st}')").first
        if cb.is_visible():
            cb.click(force=True)
            pg.wait_for_timeout(300)
            
    print("Checked statement checkboxes!")
    pg.wait_for_timeout(1500)
    
    # 5. Click Continue
    cont = pg.get_by_role("button", name="Continue")
    cont.click(force=True)
    pg.wait_for_timeout(3000)
    
    pg.screenshot(path="scratch/after_checkboxes.png")
    print("Screenshot saved to scratch/after_checkboxes.png")
