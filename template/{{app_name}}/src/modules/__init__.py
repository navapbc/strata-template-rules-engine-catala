"""Auto-discovery of Catala module routers.

Any Python file in this package that defines a `router` attribute
(a FastAPI APIRouter) will be automatically discovered and included
in the main application.
"""

import importlib
import logging
import os
import pkgutil
from typing import Generator

from fastapi import APIRouter

logger = logging.getLogger(__name__)


def _disabled_modules() -> set[str]:
    """Parse the DISABLED_MODULES env var into a set of module names."""
    raw = os.getenv("DISABLED_MODULES", "")
    return {name.strip() for name in raw.split(",") if name.strip()}


def discover_routers() -> Generator[APIRouter, None, None]:
    """Yield all APIRouter instances found in submodules of this package.

    Set the DISABLED_MODULES environment variable to a comma-separated list
    of module names to exclude (e.g. DISABLED_MODULES=paidleave).
    """
    disabled = _disabled_modules()
    for module_info in sorted(pkgutil.iter_modules(__path__, prefix=__name__ + "."),
                              key=lambda m: m.name):
        short_name = module_info.name.rsplit(".", 1)[-1]
        if short_name in disabled:
            logger.info("Module '%s' is disabled via DISABLED_MODULES", short_name)
            continue
        module = importlib.import_module(module_info.name)
        router = getattr(module, "router", None)
        if isinstance(router, APIRouter):
            logger.info("Loaded module '%s'", short_name)
            yield router
        else:
            logger.warning(
                "Module '%s' does not export a 'router' APIRouter — skipping", short_name
            )
