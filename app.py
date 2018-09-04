#!/usr/bin/python3
from flask import Flask, request, jsonify
from rsspotify import rsspotify
import json

try:
    with open("settings.json") as f:
        client_settings = json.load(f)
    client_id = client_settings["client_id"]
    client_secret = client_settings["client_secret"]
    hostname = client_settings["hostname"]
    port = client_settings["port"]
except Exception as e:
    raise e


app = Flask("RSSpotify", static_url_path='')

@app.route("/v1/generate_feed_urls")
def gen_urls():
    return app.send_static_file('index.html')

@app.route("/v1/search", methods=["GET"])
def search_artists():
    query = request.args.get('query')
    return jsonify(app.client.search_for_artists(query))

@app.route("/v1/artists/<artist_id>", methods=["GET"])
def get_artists(artist_id):
    feed = app.client.get_artist_feed(artist_id)
    if feed is not None:
        return feed.xml()
    return ""

def main():
    app.client = rsspotify.SpotifyClient(client_id, client_secret, hostname, port)
    print(app.client.get_artist_feed("1vCWHaC5f2uS3yhpwWbIA6"))
    print(app.client.search_for_artists("Kendrick"))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()