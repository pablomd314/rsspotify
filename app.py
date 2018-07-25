#!/usr/bin/python3
from flask import Flask
app = Flask("RSSpotify")

@app.route("/v1/artists", methods=["GET"])
def get_artists():
	print('word')

def main():
	print('Main')

if __name__ == '__main__':
	main()