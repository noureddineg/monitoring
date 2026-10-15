#!/usr/bin/env python3
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        payload = json.loads(self.rfile.read(length) or b"{}")
        print("="*64)
        print(f"POST {self.path} status={payload.get('status')} receiver={payload.get('receiver')}")
        for a in payload.get("alerts", []):
            lb, an = a["labels"], a["annotations"]
            print(f" [{a['status']:8}] {lb.get('alertname')} severity={lb.get('severity')} instance={lb.get('instance')}")
            print(f"      {an.get('summary')}")
        self.send_response(200)
        self.end_headers()
    def log_message(self, *args):
        pass

if __name__ == "__main__":
    print("Webhook listener on http://0.0.0.0:5001 ...")
    HTTPServer(("0.0.0.0", 5001), Handler).serve_forever()