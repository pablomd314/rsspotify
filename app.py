#!/usr/bin/python3
from flask import Flask
import urllib
import socket
import requests
from rsspotify import rsspotify

CALLBACK_HOST = "localhost"
CALLBACK_PORT = 5000
CALLBACK_PATH = '/v1/authorization'
TOKEN_URL = "https://accounts.spotify.com/api/token"
client_id = "acd31fda177a4c66b264b9a086c72f49"
client_secret = "a0e8ec4f430544069d766ada2636620a"

app = Flask("RSSpotify")

def get_tokens(authorization_code):
    payload = {"grant_type": "authorization_code", 
    "code": authorization_code, 
    "redirect_uri": "http://{0}:{1}{2}".format(CALLBACK_HOST, CALLBACK_PORT, CALLBACK_PATH),
    "client_id": client_id, 
    "client_secret": client_secret}
    r = requests.post(TOKEN_URL, data=payload)
    j = r.json()
    return j.get("access_token"), j.get("refresh_token")

def start_callback_server():
    HOST = 'localhost'                 # Symbolic name meaning all available interfaces
    PORT = CALLBACK_PORT              # Arbitrary non-privileged port
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

def get_authorize_link():
    client_id = "acd31fda177a4c66b264b9a086c72f49"
    response_type = "code"
    redirect_uri = "http://localhost:5000/v1/authorization"
    return "https://accounts.spotify.com/authorize/?{0}".format(
        urllib.parse.urlencode({
            "client_id": client_id, 
            "response_type": response_type,
            "redirect_uri": redirect_uri
        }))

@app.route("/v1/artists", methods=["GET"])
def get_artists():
    return rsspotify.getArtistFeed(app.authorization_token, "1vCWHaC5f2uS3yhpwWbIA6").xml()

def main():
    print("Please authorize app here: {0}".format(get_authorize_link()))
    http_response = start_callback_server()
    print(http_response)
    if not http_response.startswith("GET {0}?code=".format(CALLBACK_PATH)):
        raise Exception("BAD BHADDIE")
    app.authorization_code = http_response.split()[1].split("=")[1]
    app.authorization_token, app.refresh_token = get_tokens(app.authorization_code)
    print(rsspotify.getArtistFeed(app.authorization_token, "1vCWHaC5f2uS3yhpwWbIA6"))
    app.run()

if __name__ == '__main__':
    main()