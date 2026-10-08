import base64, os, re
from pathlib import Path
import requests
from dotenv import load_dotenv
load_dotenv(Path("C:/Users/Abhinav/Desktop/coursera/handshake/.env"))
key=os.getenv("OPENROUTER_API_KEY","").strip()
base=os.getenv("OPENROUTER_BASE_URL","https://openrouter.ai/api/v1").rstrip("/")
img=Path("C:/Users/Abhinav/Desktop/coursera/handshake/workspace/v2/diagram.png")
prompt=Path("C:/Users/Abhinav/Desktop/coursera/handshake/workspace/v2/prompt.txt").read_text(encoding="utf-8")
b64=base64.b64encode(img.read_bytes()).decode()
data_url=f"data:image/png;base64,{b64}"
def call(name):
    headers={"Authorization":f"Bearer {key}","Content-Type":"application/json","HTTP-Referer":"https://ai.joinhandshake.com","X-Title":"Lumiere v2 test2"}
    body={"model":name,"max_tokens":900,"messages":[{"role":"user","content":[{"type":"text","text":prompt},{"type":"image_url","image_url":{"url":data_url}}]}]}
    print(f"\n--- {name} ---")
    try:
        r=requests.post(f"{base}/chat/completions",headers=headers,json=body,timeout=90)
        print("Status",r.status_code)
        if r.status_code!=200:
            print(r.text[:1200]); return
        c=r.json()["choices"][0]["message"]["content"]
        print(c[:2200])
        nums=re.findall(r"\b\d{2,3}\b",c)
        for n in nums:
            if 60<=int(n)<=100:
                err=abs(int(n)-77)/77*100
                print(f" {n} err {err:.1f}% {'>2% FAIL' if err>2 else 'pass'}")
    except Exception as e: print(e)

for m in ["google/gemini-2.5-pro","openai/gpt-4o","openai/gpt-4o-mini","google/gemini-2.0-flash-001"]:
    call(m)
