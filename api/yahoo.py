from http.server import BaseHTTPRequestHandler
import urllib.request, urllib.parse, json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        symbol = q.get('symbol', [''])[0]
        range_ = q.get('range',  ['6mo'])[0]
        url = (f'https://query1.finance.yahoo.com/v8/finance/chart/'
               f'{urllib.parse.quote(symbol)}?interval=1d&range={range_}')
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as r:
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
