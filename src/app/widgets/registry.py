"""Widget demo registry for the showcase application."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget


@dataclass
class WidgetDemo:
    """Describes a single widget demo entry in the showcase."""

    id: str
    name: str
    create_page: Callable[[], QWidget]
    create_about: Callable[[], QWidget] | None = None
    description: str = ""


class WidgetRegistry:
    """Central registry that collects all demos for the showcase."""

    def __init__(self) -> None:
        self._demos: dict[str, WidgetDemo] = {}
        self._order: list[str] = []

    def register(self, demo: WidgetDemo) -> None:
        if demo.id not in self._demos:
            self._order.append(demo.id)
        self._demos[demo.id] = demo

    def all(self) -> list[WidgetDemo]:
        return [self._demos[k] for k in self._order]

    def get(self, demo_id: str) -> WidgetDemo | None:
        return self._demos.get(demo_id)


registry = WidgetRegistry()
