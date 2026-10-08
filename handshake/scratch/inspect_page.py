import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.append(str(Path(__file__).parent))
from chrome_helper import get_task_page


def inspect_blocks():
    with sync_playwright() as p:
        browser, page = get_task_page(p)
        page.wait_for_timeout(1000)

        # Let's find all cards/sections
        cards = page.locator("div[class*='card'], div[class*='Card'], div[data-testid*='block'], div[class*='Block']").all()
        print(f"Total card-like elements: {len(cards)}")

        # Also let's find all headings / labels
        headings = page.locator("h1, h2, h3, h4, h5, h6, label, p").all()
        interesting = []
        for h in headings:
            t = h.inner_text().strip()
            if any(k in t.lower() for k in ["prompt", "image", "circuit", "model", "response", "golden", "distractor", "answer"]):
                if len(t) < 120 and t not in interesting:
                    interesting.append(t)

        print("Interesting text elements:")
        for item in interesting[:30]:
            print(" -", item)

        # Check images
        imgs = page.locator("img").all()
        print(f"Total images on page: {len(imgs)}")
        for i, img in enumerate(imgs):
            src = img.get_attribute("src") or ""
            alt = img.get_attribute("alt") or ""
            print(f"Img {i}: src={src[:80]}... alt={alt}")


if __name__ == "__main__":
    inspect_blocks()
