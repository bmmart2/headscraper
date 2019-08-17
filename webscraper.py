from bs4 import BeautifulSoup
import requests
import sys
import json
from pathlib import Path

basePath = Path(__file__).parent
scrapedSpells = []
filePath = ''
jsonData = ''


def intro():
    print('HeadScraper: WoW Classic Scraping Tool')
    print('---------------------------------------')
    print('\'c\' - create a new file.')
    print('\'l\' - load an existing file')
    print('\'a\' - add to current list.')
    print('\'p\' - view path of current loaded file.')
    print('\'q\' - quit program.')
    print('---------------------------------------')

def statusReport():
    print('Loaded list: ',end="")
    try:
        print(filePath.name + '\n')
    except:
        print('N/A\n')
    

#brain method; reroutes from program loop to appropriate functions
def readCommand(input):
    print('')
    if (input == 'q'):
        sys.exit(0)
    elif (input == 'a'):
        addAbilities()
    elif (input == 'p'):
        print(str(filePath))
    elif (input == 'c'):
        createList()
    elif (input == 'l'):
        loadList()
    else:
        print('Invalid command.')

def loadList():
    global filePath, jsonData
    print('Enter the name of the file you would like to load from the data folder.\n')
    print('>> ',end="")
    selectedFile = input() + '.json'
    print()
    filePath = (basePath / "data" / selectedFile).resolve()
    print(filePath)
    if filePath.is_file():
        try:
            jsonData = json.load(filePath)
        except:
            print('Warning: This file is empty.')
        print("File loaded.\n")
        
    else:
        print('File not found.\n')
        
        filePath = ""
    return

def addAbilities():
        global filePath, scrapedSpells
        print('Would you like to import from the command line or from a file? (\'c\' or \'f\')')
        print('>> ',end="")
        if (input() == 'c'):
            print('Enter IDs, separated by spaces.')
            print('>> ',end="")
            userinput = input().split(" ")
            while(True):
                for id in userinput:
                    scrapedSpells.append(scrapeAbility(id))
                print('Continue entering IDs. Press \'q\' when finished.\n')
                print('>> ',end="")
                userInput = input()
                if (userInput == 'q'):
                    break
                else:
                    userInput = userInput.split(' ')
                    continue
        else:
            print('Enter the .txt file name to import from the data folder. Separate all abilities by new lines. Press \'q\' to quit.\n')
            while(True):
                print('>> ',end="")
                userInput = input()
                if (userInput == 'q'):
                    return
                selectedFile = userInput + '.txt'
                tempPath = basePath / "data" / selectedFile
                if (tempPath.is_file()):
                    with open(tempPath, 'r') as f:
                        for line in f:
                            line = line.rstrip('\n')
                            scrapedSpells.append(scrapeAbility(line))
                    break
                else:
                    'File not found. Try again.'
        while(True):
            print('Press \'s\' to exit and save to volatile memory, or \'w\' to dump JSON to selected file and exit.\n')
            print('>> ',end="")
            userInput = input()
            if (userInput == 's'):
                break
            elif (userInput == 'w'):
                with open(filePath, 'a') as outfile:
                    json.dump(scrapedSpells, outfile)
                print('JSON Written. Clearing from memory.\n')
                scrapedSpells = []
                break
        return

def createList():
    global filePath, selectedFile, basePath
    print("Enter the name of the new file.")
    print('>> ',end="")
    selectedFile = input() + '.json'
    filePath = (basePath / "data" / selectedFile)
    if not (filePath.is_file()):
        filePath.touch()
        print("File created.")
    else:
        print('File already exists. Try loading instead.\n')
        filePath = ''
    return

def scrapeAbility(spell):
    url = 'https://classicdb.ch/?spell=' + spell
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "lxml")
    data = list()

    try:
        div_container = content.find('div',attrs={'class':'tooltip'})
        for things in div_container.find_all('b'):
            data.append(things.text)

        description = div_container.find('span', attrs={'class':'q'})

        table_container = content.find('table', attrs={'id':'spelldetails'})
        table = table_container.find_all('td')

        abilityObject = {
            "id" : spell,
            "name" : data[0],
            "school" : table[4].text,
            "rank" : data[1],
            "mana" : table[7].text,
            "range" : table[8].text,
            "cast" : table[9].text,
            "cooldown" : table[10].text,
            "desc" : description.text
            }
        return abilityObject

    except:
        print('Invalid ability ID. Please try again.')
        return
    

#program start
intro()

while(True):
    statusReport()
    print('>> ', end="")
    readCommand(input())
