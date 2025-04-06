#!/usr/bin/env python3
import os
import json
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from ycmladapter import YandexCloudClineAdapter

# Инициализируем адаптер YandexCloud
adapter = YandexCloudClineAdapter(async_mode=False)

class ClineRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, content_type='application/json'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()
        self.wfile.write(b'')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        print(f"Received request: {post_data[:100]}...")
        
        try:
            # Обрабатываем запрос через адаптер YandexCloud
            response = adapter.cline_handler(post_data)
            
            self._set_headers()
            self.wfile.write(response.encode('utf-8'))
            
        except Exception as e:
            error_response = json.dumps({
                'status': 'error',
                'message': str(e)
            })
            self._set_headers()
            self.wfile.write(error_response.encode('utf-8'))
            print(f"Error processing request: {str(e)}")

def run_server(host='localhost', port=3000):
    server_address = (host, port)
    httpd = HTTPServer(server_address, ClineRequestHandler)
    print(f'Starting Cline server on http://{host}:{port}')
    print(f'Using YandexCloud ML with folder ID: {os.environ.get("YC_FOLDER_ID")}')
    httpd.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cline server for YandexCloud ML')
    parser.add_argument('--host', default='localhost', help='Host to bind server to')
    parser.add_argument('--port', type=int, default=3000, help='Port to bind server to')
    
    args = parser.parse_args()
    run_server(host=args.host, port=args.port)