"""Auto-discover and register all widget demos in this package."""

from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path


def discover_demos() -> None:
    """Import every non-private module in this package so demos self-register."""
    package_dir = Path(__file__).resolve().parent
    for info in pkgutil.iter_modules([str(package_dir)]):
        if not info.name.startswith("_"):
            importlib.import_module(f"{__package__}.{info.name}")
