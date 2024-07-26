# Imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import random
from english_words import get_english_words_set
from collections import deque
import math
from typing import List, Set, Dict, Tuple
l = 1.75
letterFrequency = {
    'a': pow(9.24, l),
    'b': pow(2.51, l),
    'c': pow(3.13, l),
    'd': pow(3.78, l),
    'e': pow(10.27, l),
    'f': pow(1.72, l),
    'g': pow(2.53, l),
    'h': pow(2.71, l),
    'i': pow(5.80, l),
    'j': pow(.45, l),
    'k': pow(2.32, l),
    'l': pow(5.2, l),
    'm': pow(3.05, l),
    'n': pow(4.55, l),
    'o': pow(6.84, l),
    'p': pow(3.11, l),
    'r': pow(6.41, l),
    's': pow(10.28, l),
    't': pow(5.08, l),
    'u': pow(3.87, l),
    'v': pow(1.07, l),
    'w': pow(1.60, l),
    'y': pow(3.20, l)
}
# letterFrequency = {
#     'e': 12.02*1.24,
#     't': 9.10*1.16,
#     'a': 8.12*.99,
#     'o': 7.68*.72,
#     'i': 7.31*1.03,
#     'n': 6.95*1.14,
#     's': 6.28*1.37,
#     'r': 6.02*1.01,
#     'h': 5.92*.5,
#     'd': 4.32*1.18,
#     'l': 3.98*.71,
#     'u': 2.88*.88,
#     'c': 2.71*.61,
#     'm': 2.61*.97,
#     'f': 2.30*.83,
#     'y': 2.11*.61,
#     'w': 2.09*.5,
#     'g': 2.03*.44,
#     'p': 1.82*.88,
#     'b': 1.49*.74,
#     'v': 1.11*1.51,
#     'k': 0.69*1.06,
#     'x': 0.17*.77,
#     'q': 0.11,
#     'j': 0.10,
#     'z': 0.07*1.06
# }
# letterFrequency = {
#     'e': 12.02,
#     't': 9.10,
#     'a': 8.12,
#     'o': 7.68,
#     'i': 7.31,
#     'n': 6.95,
#     's': 6.28,
#     'r': 6.02,
#     'h': 5.92,
#     'd': 4.32,
#     'l': 3.98,
#     'u': 2.88,
#     'c': 2.71,
#     'm': 2.61,
#     'f': 2.30,
#     'y': 2.11,
#     'w': 2.09,
#     'g': 2.03,
#     'p': 1.82,
#     'b': 1.49,
#     'v': 1.11,
#     'k': 0.69,
#     'x': 0.17,
#     'q': 0.11,
#     'j': 0.10,
#     'z': 0.07
# }

hexBorders = {
    0: [1, 3, 4],
    1: [0, 2, 4, 5],
    2: [1, 5, 6],
    3: [0, 4, 7, 8],
    4: [0, 1, 3, 5, 8, 9],
    5: [1, 2, 4, 6, 9, 10],
    6: [2, 5, 10, 11],
    7: [3, 8, 12],
    8: [3, 4, 7, 9, 12, 13],
    9: [4, 5, 8, 10, 13, 14],
    10: [5, 6, 9, 11, 14, 15],
    11: [6, 10, 15],
    12: [7, 8, 13, 16],
    13: [8, 9, 12, 14, 16, 17],
    14: [9, 10, 13, 15, 17, 18],
    15: [10, 11, 14, 18],
    16: [12, 13, 17],
    17: [13, 14, 16, 18],
    18: [14, 15, 17]
}

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
    # 'a': 1,
    # 'b': 3,
    # 'c': 3,
    # 'd': 2,
    # 'e': 1,
    # 'f': 4,
    # 'g': 2,
    # 'h': 4,
    # 'i': 1,
    # 'j': 8,
    # 'k': 5,
    # 'l': 1,
    # 'm': 3,
    # 'n': 1,
    # 'o': 1,
    # 'p': 3,
    # 'q': 10,
    # 'r': 1,
    # 's': 1,
    # 't': 1,
    # 'u': 1,
    # 'v': 4,
    # 'w': 4,
    # 'x': 8,
    # 'y': 4,
    # 'z': 10
}

# dict = set(open('/usr/share/dict/words').read().split())
# dict = get_english_words_set(['web2'], lower=True)
# dict = set(word for word in dict if len(word) >= 2)
# listdict = list(dict)
# listdict.sort()
with open('words.txt', 'r') as f:
    dict = f.read().split()
    dict = set(word for word in dict if len(word) >= 2)

def letgen(frequencies):
    letters = list(frequencies.keys())
    weights = list(frequencies.values())
    generated_letter = random.choices(letters, weights=weights, k=1)[0]
    return generated_letter

def scramble(word):
    zipped = list(zip(word, word))
    random.shuffle(zipped)
    word, _ = zip(*zipped)
    return list(word)

def scrabble(word):
    naive = sum(scrabbleScores[letter] for letter in word)
    return naive
    # naive = naive * pow(len(word), 1.65)
    # return naive // 10


