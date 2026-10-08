import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const h3 = Array.from(document.querySelectorAll('h3, h2, h4')).find(el => el.textContent.includes('Error Type'));
            const card = h3.closest('div[class*="rosetta-card"]');
            const form = card.querySelector('form') || card.closest('form');
            
            // Let's inspect React Fiber on the form or card
            function getFiber(dom) {
                const key = Object.keys(dom).find(k => k.startsWith('__reactFiber$'));
                return key ? dom[key] : null;
            }
            
            let current = getFiber(card);
            let stateNodes = [];
            while (current && stateNodes.length < 20) {
                if (current.memoizedProps) {
                    const keys = Object.keys(current.memoizedProps);
                    if (keys.includes('onSubmit') || keys.includes('control') || keys.includes('register') || keys.includes('formState') || keys.includes('values')) {
                        stateNodes.push({
                            type: typeof current.type === 'string' ? current.type : current.type?.name || 'anonymous',
                            props: keys,
                            formState: current.memoizedProps.formState ? {
                                errors: current.memoizedProps.formState.errors,
                                isValid: current.memoizedProps.formState.isValid,
                                isDirty: current.memoizedProps.formState.isDirty
                            } : null,
                            values: current.memoizedProps.values
                        });
                    }
                }
                current = current.return;
            }
            
            return {
                formFound: !!form,
                formHtml: form ? form.outerHTML.slice(0, 300) : null,
                reactForm: stateNodes
            };
        }''')
        print("Form Info:", info)

if __name__ == "__main__":
    asyncio.run(main())
