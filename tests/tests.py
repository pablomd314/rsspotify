import pytest
import sys
sys.path.append("../rsspotify")
import rss 

def test_RSSElement():
  x = """<rss version="2.0">
  <channel>
    <title>Example Domain</title>
    <link>http://example.com</link>
    <description>A phrase or sentence describing the channels.</description>
  </channel>
</rss>"""
  r = rss.RSSElement()
  print(r.rss())
  print(x)
  assert r.rss() == x
