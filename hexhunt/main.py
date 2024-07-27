# HINT 1: but yeah if you're just taking the best scoring string you can find with successive single-character changes, then your high score is a matter of how many of these initial strings you push through

# HINT 2: anyway a more clever way to handle this would be to sort hrough 2-grams rather than single character perms

# PATTERN: iter through a dictionary and test, then make 2-gram permutations of the most successful words and test those.

# Imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from english_words import get_english_words_set
from time import sleep
import os
from dotenv import load_dotenv
import json
import random

results = json.load(open('results.json'), )

# Init env variables
load_dotenv()

# Init word list
web2lowerset = get_english_words_set(['web2'], lower=True)

# Init web crawler
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://hacktimes.hackmit.org/')

# Connect to board
driver.get('https://hexhunt.hackmit.org/u/TheWelcomer_ae0cf11f')
# Nav to Hexhunt
score = 0
numRead = len(results)
with open('mamba.txt', 'r') as f:
    f = f.read()
    words = [f[i:i + 19] for i in range(0, len(f), 19)]
    for i in range(0, 1000):
        # i = random.randint(0, len(words) - 1)
        word = words[i].strip().lower()
        toInput = ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a']
        i = 0
        for j in range(3):
            toInput[j] = word[i % len(word)]
            i += 1
        for j in range(6, 2, -1):
            toInput[j] = word[i % len(word)]
            i += 1
        for j in range(7, 12):
            toInput[j] = word[i % len(word)]
            i += 1
        for j in range(15, 11, -1):
            toInput[j] = word[i % len(word)]
            i += 1
        for j in range(16, 19):
            toInput[j] = word[i % len(word)]
            i += 1
        driver.find_element('xpath', '//div[@class="hexagon"]').click()
        for i in range(19):
            input = driver.find_element('xpath', '//input[@class="hex-input"]')
            input.send_keys(toInput[i])
        driver.find_elements('xpath', '//button[@type="button"]')[1].click()
        while (len(driver.find_elements('xpath', '//p[@class="mantine-focus-auto m_b6d8b162 mantine-Text-root"]')) == 1):
            continue
        sleep(2.5)
        temp = score
        textboxes = driver.find_elements('xpath', '//p[@class="mantine-focus-auto m_b6d8b162 mantine-Text-root"]')
        for i in range(len(textboxes)):
            textboxes[i] = textboxes[i].text
        print(textboxes)
        if len(textboxes) == 2:
            word = textboxes[-2]
            score = 0
        else:
            word = textboxes[1]
            score = int(textboxes[2][15:])
        if temp != score and temp != 0:
            results[word] = (word, score)
        else:
            results[word] = (word, score)
        driver.find_elements('xpath', '//button[@type="button"]')[0].click()
        with open('results.json', 'w') as json_file:
            json_file.write(json.dumps(results))
