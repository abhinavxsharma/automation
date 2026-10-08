import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    body = pg.evaluate("() => document.body ? document.body.innerText : ''")
    is_gen = "Generating response" in body or "The next response is now being generated" in body
    print("Is Block 2 generating?", is_gen)
    idx2 = body.find("Block 2 Responses:")
    if idx2 != -1:
        print("Block 2 snippet:", body[idx2:idx2+300].encode('ascii', 'replace').decode('ascii'))
