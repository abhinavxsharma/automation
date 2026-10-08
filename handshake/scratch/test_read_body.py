import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(2500)
    
    txt = page.evaluate("() => document.body ? document.body.innerText : ''")
    Path("scratch/full_body_utf8.txt").write_text(txt, encoding="utf-8")
    print("Body length:", len(txt))
    
    idx = txt.find("Label")
    print("Index of 'Label':", idx)
    if idx != -1:
        snippet = txt[idx-50:idx+500]
        Path("scratch/label_snippet.txt").write_text(snippet, encoding="utf-8")
        print("Found snippet containing Label!")
        
    idx2 = txt.find("Error Type")
    print("Index of 'Error Type':", idx2)
    if idx2 != -1:
        snippet2 = txt[idx2-50:idx2+500]
        Path("scratch/error_type_snippet.txt").write_text(snippet2, encoding="utf-8")
        print("Found snippet containing Error Type!")
