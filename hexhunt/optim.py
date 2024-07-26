# Imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import random

def letgen(frequencies):
    letters = list(frequencies.keys())
    weights = list(frequencies.values())
    generated_letter = random.choices(letters, weights=weights, k=1)[0]
    return generated_letter
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
letterFrequency = {
    'e': 12.02,
    't': 9.10,
    'a': 8.12,
    'o': 7.68,
    'i': 7.31,
    'n': 6.95,
    's': 6.28,
    'r': 6.02,
    'h': 5.92,
    'd': 4.32,
    'l': 3.98,
    'u': 2.88,
    'c': 2.71,
    'm': 2.61,
    'f': 2.30,
    'y': 2.11,
    'w': 2.09,
    'g': 2.03,
    'p': 1.82,
    'b': 1.49,
    'v': 1.11,
    'k': 0.69,
    'x': 0.17,
    'q': 0.11,
    'j': 0.10,
    'z': 0.07
}

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

# Init web crawler
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://hacktimes.hackmit.org/')
driver.get('https://hexhunt.hackmit.org/u/TheWelcomer_ae0cf11f')
def run():
    runs = 0
    score = 2000

    # bestWord = list('antperiresenotatons')
    # bestWord = ['y', 'i', 'l', 'q', 'f', 'i', 't', 'l', 'e', 'h', 't', 'u', 'l', 'z', 'a', 'g', 'z', 'w', 'b']
    # bestWord = ['i', 'n', 's', 's', 'l', 't', 'i', 's', 'r', 'a', 'r', 's', 't', 'i', 'd', 'e', 't', 'f', 'e']
    bestWord = [*'apscrataeierstnkala']
    # bestWord = []
    # for i in range(19):
    #     bestWord.append(letgen(letterFrequency))

    with open('optim.txt', 'a') as f:
        while True:
            rawWord = bestWord.copy()
            for i in range(random.randint(2, 2)):
                changeIndex = random.randint(0, 18)
                rawWord[changeIndex] = letgen(letterFrequency)
            # for i in range(random.randint(1, 1)):
            #     changeIndex = random.choice(hexBorders[changeIndex])
            #     rawWord[changeIndex] = letgen(letterFrequency)
                # rawWord[(changeIndex + 1) % 19] = random.choice('abcdefghijklmnopqrstuvwxyz')
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
                if score < int(textboxes[2][15:]):
                    runs = 0
                    bestWord = rawWord.copy()
                    bigWord = textboxes[1]
                    score = int(textboxes[2][15:])
                    print(bestWord, bigWord, score, runs)
                    f.write(f'{bestWord} {bigWord} {score} {runs} \n')
                # else:
                #     runs += 1
                    # if runs > 100:
                    #     break
            runs += 1

while True:
    run()