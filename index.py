from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

from filter_feeds import FEEDS, filter_feed


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        feed_name = parse_qs(self.path[2:])["q"][0]
        filtered_feed = filter_feed(*FEEDS.get(feed_name))
        self.send_response(200)
        self.send_header("Content-type", "application/rss+xml")
        self.end_headers()
        self.wfile.write(filtered_feed.encode())
        return
