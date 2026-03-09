"""Neumorphic collapsible section – standalone reusable widget.

Can be imported independently of the catalog demo system::

    from widgets.collapsible_section import CollapsibleSection
"""

from __future__ import annotations

import qtawesome as qta
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QFrame

from styles.theme_manager import theme_manager


class CollapsibleSection(QFrame):
    """A collapsible section with animated content reveal.

    Usage::

        sec = CollapsibleSection("Settings", "mdi6.cog-outline")
        sec.addContent(my_widget)
        sec.setExpanded(True)
    """

    def __init__(self, title: str = "", icon_name: str = "",
                 parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self._expanded = False

        p = theme_manager.palette
        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        # Header button
        self._toggle_btn = QtWidgets.QPushButton()
        self._toggle_btn.setCheckable(True)
        self._toggle_btn.setFlat(True)
        self._toggle_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self._toggle_btn.setFocusPolicy(QtCore.Qt.FocusPolicy.TabFocus)
        header_text = f"  {title}" if title else ""
        self._toggle_btn.setText(header_text)
        self._toggle_btn.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding: 12px 16px;
                font-weight: 600;
                font-size: 13px;
                color: {p['text_heading']};
                background: {p['card_bg']};
                border: none;
                border-radius: 12px;
            }}
            QPushButton:hover {{
                background: {p['menu_hover']};
            }}
            QPushButton:focus {{
                border: 2px solid {p['accent']};
            }}
        """)

        if icon_name:
            self._toggle_btn.setIcon(
                qta.icon(icon_name, color=p['text']))
            self._toggle_btn.setIconSize(QtCore.QSize(20, 20))

        self._layout.addWidget(self._toggle_btn)

        # Content area
        self._content = QtWidgets.QWidget()
        self._content.setMaximumHeight(0)
        self._content_layout = QtWidgets.QVBoxLayout(self._content)
        self._content_layout.setContentsMargins(16, 8, 16, 12)
        self._layout.addWidget(self._content)

        # Animation
        self._animation = QtCore.QPropertyAnimation(self._content, b"maximumHeight")
        self._animation.setDuration(200)
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuad)

        self._toggle_btn.clicked.connect(self._on_toggle)

    def addContent(self, widget: QtWidgets.QWidget) -> None:
        self._content_layout.addWidget(widget)

    def setExpanded(self, expanded: bool) -> None:
        if expanded != self._expanded:
            self._expanded = expanded
            self._toggle_btn.setChecked(expanded)
            self._animate(expanded)

    def isExpanded(self) -> bool:
        return self._expanded

    def _on_toggle(self) -> None:
        self._expanded = self._toggle_btn.isChecked()
        self._animate(self._expanded)

    def _animate(self, expand: bool) -> None:
        self._animation.stop()
        content_height = self._content_layout.sizeHint().height() + 20
        self._animation.setStartValue(self._content.maximumHeight())
        self._animation.setEndValue(content_height if expand else 0)
        self._animation.start()
