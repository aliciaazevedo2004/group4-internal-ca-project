from app.routers import api, wiki
from fastapi import FastAPI

app = FastAPI(title="Internal Network Services", version="1.0")

# Include your wiki and API routers
app.include_router(wiki.router)
app.include_router(api.router)

if __name__ == "__main__":
    import uvicorn

    # Runs the application on port 8080 (or adjust as needed for your ports)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8080, reload=True)