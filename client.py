from datetime import date
from client_utils import NeoData, neo_url_from_date, filter_json_resp

import aiohttp
from pysondb import db as database

from shared import MAX_REQUESTS_PER_HOUR

db = database.getDb('database.json')

remaining_requests = MAX_REQUESTS_PER_HOUR


async def neo_from_date(day: date) -> NeoData:
    data = db.getByQuery({'date': day.strftime('%Y-%m-%d')})
    if not data:
        async with aiohttp.ClientSession() as session:
            async with session.get(neo_url_from_date(day)) as resp:
                data = []
                for neo in filter_json_resp(await resp.json()):
                    db.add(neo)
                    data.append(neo)
                    global remaining_requests
                    remaining_requests = int(resp.headers['X-Ratelimit-Remaining'])
    return NeoData(remaining_requests, day, data)
