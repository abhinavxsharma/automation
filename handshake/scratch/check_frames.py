import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import ensure_chrome, PORT

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    for c_i, ctx in enumerate(browser.contexts):
        for p_i, pg in enumerate(ctx.pages):
            print(f"Context {c_i} Page {p_i}: URL={pg.url}")
            print(f"  Frames: {len(pg.frames)}")
            for f_i, fr in enumerate(pg.frames):
                print(f"    Frame {f_i}: name='{fr.name}', url={fr.url}")
                ex = fr.get_by_text("Exit", exact=True)
                if ex.count() > 0:
                    print(f"      FOUND EXIT IN FRAME {f_i}! count={ex.count()}, box={ex.first.bounding_box()}")
