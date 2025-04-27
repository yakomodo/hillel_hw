import json

with open('pokemons.json', 'r') as file:
    pokemons = json.load(file)

search_type = input("Який тип покемону тебе цікавать ? (наприклад, grass, fire, water): ").lower()

found_pokemons = []

for pokemon in pokemons:
    if search_type in pokemon['types']:
        found_pokemons.append(pokemon['name'])

if found_pokemons:
    print(f"Покемони з типом '{search_type}':")
    for name in found_pokemons:
        print(f"- {name}")
else:
    print(f"Покемонів з типом '{search_type}' не знайдено.")