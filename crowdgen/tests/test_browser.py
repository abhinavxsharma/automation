"""Tests for browser session manager and CDP connection."""

from unittest.mock import MagicMock, patch

from crowdgen_automation.browser import (
    acquire_browser_session,
    get_chrome_debug_dir,
    is_cdp_available,
)
from crowdgen_automation.instances import InstanceConfig


def test_is_cdp_available_true() -> None:
    """Verify is_cdp_available returns True on successful connect."""
    with patch("socket.socket") as mock_sock_cls:
        mock_sock = MagicMock()
        mock_sock_cls.return_value.__enter__.return_value = mock_sock
        mock_sock.connect_ex.return_value = 0
        assert is_cdp_available(9222) is True


def test_is_cdp_available_false() -> None:
    """Verify is_cdp_available returns False when port is closed."""
    with patch("socket.socket") as mock_sock_cls:
        mock_sock = MagicMock()
        mock_sock_cls.return_value.__enter__.return_value = mock_sock
        mock_sock.connect_ex.return_value = 111
        assert is_cdp_available(9222) is False


def test_get_chrome_debug_dir() -> None:
    """Verify Chrome debug user data directory path."""
    path = get_chrome_debug_dir()
    assert ".chrome-debug" in str(path)


def test_acquire_browser_session_cdp() -> None:
    """Verify connects over CDP when port is available."""
    mock_p = MagicMock()
    mock_browser = MagicMock()
    mock_ctx = MagicMock()
    mock_page = MagicMock()
    mock_page.url = "https://dq0uw9vf3nt8l.cloudfront.net/annotate/123?mode=annotation"
    mock_ctx.pages = [mock_page]
    mock_browser.contexts = [mock_ctx]
    mock_p.chromium.connect_over_cdp.return_value = mock_browser

    inst = InstanceConfig(email="user@test.com", password="pwd")
    with patch("crowdgen_automation.browser.is_cdp_available", return_value=True):
        ctx, page, is_cdp = acquire_browser_session(mock_p, inst)
        assert is_cdp is True
        assert ctx == mock_ctx
        assert page == mock_page
        mock_p.chromium.connect_over_cdp.assert_called_once_with("http://127.0.0.1:9222")


def test_acquire_browser_session_persistent() -> None:
    """Verify launches persistent context when CDP is not available."""
    mock_p = MagicMock()
    mock_ctx = MagicMock()
    mock_page = MagicMock()
    mock_ctx.pages = [mock_page]
    mock_p.chromium.launch_persistent_context.return_value = mock_ctx

    inst = InstanceConfig(email="user@test.com", password="pwd")
    with (
        patch("crowdgen_automation.browser.is_cdp_available", return_value=False),
        patch("crowdgen_automation.browser.get_chrome_debug_dir") as mock_ud,
    ):
        mock_dir = MagicMock()
        mock_dir.glob.return_value = []
        mock_ud.return_value = mock_dir
        ctx, page, is_cdp = acquire_browser_session(mock_p, inst)
        assert is_cdp is False
        assert ctx == mock_ctx
        assert page == mock_page
        mock_p.chromium.launch_persistent_context.assert_called_once()
