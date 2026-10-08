import json
import os

with open(
    "handshake/scratch/live_body_text.txt", "r", encoding="utf-8", errors="ignore"
) as f:
    text = f.read()


def extract_between(text, start_marker, end_marker):
    p1 = text.find(start_marker)
    if p1 == -1:
        return ""
    p2 = text.find(end_marker, p1 + len(start_marker))
    if p2 == -1:
        return text[p1 + len(start_marker) :].strip()
    return text[p1 + len(start_marker) : p2].strip()


data = {
    "prompt": extract_between(text, "Enter your prompt:", "PNG"),
    "img_desc": extract_between(
        text, "The description should be a minimum of 200 words", "Error Type"
    ),
    "justification": extract_between(
        text, "Model Failure Justification", "Golden Solution:"
    ),
    "golden": extract_between(
        text, "Enter the Golden Solution:", "Provide links to any sources"
    ),
    "distractors": extract_between(
        text,
        "Ensure it is in the same answer format as the Final Answer",
        "Now, a judge will evaluate",
    ),
}

with open(
    "handshake/scratch/backed_up_fields.json", "w", encoding="utf-8"
) as out:
    json.dump(data, out, indent=2, ensure_ascii=False)

print("Saved backed_up_fields.json successfully!")
for k, v in data.items():
    print(f"{k}: length={len(v)}")
