from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bs4 import BeautifulSoup
from bisect import bisect
from apscheduler.schedulers.background import BackgroundScheduler
from typing import Dict, Tuple, List
import requests
import uvicorn
import logging
import time


DB: Dict[Tuple[str, str], int] = {}
COUNTERS: List[Tuple[int, int]] = []

logger = logging.getLogger(__name__)
app = FastAPI()
scheduler = BackgroundScheduler()
scheduler.start()


class RequestAdd(BaseModel):
    search_phrase: str
    region: str


class RequestStat(BaseModel):
    id_search: int
    interval: List[int]


def count_counters(id_search: int, search_phrase: str, region: str):
    logger.warning(f"task start with args {id_search}, {search_phrase}, {region}")
    global COUNTERS
    URL = f'https://www.avito.ru/{region}?q={search_phrase}'

    response = requests.get(URL)
    timestamp = int(time.time())
    soup = BeautifulSoup(response.content, 'html.parser')

    count = int(soup.find(attrs={"data-marker": "page-title/count"}).string.replace(' ', ''))
    COUNTERS[id_search].append((timestamp, count))
    logger.warning(f"task finished with result {count}, timestamp = {timestamp}")


@app.put('/add')
async def get_id(request: RequestAdd):
    global DB, COUNTERS, scheduler
    URL = f'https://www.avito.ru/{request.region}?q={request.search_phrase}'
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    tmp = soup.find(attrs={"data-marker": "page-title/count"})
    if tmp is None:
        raise HTTPException(status_code=400, detail="search phrase or region is incorrect")

    key = (request.search_phrase, request.region)
    if key not in DB:
        DB[key] = len(DB)
        COUNTERS.append([])
        count_counters(DB[key], request.search_phrase, request.region)
        scheduler.add_job(count_counters, 'interval', hours=1, args=[DB[key], request.search_phrase, request.region])
        logger.warning("task add")
    return {'id': DB[key]}


@app.put('/stat')
async def get_counters(request: RequestStat):
    global COUNTERS
    if request.id_search >= len(COUNTERS):
        raise HTTPException(status_code=404, detail="no counters with the given id found")

    left = request.interval[0]
    right = request.interval[1]
    
    first = bisect(list(map(lambda x: x[0], COUNTERS[request.id_search])), left)
    end = bisect(list(map(lambda x: x[0], COUNTERS[request.id_search])), right)

    return {"result": COUNTERS[request.id_search][first:end]}

@app.get('/top5/{id_search}')
async def get_top_ads(id_search: int):
    if id_search >= len(COUNTERS):
        raise HTTPException(status_code=404, detail="this id is not registered in the system")

    URL: str = ''
    for key in DB:
        if DB[key] == id_search:
            URL = f'https://www.avito.ru/{key[1]}?q={key[0]}'
            break
    
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    tmp = soup.find_all(attrs={'data-marker': 'item'})[0:5]

    result: Dict[str, str] = {}
    for i, x in enumerate(tmp):
        href = x.find('a').get('href')
        result[f'top_{i+1}'] = href
    return result
