from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import json
import random

num_clicks = 0


def get_all_tiles(driver):
    return driver.find_elements(By.XPATH, '//button[contains(@class, "bg-cell-0")]')


def get_clickable_tiles(driver):
    return [tile for tile in get_all_tiles(driver)
            if 'bg-cell-1' not in tile.get_attribute('class')]


def click_tile(tile):
    tile.click()
    sleep(1)
    global num_clicks
    num_clicks += 1
    if num_clicks % 100 == 0:
        print(num_clicks)


def catClear(driver, emoji, hiddenEmojis):
    tiles = driver.find_elements(By.CLASS_NAME, 'bg-cell-0')
    for i in range(len(tiles)):
        if tiles[i].text == '🐀':
            click_tile(tiles[i])
    driver.find_element(By.XPATH,
                        '//button[@class="border rounded-full px-4 py-3 bg-black text-white"]').click()
    sleep(3)


def advClear(driver, cat, COOKBOOK, hiddenEmojis):
    mom = COOKBOOK[cat]['mom']
    fam = COOKBOOK[cat]['fam']
    edge = COOKBOOK[cat]['edging']

    while True:
        tiles = [tile for tile in get_clickable_tiles(driver)
                 if tile.text not in hiddenEmojis]
        mom_tiles = [tile for tile in tiles if tile.text == mom]
        for tile in mom_tiles:
            click_tile(tile)

        fam_tiles = [tile for tile in tiles if tile.text in fam]
        if not fam_tiles:
            if not tiles:
                break
            random_tile = random.choice(tiles)
            click_tile(random_tile)
            click_tile(random_tile)
            continue

        target_tile = fam_tiles[0]
        path = find_path(mom, target_tile.text, edge)
        if type(path) is not list and target_tile.text != mom:
            if not tiles:
                break
            random_tile = random.choice(tiles)
            click_tile(random_tile)
            click_tile(random_tile)
            continue

        if (int(cat) >= 3):
            path.reverse()

        for step in path:
            step_tile = get_all_tiles(driver)[step]
            if step_tile:
                click_tile(step_tile)
                click_tile(step_tile)

        if 'bg-cell-1' not in target_tile.get_attribute('class'):
            click_tile(target_tile)

        if len(driver.find_elements(By.XPATH, '//button[contains(@class, "bg-cell-1")]')) == 8:
            hiddenEmojis.append(mom)
            driver.find_element(By.XPATH,
                                '//button[@class="border rounded-full px-4 py-3 bg-black text-white"]').click()
            sleep(3)
            return


def edge(driver, num, COOKBOOK, hiddenEmojis):
    emojiList = COOKBOOK[num]['fam']
    mom = COOKBOOK[num]['mom']
    if 'famKnown' not in COOKBOOK[num]:
        COOKBOOK[num]['famKnown'] = []
    famKnown = COOKBOOK[num]['famKnown']
    emojisLeft = [emoji for emoji in emojiList if emoji not in famKnown]

    while emojisLeft:
        all_tiles = get_all_tiles(driver)
        clickable_tiles = [tile for tile in get_clickable_tiles(driver)
                           if tile.text not in hiddenEmojis]
        target_tile = next((tile for tile in clickable_tiles if tile.text in emojisLeft), None)
        for tile in clickable_tiles:
            if tile.text == mom:
                target_tile = tile

        if not target_tile or mom not in famKnown:
            if not clickable_tiles:
                break
            random_tile = random.choice(clickable_tiles)
            click_tile(random_tile)
            click_tile(random_tile)
            continue

        target_emoji = target_tile.text
        target_index = all_tiles.index(target_tile)

        for tile in clickable_tiles:
            if tile == target_tile:
                continue

            click_tile(tile)
            click_tile(tile)

            new_all_tiles = get_all_tiles(driver)
            new_target_tile = new_all_tiles[target_index]
            new_emoji = new_target_tile.text

            if new_emoji == target_emoji:
                continue

            if new_emoji not in COOKBOOK[num]['edging']:
                COOKBOOK[num]['edging'][new_emoji] = {}
            if target_emoji not in COOKBOOK[num]['edging'][new_emoji]:
                COOKBOOK[num]['edging'][new_emoji][target_emoji] = []
            COOKBOOK[num]['edging'][new_emoji][target_emoji].append(all_tiles.index(tile))

            # if target_emoji not in COOKBOOK[num]['edging']:
            #     COOKBOOK[num]['edging'][target_emoji] = {}
            # if new_emoji not in COOKBOOK[num]['edging'][target_emoji]:
            #     COOKBOOK[num]['edging'][target_emoji][new_emoji] = []
            # COOKBOOK[num]['edging'][target_emoji][new_emoji].append(all_tiles.index(tile))

            print(target_emoji + ' -> ' + new_emoji)

            click_tile(tile)
            click_tile(tile)

        COOKBOOK[num]['famKnown'].append(target_emoji)
        emojisLeft.remove(target_emoji)

        with open('COOKBOOK.json', 'w') as f:
            json.dump(COOKBOOK, f)


def find_path(start, end, edge_dict):
    queue = [(start, [])]
    visited = set()

    while queue:
        node, path = queue.pop(0)
        if node == end:
            return path

        if node in visited:
            continue

        visited.add(node)

        for next_node in edge_dict.get(node, {}):
            queue.append((next_node, path + [edge_dict[node][next_node][0]]))


COOKBOOK = json.load(open('COOKBOOK.json'))
chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://connections.hackmit.org/?u=TheWelcomer_ae0cf11f')
hiddenEmojis = ['🐀']


while True:
    catClear(driver, '🐀', hiddenEmojis)
    for i in range(1, 3):
        advClear(driver, str(i), COOKBOOK, hiddenEmojis)
    for i in range(3, 8):
        edge(driver, str(i), COOKBOOK, hiddenEmojis)
        advClear(driver, str(i), COOKBOOK, hiddenEmojis)
