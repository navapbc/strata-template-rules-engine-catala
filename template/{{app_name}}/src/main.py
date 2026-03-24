"""Entrypoint for running the rules engine API server."""

import os

import uvicorn

from src.telemetry import configure_telemetry


def main() -> None:
    configure_telemetry()

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))

    uvicorn.run("src.api:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()
