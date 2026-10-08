"""Browser session manager for Handshake AI automation."""

import logging
import os
import socket
import subprocess
import time
from pathlib import Path

from playwright.sync_api import BrowserContext, Playwright

logger = logging.getLogger(__name__)


def is_cdp_available(port: int = 9222) -> bool:
    """Check if Chrome remote debugging port is open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.3)
            return s.connect_ex(("127.0.0.1", port)) == 0
    except OSError:
        return False


def get_chrome_path() -> str:
    """Find system Google Chrome executable path."""
    for p in [r"%ProgramFiles%\Google\Chrome\Application\chrome.exe", r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe", r"%LocalAppData%\Google\Chrome\Application\chrome.exe"]:
        if Path(exp := os.path.expandvars(p)).is_file():
            return exp
    return "chrome"


def launch_chrome_debug_process(port: int = 9222) -> None:
    """Launch Google Chrome in remote debugging mode."""
    chrome_bin = get_chrome_path()
    profile_dir = Path.home() / ".handshake_chrome_profile"
    profile_dir.mkdir(parents=True, exist_ok=True)
    cmd = [chrome_bin, f"--remote-debugging-port={port}", f"--user-data-dir={profile_dir}", "--no-first-run"]
    flags = getattr(subprocess, "DETACHED_PROCESS", 0) | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=flags)


def create_browser_context(playwright: Playwright, headless: bool = False, port: int = 9222) -> BrowserContext:
    """Attach to existing Chrome via CDP or launch persistent context."""
    if not is_cdp_available(port):
        logger.info("CDP not detected on port %d. Launching Chrome...", port)
        launch_chrome_debug_process(port)
        for _ in range(12):
            if is_cdp_available(port):
                break
            time.sleep(0.5)
    if not is_cdp_available(port):
        raise RuntimeError(f"Chrome CDP port {port} unavailable. Run start_chrome_debug.bat first.")
    logger.info("Connecting to Chrome on CDP port %d...", port)
    browser = playwright.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
    return browser.contexts[0] if browser.contexts else browser.new_context()
