import argparse
import os

import uvicorn
from fastapi import FastAPI

from services.api import api
from services.wiki import wiki

HOST = os.getenv("BIND_HOST", "127.0.0.1")
CERT_DIR = os.getenv("CERT_DIR", "certificates") 

SERVICES = {
    "wiki": {"router": wiki.router, "title": "Internal Wiki",
             "http_port": 8080, "https_port": 8443,
             "cert": "wiki.crt", "key": "wiki.key"},
    "api": {"router": api.router, "title": "Internal API",
            "http_port": 8082, "https_port": 8444,
            "cert": "api.crt", "key": "api.key"},
}


def build_app(name):
    cfg = SERVICES[name]
    app = FastAPI(title=cfg["title"], version="1.0")
    app.include_router(cfg["router"])
    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("service", choices=SERVICES)
    parser.add_argument("--mode", choices=["http", "https"], default="http")
    args = parser.parse_args()

    os.environ["SERVICE_MODE"] = args.mode
    cfg = SERVICES[args.service]

    if args.mode == "https":
        uvicorn.run(build_app(args.service), host=HOST, port=cfg["https_port"],
                    ssl_certfile=os.path.join(CERT_DIR, cfg["cert"]),
                    ssl_keyfile=os.path.join(CERT_DIR, cfg["key"]))
    else:
        uvicorn.run(build_app(args.service), host=HOST, port=cfg["http_port"])
