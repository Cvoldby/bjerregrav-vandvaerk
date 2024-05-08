import requests

response = requests.get("https://www.elprisenligenu.dk/api/v1/prices/2024/04-19_DK1.json")

print(response.status_code)

print(response.json())

for i in response.json():
    print('Tidsinterval:', i['time_start'][11:16], i['time_end'][11:16], 'Pris', i['DKK_per_kWh'], 'oere/kWh')



response = requests.get("https://api.energidataservice.dk/dataset/CO2Emis/download?format=json&limit=10")

print(response.status_code)


