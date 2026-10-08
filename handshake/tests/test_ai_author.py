"""Tests for AI authoring engine."""

from unittest.mock import MagicMock, patch

from handshake_automation.config import Settings
from handshake_automation.tasks.ai_author import author_task


def test_author_task_success(mock_settings: Settings) -> None:
    """Verify author_task calls model and parses structured JSON."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": (
                        '{"prompt": "Calculate deflection $y$. The answer should be expressed in mm. Report your final answer as a 3 significant figure number without units. Any intermediate calculations should be carried out to 6 significant figures. All unstated fundamental constants should be used to 4 significant figures.", '
                        '"gtfa": "14.2", '
                        '"image_description": "Beam with loads", '
                        '"solution": "Step 1: Inspect beam...", '
                        '"distractors": ["10.1", "12.3", "16.4", "18.2", "20.1"], '
                        '"answer_format": "Decimal", '
                        '"decimal_places": 1, '
                        '"failure_category": "Spatial", '
                        '"failure_justification": "Model misread point load location."}'
                    )
                }
            }
        ]
    }
    with patch("requests.post", return_value=mock_resp):
        res = author_task({"p1": 20, "l1": 3}, mock_settings)
        assert "Calculate deflection" in res["prompt"]
        assert res["gtfa"] == "14.2"
        assert len(res["distractors"]) == 5
