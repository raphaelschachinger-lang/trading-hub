from http.server import BaseHTTPRequestHandler
import urllib.request, urllib.parse, json, os

FRED_KEY = os.environ.get('FRED_KEY', '')

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        series = q.get('series', [''])[0]
        limit  = q.get('limit',  ['65'])[0]
        sort   = q.get('sort',   ['desc'])[0]
        url = (f'https://api.stlouisfed.org/fred/series/observations'
               f'?series_id={series}&api_key={FRED_KEY}'
               f'&file_type=json&sort_order={sort}&limit={limit}')
        try:
            with urllib.request.urlopen(urllib.request.Request(url), timeout=15) as r:
                data = r.read()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
