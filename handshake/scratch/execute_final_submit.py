import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # 1. Pause timer
        print("Pausing timer...", flush=True)
        pause_btn = page.locator("button[aria-label='Pause timer']").first
        if await pause_btn.is_visible():
            await pause_btn.click()
            await asyncio.sleep(1.0)
            print("Timer paused successfully.", flush=True)
            
        # 2. Click Submit task button in sidebar
        print("Clicking 'Submit task' button...", flush=True)
        submit_btn = page.locator("button:has-text('Submit task')").first
        await submit_btn.click()
        await asyncio.sleep(2.0)
        
        # 3. Check if a confirmation dialog appears
        dialog = page.locator("div[role='dialog']")
        if await dialog.is_visible():
            text = await dialog.inner_text()
            print("Confirmation dialog appeared:\n", text, flush=True)
            # Find confirmation button in dialog (e.g. 'Submit', 'Confirm', 'Submit task')
            confirm_btn = dialog.locator("button:has-text('Submit'), button:has-text('Confirm')").first
            if await confirm_btn.is_visible():
                print(f"Clicking confirmation button: '{await confirm_btn.inner_text()}'...", flush=True)
                await confirm_btn.click()
                await asyncio.sleep(4.0)
                
        # 4. Check page state after submission
        print("\nPage URL after submission:", page.url, flush=True)
        print("Page Title:", await page.title(), flush=True)
        
        # Check toasts or body text
        state = await page.evaluate('''() => {
            const toast = document.querySelector('[role="status"], [role="alert"], div[class*="toast"]');
            const h = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6')).map(el => el.innerText.trim()).filter(Boolean);
            return {
                toast: toast ? toast.innerText : null,
                headings: h.slice(0, 10),
                bodyTextSnippet: document.body.innerText.slice(0, 500).replace(/\\n+/g, ' -- ')
            };
        }''')
        print("State after submission:", state, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
