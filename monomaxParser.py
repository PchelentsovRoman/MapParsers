import requests
import json
from bs4 import BeautifulSoup

class Parser:

    def __init__(self):
        self.url = 'https://monomax.by/map'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
        self.monomax_array = []

    def data_generation(self):
        r = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        shops = soup.findAll('div', class_='shop')
        lon_lat_array = []
        for i in range(0, len(shops)-1):
            dictionary = {
                'adress': "",
                'location': "",
                'name': "",
                'phones': ""
            }
            script = str(soup.findAll('script'))
            l_l_index = script.find(f'myPlacemark{i}')
            lon_lat_array.append(script[l_l_index + 57:l_l_index + 91].strip())

            dictionary['adress'] = shops[i].find('p', class_='name').text
            dictionary['name'] = shops[i].find('p', class_='name').text
            dictionary['phones'] = shops[i].find('p', class_='phone').text
            dictionary['location'] = lon_lat_array[i]
            self.monomax_array.append(dictionary)

    def saveData(self):
        with open("data_file_monomax.json", "w", encoding="utf8") as write_file:
            json.dump(self.monomax_array, write_file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    sample = Parser()
    sample.data_generation()
    sample.saveData()



