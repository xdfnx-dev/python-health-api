"""Small production-style HTTP API with health and Prometheus endpoints."""
import json
import os
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

STARTED_AT = time.time()
APP_NAME = os.getenv("APP_NAME", "python-health-api")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")


def payload(status, **data):
    return json.dumps({"status": status, **data}).encode()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.respond(200, payload("ok", service=APP_NAME, version=APP_VERSION))
        elif self.path == "/ready":
            self.respond(200, payload("ready"))
        elif self.path == "/version":
            self.respond(200, payload("ok", service=APP_NAME, version=APP_VERSION))
        elif self.path == "/metrics":
            uptime = time.time() - STARTED_AT
            body = f"# HELP app_uptime_seconds Process uptime.\n# TYPE app_uptime_seconds gauge\napp_uptime_seconds {uptime:.2f}\n"
            self.respond(200, body.encode(), "text/plain; version=0.0.4")
        else:
            self.respond(404, payload("error", message="not found"))

    def respond(self, status, body, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} - {fmt % args}", flush=True)


def main():
    port = int(os.getenv("PORT", "8000"))
    server = ThreadingHTTPServer((os.getenv("HOST", "0.0.0.0"), port), Handler)
    print(f"{APP_NAME} listening on :{port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
