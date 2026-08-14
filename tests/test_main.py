import json
import unittest
from unittest.mock import patch
from app.main import Handler


class FakeRequest:
    def __init__(self, path):
        self.path = path
        self.wfile = self
        self.response = b""

    def send_response(self, code): self.code = code
    def send_header(self, *_): pass
    def end_headers(self): pass
    def write(self, body): self.response += body


class HandlerTests(unittest.TestCase):
    def request(self, path):
        request = FakeRequest(path)
        with patch.object(Handler, "__init__", lambda self, *a, **kw: None):
            handler = Handler()
        handler.path, handler.wfile = path, request
        handler.send_response, handler.send_header, handler.end_headers = request.send_response, request.send_header, request.end_headers
        handler.do_GET()
        return request

    def test_health(self):
        response = self.request("/health")
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.response)["status"], "ok")

    def test_unknown_route(self):
        self.assertEqual(self.request("/missing").code, 404)


if __name__ == "__main__": unittest.main()
