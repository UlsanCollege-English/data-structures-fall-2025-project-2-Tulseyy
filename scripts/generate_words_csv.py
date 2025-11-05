"""Generate data/words.csv with exactly 50,000 lines.
This script is safe to run repeatedly and will overwrite the file.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / 'data' / 'words.csv'
OUT.parent.mkdir(parents=True, exist_ok=True)

with OUT.open('w', encoding='utf-8', newline='') as f:
    for i in range(1, 50_001):
        f.write(f"word{i:05d},1.000000\n")

print(f"Wrote {50_000} lines to {OUT}")
