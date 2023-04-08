from colorama import Fore, Back, Style
import requests
from bs4 import BeautifulSoup
import time
import os
import plyer

timeBetweenEachCheck = 120 # change this to any amount (2 minutes)

url = 'https://www.roblox.com/catalog?Category=11&Subcategory=19&CurrencyType=3&pxMin=0&pxMax=0&salesTypeFilter=1&SortType=3&IncludeNotForSale'

id_file = 'ids.txt'

print(Fore.RED + 'Keep this running.\nTo close it press control + c.\n')
print(Style.RESET_ALL)

while True:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    items = soup.find_all('div', class_='item-card')
    limiteds = []
    for item in items:
        if 'Limited' in item.text:
            item_id = item['data-item-id']
            item_name = item.find('a', class_='text-name').text.strip()
            item_link = 'https://www.roblox.com/catalog/' + item_id + '/' + item_name.replace(' ', '-')

            if item_id not in open(id_file).read():
                limiteds.append((item_name, item_link))

                #print("Name: ", item_name, "\n", item_link, "\n\n")

                with open(id_file, 'a') as f:
                    f.write(item_id + '\n')

    if limiteds:
        print('New limited!')
        for limited in limiteds:
            print(limited[0] + ': ' + limited[1])
            plyer.notification.notify(title='New free limited!', message=limited[0] + ': ' + limited[1])

    time.sleep(timeBetweenEachCheck)
