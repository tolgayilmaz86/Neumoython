"""Expanders demo – collapsible sections in three neumorphic themes.

Mirrors Neumorphism.Avalonia's ExpandersDemo with:
  • Vertical expanders   (Down / Up)   × 3 themes
  • Horizontal expanders (Right / Left) × 3 themes
  • Customized expander with custom icon
"""

from __future__ import annotations

import qtawesome as qta
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QFrame

from widgets.registry import registry, WidgetDemo
from widgets.box_shadow import BoxShadow, BoxShadowWrapper
from styles.theme_manager import theme_manager
from styles.snippets import (
    transparent_label as _transparent_label_qss,
    expander_default, expander_circle, expander_stroke,
    expander_stroke_horizontal,
)

_LOREM = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
    "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris "
    "nisi ut aliquip ex ea commodo consequat."
)


# ── helpers ──────────────────────────────────────────────────────────────────

def _neu_group(group: QtWidgets.QGroupBox) -> BoxShadowWrapper:
    shadows = theme_manager.shadow_configs()
    return BoxShadowWrapper(
        group, shadow_list=shadows["outside_raised"],
        smooth=True, margins=(12, 12, 12, 12),
    )


def _content_label() -> QtWidgets.QLabel:
    lbl = QtWidgets.QLabel(_LOREM)
    lbl.setWordWrap(True)
    lbl.setStyleSheet(_transparent_label_qss(extra=" padding: 10px;"))
    return lbl


class _VerticalButton(QtWidgets.QPushButton):
    """A QPushButton that paints its text rotated 90° (bottom-to-top).

    Used as the header strip for horizontal expanders.
    """

    def __init__(self, text: str = "", parent=None):
        super().__init__(parent)
        self._vtext = text
        self.setText("")  # prevent default text painting

    def setVerticalText(self, text: str) -> None:
        self._vtext = text
        self.update()

    def sizeHint(self) -> QtCore.QSize:
        fm = self.fontMetrics()
        w = fm.height() + 24  # text height becomes width
        h = fm.horizontalAdvance(self._vtext) + 40  # text width becomes height
        return QtCore.QSize(max(w, 40), max(h, 80))

    def paintEvent(self, event) -> None:
        # let QPushButton draw the background/border
        super().paintEvent(event)
        if not self._vtext:
            return
        painter = QtGui.QPainter(self)
        painter.setPen(self.palette().color(QtGui.QPalette.ColorRole.ButtonText))
        painter.setFont(self.font())
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(-90)
        painter.drawText(
            QtCore.QRectF(
                -self.height() / 2, -self.width() / 2,
                self.height(), self.width(),
            ),
            QtCore.Qt.AlignmentFlag.AlignCenter,
            self._vtext,
        )
        painter.end()


# ── Neumorphic Expander widget ──────────────────────────────────────────────

