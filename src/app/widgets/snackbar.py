"""Neumorphic Snackbar / Toast notification widget.

A lightweight overlay that slides in from the bottom of its parent window,
displays a message for a configurable duration, then slides back out.

Usage::

    from widgets.snackbar import Snackbar

    # Plain toast
    Snackbar.show(main_window, "File saved successfully")

    # With action button
    Snackbar.show(main_window, "Item deleted", action_label="Undo",
                  on_action=lambda: restore_item())

    # With explicit duration (ms) and type
    Snackbar.show(main_window, "Network error", duration=5000,
                  snack_type="error")
"""

from __future__ import annotations

from typing import Callable

import qtawesome as qta
from PySide6 import QtCore, QtWidgets, QtGui

from styles.theme_manager import theme_manager

# Available snack types → (icon, color-role)
_SNACK_TYPES: dict[str, tuple[str, str]] = {
    "info":    ("mdi6.information-outline",    "#1976D2"),
    "success": ("mdi6.check-circle-outline",   "#388E3C"),
    "warning": ("mdi6.alert-outline",          "#F57C00"),
    "error":   ("mdi6.close-circle-outline",   "#D32F2F"),
    "default": ("mdi6.bell-outline",           ""),
}


class Snackbar(QtWidgets.QFrame):
    """Overlay toast notification attached to a parent window.

    Never construct directly — use the :meth:`show` class method.
    """

    _active: Snackbar | None = None  # at most one at a time per process

    def __init__(self, parent: QtWidgets.QWidget, message: str,
                 duration: int = 3000, action_label: str | None = None,
                 on_action: Callable | None = None,
                 snack_type: str = "default") -> None:
        super().__init__(parent)
        self.setObjectName("snackbar")
        self._duration = duration
        self._action_cb = on_action

        # ── visuals ────────────────────────────────────────────────────────
        p = theme_manager.palette
        icon_name, type_color = _SNACK_TYPES.get(snack_type, _SNACK_TYPES["default"])
        accent = type_color or p["accent"]

        # semi-dark background regardless of theme for contrast
        bg = p["bg_secondary"]
        self.setStyleSheet(f"""
            QFrame#snackbar {{
                background: {bg};
                border-radius: 14px;
                border: 1px solid {accent};
            }}
            QLabel#snackbar_msg {{
                color: {p['text']};
                font-size: 13px;
                background: transparent;
            }}
            QPushButton#snackbar_action {{
                background: transparent;
                color: {accent};
                border: none;
                font-weight: 700;
                font-size: 13px;
                padding: 4px 8px;
            }}
            QPushButton#snackbar_action:hover {{
                color: {p['text_heading']};
            }}
            QPushButton#snackbar_close {{
                background: transparent;
                border: none;
                color: {p['text_muted']};
                font-size: 16px;
                padding: 4px;
            }}
            QPushButton#snackbar_close:hover {{
                color: {p['text']};
            }}
        """)

        row = QtWidgets.QHBoxLayout(self)
        row.setContentsMargins(16, 12, 12, 12)
        row.setSpacing(10)

        # type icon
        icon_lbl = QtWidgets.QLabel()
        icon_lbl.setPixmap(qta.icon(icon_name, color=accent).pixmap(20, 20))
        row.addWidget(icon_lbl)

        # message
        msg_lbl = QtWidgets.QLabel(message)
        msg_lbl.setObjectName("snackbar_msg")
        msg_lbl.setWordWrap(True)
        row.addWidget(msg_lbl, stretch=1)

        # optional action button
        if action_label:
            action_btn = QtWidgets.QPushButton(action_label)
            action_btn.setObjectName("snackbar_action")
            action_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            action_btn.clicked.connect(self._on_action)
            row.addWidget(action_btn)

        # close button
        close_btn = QtWidgets.QPushButton()
        close_btn.setObjectName("snackbar_close")
        close_btn.setFixedSize(24, 24)
        close_btn.setIcon(qta.icon("mdi6.close", color=p["text_muted"]))
        close_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self._slide_out)
        row.addWidget(close_btn)

        # ── geometry & shadow ──────────────────────────────────────────────
        self.setFixedWidth(min(480, parent.width() - 48))
        self.adjustSize()

        # ── animations ────────────────────────────────────────────────────
        self._slide_anim = QtCore.QPropertyAnimation(self, b"pos")
        self._slide_anim.setDuration(280)
        self._slide_anim.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)

        self._dismiss_timer = QtCore.QTimer(self)
        self._dismiss_timer.setSingleShot(True)
        self._dismiss_timer.timeout.connect(self._slide_out)

    # ── public factory ────────────────────────────────────────────────────
    @classmethod
    def show(cls, parent: QtWidgets.QWidget, message: str,
             duration: int = 3000, action_label: str | None = None,
             on_action: Callable | None = None,
             snack_type: str = "default") -> "Snackbar":
        """Create and show a toast notification anchored to *parent*.

        :param parent:       The window to overlay the toast on.
        :param message:      Short message text (wraps if needed).
        :param duration:     Auto-dismiss delay in milliseconds (default 3 s).
        :param action_label: Optional action button label.
        :param on_action:    Callable invoked when the action button is clicked.
        :param snack_type:   One of ``"default"``, ``"info"``, ``"success"``,
                             ``"warning"``, ``"error"``.
        """
        # dismiss any existing snackbar on the same parent
        if cls._active is not None:
            try:
                cls._active._dismiss_timer.stop()
                cls._active.deleteLater()
            except RuntimeError:
                pass
            cls._active = None

        snackbar = cls(parent, message, duration, action_label, on_action, snack_type)
        cls._active = snackbar
        snackbar._slide_in()
        return snackbar

    # ── internal ──────────────────────────────────────────────────────────
    def _slide_in(self) -> None:
        self.adjustSize()
        parent = self.parent()
        pw, ph = parent.width(), parent.height()
        sw = self.width()
        sh = self.sizeHint().height()
        self.setFixedHeight(sh)

        margin = 24
        x = (pw - sw) // 2
        y_target = ph - sh - margin
        y_start = ph + sh  # off-screen below

        self.move(x, y_start)
        self.raise_()
        self.setVisible(True)

        self._slide_anim.setStartValue(QtCore.QPoint(x, y_start))
        self._slide_anim.setEndValue(QtCore.QPoint(x, y_target))
        self._slide_anim.start()

        if self._duration > 0:
            self._dismiss_timer.start(self._duration)

    def _slide_out(self) -> None:
        self._dismiss_timer.stop()
        parent = self.parent()
        ph = parent.height()
        sh = self.height()
        x = self.x()

        self._slide_anim.stop()
        self._slide_anim.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self._slide_anim.setStartValue(self.pos())
        self._slide_anim.setEndValue(QtCore.QPoint(x, ph + sh))
        self._slide_anim.start()
        self._slide_anim.finished.connect(self.deleteLater)
        if Snackbar._active is self:
            Snackbar._active = None

    def _on_action(self) -> None:
        if self._action_cb:
            self._action_cb()
        self._slide_out()

    def resizeEvent(self, event) -> None:
        """Keep centred when parent resizes."""
        super().resizeEvent(event)
