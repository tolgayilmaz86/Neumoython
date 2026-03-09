"""Neumorphic toggle switch – standalone reusable widget.

Can be imported independently of the catalog demo system::

    from widgets.toggle_switch import ToggleSwitch
"""

from __future__ import annotations

from PySide6 import QtCore, QtWidgets

from styles.theme_manager import theme_manager


class ToggleSwitch(QtWidgets.QWidget):
    """Neumorphic toggle switch – a sliding on/off control.

    Usage::

        switch = ToggleSwitch(checked=False, label="Enable feature")
        switch.toggled.connect(lambda on: print("State:", on))
    """

    toggled = QtCore.Signal(bool)

    def __init__(self, checked: bool = False, label: str = "",
                 parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self._checked = checked
        self._label = label
        self._anim_pos = 1.0 if checked else 0.0
        self._track_w = 48
        self._track_h = 26
        self._thumb_r = 10
        self.setFixedHeight(30)
        self.setMinimumWidth(self._track_w + 8)
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.TabFocus)

        self._animation = QtCore.QPropertyAnimation(self, b"handlePosition")
        self._animation.setDuration(150)

    # -- Qt property for animation -------------------------------------------
    def _get_handle_pos(self) -> float:
        return self._anim_pos

    def _set_handle_pos(self, v: float) -> None:
        self._anim_pos = v
        self.update()

    handlePosition = QtCore.Property(float, _get_handle_pos, _set_handle_pos)

    # -- public API ----------------------------------------------------------
    def isChecked(self) -> bool:
        return self._checked

    def setChecked(self, v: bool) -> None:
        if v == self._checked:
            return
        self._checked = v
        self._animate(v)
        self.toggled.emit(v)

    def setEnabled(self, enabled: bool) -> None:
        super().setEnabled(enabled)
        self.update()

    # -- events --------------------------------------------------------------
    def mousePressEvent(self, event) -> None:
        self.setChecked(not self._checked)

    def keyPressEvent(self, event) -> None:
        """Toggle on Space or Return for keyboard accessibility."""
        if event.key() in (QtCore.Qt.Key.Key_Space, QtCore.Qt.Key.Key_Return):
            self.setChecked(not self._checked)
        else:
            super().keyPressEvent(event)

    def focusInEvent(self, event) -> None:
        self.update()
        super().focusInEvent(event)

    def focusOutEvent(self, event) -> None:
        self.update()
        super().focusOutEvent(event)

    def sizeHint(self) -> QtCore.QSize:
        w = self._track_w + 8
        if self._label:
            fm = self.fontMetrics()
            w += fm.horizontalAdvance(self._label) + 10
        return QtCore.QSize(w, 30)

    def paintEvent(self, event) -> None:
        from PySide6.QtGui import QPainter, QColor

        p = theme_manager.palette
        ptr = QPainter(self)
        ptr.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Focus ring
        if self.hasFocus():
            ptr.setPen(QtCore.Qt.PenStyle.NoPen)
            ring_color = QColor(p["accent"])
            ring_color.setAlpha(80)
            ptr.setBrush(ring_color)
            ptr.drawRoundedRect(
                QtCore.QRectF(1, (self.height() - self._track_h) // 2 - 3,
                              self._track_w + 6, self._track_h + 6),
                (self._track_h + 6) / 2, (self._track_h + 6) / 2,
            )

        # Track
        track_x = 4
        track_y = (self.height() - self._track_h) // 2
        track_rect = QtCore.QRectF(track_x, track_y, self._track_w, self._track_h)

        if not self.isEnabled():
            track_color = QColor(p["text_muted"])
            track_color.setAlpha(60)
        elif self._checked:
            track_color = QColor(p["accent"])
        else:
            track_color = QColor(p["bg_secondary"])

        ptr.setPen(QtCore.Qt.PenStyle.NoPen)
        ptr.setBrush(track_color)
        ptr.drawRoundedRect(track_rect, self._track_h / 2, self._track_h / 2)

        # Thumb
        margin = (self._track_h - self._thumb_r * 2) / 2
        min_x = track_x + margin + self._thumb_r
        max_x = track_x + self._track_w - margin - self._thumb_r
        cx = min_x + (max_x - min_x) * self._anim_pos
        cy = track_y + self._track_h / 2

        if not self.isEnabled():
            thumb_color = QColor(p["text_muted"])
        else:
            thumb_color = QColor("#FFFFFF")

        ptr.setBrush(thumb_color)
        ptr.drawEllipse(QtCore.QPointF(cx, cy), self._thumb_r, self._thumb_r)

        # Label
        if self._label:
            ptr.setPen(QColor(p["text"]) if self.isEnabled() else QColor(p["text_muted"]))
            label_x = track_x + self._track_w + 10
            ptr.drawText(QtCore.QRectF(label_x, 0, self.width() - label_x, self.height()),
                         QtCore.Qt.AlignmentFlag.AlignVCenter, self._label)

        ptr.end()

    def _animate(self, to_checked: bool) -> None:
        self._animation.stop()
        self._animation.setStartValue(self._anim_pos)
        self._animation.setEndValue(1.0 if to_checked else 0.0)
        self._animation.start()