# def precompute_words(board):
#     word_dict = {}
#     for i in range(19):
#         for length in range(1, 20):  # Assuming maximum word length is 19
#             frontier = deque([(str(i), board[i])])
#             while frontier:
#                 path, word = frontier.popleft()
#                 if word in dict:
#                     word_dict[path] = word
#                 if len(path) < length:
#                     last = int(path.split(',')[-1])
#                     for j in hexBorders[last]:
#                         if str(j) not in path:
#                             new_path = path + ',' + str(j)
#                             new_word = word + board[j]
#                             frontier.append((new_path, new_word))
#     return word_dict
#
#
# def search(board):
#     score = 0
#     words_found = set()
#     precomputed_words = precompute_words(board)
#
#     for path, word in precomputed_words.items():
#         if word not in words_found:
#             score += scrabble(word)
#             words_found.add(word)
#
#     return score, words_found, len(precomputed_words)

# def search(board):
#     tries = 0
#     score = 0
#     words_found = set()
#     for i in range(19):
#         tried = set()
#         frontier = deque([str(i)])
#         while frontier:
#             next = frontier.popleft()
#             if next not in tried:
#                 tries += 1
#                 tried.add(next)
#                 nextList = next.split(',')
#                 word = ''.join(board[int(j)] for j in nextList)
#                 if word in dict and word not in words_found:
#                     score += scrabble(word)
#                     words_found.add(word)
#                 for j in hexBorders[int(nextList[-1])]:
#                     if str(j) not in nextList:
#                         frontier.append(next + ',' + str(j))
#     return score, words_found, tries

from collections import deque
from typing import List, Set, Dict, Tuple


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


def search(board: List[str], dict: List[str], hex_borders: Dict[int, List[int]],
           scrabble: callable) -> Tuple[int, Set[str], int]:
    trie = build_trie(dict)
    precomputed_words = precompute_words(board, trie, hex_borders)

    score = 0
    words_found: Set[str] = set()
    for word in precomputed_words.values():
        if word not in words_found:
            score += scrabble(word)
            words_found.add(word)

    return score, words_found, len(precomputed_words)


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://hacktimes.hackmit.org/')
driver.get('https://hexhunt.hackmit.org/u/TheWelcomer_ae0cf11f')


def run():
    runs = 0
    lastChange = 0
    tested = set()
    # bestWord = [letgen(letterFrequency) for _ in range(19)]
    bestWord = [*'masserernilsetapsse']
    bestScore = 0
    bestHexScore = 0
    # print(f'Run {runs} {tries}: {"".join(bestWord)} ({bestScore}) {words}')
    # bestWord = scramble(bestWord)
    while True:
        with open('mamba.txt', 'a') as f:
            rawWord = bestWord.copy()
            # tech = random.randint(0, 1)
            # if tech == 0:
            if runs != 0:
                while True:
                    changeIndex = random.randint(0, 18)
                    rawWord[changeIndex] = letgen(letterFrequency)
                    if random.randint(1, 1) == 1:
                        # changeIndex = random.randint(0, 18)
                        changeIndex = hexBorders[changeIndex][random.randint(0, len(hexBorders[changeIndex]) - 1)]
                        rawWord[changeIndex] = letgen(letterFrequency)
                    if tuple(rawWord) not in tested:
                        break
            # if tech == 1:
            #     tiles = random.randint(2, 3)
            #     dictListInsert = [w for w in dict if len(w) == tiles]
            #     toInsert = random.choice(dictListInsert).lower()
            #     changeIndex = random.randint(0, 18)
            #     for i in range(tiles):
            #         rawWord[changeIndex] = toInsert[i]
            #         changeIndex = hexBorders[changeIndex][random.randint(0, len(hexBorders[changeIndex]) - 1)]

            score, words, tries = search(rawWord)
            tested.add(tuple(rawWord))
            if score > bestScore * .95:
                # bestScore += 10
                print(f'Run {runs} {tries}: {"".join(rawWord)} ({score}) {words}')
                f.write(f'Run {runs} {tries}: {"".join(rawWord)} ({score}) {words}\n')
                driver.find_element('xpath', '//div[@class="hexagon"]').click()
                for i in range(19):
                    input = driver.find_element('xpath', '//input[@class="hex-input"]')
                    input.send_keys(rawWord[i])
                driver.find_elements('xpath', '//button[@type="button"]')[1].click()
                while (len(driver.find_elements('xpath', '//p[@class="mantine-focus-auto m_b6d8b162 mantine-Text-root"]')) == 1):
                    continue
                sleep(2.75)
                textboxes = driver.find_elements('xpath', '//p[@class="mantine-focus-auto m_b6d8b162 mantine-Text-root"]')
                for i in range(len(textboxes)):
                    textboxes[i] = textboxes[i].text
                if len(textboxes) != 2:
                    bigWord = textboxes[1]
                    hexScore = int(textboxes[2][15:])
                    print(bigWord, hexScore)
                    f.write(f'{bigWord} {hexScore}\n')
                    if hexScore >= bestHexScore:
                        print('New best')
                        f.write('New best')
                        bestScore = score
                        lastChange = 0
                        bestHexScore = hexScore
                        bestWord = rawWord.copy()
            # else:
                # if lastChange > (score // 10) * math.log(score // 10):
                #     break
            # bestScore -= 1
            lastChange += 1
            runs += 1

while True:
    run()
