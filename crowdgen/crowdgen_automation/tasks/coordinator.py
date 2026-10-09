"""Orchestrator for Project Origami / Maven task processing lifecycle."""

import logging
import time

import requests
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page
from tenacity import RetryError

from crowdgen_automation.auth import launch_project
from crowdgen_automation.config import Settings
from crowdgen_automation.tasks.capture import capture_task_image, get_task_context
from crowdgen_automation.tasks.filler import fill_maven_form
from crowdgen_automation.tasks.submit import submit_task
from crowdgen_automation.tasks.unit_loader import wait_for_new_unit
from crowdgen_automation.tasks.validator import click_validate
from crowdgen_automation.tasks.vision_solver import generate_captions

logger = logging.getLogger(__name__)


def process_single_task(page: Page, cfg: Settings, auto_submit: bool) -> bool:
    start_time, context = time.monotonic(), get_task_context(page)
    _, img_ref = capture_task_image(context)
    error_feedback: str | None = None
    for attempt in range(1, 4):
        logger.info("Generating captions (attempt %d/3)...", attempt)
        captions = generate_captions(img_ref, cfg, error_feedback=error_feedback)
        fill_maven_form(context, captions)
        if captions.get("unusable_quality") in (True, "true"):
            return submit_task(context, start_time, auto_submit, cfg.target_remaining_sec, page=page)
        passed, error_feedback = click_validate(context)
        if passed:
            return submit_task(context, start_time, auto_submit, cfg.target_remaining_sec, page=page)
        logger.warning("Attempt %d error: %s. Retrying...", attempt, error_feedback)
    logger.error("Task failed validation after 3 attempts.")
    return False


def process_maven_tasks(page: Page, cfg: Settings, auto_submit: bool = True) -> None:
    launch_project(page)
    logger.info("Starting continuous Maven task loop (max: %d)...", cfg.max_tasks)
    curr_unit = ""
    for task_idx in range(1, cfg.max_tasks + 1):
        logger.info("=== Processing Task %d / %d ===", task_idx, cfg.max_tasks)
        if "/annotate/" not in page.url:
            launch_project(page)
        curr_unit = wait_for_new_unit(page, curr_unit)
        try:
            ok = process_single_task(page, cfg, auto_submit=auto_submit)
        except (PlaywrightError, TimeoutError, ValueError, RuntimeError, OSError, requests.RequestException, RetryError) as exc:
            logger.warning("Task error: %s", exc)
            ok = False
        if not ok:
            page.reload()
            if not auto_submit:
                break
        page.wait_for_timeout(2000)
