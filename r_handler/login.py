from bs4 import BeautifulSoup
import re
import requests

class Login:
    
    def __init__(self, 
    username, 
    password, 
    service_url='https://s2-cz.kingsage.gameforge.com/game.php'
    ):
        self.username = username
        self.password = password
        self.service_url = service_url
    
    def set_session(self):
        session = requests.Session()
        login_url = f'{self.service_url}?a=login&user={self.username}&pass={self.password}'
        session.post(login_url)
        target_url = f'{self.service_url}?village=1234&s=info_player'
        response = session.get(target_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        return soup
    
    def villages_dic(self):
        soup = self.set_session()
        outer_table = soup.find('table', style='width:820px;')
        inner_table = outer_table.find('table', class_='borderlist', style='width:420px;')
        cells = inner_table.find_all('td', text='Aliance:')
        values = [cell.find_parent('tr').find('a').get('href') for cell in cells]
        villages = [re.search(r'village=(\d+)', value).group(1) for value in values]

        # Create a dictionary mapping the "Body" and "70" values to the village IDs
        data = {(td_body.text, td_value.text): village for village, (td_body, td_value) in zip(villages, zip(soup.find_all("td", string="Body:"), soup.find_all("td", string=re.compile(r'\d+'))))}
        
        return data