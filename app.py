import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import redis

MESSAGE = os.getenv("MESSAGE", "Hello, def!")
PORT=int(os.getenv("PORT", 8080))
REDIS_HOST = os.getenv("REDIS_HOST", "redis")

r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            try:
                r.ping()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"OK: app and redis healthy")
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"ERROR: redis unhealthy: {e}".encode())
            return
        if self.path == "/crash":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Crashing now")
            os._exit(1)
        count=r.incr("counter2")
        self.send_response(200)
        self.end_headers()
        response=f"Message is: {MESSAGE}. This page has been visited {count} times."
        self.wfile.write(response.encode())

server= HTTPServer(("0.0.0.0", PORT), Handler)
print(f"Listening on port {PORT}...")
server.serve_forever()
