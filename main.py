from fastapi import FastAPI
import requests
import uvicorn


app = FastAPI()


REQUEST_COUNTER = 0
CACHE = {}


@app.get('/')
def info():
    REQUEST_COUNTER += 1
    return {'Info': 'Go to `/characters/<id: int>` to get results. E.g., `/characters/1052`.'}


@app.get('/request_counter')
def get_request_count():
    return {'request count': REQUEST_COUNTER}


@app.get("/characters/{id}")
def get_characters(id: int):
    REQUEST_COUNTER += 1
    # Cache hit — No API request required
    if id in CACHE:
        cache_hit = True
        data = CACHE[id]

    # Cache miss — Request API
    else:
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
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    pass