class _NeuExpander(QFrame):
    """A single collapsible expander with animated content reveal.

    *theme* controls the visual appearance of the toggle header:
        ``"default"``  – raised neumorphic header
        ``"circle"``   – circular toggle button on the left
        ``"stroke"``   – outlined / bordered header

    *direction* controls expansion direction:
        ``"down"`` | ``"up"`` | ``"right"`` | ``"left"``
    """

    def __init__(
        self,
        title: str = "Expand me",
        icon_name: str = "",
        theme: str = "default",
        direction: str = "down",
        enabled: bool = True,
        parent: QtWidgets.QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self._expanded = False
        self._direction = direction
        self._theme = theme

        p = theme_manager.palette
        shadows = theme_manager.shadow_configs()
        is_vertical = direction in ("down", "up")

        # ── outer layout ──
        if is_vertical:
            self._outer = QtWidgets.QVBoxLayout(self)
        else:
            self._outer = QtWidgets.QHBoxLayout(self)
        self._outer.setContentsMargins(0, 0, 0, 0)
        self._outer.setSpacing(0)

        # ── header / toggle button ──
        self._toggle = QtWidgets.QPushButton()
        self._toggle.setCheckable(True)
        self._toggle.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self._toggle.setEnabled(enabled)
        self._toggle.setFocusPolicy(QtCore.Qt.FocusPolicy.TabFocus)

        # icon for header
        if icon_name:
            self._toggle.setIcon(qta.icon(icon_name, color=p["text"]))
            self._toggle.setIconSize(QtCore.QSize(20, 20))

        # chevron icon name depends on direction & state
        self._chev_collapsed = {
            "down": "mdi6.chevron-down",
            "up": "mdi6.chevron-up",
            "right": "mdi6.chevron-right",
            "left": "mdi6.chevron-left",
        }[direction]
        self._chev_expanded = {
            "down": "mdi6.chevron-up",
            "up": "mdi6.chevron-down",
            "right": "mdi6.chevron-left",
            "left": "mdi6.chevron-right",
        }[direction]

        self._apply_theme(title, p, shadows, is_vertical)

        # ── content area ──
        self._content = QtWidgets.QWidget()
        if is_vertical:
            self._content.setMaximumHeight(0)
            self._anim_prop = b"maximumHeight"
        else:
            self._content.setMaximumWidth(0)
            self._anim_prop = b"maximumWidth"

        self._content_layout = QtWidgets.QVBoxLayout(self._content)
        self._content_layout.setContentsMargins(10, 8, 10, 10)

        # order depends on direction
        if direction in ("down", "right"):
            self._outer.addWidget(self._header_widget)
            self._outer.addWidget(self._content)
        else:
            self._outer.addWidget(self._content)
            self._outer.addWidget(self._header_widget)

        # ── animation ──
        self._animation = QtCore.QPropertyAnimation(self._content, self._anim_prop)
        self._animation.setDuration(200)
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuad)

        self._toggle.clicked.connect(self._on_toggle)

    # ── theme styling ──

    def _apply_theme(self, title: str, p: dict, shadows: dict,
                     is_vertical: bool) -> None:
        """Build the header widget according to theme."""
        if self._theme == "circle":
            self._build_circle_header(title, p, shadows, is_vertical)
        elif self._theme == "stroke":
            self._build_stroke_header(title, p, is_vertical)
        else:
            self._build_default_header(title, p, shadows, is_vertical)

    def _build_default_header(self, title: str, p: dict, shadows: dict,
                              is_vertical: bool) -> None:
        """Default neumorphic raised header."""
        obj = "neuExpanderDefault"
        if is_vertical:
            self._toggle.setText(f"  {title}")
            self._toggle.setObjectName(obj)
            self._toggle.setStyleSheet(expander_default(obj))
        else:
            # Horizontal: narrow vertical strip with rotated text
            vbtn = _VerticalButton(title)
            vbtn.setCheckable(True)
            vbtn.setEnabled(self._toggle.isEnabled())
            vbtn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            vbtn.setFocusPolicy(QtCore.Qt.FocusPolicy.TabFocus)
            # Reconnect signals: replace self._toggle
            self._toggle = vbtn
            self._toggle.setObjectName(obj)
            self._toggle.setFixedWidth(40)
            self._toggle.setStyleSheet(expander_default(obj, horizontal=True))
        wrapper = BoxShadowWrapper(
            self._toggle, shadow_list=shadows["button_raised"],
            smooth=True, margins=(4, 4, 4, 4),
        )
        self._header_widget = wrapper

    def _build_circle_header(self, title: str, p: dict, shadows: dict,
                             is_vertical: bool) -> None:
        """Circle theme – small circular toggle + label."""
        container = QFrame()
        container.setObjectName("neuExpanderCircleCont")
        container.setStyleSheet(f"""
            #neuExpanderCircleCont {{
                background: transparent;
                border: none;
            }}
        """)

        # circular button
        self._toggle.setFixedSize(32, 32)
        self._toggle.setText("")
        self._toggle.setObjectName("neuExpanderCircle")
        self._toggle.setIcon(
            qta.icon(self._chev_collapsed, color=p["text"]))
        self._toggle.setIconSize(QtCore.QSize(18, 18))
        self._toggle.setStyleSheet(expander_circle("neuExpanderCircle"))

        circle_wrap = BoxShadowWrapper(
            self._toggle, shadow_list=shadows["button_raised"],
            smooth=True, margins=(4, 4, 4, 4),
        )

        if is_vertical:
            lay = QtWidgets.QHBoxLayout(container)
            lay.setContentsMargins(4, 4, 4, 4)
            lay.setSpacing(8)
            lbl = QtWidgets.QLabel(title)
            lbl.setStyleSheet(
                _transparent_label_qss("text_heading", 13, 600))
            lay.addWidget(circle_wrap)
            lay.addWidget(lbl)
            lay.addStretch()
        else:
            # Vertical column: circle on top, rotated label below
            lay = QtWidgets.QVBoxLayout(container)
            lay.setContentsMargins(4, 8, 4, 8)
            lay.setSpacing(8)
            container.setFixedWidth(48)
            lbl = QtWidgets.QLabel(title)
            lbl.setStyleSheet(
                _transparent_label_qss("text_heading", 12, 600))
            lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            # Use a rotated proxy widget for the label
            proxy_container = QtWidgets.QGraphicsView()
            proxy_container.setFrameShape(QFrame.Shape.NoFrame)
            proxy_container.setStyleSheet("background: transparent; border: none;")
            proxy_container.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            proxy_container.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            scene = QtWidgets.QGraphicsScene()
            proxy = scene.addWidget(lbl)
            proxy.setRotation(-90)
            proxy_container.setScene(scene)
            proxy_container.setFixedWidth(40)
            proxy_container.setMinimumHeight(80)

            lay.addWidget(circle_wrap, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
            lay.addWidget(proxy_container, 1)

        self._header_widget = container

    def _build_stroke_header(self, title: str, p: dict,
                             is_vertical: bool) -> None:
        """Stroke / outlined theme – bordered header."""
        obj = "neuExpanderStroke"
        if is_vertical:
            self._toggle.setText(f"  {title}")
            self._toggle.setObjectName(obj)
            self._toggle.setIcon(
                qta.icon(self._chev_collapsed, color=p["text"]))
            self._toggle.setIconSize(QtCore.QSize(18, 18))
            self._toggle.setStyleSheet(expander_stroke(obj))
            self._header_widget = self._toggle
        else:
            # Narrow vertical strip with rotated text + border
            vbtn = _VerticalButton(title)
            vbtn.setCheckable(True)
            vbtn.setEnabled(self._toggle.isEnabled())
            vbtn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            vbtn.setFocusPolicy(QtCore.Qt.FocusPolicy.TabFocus)
            self._toggle = vbtn
            self._toggle.setObjectName(obj)
            self._toggle.setFixedWidth(40)
            self._toggle.setStyleSheet(expander_stroke_horizontal(obj))
            self._header_widget = self._toggle

    # ── expand / collapse ──

    def addContent(self, widget: QtWidgets.QWidget) -> None:
        self._content_layout.addWidget(widget)

    def setExpanded(self, expanded: bool) -> None:
        if expanded != self._expanded:
            self._expanded = expanded
            self._toggle.setChecked(expanded)
            self._animate(expanded)

    def _on_toggle(self) -> None:
        self._expanded = self._toggle.isChecked()
        self._animate(self._expanded)

    def _animate(self, expand: bool) -> None:
        self._animation.stop()
        is_vertical = self._direction in ("down", "up")
        if is_vertical:
            target = self._content_layout.sizeHint().height() + 20
        else:
            target = self._content_layout.sizeHint().width() + 40
        self._animation.setStartValue(self._content.maximumHeight()
                                       if is_vertical
                                       else self._content.maximumWidth())
        self._animation.setEndValue(target if expand else 0)
        self._animation.start()

        # update chevron icon
        p = theme_manager.palette
        ico = self._chev_expanded if expand else self._chev_collapsed
        if self._theme == "circle":
            self._toggle.setIcon(qta.icon(ico, color=p["text"]))
        elif self._theme == "stroke":
            self._toggle.setIcon(qta.icon(ico, color=p["text"]))


# ── Page builder ─────────────────────────────────────────────────────────────

def create_page() -> QtWidgets.QWidget:
    page = QtWidgets.QWidget()
    scroll = QtWidgets.QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.Shape.NoFrame)

    inner = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(inner)
    layout.setSpacing(16)
    layout.setContentsMargins(24, 24, 24, 24)

    p = theme_manager.palette

    title = QtWidgets.QLabel("Expanders")
    title.setProperty("heading", True)
    f = title.font(); f.setPointSize(20); title.setFont(f)
    layout.addWidget(title)

    desc = QtWidgets.QLabel(
        "Collapsible sections in three neumorphic themes, "
        "with both vertical and horizontal expand directions."
    )
    desc.setWordWrap(True)
    desc.setProperty("subheading", True)
    layout.addWidget(desc)

    # ── Section 1: Vertical expanders ──
    group1 = QtWidgets.QGroupBox("Vertical expanders")
    g1 = QtWidgets.QVBoxLayout(group1)
    g1.setContentsMargins(16, 28, 16, 16)
    g1.setSpacing(12)

    # Row of 3 columns (Default / Circle / Stroke), each with Down + Up
    row1 = QtWidgets.QHBoxLayout()
    row1.setSpacing(16)

    for theme_name, col_title in [
        ("default", "Default"),
        ("circle", "Circle"),
        ("stroke", "Stroke"),
    ]:
        col = QtWidgets.QVBoxLayout()
        col.setSpacing(10)
        col_label = QtWidgets.QLabel(col_title)
        col_label.setStyleSheet(
            _transparent_label_qss("text_muted", 12, 600))
        col.addWidget(col_label)

        # Down expander
        exp_down = _NeuExpander(
            "Expand me", theme=theme_name, direction="down")
        exp_down.addContent(_content_label())
        exp_down.setFixedWidth(260)
        col.addWidget(exp_down)

        # Up expander (with icon for default, rounded for stroke)
        kw: dict = {}
        if theme_name == "default":
            kw["icon_name"] = "mdi6.shield-lock-outline"
        exp_up = _NeuExpander(
            "Expand me", theme=theme_name, direction="up", **kw)
        exp_up.addContent(_content_label())
        exp_up.setFixedWidth(260)
        col.addWidget(exp_up)
        col.addStretch()

        row1.addLayout(col)

    row1.addStretch()
    g1.addLayout(row1)
    layout.addWidget(_neu_group(group1))

    # ── Section 2: Horizontal expanders ──
    group2 = QtWidgets.QGroupBox("Horizontal expanders")
    g2 = QtWidgets.QVBoxLayout(group2)
    g2.setContentsMargins(16, 28, 16, 16)
    g2.setSpacing(12)

    row2 = QtWidgets.QHBoxLayout()
    row2.setSpacing(12)

    for theme_name, direction, enabled, ico in [
        ("default", "right", False, ""),
        ("default", "left", True, "mdi6.shield-lock-outline"),
        ("circle", "right", False, ""),
        ("circle", "left", True, ""),
        ("stroke", "right", True, ""),
        ("stroke", "left", False, ""),
    ]:
        exp = _NeuExpander(
            "Expand me", icon_name=ico, theme=theme_name,
            direction=direction, enabled=enabled,
        )
        exp.addContent(_content_label())
        exp.setFixedHeight(210)
        row2.addWidget(exp)

    row2.addStretch()
    g2.addLayout(row2)
    layout.addWidget(_neu_group(group2))

    # ── Section 3: Customised expander ──
    group3 = QtWidgets.QGroupBox("Customised expanders")
    g3 = QtWidgets.QVBoxLayout(group3)
    g3.setContentsMargins(16, 28, 16, 16)
    g3.setSpacing(12)

    row3 = QtWidgets.QHBoxLayout()
    row3.setSpacing(16)

    # Custom icon expander
    custom1 = _NeuExpander(
        "Open me", icon_name="mdi6.scissors-cutting",
        theme="circle", direction="right",
    )
    custom1.addContent(_content_label())
    custom1.setFixedHeight(210)
    row3.addWidget(custom1)

    # Nested vertical expander
    nested_outer = _NeuExpander("Parent section",
                                icon_name="mdi6.folder-outline",
                                theme="default", direction="down")
    child_a = _NeuExpander("Child section A", icon_name="mdi6.file-outline",
                           theme="stroke", direction="down")
    child_a.addContent(_content_label())
    child_b = _NeuExpander("Child section B", icon_name="mdi6.file-outline",
                           theme="stroke", direction="down")
    child_b.addContent(_content_label())
    nested_outer.addContent(child_a)
    nested_outer.addContent(child_b)
    nested_outer.setExpanded(True)
    nested_outer.setFixedWidth(340)

    row3.addWidget(nested_outer)
    row3.addStretch()
    g3.addLayout(row3)
    layout.addWidget(_neu_group(group3))

    layout.addStretch()
    scroll.setWidget(inner)

    outer = QtWidgets.QVBoxLayout(page)
    outer.setContentsMargins(0, 0, 0, 0)
    outer.addWidget(scroll)
    return page


def create_about() -> QtWidgets.QWidget:
    page = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(page)
    layout.setContentsMargins(24, 24, 24, 24)

    title = QtWidgets.QLabel("About Expanders")
    title.setProperty("heading", True)
    f = title.font(); f.setPointSize(20); title.setFont(f)
    layout.addWidget(title)

    info = QtWidgets.QLabel(
        "Collapsible container controls in three neumorphic themes:\n\n"
        "  • Default – raised header with neumorphic box-shadow\n"
        "  • Circle – small circular toggle button + label\n"
        "  • Stroke – outlined / bordered header\n\n"
        "Each theme supports four expand directions:\n"
        "  Down, Up, Right, Left\n\n"
        "Disabled states and nested expanders are also demonstrated."
    )
    info.setWordWrap(True)
    layout.addWidget(info)
    layout.addStretch()
    return page


registry.register(WidgetDemo(
    id="expanders",
    name="Expanders",
    create_page=create_page,
    create_about=create_about,
    description="Collapsible sections with animated reveal.",
))
