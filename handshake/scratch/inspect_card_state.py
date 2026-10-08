import sys

sys.path.append("handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.screenshot(path="handshake/scratch/current_card_state.png")

    spinners = page.locator("svg.animate-spin, [class*='spin']").all()
    print("Spinners found:", len(spinners))

    rem_btns = page.locator("button[aria-label='Remove']").all()
    print("Remove buttons found:", len(rem_btns))
    for i, r in enumerate(rem_btns):
        print(f"Remove btn {i}: visible={r.is_visible()}")

    imgs = page.locator("img").all()
    print("Images found on page:", len(imgs))
    for i, im in enumerate(imgs):
        print(
            f"Image {i}: visible={im.is_visible()}, src={im.get_attribute('src')[:80]}"
        )

    # Check text inside the Step 7 area
    card = page.locator("textarea").first
    print("Textarea visible:", card.is_visible())
    if card.is_visible():
        print("Textarea value:", card.input_value()[:100])
