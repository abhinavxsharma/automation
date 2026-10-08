import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    step_info = pg.evaluate('''() => {
        const editBtns = Array.from(document.querySelectorAll('button[aria-label="Edit this step"]'));
        const s11 = editBtns[11] ? editBtns[11].parentElement.parentElement.innerText : '';
        const s14 = editBtns[14] ? editBtns[14].parentElement.parentElement.innerText : '';
        const s15 = editBtns[15] ? editBtns[15].parentElement.parentElement.innerText : '';
        const s16 = editBtns[16] ? editBtns[16].parentElement.parentElement.innerText : '';
        return { s11, s14, s15, s16 };
    }''')
    
    with open("scratch/step11_desc.txt", "w", encoding="utf-8") as f:
        f.write(step_info["s11"])
    with open("scratch/step14_error_type.txt", "w", encoding="utf-8") as f:
        f.write(step_info["s14"])
    with open("scratch/step15_justification.txt", "w", encoding="utf-8") as f:
        f.write(step_info["s15"])
    with open("scratch/step16_golden_solution.txt", "w", encoding="utf-8") as f:
        f.write(step_info["s16"])
        
    print("Saved step details to scratch/")
