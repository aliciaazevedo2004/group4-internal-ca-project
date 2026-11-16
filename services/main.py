
import argparse
import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from services.api import api
from services.wiki import wiki


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Default host for local testing
HOST = os.getenv("BIND_HOST", "127.0.0.1")


# Service configurations
SERVICES = {
    "wiki": {
        "router": wiki.router,
        "title": "Internal Wiki",
        "http_port": 8080,
        "https_port": 8443,
        "cert": PROJECT_ROOT / "ca" / "wiki" / "wiki.crt",
        "key": PROJECT_ROOT / "ca" / "wiki" / "wiki.key",
    },
    "api": {
        "router": api.router,
        "title": "Internal API",
        "http_port": 8082,
        "https_port": 8444,
        "cert": PROJECT_ROOT / "ca" / "api" / "api.crt",
        "key": PROJECT_ROOT / "ca" / "api" / "api.key",
    },
}


def build_app(name):
    cfg = SERVICES[name]

    app = FastAPI(
        title=cfg["title"],
        version="1.0"
    )

    app.include_router(cfg["router"])

    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Start the internal wiki or API using HTTP or HTTPS."
    )

    parser.add_argument(
        "service",
        choices=SERVICES.keys(),
        help="Service to start: wiki or api"
    )

    parser.add_argument(
        "--mode",
        choices=["http", "https"],
        default="http",
        help="Connection mode (default: http)"
    )

    args = parser.parse_args()

    os.environ["SERVICE_MODE"] = args.mode

    cfg = SERVICES[args.service]

    if args.mode == "https":
        cert_file = cfg["cert"]
        key_file = cfg["key"]

        # Verify that the required certificate and key exist
        if not cert_file.is_file():
            parser.error(f"Certificate not found: {cert_file}")

        if not key_file.is_file():
            parser.error(f"Private key not found: {key_file}")

        uvicorn.run(
            build_app(args.service),
            host=HOST,
            port=cfg["https_port"],
            ssl_certfile=str(cert_file),
            ssl_keyfile=str(key_file)
        )

    else:
        uvicorn.run(
            build_app(args.service),
            host=HOST,
            port=cfg["http_port"]
        )
