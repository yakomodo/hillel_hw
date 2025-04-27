import requests
import json

pokemons = []

for pokemon_id in range(1, 11):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
    response = requests.get(url)
    data = response.json()
    pokemon_info = {
        'name': data['name'],
        'height': data['height'],
        'weight': data['weight'],
        'types': [poke_type['type']['name'] for poke_type in data['types']]
    }
    pokemons.append(pokemon_info)


# Записуємо всі дані у файл
with open('pokemons.json', 'w') as file:
    json.dump(pokemons, file, indent=2)

print("Дані записано у файл pokemons.json!")