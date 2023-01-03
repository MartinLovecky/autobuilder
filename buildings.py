from bs4 import BeautifulSoup
import requests
import re

from hrad import Hrad
from stone import Stone
from wood import Wood
from iron import Iron
from storage import Storage
from workers import Workers


class Buildings:

    def __init__(
        self,
        login,
        stone_left=0,
        wood_left=0,
        iron_left=0,
        storage_left=0,
        free_workers_left=0
    ):
        self.login = login
        self.stone_left = stone_left
        self.wood_left = wood_left
        self.iron_left = iron_left
        self.storage_left = storage_left
        self.free_workers_left = free_workers_left,
        self.hrad = None,
        self.stone = None,
        self.wood = None,
        self.iron = None,
        self.storage = None,
        self.workers = None,

    def init_buildings(self, buildings, name):

        for buildings in buildings:
            if name == 'hrad':
                self.hrad = Hrad(buildings['buildtime'], buildings['workers'], buildings['link'],
                                 buildings['res1'], buildings['res2'], buildings['res3'], buildings['level'])
                return self.hrad
            elif name == 'kamen':
                self.stone = Stone(buildings['buildtime'], buildings['workers'], buildings['link'],
                                   buildings['res1'], buildings['res2'], buildings['res3'], buildings['level'])
                return self.stone
            elif name == 'pila':
                self.wood = Wood(buildings['buildtime'], buildings['workers'], buildings['link'],
                                 buildings['res1'], buildings['res2'], buildings['res3'], buildings['level'])
                return self.wood
            elif name == 'ruda':
                self.iron = Iron(buildings['buildtime'], buildings['workers'], buildings['link'],
                                 buildings['res1'], buildings['res2'], buildings['res3'], buildings['level'])
                return self.iron
            elif name == 'sklad':
                storage = Storage(buildings['buildtime'], buildings['workers'], buildings['link'],
                                  buildings['res1'], buildings['res2'], buildings['res3'], buildings['level'])
                return self.storage
            elif name == 'mlyn':
                self.workers = Workers(buildings['buildtime'], buildings['workers'], buildings['link'],
                                       buildings['res1'], buildings['res2'], buildings['res3'], buildings['level'])
                return self.workers

    def parse_building(self, box):

        # parse the information for a single building from the HTML
        name = box.find('div', {'class': 'name'}).find('a').text
        buildtime = box.find('div', {'class': 'buildtime'}).text
        workers = int(
            box.find('div', {'class': 'workers'}).text.replace('.', ''))
        link = 'https://s2-cz.kingsage.gameforge.com/' + \
            box.find('div', {'class': 'button'}).find('a').get('href')
        res1 = int(box.find('div', {'class': 'res1'}).text.replace('.', ''))
        res2 = int(box.find('div', {'class': 'res2'}).text.replace('.', ''))
        res3 = int(box.find('div', {'class': 'res3'}).text.replace('.', ''))
        level = box.find('div', {'class': 'button'}).find('a').text

        return {
            'name': name,
            'buildtime': buildtime,
            'workers': workers,
            'link': link,
            'res1': res1,
            'res2': res2,
            'res3': res3,
            'level': level
        }

    def pasrse_buildings(self, village_id, url):
        buildings = []
        target_url = f'{url}?village={village_id}&s=build_main'
        response = self.login.session.get(target_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Resources
        stone_span = soup.find('span', id='stone')
        wood_span = soup.find('span', id='wood')
        iron_span = soup.find('span', id='iron')
        free_workers_span = soup.find(
            'div', {'class': 'villageInfobar'}).find_all('span')[-1]
        storage_span = soup.find(
            'div', {'class': 'villageInfobar'}).find_all('span')[-2]

        for element in storage_span:
            if re.match(r'\d+\.\d+', element.text):
                storage_span = element
            break
        self.stone_left = int(stone_span.get_text().replace('.', ''))
        self.wood_left = int(wood_span.get_text().replace('.', ''))
        self.iron_left = int(iron_span.get_text().replace('.', ''))
        self.storage_left = int(storage_span.get_text().replace('.', ''))
        self.free_workers_left = int(
            free_workers_span.get_text().replace('.', ''))

        box = soup.find('div', {'class': 'box'})
        while box:
            buildings.append(self.parse_building(box))
            box = box.find_next_sibling('div', {'class': 'box'})
        return buildings

    def select_village(self, villages):
        if len(villages) > 1:
            page_size = 20  # Number of items to display per page
            page_count = len(villages) // page_size  # Number of pages

            # Loop through the pages
            for page in range(page_count):
                # Calculate the starting and ending indices of the current page
                start = page * page_size
                end = start + page_size
                # Display the current page
                print(f"Page {page+1}/{page_count}")
                for village in villages[start:end]:
                    for key, value in village.items():
                        print(f"{key} (Village ID: {value})")

                # Ask the user if they want to see the next page
                choice = input(
                    "Enter the village ID or 'n' to see the next page or 'q' to quit: ")
                if choice.lower() == "n":
                    continue
                elif choice.lower() == "q":
                    break
                else:
                    # Check if the user's input matches any of the village IDs
                    for village in villages:
                        for key, value in village.items():
                            if value == choice:
                                # Return the selected village
                                return value
                # If the loop completes without finding a matching village, return None
                return None

        elif len(villages) == 1:
            # If there is only one village, display it and return its ID
            for key, value in villages[0].items():
                return value

        else:
            # If there are no villages, return None
            return None
