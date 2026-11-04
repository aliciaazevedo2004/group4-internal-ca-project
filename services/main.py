import sys

import uvicorn
from fastapi import FastAPI

from services.api import api
from services.wiki import wiki

wiki_app = FastAPI(title="Internal Wiki", version="1.0")
wiki_app.include_router(wiki.router)

api_app = FastAPI(title="Internal API", version="1.0")
api_app.include_router(api.router)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "wiki"
    if target == "wiki":
        uvicorn.run(wiki_app, host="127.0.0.1", port=8080)
    elif target == "api":
        uvicorn.run(api_app, host="127.0.0.1", port=8081)
    else:
        sys.exit("Usage: python -m services.main [wiki|api]")
