import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        print("Current page URL:", page.url)
        
        # If we are on dashboard, let's inspect everything on dashboard
        if "tasks" in page.url:
            print("Currently on dashboard.")
            # Let's inspect buttons, rows, etc.
            buttons = await page.evaluate('''() => {
                return Array.from(document.querySelectorAll('button, a')).map(b => ({
                    tag: b.tagName,
                    text: b.innerText.trim(),
                    aria: b.getAttribute('aria-label'),
                    className: b.className
                })).filter(b => b.text || b.aria);
            }''')
            for b in buttons:
                print("  Dashboard action:", b)
                
            # Click Continue on dashboard to go into the task
            cont_btn = page.locator("button:has-text('Continue')").first
            if await cont_btn.is_visible():
                print("Clicking Continue to enter task...")
                await cont_btn.click()
                await asyncio.sleep(2.0)
                
                # Check for modal dialog
                dialog = page.locator("div[role='dialog']")
                if await dialog.is_visible():
                    print("Dialog text:", await dialog.inner_text())
                    start_btn = dialog.locator("button:has-text('Start timer')")
                    if await start_btn.is_visible():
                        print("Clicking Start timer...")
                        await start_btn.click()
                        await asyncio.sleep(2.0)
                        
        print("Page URL now:", page.url)
        # Now we are inside the task (/run). Let's search for every button on the page!
        elements = await page.evaluate('''() => {
            const all = Array.from(document.querySelectorAll('button, a, div[role="button"], input[type="submit"]'));
            return all.map(el => {
                const rect = el.getBoundingClientRect();
                return {
                    tag: el.tagName,
                    text: el.innerText?.trim(),
                    aria: el.getAttribute('aria-label'),
                    visible: rect.width > 0 && rect.height > 0,
                    x: Math.round(rect.x),
                    y: Math.round(rect.y),
                    w: Math.round(rect.width),
                    h: Math.round(rect.height),
                    disabled: el.disabled
                };
            }).filter(el => el.visible);
        }''')
        print(f"\nVisible interactive elements in /run ({len(elements)}):")
        for el in elements:
            if any(k in (el['text'] + str(el['aria'])).lower() for k in ['submit', 'finish', 'complete', 'continue', 'done', 'save', 'exit', 'timer']):
                print(" ->", el)

if __name__ == "__main__":
    asyncio.run(main())
