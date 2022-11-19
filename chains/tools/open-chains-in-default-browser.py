import os
import time
import json
import webbrowser
from pathlib import Path

with open(os.path.join(Path(os.getcwd()).parent.absolute(), "chains.json")) as f:
    explorers = [
        explorers[0]
        for c in json.load(f)
        if (explorers := c.get('explorers', []))
    ]

for i, explorer in enumerate(explorers):
    webbrowser.open(explorer['url'])
    if i % 5 == 0:
        time.sleep(5)
    else:
        time.sleep(1)
