from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Wiki"])


@router.get("/", response_class=HTMLResponse)
def get_wiki():
    return """
    <html>
        <head><title>Internal Wiki</title></head>
        <body style="font-family: Arial, sans-serif; margin: 40px;">
            <h1>Internal Organizational Wiki</h1>
            <p>Welcome to the internal documentation portal (HTTP Baseline).</p>
            <hr>
            <p><em>Security Notice: This page is currently served over plain unencrypted HTTP.</em></p>
        </body>
    </html>
    """