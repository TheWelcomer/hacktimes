from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import json
import random

attempts = 0
COOKBOOK = json.load(open('COOKBOOK.json'))

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
    hiddenEmojis.append(emoji)

def advClear(cat):
    mom = COOKBOOK[cat]['mom']
    fam = COOKBOOK[cat]['fam']
    edge = COOKBOOK[cat]['edging']
    tiles = driver.find_elements(By.CLASS_NAME, 'bg-cell-0')
    for i in range(len(tiles)):
        if tiles[i].text == mom:
            tiles[i].click()
            sleep(.8)
    watch = None
    while True:
        while True:
            tiles = driver.find_elements(By.CLASS_NAME, 'bg-cell-0')
            outerBreak = False
            for i in range(len(tiles)):
                if tiles[i].get_attribute('class') == 'relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71 bg-cell-1 text-white':
                    continue
                if tiles[i].text in fam:
                    watch = i
                    outerBreak = True
                    break
            if outerBreak:
                break
            while True:
                tiles = driver.find_elements(By.CLASS_NAME, 'bg-cell-0')
                toClick = random.choice(tiles)
                if toClick.get_attribute('class') == 'relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71 bg-cell-1 text-white':
                    continue
                if toClick.text in hiddenEmojis:
                    continue
                toClick.click()
                sleep(.8)
                toClick.click()
                sleep(.8)
                break
        tiles = driver.find_elements(By.CLASS_NAME, 'bg-cell-0')
        ct = False
        for i in range(len(tiles)):
            if tiles[i].text == mom and i != watch:
                tiles[i].click()
                sleep(.8)
                ct = True
                continue
        if ct:
            continue
        sequence = []
        searched = []
        frontier = [(mom, [])]
        outCont = False
        while True:
            tiles = driver.find_elements(By.CLASS_NAME, 'bg-cell-0')
            emoji = tiles[watch].text
            if len(frontier) == 0:
                print('No path found')
                tiles = driver.find_elements(By.CLASS_NAME, 'bg-cell-0')
                while True:
                    toClick = random.choice(tiles)
                    if toClick.get_attribute('class') == 'relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71 bg-cell-1 text-white':
                        continue
                    if toClick.text in hiddenEmojis:
                        continue
                    toClick.click()
                    sleep(.8)
                    toClick.click()
                    sleep(.8)
                    break
                outCont = True
                break
            node, path = frontier.pop(0)
            if node == tiles[watch].text:
                outCont = False
                for i in range(len(path)):
                    if path[i] == watch:
                        outCont = True
                        break
                if outCont:
                    continue
                sequence = path
                break
            if node in searched:
                continue
            searched.append(node)
            for key in edge[node]:
                for i in edge[node][key]:
                    frontier.append((key, path + [i]))
        if outCont:
            continue
        sequence.reverse()
        print(tiles[watch].text, sequence)
        for i in range(len(sequence)):
            tiles[int(sequence[i])].click()
            sleep(.8)
            tiles[int(sequence[i])].click()
            sleep(.8)
        tiles[watch].click()
        sleep(.8)
        t = driver.find_elements('xpath', f'//button[@class="relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71 bg-cell-1 text-white"]')
        if len(t) == 8:
            hiddenEmojis.append(mom)
            driver.find_element('xpath', '//button[@class="border rounded-full px-4 py-3 bg-black text-white"]').click()
            sleep(3)
            return




def edge(num):
    emojiList = COOKBOOK[num]['fam']
    emojisLeft = emojiList.copy()
    mom = COOKBOOK[num]['mom']
    if 'famKnown' not in COOKBOOK[num]:
        COOKBOOK[num]['famKnown'] = []
    famKnown = COOKBOOK[num]['famKnown']
    watch = None
    outBreak = False
    for emoji in famKnown:
        if emoji in emojisLeft:
            emojisLeft.remove(emoji)
    while len(emojisLeft) > 0:
        while True:
            tiles = driver.find_elements(By.CLASS_NAME, 'bg-cell-0')
            for i in range(len(tiles)):
                if tiles[i].get_attribute('class') == 'relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71 bg-cell-1 text-white':
                    continue
            for i in range(len(tiles)):
                if tiles[i].get_attribute('class') == 'relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71 bg-cell-1 text-white':
                    continue
                if tiles[i].text in emojisLeft:
                    watch = i
                    emoji = tiles[i].text
                    outBreak = True
                    break
            if outBreak:
                break
            toClick = random.choice(tiles)
            if tiles[i].get_attribute('class') == 'relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71 bg-cell-1 text-white':
                continue
            if toClick.text in hiddenEmojis:
                continue
            print(toClick, toClick.text)
            toClick.click()
            sleep(.8)
            toClick.click()
            sleep(.8)
        tiles = driver.find_elements(By.CLASS_NAME, 'bg-cell-0')
        for i in range(len(tiles)):
            if tiles[i].get_attribute('class') == 'relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71 bg-cell-1 text-white':
                continue
            if tiles[i].text in hiddenEmojis:
                continue
            if i == watch:
                continue
            tiles[i].click()
            sleep(.8)
            tiles[i].click()
            sleep(.8)
            tiles = driver.find_elements(By.CLASS_NAME, 'bg-cell-0')
            newEmoji = tiles[watch].text
            print(emoji, newEmoji)
            if newEmoji == emoji:
                continue
            if not newEmoji in COOKBOOK[num]['edging']:
                COOKBOOK[num]['edging'][newEmoji] = {}
            if not emoji in COOKBOOK[num]['edging'][newEmoji]:
                COOKBOOK[num]['edging'][newEmoji][emoji] = []
            COOKBOOK[num]['edging'][newEmoji][emoji].append(i)
            tiles[i].click()
            sleep(.8)
            tiles[i].click()
            sleep(.8)
        COOKBOOK[num]['famKnown'].append(emoji)
        emojisLeft.remove(emoji)
        with open('COOKBOOK.json', 'w') as f:
            json.dump(COOKBOOK, f)

