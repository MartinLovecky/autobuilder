from bs4 import BeautifulSoup
from login import Login
import requests
import re


class Buildings:

    def __init__(
        self,
        stone_left = 0,
        wood_left = 0,
        iron_left = 0,
        storage_left = 0,
        free_villagers_left = 0
    ):
        self.stone_left = stone_left
        self.wood_left = wood_left
        self.iron_left = iron_left
        self.storage_left = storage_left
        self.free_villagers_left = free_villagers_left

    def get_resources(self, soup):
        # parse the resource information from the HTML
        stone_span = soup.find('span', id='stone')
        wood_span = soup.find('span', id='wood')
        iron_span = soup.find('span', id='iron')
        free_villagers_span = soup.find(
            'div', {'class': 'villageInfobar'}).find_all('span')[-1]
        storage_span = soup.find(
            'div', {'class': 'villageInfobar'}).find_all('span')[-2]

        for element in storage_span:
            if re.match(r'\d+\.\d+', element.text):
                storage_span = element
            break

        # Resources
        self.stone_left = int(stone_span.get_text().replace('.', ''))
        self.wood_left = int(wood_span.get_text().replace('.', ''))
        self.iron_left = int(iron_span.get_text().replace('.', ''))
        self.storage_left = int(storage_span.get_text().replace('.', ''))
        self.free_villagers_left = int(
            free_villagers_span.get_text().replace('.', ''))

    def parse_building(self, box):

        # parse the information for a single building from the HTML
        name = box.find('div', {'class': 'name'}).find('a').text
        buildtime = box.find('div', {'class': 'buildtime'}).text
        workers = int(
            box.find('div', {'class': 'workers'}).text.replace('.', ''))
        link = Login.service_url + \
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

    def pasrse_buildings(self, village_id):
        buildings = []
        target_url = f'{Login.service_url}?village={village_id}&s=build_main'
        response = requests.Session().get(target_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.get_resources(soup)
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
                for village_name, village_id in villages.items():
                    if start <= int(village_id) < end:
                        key, value = village_name
                        print(f"{key} {value} (Village ID: {village_id})")

                # Ask the user if they want to see the next page
                choice = input(
                    "Enter the village ID or 'n' to see the next page or 'q' to quit: ")
                if choice.lower() == 'n':
                    continue
                elif choice.lower() == 'q':
                    break
                else:
                    # Check if the user's input matches any of the village IDs
                    for village_name, village_id in villages.items():
                        if village_id == choice:
                            # Return the selected village
                            return village_id
            # If the loop completes without finding a matching village, return None
            return None
        else:
            for village_name, village_id in villages.items():
                key, value = village_name
                print(f"{key} {value} (Village ID: {village_id})")
            return villages[0]
