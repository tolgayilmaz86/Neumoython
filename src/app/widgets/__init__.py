"""Reusable PySide6 neumorphic widget library.

All public widgets are re-exported from this package::

    from widgets import ToggleSwitch, CollapsibleSection
    from widgets import BoxShadow, BoxShadowWrapper
    from widgets import roundProgressBar
    from widgets import Snackbar, RippleButton
"""

from __future__ import annotations

__version__ = "0.1.0"

from widgets.box_shadow import BoxShadow, BoxShadowWrapper
from widgets.toggle_switch import ToggleSwitch
from widgets.collapsible_section import CollapsibleSection
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
    "roundProgressBar",
    "spiralProgressBar",
    "NeuProgressBar",
    "NeuProgressBarOutset",
    "NeuProgressBarDeepInset",
    "Snackbar",
    "RippleButton",
    "AnimatedCard",
]
