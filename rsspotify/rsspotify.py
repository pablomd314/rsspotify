import requests
import copy
from . import rss
import urllib
import time
import requests
import socket
import datetime

class SpotifyClient(object):
    """This class handles all communication with the spotify server"""
    CALLBACK_PATH = "/v1/authorization"
    TOKEN_URL = "https://accounts.spotify.com/api/token"
    # constructor needs to authenticate client
    def __init__(self, client_id, client_secret, hostname, port):
        self.CALLBACK_HOST = hostname
        self.CALLBACK_PORT = port
        self.client_id = client_id
        self.client_secret = client_secret
        print("Please authorize app here: {0}".format(get_authorize_link(client_id,
            self.CALLBACK_HOST, self.CALLBACK_PORT)))
        http_response = self.start_callback_server()

        # once we've gotten our callback, we have the authorization_code
        # and refresh token
        if not http_response.startswith("GET {0}?code=".format(self.CALLBACK_PATH)):
            raise Exception("Bad request.")
        authorization_code = http_response.split()[1].split("=")[1]
        self.get_tokens(authorization_code)
        print(self.authorization_token, self.refresh_token)
        if self.authorization_token is None or self.refresh_token is None:
            raise Exception("Failed to get tokens.")

    def start_callback_server(self):
        print("!!!! CALLBACK SERVER !!!!")
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

    def refresh_tokens(self):
        payload = {"grant_type": "refresh_token", 
        "refresh_token": self.refresh_token, 
        "client_id": self.client_id, 
        "client_secret": self.client_secret}
        r = requests.post(self.TOKEN_URL, data=payload)
        j = r.json()
        self.tokensExpiry = time.time() + j.get("expires_in")
        self.authorization_token = j.get("access_token")        

    def get(self, api_link):
        if self.tokensExpiry <= time.time():
            self.refresh_tokens()
        headers = {"Authorization": "Bearer {0}".format(self.authorization_token),
        "Content-Type": "application/json", "Accept": "application/json"}
        try:
            r = requests.get(api_link, headers=headers)
        except Exception as e:
            raise e
        j = r.json()
        return j

    def get_artist_info(self, artist_id):
        api_link = "https://api.spotify.com/v1/artists/{0}".format(artist_id)
        j = self.get(api_link)
        return j


    def get_artist_feed(self, artist_id):
        # check if need to refresh
        api_link = "https://api.spotify.com/v1/artists/{0}/albums".format(artist_id)
        j = self.get(api_link)
        artist_info = self.get_artist_info(artist_id)
        config = {
        "version": "2.0",
        "channel": {
            "title": artist_info["name"],
            "description": "A much shorter description.", 
            "link": artist_info["external_urls"]["spotify"],
            "items": []
            }
        }
        item = {"title": "RSS Solutions for Restaurants", "description": "Do less."}
        for x in j['items']:
            i = copy.copy(item)
            i['title'] = x['name']
            i['description'] = x['album_type'].capitalize()
            i['link'] = x['external_urls']['spotify']
            i['pubDate'] = datetime.datetime.strptime(x['release_date'], "%Y-%m-%d")
            config["channel"]["items"].append(i)
        return rss.RSSElement(config)

    def search_for_artists(self, query):
        # check if need to refresh
        api_link = "https://api.spotify.com/v1/search?{0}".format(
            urllib.parse.urlencode({
                "type": "artist", 
                "q": query 
            }))
        j = self.get(api_link)
        list_of_artists = j.get('artists').get('items')
        return list_of_artists

def get_authorize_link(client_id, hostname, port):
    response_type = "code"
    redirect_uri = "http://{0}:{1}/v1/authorization".format(hostname, port)
    return "https://accounts.spotify.com/authorize/?{0}".format(
        urllib.parse.urlencode({
            "client_id": client_id, 
            "response_type": response_type,
            "redirect_uri": redirect_uri
        }))

