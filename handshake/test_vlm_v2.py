"""Live VLM stump test for workspace/v2/diagram.png GTFA=77."""
import base64, json, os, sys
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv(Path("C:/Users/Abhinav/Desktop/coursera/handshake/.env"))

key = os.getenv("OPENROUTER_API_KEY", "").strip()
base = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/")
model = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash")
fallback = os.getenv("OPENROUTER_FALLBACK_MODEL", "google/gemini-2.5-flash")

img_path = Path("C:/Users/Abhinav/Desktop/coursera/handshake/workspace/v2/diagram.png")
print(f"Model: {model} fallback: {fallback}")
print(f"Image: {img_path} {img_path.stat().st_size}B")
print(f"Key prefix: {key[:10]}... len {len(key)}")
print(f"GTFA expected: 77")

# Load prompt from artifacts
prompt = Path("C:/Users/Abhinav/Desktop/coursera/handshake/workspace/v2/prompt.txt").read_text(encoding="utf-8")
print(f"Prompt: {prompt[:120]}...")

b64 = base64.b64encode(img_path.read_bytes()).decode()
# data url
data_url = f"data:image/png;base64,{b64}"

def call(model_name):
    url = f"{base}/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ai.joinhandshake.com",
        "X-Title": "Lumiere VLM test",
    }
    body = {
        "model": model_name,
        "max_tokens": 800,
        "messages": [
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": data_url}}
            ]}
        ]
    }
    print(f"\n--- Calling {model_name} ---")
    try:
        r = requests.post(url, headers=headers, json=body, timeout=90)
        print(f"Status: {r.status_code}")
        if r.status_code != 200:
            print(r.text[:1500])
            return None
        j = r.json()
        content = j["choices"][0]["message"]["content"]
        print(f"Response: {content[:2000]}")
        # extract number
        import re
        nums = re.findall(r"\b\d{2,3}\b", content)
        print(f"Numbers found: {nums[:10]}")
        # compute error vs 77
        for n in nums:
            try:
                v = int(n)
                if 60 <= v <= 100:
                    err = abs(v-77)/77*100
                    print(f"  Candidate {v} -> error {err:.1f}% {'FAIL >2%' if err>2 else 'PASS (<2%)'}")
            except: pass
        return content
    except Exception as e:
        print(f"Error: {e}")
        return None

# Try primary
res = call(model)
if res is None and fallback != model:
    print(f"\n--- Falling back to {fallback} ---")
    call(fallback)

# Also try a second vision model for 2/2 simulation: anthropic/claude-3.5-sonnet if available, else same
alt = "anthropic/claude-3.5-sonnet"
if alt != model:
    print(f"\n--- Alt model try {alt} (for 2/2 simulation) ---")
    call(alt)
