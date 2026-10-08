"""Assembles problem artifacts and diagram generation for CS & Engineering."""

import json
import time
from pathlib import Path
from typing import Any

from handshake_automation.config import Settings
from handshake_automation.tasks import ai_author, cs_diagram_creator, diagram_creator

V2_PATH = Path("workspace/v2/artifacts.json")


def build_lumiere_task(cfg: Settings, domain: str = "cs") -> dict[str, Any]:
    """Create self-authored diagram and LLM authored problem artifacts."""
    if domain.lower() in ("v2", "preauthored") and V2_PATH.is_file():
        return json.loads(V2_PATH.read_text(encoding="utf-8"))


    d_path = Path("scratch") / f"diagram_{int(time.monotonic())}.png"
    d_path.parent.mkdir(parents=True, exist_ok=True)
    if domain.lower() in ("cs", "computer_science"):
        d_info = cs_diagram_creator.create_network_flow_diagram(d_path)
    else:
        d_info = diagram_creator.create_beam_diagram(d_path)
        d_info["supertype"] = "Mechanical Engineering"
        d_info["subtype"] = "Beam Analysis"

    task = ai_author.author_task(d_info, cfg)
    task["image_path"] = str(d_info["path"])
    task["is_original"] = True
    task["supertype"] = d_info.get("supertype", "Computer Science")
    task["subtype"] = d_info.get("subtype", "Algorithms & Complexity")
    return task

