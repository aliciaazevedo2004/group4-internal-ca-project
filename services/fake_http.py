# services/fake_http.py
# LAB SIMULATION: Diya - Fake HTTP endpoint demonstrating identity ambiguity
from http.server import HTTPServer, BaseHTTPRequestHandler

class FakeWikiHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        html = (
            "<html><body>"
            "<h1>Internal Company Wiki</h1>"
            "<p>Simulated baseline endpoint for security testing.</p>"
            "<!-- LAB SIMULATION: Impersonated HTTP service -->"
            "</body></html>"
        )
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    print("[LAB SIMULATION] Fake HTTP wiki running on port 8081...")
    HTTPServer(("0.0.0.0", 8081), FakeWikiHandler).serve_forever()
