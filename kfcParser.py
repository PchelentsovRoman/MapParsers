import json


class Parser:

    def __init__(self):
        with open('store.json', encoding="utf8") as f:
            self.kfc_stores = json.load(f)
            self.kfc_array = []

    def data_generation(self):
        for i in range(0, len(self.kfc_stores['searchResults'])):
            try:
                contacts = self.kfc_stores['searchResults'][i]['storePublic']['contacts']
                adress = contacts['streetAddress']['ru']
                if int(adress[0]):
                    adress = adress[7:]
                location = contacts['coordinates']['geometry']['coordinates']
                name = contacts['coordinates']['properties']['name']['ru']
                if len(name) < 5 or 'test' in name.lower() or len(adress) < 5:
                    continue
                phones = contacts['phoneNumber']
                start_time_local = self.kfc_stores['searchResults'][i]['storePublic']['openingHours']['regular'][
                    'startTimeLocal']
                end_time_local = self.kfc_stores['searchResults'][i]['storePublic']['openingHours']['regular'][
                    'endTimeLocal']
                status = self.kfc_stores['searchResults'][i]['storePublic']['status']

                dictionary = {
                    'adress': adress,
                    'location': location,
                    'name': name,
                    'phones': phones,
                    'working_hours': [
                        f"пн-пт {start_time_local} до {end_time_local}, сб-вс {start_time_local}-{end_time_local}"]
                }

                if status == 'Closed':
                    dictionary["working_hours"] = 'closed'

                self.kfc_array.append(dictionary)
            except:
                continue

    def save_data(self):

        with open("data_file_kfc.json", "w", encoding="utf8") as write_file:
            json.dump(self.kfc_array, write_file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    sample = Parser()
    sample.data_generation()
    sample.save_data()
