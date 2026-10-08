import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        page = browser.contexts[0].pages[0]
        
        # 1. Remove old file
        remove_btn = page.locator('button[aria-label="Remove"]')
        if await remove_btn.is_visible():
            print("Clicking Remove button...")
            await remove_btn.click()
            await asyncio.sleep(1)
            
        # 2. Upload new image using expect_file_chooser
        img_path = os.path.abspath('handshake/scratch/dag_10nodes_hard.png')
        print(f"Uploading file: {img_path}")
        async with page.expect_file_chooser() as fc_info:
            await page.locator('button[aria-label="Upload files"]').click()
        file_chooser = await fc_info.value
        await file_chooser.set_files(img_path)
        print("File set on file_chooser, waiting 3s for upload...")
        await asyncio.sleep(3)
        
        # 3. Update textarea content
        prompt_text = (
            "The figure shows a task-dependency directed acyclic graph (DAG) representing a parallel computation pipeline. "
            "Tasks are nodes $S, A, B, C, D, E, F, G, H, T$, where $S$ is entry and $T$ is terminal. "
            "Directed edges $(u, v)$ represent precedence with latency in milliseconds ($\\text{ms}$). "
            "Assuming each task starts immediately once all predecessors complete, determine the critical path duration (maximum latency from $S$ to $T$). "
            "The answer should be expressed in $\\text{ms}$. "
            "Report your final answer as a 2 significant figure number without units. "
            "Any intermediate calculations should be carried out to 6 significant figures. "
            "All unstated fundamental constants should be used to 4 significant figures."
        )
        
        ta = page.locator('textarea').first
        await ta.fill(prompt_text)
        print("Prompt text filled into textarea.")
        await asyncio.sleep(1)
        
        # 4. Take screenshot of editor before submitting
        await page.screenshot(path='handshake/scratch/prompt_editor_ready.png')
        print("Saved prompt_editor_ready.png")

if __name__ == '__main__':
    asyncio.run(main())
