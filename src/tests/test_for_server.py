import requests

URL = 'http://' + 'server:8000'

REGION1 = 'moskva'
REGION2 = 'moskvaa'
REGION3 = 'kazan'

PHRASE1 = 'ps5'
PHRASE2 = 'собака'
PHRASE3 = 'квартира'

def test_stat_404():
    data = {
        'id_search': 0,
        'interval': [0, 1]
    }
    response = requests.put(URL + '/stat', json=data)
    assert response.status_code == 404