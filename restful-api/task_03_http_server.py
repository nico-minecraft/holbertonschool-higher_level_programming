#!/usr/bin/python3
"""Simple API built with the http.server module."""
import http.server
import json
import socketserver

PORT = 8000


class SimpleAPIHandler(http.server.BaseHTTPRequestHandler):
    """Handle GET requests for a few simple endpoints."""

    def _send(self, status, content_type, body):
        """Send a complete response with the given status, type and body."""
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        """Route GET requests based on the request path."""
        if self.path == "/":
            self._send(200, "text/plain",
                       b"Hello, this is a simple API!")

        elif self.path == "/data":
            data = {"name": "John", "age": 30, "city": "New York"}
            self._send(200, "application/json",
                       json.dumps(data).encode("utf-8"))

        elif self.path == "/status":
            self._send(200, "text/plain", b"OK")

        elif self.path == "/info":
            info = {"version": "1.0",
                    "description": "A simple API built with http.server"}
            self._send(200, "application/json",
                       json.dumps(info).encode("utf-8"))

        else:
            self._send(404, "text/plain", b"Endpoint not found")


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), SimpleAPIHandler) as httpd:
        print("Serving on port {}".format(PORT))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
