import requests

def getArtistFeed(artist_id):
    api_link = "https://api.spotify.com/v1/artists/{0}/albums".format(artist_id)
    headers = {"Authorization": "Bearer BQAJpDq3kKA6_G-h1YxadnLONyZZpgZN2BkJODIYVKMTDTpu4QY1CAix-Dfqf44iWLSGyr4CuP3Eo72ThKBV5lG_Sq_8CqhcGKPRClrPZt5SlWJtWLd2Q87LucBbdneDhUW66FexhktYDwg",
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
    return r.json()
    item = {"title": "RSS Solutions for Restaurants", "description": "Do less."}
    # config["channel"]["items"].append()
