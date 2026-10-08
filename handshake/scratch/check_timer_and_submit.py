import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const timerBtn = Array.from(document.querySelectorAll('button')).find(b => {
                const a = b.getAttribute('aria-label') || '';
                return a.includes('Pause timer') || a.includes('Resume timer');
            });
            
            const submitBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
            
            return {
                timerLabel: timerBtn ? timerBtn.getAttribute('aria-label') : 'No timer button',
                submitBtnFound: !!submitBtn,
                submitBtnDisabled: submitBtn ? submitBtn.disabled : null,
                submitBtnHtml: submitBtn ? submitBtn.outerHTML : null
            };
        }''')
        print("Status before final submission:")
        print("Timer status:", info['timerLabel'])
        print("Submit button found:", info['submitBtnFound'])
        print("Submit button disabled:", info['submitBtnDisabled'])
        print("Submit button HTML:", info['submitBtnHtml'])

if __name__ == "__main__":
    asyncio.run(main())
