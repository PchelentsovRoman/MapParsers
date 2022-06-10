import requests
import json
from bs4 import BeautifulSoup

class Parser:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User Agent': 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept': '*/*',
            'Content-Type': 'text/html; charset=UTF-8',
        }

        self.result = {}
        self.url = 'https://www.ziko.pl/wp-admin/admin-ajax.php?action=get_pharmacies'

    def json_to_dict(self):
        response = self.session.get(url=self.url)
        return response.json()


    def save_json(self):
        parsed = self.json_to_dict()
        ziko_array = []
        for key in parsed.keys():
            name = parsed[key]['title']
            location = []
            location.append(float(parsed[key]['lat']))
            location.append(float(parsed[key]['lng']))
            adress = parsed[key]['address']
            working_hours = parsed[key]['hours'].replace("\r\n"," ")

            dictionary = {
                        'adress': adress,
                        'location': location,
                        'name': name,
                        'working_hours': working_hours
                         }
            ziko_array.append(dictionary)

        self.url = 'https://www.ziko.pl/lokalizator/'
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, "lxml")

        for row in soup.findAll('td', class_='mp-table-address'):
            for key in ziko_array:
                if str(row).find(key['adress']) != -1:
                    index_of_phone = str(row).find('tel.')
                    key['phones'] = str(row)[int(index_of_phone)+5:int(index_of_phone)+17]

        with open("data_file_ziko.json", "w", encoding="utf8") as write_file:
            json.dump(ziko_array, write_file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    sample = Parser()
    sample.save_json()