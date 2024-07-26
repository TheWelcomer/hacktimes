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
letterFrequency = {
    'e': 12.02*1.24,
    't': 9.10*1.16,
    'a': 8.12*.99,
    'o': 7.68*.72,
    'i': 7.31*1.03,
    'n': 6.95*1.14,
    's': 6.28*1.37,
    'r': 6.02*1.01,
    'h': 5.92*.5,
    'd': 4.32*1.18,
    'l': 3.98*.71,
    'u': 2.88*.88,
    'c': 2.71*.61,
    'm': 2.61*.97,
    'f': 2.30*.83,
    'y': 2.11*.61,
    'w': 2.09*.5,
    'g': 2.03*.44,
    'p': 1.82*.88,
    'b': 1.49*.74,
    'v': 1.11*1.51,
    'k': 0.69*1.06,
    'x': 0.17*.77,
    # 'q': 0.11,
    'j': 0.10,
    'z': 0.07*1.06
}

# Init web crawler
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://hacktimes.hackmit.org/')
driver.get('https://hexhunt.hackmit.org/u/TheWelcomer_ae0cf11f')
score = 0
# bestWord = list('antperiresenotatons')
# bestWord = ['y', 'i', 'l', 'q', 'f', 'i', 't', 'l', 'e', 'h', 't', 'u', 'l', 'z', 'a', 'g', 'z', 'w', 'b']
list1 = ['s', 'h', 't', 't', 'a', 'r', 'i', 's', 'e', 'd', 'e', 'n', 'r', 'i', 's', 'e', 'a', 't', 't']
list2 = ['r', 'e', 's', 't', 'i', 'n', 't', 'e', 'l', 't', 'e', 'r', 's', 'a', 's', 'd', 't', 'r', 'i']
bestWord = []
# for i in range(19):
#     bestWord.append(letgen(letterFrequency))

with open('optim.txt', 'a') as f:
    while True:
        zipped = list(zip(list1, list2))
        random.shuffle(zipped)
        rawWord, _ = zip(*zipped)
        rawWord = list(rawWord)
        driver.find_element('xpath', '//div[@class="hexagon"]').click()
        for i in range(19):
            input = driver.find_element('xpath', '//input[@class="hex-input"]')
            input.send_keys(rawWord[i])
        driver.find_elements('xpath', '//button[@type="button"]')[1].click()
        while (len(driver.find_elements('xpath', '//p[@class="mantine-focus-auto m_b6d8b162 mantine-Text-root"]')) == 1):
            continue
        sleep(2.75)
        temp = score
        textboxes = driver.find_elements('xpath', '//p[@class="mantine-focus-auto m_b6d8b162 mantine-Text-root"]')
        for i in range(len(textboxes)):
            textboxes[i] = textboxes[i].text
        if len(textboxes) != 2:
            if score <= int(textboxes[2][15:]):
                bestWord = rawWord.copy()
                score = int(textboxes[2][15:])
                print(bestWord, score)
                # f.write(f'{bestWord} {score}\n')