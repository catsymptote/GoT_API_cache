from fastapi import FastAPI
import requests
import uvicorn


app = FastAPI()


REQUEST_COUNTER = 0
CACHE_MISSES = 0
CACHE = {}


@app.get('/')
def info():
    global REQUEST_COUNTER
    REQUEST_COUNTER += 1
    return {'Info': 'Go to `/characters/<id: int>` to get results. E.g., `/characters/1052`.'}


@app.get('/info')
def get_request_count():
    global REQUEST_COUNTER, CACHE_MISSES, CACHE
    return {
        'request count': REQUEST_COUNTER,
        'cache misses': CACHE_MISSES,
        'cache size': len(CACHE)
    }


@app.get("/characters/{id}")
def get_characters(id: int):
    global REQUEST_COUNTER, CACHE_MISSES, CACHE
    REQUEST_COUNTER += 1

    cache_hit = True
    if id not in CACHE:
        CACHE_MISSES += 1
        cache_hit = False
        URL = f'https://anapioficeandfire.com/api/characters/{id}'
        response = requests.get(URL)
        data = response.json()
        CACHE[id] = data

    # Return results
    return_message = {
        'cache-hit': cache_hit,
        'data': CACHE[id]
    }
    return return_message


if __name__ == "__main__":
    # uvicorn main:app --host 0.0.0.0 --port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
    pass
