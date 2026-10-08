"""Tests for Handshake instance loader and validation."""

from pathlib import Path

import pytest

from handshake_automation.instances import InstanceConfig, load_instances


def test_instance_validation_success() -> None:
    """Verify valid instance passes validation."""
    inst = InstanceConfig(
        email="fellow@example.com",
        tasks_url="https://ai.joinhandshake.com/fellow/123/tasks",
    )
    inst.validate()
    cfg = inst.to_settings()
    assert cfg.max_tasks == 50
    assert cfg.auto_submit is True


def test_instance_validation_empty_email() -> None:
    """Verify empty email raises ValueError."""
    with pytest.raises(ValueError, match="email must not be empty"):
        InstanceConfig(email="", tasks_url="https://example.com").validate()


def test_instance_validation_invalid_url() -> None:
    """Verify invalid URL raises ValueError."""
    with pytest.raises(ValueError, match="Invalid tasks_url"):
        InstanceConfig(email="user@test.com", tasks_url="not_a_url").validate()


def test_load_instances(tmp_path: Path) -> None:
    """Verify dynamic loading from instances.py file."""
    inst_file = tmp_path / "instances.py"
    inst_file.write_text(
        "from handshake_automation.instances import InstanceConfig\n"
        "INSTANCES = [InstanceConfig(email='fellow@test.com')]\n"
    )
    loaded = load_instances(str(inst_file))
    assert len(loaded) == 1
    assert loaded[0].email == "fellow@test.com"
