import requests
import copy
from . import rss
import urllib
import time
import requests
import socket

class SpotifyClient(object):
    """This class handles all communication with the spotify server"""
    CALLBACK_HOST = "localhost"
    CALLBACK_PORT = 5000
    CALLBACK_PATH = "/v1/authorization"
    TOKEN_URL = "https://accounts.spotify.com/api/token"
    # constructor needs to authenticate client
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        print("Please authorize app here: {0}".format(get_authorize_link(client_id)))
        http_response = self.start_callback_server()

        # once we've gotten our callback, we have the authorization_code
        # and refresh token
        if not http_response.startswith("GET {0}?code=".format(self.CALLBACK_PATH)):
            raise Exception("Bad request.")
        authorization_code = http_response.split()[1].split("=")[1]
        self.get_tokens(authorization_code)
        if self.authorization_token is None or self.refresh_token is None:
            raise Exception("Failed to get tokens.")

    def start_callback_server(self):
        HOST = self.CALLBACK_HOST
        PORT = self.CALLBACK_PORT
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024)
                conn.sendall(b"""HTTP/1.1 200 OK
    Date: Mon, 25 Aug 2018 11:11:53 GMT
    Server: Apache/2.2.14 (Win32)
    Last-Modified: Mon, 25 Aug 2018 11:11:53 GMT
    Content-Length: 0
    Content-Type: text/html
    Connection: Closed!""")
        return data.decode("utf-8")

    def get_tokens(self, authorization_code):
        payload = {"grant_type": "authorization_code", 
        "code": authorization_code, 
        "redirect_uri": "http://{0}:{1}{2}".format(self.CALLBACK_HOST,
            self.CALLBACK_PORT, self.CALLBACK_PATH),
        "client_id": self.client_id, 
        "client_secret": self.client_secret}
        r = requests.post(self.TOKEN_URL, data=payload)
        j = r.json()
        self.tokensExpiry = time.time() + j.get("expires_in")
        self.authorization_token, self.refresh_token = j.get("access_token"), j.get("refresh_token")

    def get_artist_feed(self, artist_id):
        # check if need to refresh
        if self.tokensExpiry <= time.time():
            self.get_tokens(self.refresh_token) 
        api_link = "https://api.spotify.com/v1/artists/{0}/albums".format(artist_id)
        headers = {"Authorization": "Bearer {0}".format(self.authorization_token),
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

    def search_for_artists(self, query):
        # check if need to refresh
        if self.tokensExpiry <= time.time():
            self.get_tokens(self.refresh_token)
        api_link = "https://api.spotify.com/v1/search?{0}".format(
            urllib.parse.urlencode({
                "type": "artist", 
                "q": query 
            }))
        headers = {"Authorization": "Bearer {0}".format(self.authorization_token),
        "Content-Type": "application/json", "Accept": "application/json"}
        try:
            r = requests.get(api_link, headers=headers)
        except Exception as e:
            raise e
        j = r.json()
        list_of_artists = j.get('artists').get('items')
        return list_of_artists

def get_authorize_link(client_id):
    response_type = "code"
    redirect_uri = "http://localhost:5000/v1/authorization"
    return "https://accounts.spotify.com/authorize/?{0}".format(
        urllib.parse.urlencode({
            "client_id": client_id, 
            "response_type": response_type,
            "redirect_uri": redirect_uri
        }))

