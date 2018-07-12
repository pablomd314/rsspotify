#!/usr/bin/python3
import pytest
import sys
sys.path.append("../rsspotify")
import rss 

def test_RSSElement():
  with open('rss_element.xml') as file:
    x = file.read() 
  config = {
    "version": "2.0", 
    "channel": {
      "title": "FeedForAll Sample Feed",
      "description": "A much shorter description.", 
      "link": "http://www.feedforall.com/industry-solutions.htm",
      "category": [
        {
          "domain": "www.dmoz.com",
          "text": "Computers/Software/Internet/Site Management/Content Management"
        }
      ],
      "copyright": "Copyright 2004 NotePage, Inc.",
      "docs": "http://blogs.law.harvard.edu/tech/rss",
      "language": "en-us",
      "lastBuildDate": "Tue, 19 Oct 2004 13:39:14 -0400",
      "managingEditor": "marketing@feedforall.com",
      "pubDate": "Tue, 19 Oct 2004 13:38:55 -0400",
      "webMaster": "webmaster@feedforall.com",
      "generator": "FeedForAll Beta1 (0.0.1.8)",
      "image": {
        "url": "http://www.feedforall.com/ffalogo48x48.gif",
        "title": "FeedForAll Sample Feed",
        "link": "http://www.feedforall.com/industry-solutions.htm",
        "description": "FeedForAll Sample Feed",
        "width": 48,
        "height": 48
      },
      "items": [
        {
          "title": "RSS Solutions for Restaurants",
          "description": "Do less.",
          "link": "http://www.feedforall.com/restaurant.htm",
          "category": {
            "domain": "www.dmoz.com",
            "text": "Computers/Software/Internet/Site Management/Content Management"
          },
          "comments": "http://www.feedforall.com/forum",
          "pubDate": "Tue, 19 Oct 2004 11:09:11 -0400"
        }
      ]
    }
  }
  r = rss.RSSElement(config)
  # with open('out.xml', 'w+') as file:
  #   file.write(r.xml())
  # print(x)
  r.xml()
  # assert r.xml() == x

def main():
  test_RSSElement()

if __name__ == '__main__':
  main()