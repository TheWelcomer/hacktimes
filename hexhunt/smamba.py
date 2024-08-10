from typing import List, Set, Dict, Tuple

scrabbleScores = {
    'a': 1,
    'b': 1,
    'c': 1,
    'd': 1,
    'e': 1,
    'f': 1,
    'g': 1,
    'h': 1,
    'i': 1,
    'j': 1,
    'k': 1,
    'l': 1,
    'm': 1,
    'n': 1,
    'o': 1,
    'p': 1,
    'q': 1,
    'r': 1,
    's': 1,
    't': 1,
    'u': 1,
    'v': 1,
    'w': 1,
    'x': 1,
    'y': 1,
    'z': 1
}

squareBorders = {
    0: [1, 4, 5],
    1: [0, 2, 4, 5, 6],
    2: [1, 3, 5, 6, 7],
    3: [2, 6, 7],
    4: [0, 1, 5, 8, 9],
    5: [0, 1, 2, 4, 6, 8, 9, 10],
    6: [1, 2, 3, 5, 7, 9, 10, 11],
    7: [2, 3, 6, 10, 11],
    8: [4, 5, 9, 12, 13],
    9: [4, 5, 6, 8, 10, 12, 13, 14],
    10: [5, 6, 7, 9, 11, 13, 14, 15],
    11: [6, 7, 10, 14, 15],
    12: [8, 9, 13],
    13: [8, 9, 10, 12, 14],
    14: [9, 10, 11, 13, 15],
    15: [10, 11, 14]
}

def scrabble(word):
    wordlen = len(word)
    match wordlen:
        case 8:
            return 11
        case 7:
            return 5
        case 6:
            return 3
        case 5:
            return 2
        case _:
            return 1

class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_end_of_word: bool = False
        self.word: str = ""  # Store the complete word at end nodes


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.word = word

    def is_prefix(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True


def build_trie(dict: List[str]) -> Trie:
    trie = Trie()
    for word in dict:
        trie.insert(word)
    return trie


def precompute_words(board: List[str], trie: Trie, hex_borders: Dict[int, List[int]]) -> Dict[str, str]:
    word_dict: Dict[str, str] = {}
    max_length = 19

    for i in range(len(board)):
        visited = set([i])
        dfs(i, board[i], "", visited, board, trie, hex_borders, word_dict, max_length)

    return word_dict


def dfs(index: int, current_word: str, path: str, visited: Set[int], board: List[str],
        trie: Trie, hex_borders: Dict[int, List[int]], word_dict: Dict[str, str], max_length: int) -> None:
    node = trie.root
    for char in current_word:
        if char not in node.children:
            return
        node = node.children[char]

    if node.is_end_of_word:
        word_dict[path] = node.word

    if len(current_word) >= max_length:
        return

    for neighbor in hex_borders[index]:
        if neighbor not in visited:
            visited.add(neighbor)
            new_path = f"{path},{neighbor}" if path else str(neighbor)
            dfs(neighbor, current_word + board[neighbor], new_path, visited, board, trie, hex_borders, word_dict,
                max_length)
            visited.remove(neighbor)

def search(board: List[str], trie, hex_borders: Dict[int, List[int]],
           scrabble: callable) -> Tuple[int, Set[str], int]:
    precomputed_words = precompute_words(board, trie, hex_borders)

    score = 0
    words_found: Set[str] = set()
    for word in precomputed_words.values():
        if word not in words_found:
            score += scrabble(word)
            words_found.add(word)

    return score, words_found, len(precomputed_words)

with open('npm1.txt', 'r') as f:
    dict = f.read().split()
    dict = [word for word in dict if len(word) >= 2]
trie = build_trie(list(dict))

print(search('obnetatkshnpgoea', trie, squareBorders, scrabble))