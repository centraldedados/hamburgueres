from pyzomato import Pyzomato
import re

api_token = 'your_api_token'
cuisinesFilter = 'Burger' # Must match the API Name
locationName = 'porto'
filteredCuisine = []
filteredRestaurants = []

p = Pyzomato(api_token)

location = p.getLocations(query=locationName)['location_suggestions'][0]

# Filter by cuisine name
pattern = re.compile('.*' + cuisinesFilter + '.*')
for cuisine in p.getCuisines(city_id=location['city_id'])['cuisines']:
    # cuisine_id
    if cuisinesFilter not in cuisine['cuisine']['cuisine_name']:
        continue
    filteredCuisine.append(cuisine['cuisine'])

# entity_id=311&entity_type=city&cuisines=168
startDocuments = 0
totalDocuments = 0

while totalDocuments == 0 or startDocuments != totalDocuments:
    request = p.search(start=startDocuments, entity_id=location['entity_id'], entity_type=location['entity_type'], cuisines=filteredCuisine[0]['cuisine_id'])
    startDocuments = request['results_start'] + request['results_shown']
    totalDocuments = request['results_found']

    for restaurant in request['restaurants']:
        filteredRestaurants.append(restaurant)

result = []
for restaurant in filteredRestaurants:
    important_keys = ('name', 'url', 'address', 'locality', 'latitude', 'longitude', 'aggregate_rating', 'rating_text')
    restaurant['restaurant'].update(restaurant['restaurant']['location'])
    restaurant['restaurant'].update(restaurant['restaurant']['user_rating'])
    result.append({ key: restaurant['restaurant'][key] for key in important_keys })

print(result)