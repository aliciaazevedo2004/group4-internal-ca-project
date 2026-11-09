
#!/usr/bin/env python3
"""
ITIS 3200 - Group 4
Internal Certificate Authority Setup for a Small Network

Member 3: Fake HTTP Wiki
Purpose: Demonstrate HTTP server impersonation in a controlled lab.

This server intentionally uses HTTP without TLS.
It is for authorized local testing only.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "127.0.0.1"
PORT = 8081


class FakeWikiHandler(BaseHTTPRequestHandler):
    """Handles requests to the simulated fake internal wiki."""

    def do_GET(self):
        if self.path != "/":
            self.send_error(404, "Page Not Found")
            return

        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Internal Company Wiki</title>
        </head>
        <body>
            <h1>Internal Company Wiki</h1>
            <h2>Employee Knowledge Base</h2>

            <p>Welcome to the internal company wiki.</p>
            <p>Access internal documentation and resources here.</p>

            <hr>

            <p>LAB SIMULATION: FAKE HTTP WIKI</p>
            <p>This endpoint represents an impersonating server.</p>
        </body>
        </html>
        """

        response = html.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()

        self.wfile.write(response)


def main():
    server = HTTPServer((HOST, PORT), FakeWikiHandler)

    print("=" * 50, flush=True)
    print("GROUP 4 - FAKE HTTP WIKI", flush=True)
    print(f"Server running: http://{HOST}:{PORT}/", flush=True)
    print("Protocol: HTTP (No TLS)", flush=True)
    print("Press Ctrl+C to stop.", flush=True)
    print("=" * 50, flush=True)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
