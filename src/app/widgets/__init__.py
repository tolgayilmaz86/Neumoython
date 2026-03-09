"""Reusable PySide6 neumorphic widget library.

Quick-start
-----------
Import widgets directly from this package::

    from widgets import ToggleSwitch, CollapsibleSection
    from widgets import BoxShadow, BoxShadowWrapper
    from widgets import roundProgressBar
    from widgets import Snackbar, RippleButton

Theming & QSS helpers live in the :mod:`styles` package::

    from styles import theme_manager, qss

    theme_manager.set_theme("dark")
    theme_manager.apply()

    my_label.setStyleSheet(qss.transparent_label("text_muted", 14, 600))
    my_cal.setStyleSheet(qss.calendar_qss())
"""

from __future__ import annotations

__version__ = "0.1.0"

from widgets.box_shadow import BoxShadow, BoxShadowWrapper
from widgets.toggle_switch import ToggleSwitch
from widgets.collapsible_section import CollapsibleSection
from widgets.popup_datetime_field import PopupDateTimeField
from widgets.progress_widgets import (
    roundProgressBar,
    spiralProgressBar,
    NeuProgressBar,
    NeuProgressBarOutset,
    NeuProgressBarDeepInset,
)

# Lazy imports for widgets that need a QApplication to be constructed;
# import them directly when needed:
#   from widgets.snackbar import Snackbar
#   from widgets.ripple_button import RippleButton
#   from widgets.animated_card import AnimatedCard

__all__ = [
    "__version__",
    "BoxShadow",
    "BoxShadowWrapper",
    "ToggleSwitch",
    "CollapsibleSection",
    "PopupDateTimeField",
    "roundProgressBar",
    "spiralProgressBar",
    "NeuProgressBar",
    "NeuProgressBarOutset",
    "NeuProgressBarDeepInset",
    "Snackbar",
    "RippleButton",
    "AnimatedCard",
]
