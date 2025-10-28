import aiohttp
import requests

URL = "https://api.exchangerate-api.com/v4/latest/"


# WSGI приложение
# Для запуска: gunicorn asgi_and_wsgi_task:application_wsgi -b :8000 --reload
def application_wsgi(environ, start_response):
    request_to_api = requests.get(URL + environ["PATH_INFO"].lstrip("/"))
    if request_to_api.status_code == 200:
        status = "200 OK"
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        return [request_to_api.content]

    else:
        status = "500 Internal server error"
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        body = {
            "message": "something went wrong",
        }
        return [bytes(str(body), encoding='utf-8')]


# ASGI приложение
# Для запуска: uvicorn asgi_and_wsgi_task:application_asgi --reload --port 8000
async def application_asgi(scope, receive, send):
    currency = scope["path"].lstrip("/")

    async with aiohttp.ClientSession() as session:
        async with session.get(URL + currency) as resp:
            data = await resp.read()

    if resp.status == 200:
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [[b"content-type", b"application/json"]]
        })

        await send({
            'type': 'http.response.body',
            'body': data,
        })

    else:
        await send({
            "type": "http.response.start",
            "status": resp.status,
            "headers": [[b"content-type", b"application/json"]]
        })

        await send({
            'type': 'http.response.body',
            'body': '',
        })
