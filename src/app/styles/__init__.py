"""Neumorphic theming and stylesheet utilities.

Quick-start for library consumers::

    from styles import theme_manager, qss

    # Apply the neumorphic theme to a QApplication
    theme_manager.apply(app)

    # Use ready-made QSS snippets on any widget
    my_label.setStyleSheet(qss.transparent_label("text_muted", 14, 600))
    my_frame.setStyleSheet(qss.card_frame(16))
    my_calendar.setStyleSheet(qss.calendar_qss())

    # Switch between light / dark
    theme_manager.toggle()

    # Change accent colour
    theme_manager.set_accent("#1976D2")
    theme_manager.apply()

The :mod:`styles.snippets` module (aliased here as ``qss``) provides
palette-aware QSS factory functions so you never hard-code colour
values.  The :pyclass:`ThemeManager` singleton keeps palettes,
shadow configs, and the master QSS in sync.
"""

from __future__ import annotations

from styles.theme_manager import (
    ThemeManager,
    theme_manager,
    ACCENT_PURPLE,
    ACCENT_BLUE,
    ACCENT_TEAL,
    ACCENT_CORAL,
    ACCENT_PINK,
)

# Alias the snippets module for a shorter import path:
#   from styles import qss
#   lbl.setStyleSheet(qss.transparent_label("accent"))
from styles import snippets as qss  # noqa: F401

__all__ = [
    "ThemeManager",
    "theme_manager",
    "qss",
    "ACCENT_PURPLE",
    "ACCENT_BLUE",
    "ACCENT_TEAL",
    "ACCENT_CORAL",
    "ACCENT_PINK",
]
