# RSSpotify

RSSpotify is an RSS server that allows users to keep up to date with new music releases. I've setup my server at ec2-54-86-197-148.compute-1.amazonaws.com. An example feed is at http://ec2-54-86-197-148.compute-1.amazonaws.com/v1/artists/1EpyA68dKpjf7jXmQL88Hy.
### Artist Feeds
Artist feeds contain the most recent releases of an artists.
### Genre Feeds (coming soon)
Genre feeds contain the newest releases by genre, as defined by Spotify's *Explore* feature. 
### Playlist Feeds (coming soon)
Playlist feeds contain updates to a playlist so you know when a song gets added to a playlist.

## How to use
### Config
This app requires a `settings.json` file in the root folder of the project. `settings.json` requires **four** values (client_id, client_secret, hostname, port). Here's an example `settings.json`:
```
{
	"client_id": "abcdefgh12345678",
	"client_secret": "abcdefgh12345678",
	"hostname": "localhost",
	"port": 8000
}
```
`client_id` and `client_secret` refer to the client id and client secret from the associated Spotify app. See https://developer.spotify.com/documentation/ for more details. You will also need to add http://{hostname}:{port}/v1/authorization to your app's valid callback URLs.

### Dependencies
Install the dependencies using pip: `pip3 install -r requirements.txt`
### Running
Running this app is pretty simple.
1. Begin the program running the following command: `python3 app.py`
2. Authorize the app using the printed authorization URL
```
$ python3 app.py 
Please authorize app here: https://accounts.spotify.com/authorize/?client_id=abc123...
```
Once this is done, you should be able to retrieve RSS feeds from the server.
### Feed URLs
Feed URLs have different formats depending on which kind of feed you're trying to get. For example, you can get artist feeds at `/v1/artists/<artist_id>`. You can also generate URLs at `/v1/generate_feed_urls`.
###### (I am not affiliated with Spotify in any capacity, I just wanted a better way to keep up with new releases)

## Documentation
(coming soon)

## Tests
(coming soon)

## Contributing
Feel free to send issues, feedback, or pull requests my way.

## License
This project is licensed under the MIT License - see the LICENSE file for details
