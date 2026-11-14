
#!/usr/bin/env python3
"""
ITIS 3200 - Group 4
Member 3: Fake HTTPS Wiki

Controlled HTTPS impersonation demonstration.
Uses a self-signed certificate not issued by
the project's legitimate internal Root CA.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import ssl

HOST = "127.0.0.1"
PORT = 9443

BASE_DIR = Path(__file__).resolve().parent
CERT_FILE = BASE_DIR / "certs" / "t4-self-signed-rejection-ca" / "fake-wiki.crt"
KEY_FILE = BASE_DIR / "certs" / "t4-self-signed-rejection-ca" / "fake-wiki.key"


class FakeHTTPSWikiHandler(BaseHTTPRequestHandler):
    """Serves the simulated impersonating wiki."""

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
            <p>Internal documentation and resources.</p>
            <hr>
            <p>LAB SIMULATION: FAKE HTTPS WIKI</p>
            <p>This server uses an untrusted self-signed certificate.</p>
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
    server = ThreadingHTTPServer((HOST, PORT), FakeHTTPSWikiHandler)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(
        certfile=str(CERT_FILE),
        keyfile=str(KEY_FILE)
    )

    server.socket = context.wrap_socket(
        server.socket,
        server_side=True
    )

    print("=" * 50, flush=True)
    print("GROUP 4 - FAKE HTTPS WIKI", flush=True)
    print(f"Server: https://{HOST}:{PORT}/", flush=True)
    print("Certificate: Self-signed (untrusted)", flush=True)
    print("Press Ctrl+C to stop.", flush=True)
    print("=" * 50, flush=True)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nFake HTTPS wiki stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
