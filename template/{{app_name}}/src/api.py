"""FastAPI wrapper for Catala-generated rules engine."""

from fastapi import FastAPI

# Modules are auto-discovered from src/modules/ — see README § "Module system".
from src.modules import discover_routers

app = FastAPI(
    title="Rules Engine API",
    description="API for evaluating rules compiled from Catala legislative specifications.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


for _router in discover_routers():
    app.include_router(_router)
