"""Neumorphic button with a Material-style ripple ink effect.

On each click, an expanding translucent circle grows from the click point
and fades out, mimicking the Material Design ink ripple but styled to match
the neumorphic palette.
"""

from __future__ import annotations

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QPointF, QVariantAnimation
from PySide6.QtWidgets import QPushButton

from styles.theme_manager import theme_manager


class RippleButton(QPushButton):
    """QPushButton subclass that shows a ripple animation on click.

    Drop-in replacement for ``QPushButton``::

        btn = RippleButton("Click me")
        btn.setProperty("accentButton", True)  # optional accent styling
    """

    def __init__(self, text: str = "", parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(text, parent)
        self._ripple_pos = QPointF(0, 0)
        self._ripple_progress: float = 0.0

        self._anim = QVariantAnimation(self)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.setDuration(420)
        self._anim.setEasingCurve(QtCore.QEasingCurve.Type.OutQuad)
        self._anim.valueChanged.connect(self._on_anim_value)
        self._anim.finished.connect(self._on_anim_done)

    # ------------------------------------------------------------------
    # Mouse press – start ripple from click position
    # ------------------------------------------------------------------

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mousePressEvent(event)
        self._ripple_pos = QPointF(event.position())
        self._ripple_progress = 0.0
        self._anim.stop()
        self._anim.start()

    # ------------------------------------------------------------------
    # Animation callbacks
    # ------------------------------------------------------------------

    def _on_anim_value(self, value: object) -> None:
        self._ripple_progress = float(value)  # type: ignore[arg-type]
        self.update()

    def _on_anim_done(self) -> None:
        self._ripple_progress = 0.0
        self.update()

    # ------------------------------------------------------------------
    # Paint  – super draws the button, we overdraw the ripple circle
    # ------------------------------------------------------------------

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        super().paintEvent(event)

        t = self._ripple_progress
        if t <= 0.0:
            return

        p = theme_manager.palette
        accent = QtGui.QColor(p["accent"])

        # Radius: grow from 0 to diagonal of the button
        diagonal = (self.width() ** 2 + self.height() ** 2) ** 0.5
        radius = t * diagonal * 0.6

        # Alpha: fade out from ~80 → 0
        alpha = int(max(0, 80 * (1.0 - t)))
        accent.setAlpha(alpha)

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setClipRect(self.rect())

        # Clip to the button's rounded rectangle (matches QSS border-radius: 12px)
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(self.rect()), 12, 12)
        painter.setClipPath(path)

        painter.setBrush(accent)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawEllipse(self._ripple_pos, radius, radius)
        painter.end()
