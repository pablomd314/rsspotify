#!/usr/bin/python3
from flask import Flask, request, jsonify
from rsspotify import rsspotify

client_id = "acd31fda177a4c66b264b9a086c72f49"
client_secret = "a0e8ec4f430544069d766ada2636620a"

app = Flask("RSSpotify", static_url_path='')

@app.route("/v1/generate_feed_urls")
def gen_urls():
    print("BITCH IMMA COW")
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
    app.client = rsspotify.SpotifyClient(client_id, client_secret)
    print(app.client.get_artist_feed("1vCWHaC5f2uS3yhpwWbIA6"))
    print(app.client.search_for_artists("Kendrick"))
    app.run()

if __name__ == '__main__':
    main()