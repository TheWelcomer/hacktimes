from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import json
import random

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://library.hackmit.org/u/TheWelcomer_ae0cf11f')
books = ["Whiskers McFluff: Spy Cat's Return", "Kitty Kingdom: The Great Escape", "Purrfect Mystery: The Lost Collar", "Whiskers' Wild Adventure", "Sheriff Whiskers: Wild West Paws", "Galactic Doggos: Space Bark-tacular!", "Guardians of the Pack", "Pawsitive Bonds", "Woof and Wisdom", "Ranger Rover: Wild West Hound", "The Quack Detective", "Ducks Out of Water", "The Rubber Revolution", "Squeak of Destiny", "Ducking the Issues", "The Thousand Crane Journey", "Origami Crane Secrets", "Whispers of the Paper Crane", "Cranes of Hope", "The Crane Constellation", "The Midnight Pumpkin Patch", "Pumpkin Pie Perfection", "The Great Pumpkin Race", "Pumpkin: The Orange Wonder", "The Pumpkin Queen's Secret", "Cube Quest: The Puzzling Adventure", "The Rubik's Code", "Twisted: A Cube's Tale", "Speedcubing: The Path to Victory", "Six Sides of Life", "Shaken Memories", "The Blizzard Sphere", "Glass Storm", "Snowfall in Miniature", "The Globe Maker's Daughter", "The Secret Life of Teddy", "Beary Best Friends", "The Great Teddy Bear Picnic Mystery", "Teddy's Time Machine", "The Patchwork Bear", "The Luminous Legacy", "Shadows of the Lamplight", "The Genie's Lamp Shop", "Illuminating the Past", "The Last Lighthouse", "The Scoop of Love", "Frozen Dreams", "The Ice Cream Murders", "Sundae School", "Gelato Memories"]
best = driver.find_element('xpath', '//input[@id="best"]')
worst = driver.find_element('xpath', '//input[@id="worst"]')
previewed = driver.find_elements('xpath', '//h3[@class="book-title"]')
for book in previewed:
    for i in range(len(books)):
        if book.text.lower() == books[i].lower():
            books.pop(i)
            break
bestBook = None
worstBook = None
while True:
    if driver.find_element('xpath', '//button[@type="submit"]').text == 'Retry':
        driver.find_element('xpath', '//button[@type="submit"]').click()
        sleep(1)
        continue
    bestGuess = books[random.randint(0, len(books) - 1)]
    books.remove(bestGuess)
    worstGuess = books[random.randint(0, len(books) - 1)]
    books.remove(worstGuess)
    best.clear()
    sleep(1)
    worst.clear()
    best.send_keys(bestGuess)
    worst.send_keys(worstGuess)
    worst.clear()
    worst.send_keys(worstGuess)
    driver.find_element('xpath', '//button[@type="submit"]').click()
    sleep(10)