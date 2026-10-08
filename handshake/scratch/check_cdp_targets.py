import urllib.request, json

try:
    resp = urllib.request.urlopen("http://127.0.0.1:9222/json/list")
    targets = json.loads(resp.read().decode())
    print(f"Total targets: {len(targets)}")
    for t in targets:
        print(f"Type: {t.get('type')}, Title: {t.get('title')}, URL: {t.get('url')}")
except Exception as e:
    print("Error:", e)
