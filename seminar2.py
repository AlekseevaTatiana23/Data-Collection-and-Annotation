import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
ua = UserAgent()

#url = 'https://www.boxofficemojo.com/intl/?ref_=bo_nb_hm_tab'

url = 'https://www.boxofficemojo.com'
headers = {'User-Agent': ua.chrome}
params = {'ref_': 'bo_nb_hm_tab'}

session = requests.session() #чтобы не вызвало подозрений, заходим пож разными сессиями

response = session.get(url+'/intl', params=params, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
#test_link = soup.find('a', {'class': 'a-link-normal'})

rows = soup.find_all('tr')

films =[]
for row in rows[2:-1]:
    film = {}

   # area_info = row.find('td', {'class': 'mojo-field-type-area_id'}).find('a')
    area_info = row.find('td', {'class': 'mojo-field-type-area_id'}).findChildren()[0] # 2 способ
    film['area'] = [area_info.getText(), url + area_info.get('href')]

    weekend_info = row.find('td', {'class': 'mojo-field-type-date_interval'}).findChildren()[0]
    film['weekend'] = [weekend_info.getText(), url + weekend_info.get('href')]

    film['realeses'] = int(row.find('td', {'class': 'mojo-field-type-positive_integer'}).gerText())

    frealese_info = row.find('td', {'class': 'mojo-field-type-realease'}).findChildren()[0]
    film['frealese'] = [frealese_info.getText(), url + frealese_info.get('href')]

    try:
        distributor_info = row.find('td', {'class': 'mojo-field-type-studio'}).findChildren()[0]
        film['distributor'] = [distributor_info.getText(), url + distributor_info.get('href')]
    except:
        print('Exceptoin with distributor, object =', film['distributor'])
        film['distributor_info'] = None

    film['gross'] = int(row.find('td', {'class': 'mojo-field-type-positive_integer'}).gerText())
    films.append(film)

pprint(films)
