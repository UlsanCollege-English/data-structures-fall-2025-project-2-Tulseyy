# src/trie.py
"""
Trie data structure for autocomplete.

Public surface expected by tests:
- class Trie
  - insert(word: str, freq: float) -> None
  - remove(word: str) -> bool
  - contains(word: str) -> bool
  - complete(prefix: str, k: int) -> list[str]
  - stats() -> tuple[int, int, int]  # (words, height, nodes)

Complexity target (justify in docstrings):
- insert/remove/contains: O(len(word))
- complete(prefix, k): roughly O(m + k log k')
"""

class TrieNode:
    __slots__ = ("children", "is_word", "freq")

    def __init__(self):
        self.children = {}
        self.is_word = False
        self.freq = 0.0

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self._words = 0
        self._nodes = 1

    def insert(self, word, freq):
        # normalize
        w = word.lower()
        node = self.root
        for ch in w:
            if ch not in node.children:
                node.children[ch] = TrieNode()
                self._nodes += 1
            node = node.children[ch]
        # if this was not previously a word, increment word count
        if not node.is_word:
            node.is_word = True
            self._words += 1
        # store/replace frequency
        node.freq = float(freq)

    def remove(self, word):
        w = word.lower()
        node = self.root
        stack = []  # nodes along the path
        for ch in w:
            if ch not in node.children:
                return False
            stack.append((node, ch))
            node = node.children[ch]
        if not node.is_word:
            return False
        # unset word marker
        node.is_word = False
        node.freq = 0.0
        self._words -= 1
        # optional: prune nodes that are no longer needed
        # we will remove trailing nodes that have no children and are not word nodes
        while stack:
            parent, ch = stack.pop()
            child = parent.children[ch]
            if child.children or child.is_word:
                break
            # remove child
            del parent.children[ch]
            self._nodes -= 1
        return True

    def contains(self, word):
        w = word.lower()
        node = self.root
        for ch in w:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return bool(node.is_word)

    def complete(self, prefix, k):
        p = prefix.lower()
        node = self.root
        # navigate to prefix node
        for ch in p:
            if ch not in node.children:
                return []
            node = node.children[ch]

        results = []  # list of (word, freq)

        def dfs(n, path):
            if n.is_word:
                results.append((path, n.freq))
            for ch in n.children:
                dfs(n.children[ch], path + ch)

        dfs(node, p)

        # sort by descending frequency, tie-break lexicographic
        results.sort(key=lambda x: (-x[1], x[0]))
        return [w for w, _ in results[:k]]

    def stats(self):
        # words and nodes are tracked incrementally
        words = self._words

        # compute height as max depth among word nodes (number of letters)
        max_depth = 0

        def dfs_depth(n, depth):
            nonlocal max_depth
            if n.is_word:
                if depth > max_depth:
                    max_depth = depth
            for ch in n.children:
                dfs_depth(n.children[ch], depth + 1)

        dfs_depth(self.root, 0)
        height = max_depth
        nodes = self._nodes
        return words, height, nodes
