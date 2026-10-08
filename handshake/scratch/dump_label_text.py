import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    txt = page.evaluate("() => document.body ? document.body.innerText : ''")
    Path("scratch/full_body_utf8.txt").write_text(txt, encoding="utf-8")
    
    idx = txt.find("Label")
    print("Index of 'Label':", idx)
    if idx != -1:
        snippet = txt[idx-50:idx+500]
        Path("scratch/label_snippet.txt").write_text(snippet, encoding="utf-8")
        print("Snippet written to scratch/label_snippet.txt")
