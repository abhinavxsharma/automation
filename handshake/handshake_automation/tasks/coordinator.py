"""Lifecycle coordinator orchestrating all 12 Project Lumière task steps."""

import logging
import time

from playwright.sync_api import Error, Page

from handshake_automation.config import Settings
from handshake_automation.tasks import (
    distractors_filler,
    domain_selector,
    failure_justifier,
    form_filler,
    model_tester,
    navigator,
    submitter,
    task_builder,
)

logger = logging.getLogger(__name__)


def process_single_task(page: Page, cfg: Settings) -> bool:
    """Execute end-to-end authoring and submission of one Lumière task."""
    start = time.monotonic()
    page = navigator.get_task_page(page)
    if not navigator.claim_or_resume_task(page, cfg.tasks_url):
        return False
    domain = "v2" if task_builder.V2_PATH.is_file() else "cs"
    t = task_builder.build_lumiere_task(cfg, domain=domain)

    domain_selector.select_subdomain(page, t.get("supertype", "Computer Science"), t.get("subtype", "Algorithms and Complexity"))
    domain_selector.set_source_and_license(page, is_original=t.get("is_original", True), source_url=t.get("source_url", "N/A"), license_type=t.get("license", "N/A"))
    form_filler.fill_step_input(page, t["prompt"], file_path=t["image_path"])
    if not model_tester.verify_model_failures(page):
        return False
    form_filler.fill_step_input(page, t["gtfa"])
    form_filler.fill_step_input(page, t["image_description"])
    failure_justifier.fill_failure_justifications(page, t.get("failure_category", "Topological"), t["failure_justification"])
    form_filler.fill_step_input(page, t["solution"])
    distractors_filler.fill_distractors(page, t.get("distractors", []))
    distractors_filler.fill_answer_format(page, t.get("answer_format", "Decimal"), t.get("decimal_places", 2))
    return submitter.confirm_and_submit(page, start, cfg.auto_submit, cfg.min_time_sec)


def process_handshake_tasks(page: Page, cfg: Settings) -> None:
    """Continuous processing loop for Handshake AI tasks."""
    logger.info("Starting Handshake Project Lumière loop (max: %d)...", cfg.max_tasks)
    for i in range(1, cfg.max_tasks + 1):
        logger.info("=== Processing Lumière Task %d / %d ===", i, cfg.max_tasks)
        try:
            if not process_single_task(navigator.get_task_page(page), cfg):
                time.sleep(30)
        except (Error, RuntimeError, ValueError) as exc:
            logger.warning("Task error: %s. Resuming in 5s...", exc)
            time.sleep(5)
