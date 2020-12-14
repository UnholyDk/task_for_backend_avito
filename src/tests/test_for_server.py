import requests
import time

URL = 'http://' + 'server:8000'

REGION1 = 'moskva'
REGION2 = 'moskvaa'

PHRASE1 = 'ps5'

def test_stat_404():
    data = {
        'id_search': -1,
        'interval': [0, 1]
    }
    response = requests.put(URL + '/stat', json=data)
    assert response.status_code == 404

def test_add_400():
    data = {
        'search_phrase': PHRASE1,
        'region': REGION2
    }
    response = requests.put(URL + '/add', json=data)
    assert response.status_code == 400

def test_top5_404():
    response = requests.get(URL + '/top5/0')
    assert response.status_code == 404

def test_add_and_stat():
    data = {
        'search_phrase': PHRASE1,
        'region': REGION1
    }

    timestamp = int(time.time())

    response = requests.put(URL + '/add', json=data)
    assert response.status_code == 200
    assert response.json()['id'] >= 0

    id_search = response.json()['id']

    data = {
        'id_search': id_search,
        'interval': [timestamp - 100, timestamp + 100]
    }
    response = requests.put(URL + '/stat', json=data)
    assert response.status_code == 200
    result = response.json()['result']

    assert len(result) == 1
    assert len(result[0]) == 2


def test_top5():
    data = {
        'search_phrase': PHRASE1,
        'region': REGION1
    }
    response = requests.put(URL + '/add', json=data)

    assert response.status_code == 200
    assert response.json()['id'] >= 0

    id_search = response.json()['id']

    response = requests.get(URL + f'/top5/{id_search}')
    assert response.status_code == 200

    assert len(response.json()) == 5

