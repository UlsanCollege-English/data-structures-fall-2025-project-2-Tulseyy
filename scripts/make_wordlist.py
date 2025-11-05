# Generate a 50,000‑word frequency snapshot using wordfreq.
# Run locally once, commit the output to data/words.csv. Not used by tests at runtime.

from __future__ import annotations
import csv
from pathlib import Path
from typing import List, Tuple

def get_wordfreq_imports() -> Tuple[callable, callable]:
    """Get the required functions from wordfreq package."""
    try:
        from wordfreq import top_n_list, zipf_frequency
        return top_n_list, zipf_frequency
    except ImportError as e:
        raise SystemExit("Install wordfreq first: pip install wordfreq") from e

def main() -> None:
    top_n_list, zipf_frequency = get_wordfreq_imports()
    words: List[str] = top_n_list('en', 50_000)
    out_path = Path(__file__).resolve().parent.parent / 'data' / 'words.csv'
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for word in words:
            writer.writerow([word, f"{zipf_frequency(word, 'en'):.6f}"])
    
    print(f"Wrote {len(words)} rows to {out_path}")

if __name__ == '__main__':
    main()