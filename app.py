import json
import requests
import redis
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return "readme backend"


@app.route('/check/')
def check():
    return "Online"


@app.route('/lookup/<int:isbn>/')
def lookup(isbn):
    r = redis.Redis(host="redis", port=6379)
    redis_key = "isbn:%d" % isbn
    if not r.exists(redis_key):
        response = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:%d" % isbn);
        content = json.loads(response.text)
        if content['totalItems'] == 0:
            return jsonify({"success": False, "error": "No match for ISBN %s" % isbn})
        book = content['items'][0]
        volume_info = book['volumeInfo']
        payload = json.dumps(volume_info)
        for isbn in volume_info['industryIdentifiers']:
            r.set("isbn:%s" % isbn['identifier'], payload)
        return jsonify({"success": True, "content":book})
    else:
        content = r.get(redis_key)
        return jsonify({"success": True, "content": json.loads(content), "source": "cache"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
