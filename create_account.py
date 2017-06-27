import pickle
from JodelCrawler import JodelCrawlAcc

cities = [{'lat': 11.567867, 'lng': 13.408333, 'city': "Berlin"},
          {'lat': 53.550556, 'lng': 9.993333, 'city': "Hamburg"},
          {'lat': 48.148434, 'lng': 11.567867, 'city': "Munich"},
          {'lat': 50.933333, 'lng': 6.950000, 'city': "Cologne"},
          {'lat': 50.110924, 'lng': 8.682127, 'city': "Frankfurt"},
          {'lat': 48.78232, 'lng': 9.17702, 'city': "Stuttgart"},
          {'lat': 51.227741, 'lng': 6.773456, 'city': "Dusseldorf"},
          {'lat': 51.513587, 'lng': 7.465298, 'city': "Dortmund"},
          {'lat': 51.455643, 'lng': 7.011555, 'city': "Essen"},
          {'lat': 51.339695, 'lng': 12.373075, 'city': "Leipzig"},
          {'lat': 53.079296, 'lng': 8.801694, 'city': "Bremen"},
          {'lat': 51.050409, 'lng': 13.737262, 'city': "Dresden"},
          {'lat': 52.375892, 'lng': 9.732010, 'city': "Hanover"},
          {'lat': 49.452102, 'lng': 11.076665, 'city': "Nuremberg"},
          {'lat': 51.434408, 'lng': 6.762329, 'city': "Duisburg"},
          {'lat': 51.481845, 'lng': 7.216236, 'city': "Bochum"},
          {'lat': 51.256213, 'lng': 7.150764, 'city': "Wuppertal"},
          {'lat': 52.030228, 'lng': 8.532471, 'city': "Bielefeld"},
          {'lat': 50.737430, 'lng': 7.098207, 'city': "Bonn"},
          {'lat': 51.960665, 'lng': 7.626135, 'city': "Munster"},
          {'lat': 49.006890, 'lng': 8.403653, 'city': "Karlsruhe"},
          {'lat': 49.487459, 'lng': 8.466039, 'city': "Mannheim"},
          {'lat': 48.370545, 'lng': 10.897790, 'city': "Augsburg"},
          {'lat': 50.078218, 'lng': 8.239761, 'city': "Wiesbaden"},
          {'lat': 51.517744, 'lng': 7.085717, 'city': "Gelsenkirchen"},
          {'lat': 51.180457, 'lng': 6.442804, 'city': "Moenchengladbach"},
          {'lat': 52.268874, 'lng': 10.526770, 'city': "Braunschweig"},
          {'lat': 50.827845, 'lng': 12.921370, 'city': "Chemnitz"},
          {'lat': 54.323293, 'lng': 10.122765, 'city': "Kiel"},
          {'lat': 50.775346, 'lng': 6.083887, 'city': "Aachen"},
          {'lat': 49.872825, 'lng': 8.651193, 'city': "Darmstadt"}
          ]

accounts = []

# accounts.append(JodelCrawlAcc(city=cities[7]['city'], lat=cities[7]['lat'], lng=cities[7]['lng']))

for city in cities:
    accounts.append(JodelCrawlAcc(city=city['city'], lat=city['lat'], lng=city['lng'], debug=True))

for account in accounts:
    file_path = 'accounts/' + account.city + '.pickle'

    with open(file_path, 'wb') as file:
        pickle.dump(account, file)