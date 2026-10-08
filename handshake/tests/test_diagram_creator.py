"""Tests for diagram creator."""

from pathlib import Path

from handshake_automation.tasks.diagram_creator import (
    create_beam_diagram,
    create_circuit_diagram,
)


def test_create_beam_diagram(tmp_path: Path) -> None:
    """Verify beam diagram generates a readable PNG on disk."""
    out_file = tmp_path / "beam.png"
    res = create_beam_diagram(out_file)
    assert out_file.is_file()
    assert out_file.stat().st_size > 1000
    assert "p1" in res
    assert "l1" in res


def test_create_circuit_diagram(tmp_path: Path) -> None:
    """Verify circuit diagram generates a readable PNG on disk."""
    out_file = tmp_path / "circuit.png"
    res = create_circuit_diagram(out_file)
    assert out_file.is_file()
    assert out_file.stat().st_size > 1000
    assert "r1" in res
    assert "vdd" in res


def test_create_network_flow_diagram(tmp_path: Path) -> None:
    """Verify CS network flow diagram generates a readable PNG on disk."""
    from handshake_automation.tasks.cs_diagram_creator import (
        create_network_flow_diagram,
    )

    out_file = tmp_path / "network_flow.png"
    res = create_network_flow_diagram(out_file)
    assert out_file.is_file()
    assert out_file.stat().st_size > 1000
    assert res["supertype"] == "Computer Science"
    assert res["subtype"] == "Algorithms & Complexity"

