"""Main execution entry point for Handshake AI automation."""

import logging
import sys

from playwright.sync_api import sync_playwright

from handshake_automation.browser import create_browser_context
from handshake_automation.instances import InstanceConfig, load_instances
from handshake_automation.keep_awake import allow_sleep, prevent_sleep
from handshake_automation.tasks.coordinator import process_handshake_tasks

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def run_instance(inst: InstanceConfig) -> None:
    """Run automation worker for an instance on active tab."""
    cfg = inst.to_settings()
    with sync_playwright() as p:
        ctx = create_browser_context(p, headless=inst.headless)
        page = next((t for t in ctx.pages if "/task/" in t.url and "71654a38" not in t.url), None)
        if not page:
            page = next((t for t in ctx.pages if "joinhandshake.com" in t.url and "71654a38" not in t.url), None)
        page = page or (ctx.pages[0] if ctx.pages else ctx.new_page())
        logger.info("Using page: %s", page.url)
        page.set_default_timeout(cfg.timeout_ms)
        process_handshake_tasks(page, cfg)


def run() -> None:
    """Load instances, activate sleep lock, and run tasks."""
    instances = load_instances("instances.py")
    prevent_sleep()
    try:
        for inst in instances:
            run_instance(inst)
    finally:
        allow_sleep()


def main() -> None:
    """Main CLI entry."""
    try:
        run()
    except KeyboardInterrupt:
        logger.info("Automation stopped by user (Ctrl+C). Exiting cleanly.")
        sys.exit(0)


if __name__ == "__main__":
    main()
