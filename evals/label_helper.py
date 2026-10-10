import json
from pathlib import Path

import requests

API = "http://127.0.0.1:8000"
GOLDEN = Path("golden/golden.json")

for case in json.loads(GOLDEN.read_text()):
    if not case["answerable"]:
        continue
    hits = requests.post(f"{API}/retrieve", json={"question": case["question"], "k": 5}).json()["hits"]
    print(f"\n=== {case['id']}: {case['question']}")
    for h in hits:
        first_line = h["text"].split("\n")[0]
        print(f"  {h['distance']:.3f}  {h['id']}  |  {first_line}")