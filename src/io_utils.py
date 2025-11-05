# src/io_utils.py
"""CSV load/save helpers for (word, score) pairs.
The file format is two columns without header: word,score
"""

import csv
from pathlib import Path
from typing import Iterable, List, Tuple, Union


def load_csv(path: Union[str, Path]) -> List[Tuple[str, float]]:
    """Load a two-column CSV of word,score pairs.

    - `path` may be a string or Path.
    - Words are stripped and lower-cased.
    - Missing or non-numeric scores become 0.0.
    """
    p = Path(path)
    words: List[Tuple[str, float]] = []
    with p.open(newline='', encoding='utf-8') as f:
        for row in csv.reader(f):
            if not row:
                continue
            w = row[0].strip().lower()
            try:
                s = float(row[1]) if len(row) > 1 else 0.0
            except (ValueError, TypeError):
                s = 0.0
            words.append((w, s))
    return words


def save_csv(path: Union[str, Path], items: Iterable[Tuple[str, float]]) -> None:
    """Save an iterable of (word, score) pairs to CSV.

    `items` may be any iterable yielding (word, score) tuples.
    """
    p = Path(path)
    with p.open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for w, s in items:
            # Ensure we write a simple numeric value for scores
            try:
                score = float(s)
            except (ValueError, TypeError):
                score = 0.0
            writer.writerow([w, score])
