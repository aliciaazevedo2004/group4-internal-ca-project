import os
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Wiki"])


@router.get("/", response_class=HTMLResponse)
def get_wiki():
    mode = os.getenv("SERVICE_MODE", "http")
    label = "HTTP Baseline" if mode == "http" else "HTTPS"
    notice = ("This page is currently served over plain unencrypted HTTP."
              if mode == "http" else "This page is served over HTTPS.")
    return f"""
    <html>
        <head><title>Internal Wiki</title></head>
        <body style="font-family: Arial, sans-serif; margin: 40px;">
            <h1>Internal Organizational Wiki</h1>
            <p>Welcome to the internal documentation portal ({label}).</p>
            <hr>
            <p><em>Security Notice: {notice}</em></p>
        </body>
    </html>
    """
