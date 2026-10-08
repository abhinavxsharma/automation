import json

transcript_path = r"C:\Users\Abhinav\.gemini\antigravity-ide\brain\3185991a-aaa5-495b-936b-a939eebcbbd9\.system_generated\logs\transcript.jsonl"
with open(transcript_path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if 11290 <= i <= 11350:
            d = json.loads(line)
            content = d.get("content", "")
            calls = d.get("tool_calls", [])
            if content:
                print(f"Line {i} content: {content[:200]}")
            for tc in calls:
                print(
                    f"Line {i} call: {tc.get('args', {}).get('CommandLine', '')[:200]}"
                )
