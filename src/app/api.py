"""FastAPI application entry point."""

from fastapi import FastAPI

app = FastAPI(title="Agent Learning Project")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

