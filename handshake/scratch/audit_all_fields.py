import asyncio
import sys
import json
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        audit = await page.evaluate('''() => {
            const results = {};
            
            // 1. Uploaded image
            const imgBtn = document.querySelector('button[aria-label*="dag_final_corrected.png"], button[aria-label*="View file"]');
            results.uploadedImage = imgBtn ? imgBtn.getAttribute('aria-label') : 'Not found';
            
            // 2. Prompt text
            const promptBlock = document.querySelector('[data-block-id="9e254568-dd1a-476f-9eb5-d49807d95930"]');
            results.promptText = promptBlock ? promptBlock.innerText : 'Not found';
            
            // 3. Final Answer
            const faBlock = document.querySelector('[data-block-id="59f6e912-b5be-4bcf-bde5-9d9f773bfd5f"]');
            results.finalAnswer = faBlock ? faBlock.innerText : 'Not found';
            
            // 4. Answer Format
            const afBlock = document.querySelector('[data-block-id="5cd12d4c-dd4e-44ab-af36-b31bd1249550"]');
            results.answerFormat = afBlock ? afBlock.innerText : 'Not found';
            
            // 5. Image Description
            const descBlock = document.querySelector('[data-block-id="3993dc6e-cf3b-448e-873a-46d9bef303de"]');
            results.imageDescription = descBlock ? descBlock.innerText : 'Not found';
            
            // 6. Model Failure Justification
            const justBlock = document.querySelector('[data-block-id="eac54b4b-5677-48f0-bf86-228cfb012c57"]');
            results.justification = justBlock ? justBlock.innerText : 'Not found';
            
            // 7. Golden Solution
            const gsBlock = document.querySelector('[data-block-id="831895bf-4f9f-4e8f-9d56-8f6a8d80443f"]');
            results.goldenSolution = gsBlock ? gsBlock.innerText : 'Not found';
            
            // 8. Distractors
            results.distractors = [
                document.querySelector('[data-block-id="59332224-3ea1-43d3-ba7c-c02281bcf17e"]')?.innerText,
                document.querySelector('[data-block-id="7c4519e2-5462-4ec2-92fe-141b9f68eecb"]')?.innerText,
                document.querySelector('[data-block-id="80097086-5e2e-4923-809f-550f982cc900"]')?.innerText,
                document.querySelector('[data-block-id="c2d0f730-9092-4df4-9100-a96a96c7ef75"]')?.innerText,
                document.querySelector('[data-block-id="b7136582-2d3c-461f-ae88-0e151cfddd83"]')?.innerText
            ];
            
            // 9. QC Justification
            const qcBlock = document.querySelector('[data-block-id="0b98ef29-29f5-42d4-b22d-53e2d2feb178"]');
            results.qcJustification = qcBlock ? qcBlock.innerText : 'Not found';
            
            // 10. Sidebar feedback unresolved count
            const unresolved = Array.from(document.querySelectorAll('button[aria-label="Resolve"]')).length;
            results.unresolvedFeedback = unresolved;
            
            return results;
        }''')
        
        print("================ FINAL CONSISTENCY AUDIT ================\n")
        print("1. UPLOADED IMAGE:")
        print("   ", audit['uploadedImage'])
        print("\n2. PROMPT TEXT:")
        print("   ", audit['promptText'][:200].replace('\n', ' '))
        print("   Closing:", audit['promptText'][-200:].replace('\n', ' '))
        print("\n3. FINAL ANSWER:")
        print("   ", audit['finalAnswer'].replace('\n', ' '))
        print("\n4. ANSWER FORMAT:")
        print("   ", audit['answerFormat'].replace('\n', ' '))
        print("\n5. IMAGE DESCRIPTION:")
        desc = audit['imageDescription']
        words = len(desc.split())
        print(f"    Words: {words}")
        print("    Contains 'black':", 'black' in desc.lower())
        print("    Contains 'navy':", 'navy' in desc.lower())
        print("    Contains 'cross':", 'cross' in desc.lower())
        print("    Preview:", desc[:200].replace('\n', ' '))
        print("\n6. MODEL FAILURE JUSTIFICATION:")
        just = audit['justification']
        print("    Contains KaTeX \\(:", '\\(' in just)
        print("    Contains C\\to F:", 'C\\to F' in just or 'C\\to' in just)
        print("    Contains 85:", '85' in just)
        print("    Preview:", just[:200].replace('\n', ' '))
        print("\n7. GOLDEN SOLUTION:")
        gs = audit['goldenSolution']
        print("    Length:", len(gs))
        print("    Contains KaTeX \\(:", '\\(' in gs)
        print("    Contains Step 5:", 'Step 5' in gs)
        print("    Contains 64 ms (path 1):", 'S\\to A\\to C\\to E\\to T' in gs or '14 + 9 + 17 + 24 = 64' in gs)
        print("    Contains 64 ms (path 2):", 'S\\to A\\to C\\to F\\to T' in gs or '14 + 9 + 21 + 20 = 64' in gs)
        print("    Contains 76 ms critical path:", '14 + 22 + 12 + 8 + 20 = 76' in gs)
        print("\n8. DISTRACTORS:")
        for i, d in enumerate(audit['distractors']):
            print(f"    Distractor {i+1}:", d.replace('\n', ' ') if d else 'None')
        print("\n9. QC JUSTIFICATION:")
        print("    Preview:", audit['qcJustification'][:200].replace('\n', ' '))
        print("\n10. UNRESOLVED FEEDBACK COUNT:")
        print("    Count:", audit['unresolvedFeedback'])

if __name__ == "__main__":
    asyncio.run(main())
