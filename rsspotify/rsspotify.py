import requests
import copy
from . import rss


def getArtistFeed(authorization_token, artist_id):
    api_link = "https://api.spotify.com/v1/artists/{0}/albums".format(artist_id)
    headers = {"Authorization": "Bearer {0}".format(authorization_token),
    "Content-Type": "application/json", "Accept": "application/json"}
    r = requests.get(api_link, headers=headers)
    config = {
    "version": "2.0",
    "channel": {
        "title": "FeedForAll Sample Feed",
        "description": "A much shorter description.", 
        "link": "http://www.feedforall.com/industry-solutions.htm",
        "items": []
        }
    }
    item = {"title": "RSS Solutions for Restaurants", "description": "Do less."}
    for x in r.json()['items']:
        i = copy.copy(item)
        i['title'] = x['name']
        i['description'] = "An album type thing"
        i['guid'] = x['external_urls']['spotify']
        config["channel"]["items"].append(i)
    return rss.RSSElement(config)
