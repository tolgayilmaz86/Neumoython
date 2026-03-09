"""Neumorphic card widget with hover-elevation animation.

The card animates between a *resting* (outside_raised) neumorphic shadow and
a *hovered* (deeper outside_raised) shadow by tweening a custom ``elevation``
property via QPropertyAnimation.  Shadow colours are derived from the active
ThemeManager palette so they update correctly on theme / accent changes.
"""

from __future__ import annotations

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Property, QPropertyAnimation, QSize
from PySide6.QtWidgets import QFrame, QVBoxLayout

from styles.theme_manager import theme_manager
from widgets.box_shadow import BoxShadow


def _lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def _make_shadows(t: float, dark_theme: bool) -> list[dict]:
    """Return shadow-list interpolated at elevation *t* (0.0 resting → 1.0 hovered)."""
    if dark_theme:
        dark_alpha  = _lerp(136, 185, t)
        light_alpha = _lerp(34,  55,  t)
    else:
        dark_alpha  = _lerp(51,  80,  t)
        light_alpha = _lerp(204, 235, t)
    offset = _lerp(5, 9, t)
    blur   = _lerp(10, 20, t)
    return [
        {"outside": True, "offset": [offset, offset],   "blur": blur,
         "color": QtGui.QColor(0, 0, 0, dark_alpha)},
        {"outside": True, "offset": [-offset, -offset], "blur": blur,
         "color": QtGui.QColor(255, 255, 255, light_alpha)},
    ]


class AnimatedCard(QtWidgets.QWidget):
    """Neumorphic card that smoothly elevates on hover.

    The outer widget provides shadow-margin space; children should be placed
    inside the ``content`` attribute::

        card = AnimatedCard()
        card.setMinimumSize(220, 150)
        vbox = QVBoxLayout(card.content)
        vbox.addWidget(some_label)
    """

    # Shadow margin in pixels (must be ≥ max blur+offset)
    _MARGIN = 14

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_Hover, True)

        # Inner QFrame — the visible card surface
        self.content = QFrame(self)
        self.content.setObjectName("animated_card")
        self.content.setFrameShape(QFrame.Shape.NoFrame)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            self._MARGIN, self._MARGIN, self._MARGIN, self._MARGIN
        )
        layout.addWidget(self.content)

        # BoxShadow effect applied to the inner frame
        self._shadow = BoxShadow(
            _make_shadows(0.0, theme_manager.theme == "dark"), smooth=True
        )
        self.content.setGraphicsEffect(self._shadow)

        self._elevation: float = 0.0

        self._anim = QPropertyAnimation(self, b"elevation", self)
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)

    # ------------------------------------------------------------------
    # elevation Q_PROPERTY  (0.0 resting → 1.0 fully hovered)
    # ------------------------------------------------------------------

    def _get_elevation(self) -> float:
        return self._elevation

    def _set_elevation(self, value: float) -> None:
        self._elevation = max(0.0, min(1.0, value))
        self._shadow.setShadowList(
            _make_shadows(self._elevation, theme_manager.theme == "dark")
        )
        self.content.update()

    elevation = Property(float, _get_elevation, _set_elevation)

    # ------------------------------------------------------------------
    # Hover
    # ------------------------------------------------------------------

    def enterEvent(self, event: QtCore.QEvent) -> None:
        super().enterEvent(event)
        self._anim.stop()
        self._anim.setStartValue(self._elevation)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        super().leaveEvent(event)
        self._anim.stop()
        self._anim.setStartValue(self._elevation)
        self._anim.setEndValue(0.0)
        self._anim.start()

    def sizeHint(self) -> QSize:
        return QSize(240, 160)
