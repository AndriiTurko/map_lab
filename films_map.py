def films_locations(year, country):
    """
    (str), (str) -> (dict)
    Return dictionary with keys as locations where films where made
    and items as names of films.
    """
    films_dictionary = {}
    with open('locations.list', 'r') as f:
        for line in f:
            line = line.strip()
            line = line.replace('\t\t\t\t', '\t').replace('\t\t\t', '\t')
            line = line.replace('\t\t', '\t')
            line = line.split('\t', 1)
            if len(line) == 2 and check_year(line, year):
                location = location_get(line)
                name = name_get(line)
                if location not in films_dictionary and \
                        location.split(', ')[-1] == country:
                    films_dictionary[location] = name
    return films_dictionary


def check_year(line, year):
    '''
    (list), (str) -> (bool)
    Checks whether film was made in year.
    '''
    if line[0].split(')')[0][-4:] == str(year):
        return True
    else:
        return False


def name_get(line):
    '''
    (lst) -> (str)
    Returns name of the film.
    '''
    name = line[0].split(' (')
    return name[0]


def location_get(line):
    '''
    (lst) -> (str)
    Returns location where the film was made.
    '''
    location = line[1]
    location = location.split('\t')[0]
    return location


def get_address_from_coordinates(coordinates):
    '''
    (str) -> (str)
    Returns the country by coordinates.
    '''
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="Romaniuk", timeout=10)
    location = geolocator.reverse(coordinates, language='en')
    location = str(location).split(', ')
    if location[-1] == 'United States of America':
        location[-1] = 'USA'
    elif location[-1] == 'United Kingdom':
        location[-1] = 'UK'
    return location[-1]


def nearest_locations(dictionary, coordinates):
    '''
    (dict), (str) -> (list)
    Returns a list of tuples with tuples as coordinates and names of films.
    '''
    dist_dict = {}
    coordinates = coordinates.split(', ')
    our_location = (float(coordinates[0]), float(coordinates[1]))
    for place in dictionary.keys():
        try:
            geolocator = Nominatim(user_agent='Romaniuk', timeout=10)
            location = geolocator.geocode(place)
            film_location = (location.latitude, location.longitude)
            distance = great_circle(our_location, film_location).miles
            dist_dict[distance] = (film_location, dictionary[place])
        except:
            continue
    sorted_locations = sorted(dist_dict.keys())
    result = []
    if len(sorted_locations) <= 10:
        for dist in sorted_locations:
            result.append(dist_dict[dist])
    else:
        for i in range(10):
            result.append(dist_dict[sorted_locations[i]])
    return result


def map_builder(lst, coordinates, year, film_dict):
    '''
    Makes map.
    '''
    wrld_map = folium.Map()
    fg = folium.FeatureGroup(name='Films')
    location = coordinates.split(', ')
    fg.add_child(folium.Marker(location=[float(location[0]),
                               float(location[1])],
                               popup="You are here!",
                               icon=folium.Icon(color='purple')))
    for i in range(len(lst)):
        location = lst[i][0]
        fg.add_child(folium.Marker(location=[float(location[0]),
                                   float(location[1])],
                                   popup=lst[i][1],
                                   icon=folium.Icon(color='green')))

    fg2 = folium.FeatureGroup(name='Location')
    location = coordinates.split(', ')
    fg2.add_child(folium.Marker(location=[float(location[0]),
                                float(location[1])],
                                popup="You are here!"))
    fg3 = folium.FeatureGroup(name='Total')
    location = coordinates.split(', ')
    popup_str = "Total amount of films in country is " + str(len(film_dict))
    fg3.add_child(folium.Marker(location=[float(location[0]),
                                float(location[1])],
                                popup=popup_str,
                                icon=folium.Icon(color='purple')))
    wrld_map.add_child(fg)
    wrld_map.add_child(fg2)
    wrld_map.add_child(folium.LayerControl())
    wrld_map.save(str(year) + '_movies_map.html')


def main():
    year = input('Please enter a year you would like to have a map for: ')
    coordinates = input('Please enter your location (format: lat, long): ')
    country = get_address_from_coordinates(coordinates)
    print('Map is generating...')
    film_dict = films_locations(year, country)
    print('Please wait...')
    nearest_film_places = nearest_locations(film_dict, coordinates)
    print('Finished. Please have look at the map',
          str(year) + '_movies_map.html')
    map_builder(nearest_film_places, coordinates, year, film_dict)


if __name__ == "__main__":
    import folium
    from geopy.geocoders import Nominatim
    from geopy.distance import great_circle
    main()
