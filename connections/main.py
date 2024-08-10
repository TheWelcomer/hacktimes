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
attempts = 0
def p():
    global attempts
    attempts += 1
    print(attempts)
def catClear(emoji):
    while True:
        outCont = False
        sleep(.4)
        correctsUnselected = driver.find_elements('xpath', f'//button[@class="relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71"]')
        correctsUnselected = list(filter(lambda x: x.text == emoji, correctsUnselected))
        while len(correctsUnselected) > 0:
            sleep(.4)
            correctsUnselected[-1].click()
            p()
            sleep(.4)
            oldCorrectsUnselected = correctsUnselected.copy()
            correctsUnselected = driver.find_elements('xpath', f'//button[@class="relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71"]')
            correctsUnselected = list(filter(lambda x: x.text == emoji, correctsUnselected))
            if len(oldCorrectsUnselected) - 1 > len(correctsUnselected):
                oldCorrectsUnselected[-1].click()
                sleep(.4)
                oldCorrectsUnselected[-1].click()
                p()
                sleep(.4)
                outCont = True
        if outCont:
            continue
        sleep(.4)
        selected = driver.find_elements('xpath', '//button[@class="relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71 bg-cell-1 text-white"]')
        if len(selected) == 8:
            break
        while True:
            sleep(.4)
            toClick = driver.find_elements('xpath', '//button[@class="relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71"]')
            toClick += selected
            toClick = random.choice(toClick)
            if not toClick.text in hiddenEmojis:
                toClick.click()
                p()
                sleep(.4)
                toClick.click()
                break
    sleep(.4)
    driver.find_element('xpath', '//button[@class="border rounded-full px-4 py-3 bg-black text-white"]').click()
    sleep(3)


# Init web crawler
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://connections.hackmit.org/?u=TheWelcomer_ae0cf11f')
round = 0
hiddenEmojis = []

while True:
    # if round == 0:
    #     emoji = '🐀'
    # elif round == 1:
    #     emoji = '👿'
    # elif round == 2:
    #     emoji = '🐁'
    # elif round == 3:
    #     emoji = '🐃'
    # elif round == 4:
    #     emoji = '🐿'
    # elif round == 5:
    #     emoji
    # else:
    emoji = input('Enter emoji: ')
    catClear(emoji)
    hiddenEmojis.append(emoji)
    round += 1