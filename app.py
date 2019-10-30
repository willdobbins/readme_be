import json
import requests
import redis
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "Readme Backend."


@app.route('/check')
def check():
    return "Online"


@app.route('/lookup/<int:isbn>')
def lookup(isbn):
    r = redis.Redis(host="redis", port=6379)
    redis_key = "isbn:%d" % isbn
    if not r.exists(redis_key):
        response = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:%d" % isbn);
        content = json.loads(response.text)
        volumes = []
        for item in content['items']:
            volume_info = item['volumeInfo']
            volumes.append(volume_info)
            payload = json.dump(volume_info)
            for isbn in volume_info['industryIdentifiers']:
                r.set("isbn:%d" % isbn, payload)
        return volumes
    else:
        content = r.get(redis_key)
        return content


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