# Init web crawler
chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://connections.hackmit.org/?u=TheWelcomer_ae0cf11f')
hiddenEmojis = []

# catClear('🐀')
# t = driver.find_elements('xpath', f'//button[@class="relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71"]')
# test = t[22]
# test.click()
# sleep(.8)
# test.click()
# sleep(5)
# s = driver.find_elements('xpath', f'//button[@class="relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71"]')
# for i in range(len(t)):
#     print(t[i].text, s[i].text)
# tiles = driver.find_elements('xpath', f'//button[@class="relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71"]')
# for i in range(10):
#     if tiles[i].text in hiddenEmojis:
#         continue
#     tiles[i].click()
#     sleep(8)
#     tiles[i].click()
#     sleep(.8)
#
# # (7, 4), (6, 6), (1, 6), (7, 7), (4, 3), (6, 1), (1, 7), (2, 7), (
# # (7, 4), (6, 6),
#
# tiles = driver.find_elements('xpath', f'//button[@class="relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71"]')
# for i in range(10):
#     if tiles[i].text in hiddenEmojis:
#         continue
#     tiles[i].click()
#     sleep(.8)
#     tiles[i].click()
#     sleep(8)

while True:
    # if round == 0:
    #     emoji = '🐀'
    # elif round == 1:
    #     emoji = '👿'
    # elif round == 2:
    #     emoji = '🐁'
    # elif round == 3:from selenium import webdriver
    # from selenium.webdriver.chrome.options import Options
    # from selenium.webdriver.common.by import By
    # from selenium.webdriver.chrome.service import Service
    # from webdriver_manager.chrome import ChromeDriverManager
    # from time import sleep
    # import json
    # import random
    #
    # attempts = 0
    # COOKBOOK = json.load(open('COOKBOOK.json'))
    #
    # def p():
    #     global attempts
    #     attempts += 1
    #     print(attempts)
    #
    # def catClear(emoji):
    #     while True:
    #         outCont = False
    #         sleep(.4)
    #         correctsUnselected = driver.find_elements('xpath', f'//button[@class="relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71"]')
    #         correctsUnselected = list(filter(lambda x: x.text == emoji, correctsUnselected))
    #         while len(correctsUnselected) > 0:
    #             sleep(.4)
    #             correctsUnselected[-1].click()
    #             p()
    #             sleep(.4)
    #             oldCorrectsUnselected = correctsUnselected.copy()
    #             correctsUnselected = driver.find_elements('xpath', f'//button[@class="relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71"]')
    #             correctsUnselected = list(filter(lambda x: x.text == emoji, correctsUnselected))
    #             if len(oldCorrectsUnselected) - 1 > len(correctsUnselected):
    #                 oldCorrectsUnselected[-1].click()
    #                 sleep(.4)
    #                 oldCorrectsUnselected[-1].click()
    #                 p()
    #                 sleep(.4)
    #                 outCont = True
    #         if outCont:
    #             continue
    #         sleep(.4)
    #         selected = driver.find_elements('xpath', '//button[@class="relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71 bg-cell-1 text-white"]')
    #         if len(selected) == 8:
    #             break
    #         while True:
    #             sleep(.4)
    #             toClick = driver.find_elements('xpath', '//button[@class="relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71"]')
    #             toClick += selected
    #             toClick = random.choice(toClick)
    #             if not toClick.text in hiddenEmojis:
    #                 toClick.click()
    #                 p()
    #                 sleep(.4)
    #                 toClick.click()
    #                 break
    #     sleep(.4)
    #     driver.find_element('xpath', '//button[@class="border rounded-full px-4 py-3 bg-black text-white"]').click()
    #     sleep(3)
    #     hiddenEmojis.append(emoji)
    #
    # def advClear(cat):
    #     mom = COOKBOOK[cat]['mom']
    #     fam = COOKBOOK[cat]['fam']
    #     edge = COOKBOOK[cat]['edging']
    #     tiles = driver.find_elements(By.CLASS_NAME, 'bg-cell-0')
    #     for i in range(len(tiles)):
    #         if tiles[i].text == mom:
    #             tiles[i].click()
    #             sleep(.8)
    #     watch = None
    #     while True:
    #         while True:
    #             tiles = driver.find_elements(By.CLASS_NAME, 'bg-cell-0')
    #             outerBreak = False
    #             for i in range(len(tiles)):
    #                 if tiles[i].get_attribute('class') == 'relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71 bg-cell-1 text-white':
    #                     continue
    #                 if tiles[i].text in fam:
    #                     watch = i
    #                     outerBreak = True
    #                     break
    #             if outerBreak:
    #                 break
    #             while True:
    #                 tiles = driver.find_elements(By.CLASS_NAME, 'bg-cell-0')
    #                 toClick = random.choice(tiles)
    #                 if toClick.get_attribute('class') == 'relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71 bg-cell-1 text-white':
    #                     continue
    #                 if toClick.text in hiddenEmojis:
    #                     continue
    #                 toClick.click()
    #                 sleep(.8)
    #                 toClick.click()
    #                 sleep(.8)
    #                 break
    #         tiles = driver.find_elements(By.CLASS_NAME, 'bg-cell-0')
    #         ct = False
    #         for i in range(len(tiles)):
    #             if tiles[i].text == mom and i != watch:
    #                 tiles[i].click()
    #                 sleep(.8)
    #                 ct = True
    #                 continue
    #         if ct:
    #             continue
    #         sequence = []
    #         searched = []
    #         frontier = [(mom, [])]
    #         outCont = False
    #         while True:
    #             tiles = driver.find_elements(By.CLASS_NAME, 'bg-cell-0')
    #             emoji = tiles[watch].text
    #             if len(frontier) == 0:
    #                 print('No path found')
    #                 tiles = driver.find_elements(By.CLASS_NAME, 'bg-cell-0')
    #                 while True:
    #                     toClick = random.choice(tiles)
    #                     if toClick.get_attribute('class') == 'relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71 bg-cell-1 text-white':
    #                         continue
    #                     if toClick.text in hiddenEmojis:
    #                         continue
    #                     toClick.click()
    #                     sleep(.8)
    #                     toClick.click()
    #                     sleep(.8)
    #                     break
    #                 outCont = True
    #                 break
    #             node, path = frontier.pop(0)
    #             if node == tiles[watch].text:
    #                 outCont = False
    #                 for i in range(len(path)):
    #                     if path[i] == watch:
    #                         outCont = True
    #                         break
    #                 if outCont:
    #                     continue
    #                 sequence = path
    #                 break
    #             if node in searched:
    #                 continue
    #             searched.append(node)
    #             for key in edge[node]:
    #                 for i in edge[node][key]:
    #                     frontier.append((key, path + [i]))
    #         if outCont:
    #             continue
    #         sequence.reverse()
    #         print(tiles[watch].text, sequence)
    #         for i in range(len(sequence)):
    #             tiles[int(sequence[i])].click()
    #             sleep(.8)
    #             tiles[int(sequence[i])].click()
    #             sleep(.8)
    #         tiles[watch].click()
    #         sleep(.8)
    #         t = driver.find_elements('xpath', f'//button[@class="relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71 bg-cell-1 text-white"]')
    #         if len(t) == 8:
    #             hiddenEmojis.append(mom)
    #             driver.find_element('xpath', '//button[@class="border rounded-full px-4 py-3 bg-black text-white"]').click()
    #             sleep(3)
    #             return
    #
    #
    #
    #
    # def edge(num):
    #     emojiList = COOKBOOK[num]['fam']
    #     emojisLeft = emojiList.copy()
    #     mom = COOKBOOK[num]['mom']
    #     if 'famKnown' not in COOKBOOK[num]:
    #         COOKBOOK[num]['famKnown'] = []
    #     famKnown = COOKBOOK[num]['famKnown']
    #     watch = None
    #     outBreak = False
    #     for emoji in famKnown:
    #         if emoji in emojisLeft:
    #             emojisLeft.remove(emoji)
    #     while len(emojisLeft) > 0:
    #         while True:
    #             tiles = driver.find_elements(By.CLASS_NAME, 'bg-cell-0')
    #             for i in range(len(tiles)):
    #                 if tiles[i].get_attribute('class') == 'relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71 bg-cell-1 text-white':
    #                     continue
    #             for i in range(len(tiles)):
    #                 if tiles[i].get_attribute('class') == 'relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71 bg-cell-1 text-white':
    #                     continue
    #                 if tiles[i].text in emojisLeft:
    #                     watch = i
    #                     emoji = tiles[i].text
    #                     outBreak = True
    #                     break
    #             if outBreak:
    #                 break
    #             toClick = random.choice(tiles)
    #             if tiles[i].get_attribute('class') == 'relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71 bg-cell-1 text-white':
    #                 continue
    #             if toClick.text in hiddenEmojis:
    #                 continue
    #             print(toClick, toClick.text)
    #             toClick.click()
    #             sleep(.8)
    #             toClick.click()
    #             sleep(.8)
    #         tiles = driver.find_elements(By.CLASS_NAME, 'bg-cell-0')
    #         for i in range(len(tiles)):
    #             if tiles[i].get_attribute('class') == 'relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71 bg-cell-1 text-white':
    #                 continue
    #             if tiles[i].text in hiddenEmojis:
    #                 continue
    #             if i == watch:
    #                 continue
    #             tiles[i].click()
    #             sleep(.8)
    #             tiles[i].click()
    #             sleep(.8)
    #             tiles = driver.find_elements(By.CLASS_NAME, 'bg-cell-0')
    #             newEmoji = tiles[watch].text
    #             print(emoji, newEmoji)
    #             if newEmoji == emoji:
    #                 continue
    #             if not newEmoji in COOKBOOK[num]['edging']:
    #                 COOKBOOK[num]['edging'][newEmoji] = {}
    #             if not emoji in COOKBOOK[num]['edging'][newEmoji]:
    #                 COOKBOOK[num]['edging'][newEmoji][emoji] = []
    #             COOKBOOK[num]['edging'][newEmoji][emoji].append(i)
    #             tiles[i].click()
    #             sleep(.8)
    #             tiles[i].click()
    #             sleep(.8)
    #         COOKBOOK[num]['famKnown'].append(emoji)
    #         emojisLeft.remove(emoji)
    #         with open('COOKBOOK.json', 'w') as f:
    #             json.dump(COOKBOOK, f)
    #
    # # Init web crawler
    # chrome_options = Options()
    #
    # driver = webdriver.Chrome(options=chrome_options)
    # driver.get('https://connections.hackmit.org/?u=TheWelcomer_ae0cf11f')
    # hiddenEmojis = []
    #
    # # catClear('🐀')
    # # t = driver.find_elements('xpath', f'//button[@class="relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71"]')
    # # test = t[22]
    # # test.click()
    # # sleep(.8)
    # # test.click()
    # # sleep(5)
    # # s = driver.find_elements('xpath', f'//button[@class="relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71"]')
    # # for i in range(len(t)):
    # #     print(t[i].text, s[i].text)
    # # tiles = driver.find_elements('xpath', f'//button[@class="relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71"]')
    # # for i in range(10):
    # #     if tiles[i].text in hiddenEmojis:
    # #         continue
    # #     tiles[i].click()
    # #     sleep(8)
    # #     tiles[i].click()
    # #     sleep(.8)
    # #
    # # # (7, 4), (6, 6), (1, 6), (7, 7), (4, 3), (6, 1), (1, 7), (2, 7), (
    # # # (7, 4), (6, 6),
    # #
    # # tiles = driver.find_elements('xpath', f'//button[@class="relative size-full rounded-md flex justify-center items-center transition bg-cell-0 svelte-mkwl71"]')
    # # for i in range(10):
    # #     if tiles[i].text in hiddenEmojis:
    # #         continue
    # #     tiles[i].click()
    # #     sleep(.8)
    # #     tiles[i].click()
    # #     sleep(8)
    #
    # while True:
    #     # if round == 0:
    #     #     emoji = '🐀'
    #     # elif round == 1:
    #     #     emoji = '👿'
    #     # elif round == 2:
    #     #     emoji = '🐁'
    #     # elif round == 3:
    #     #     emoji = '🐃'
    #     # elif round == 4:
    #     #     emoji = '🐿'
    #     # elif round == 5:
    #     #     emoji
    #     # else:
    #     catClear('🐀')
    #     # connection = input('Enter connection: ')
    #     # edge('1')
    #     for i in range(1, 8):
    #         edge(str(i))
    #         advClear(str(i))
    #     emoji = '🐃'
    # elif round == 4:
    #     emoji = '🐿'
    # elif round == 5:
    #     emoji
    # else:
    catClear('🐀')
    # connection = input('Enter connection: ')
    # edge('1')
    for i in range(1, 8):
        edge(str(i))
        advClear(str(i))