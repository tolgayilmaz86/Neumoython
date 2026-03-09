"""Cards demo – outset (raised) and inset (pressed) neumorphic cards.
"""

import qtawesome as qta
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QFrame

from widgets.registry import registry, WidgetDemo
from widgets.box_shadow import BoxShadowWrapper
from styles.theme_manager import theme_manager


def _outset_card(shadow_list: list[dict], content_widget: QtWidgets.QWidget,
                 *, corner_radius: int = 16) -> BoxShadowWrapper:
    """Wrap *content_widget* in a raised neumorphic card."""
    frame = QFrame()
    frame.setFrameShape(QFrame.Shape.NoFrame)
    p = theme_manager.palette
    frame.setStyleSheet(
        f"QFrame {{ background: {p['card_bg']}; border-radius: {corner_radius}px; }}"
    )
    lay = QtWidgets.QVBoxLayout(frame)
    lay.setContentsMargins(20, 20, 20, 20)
    lay.addWidget(content_widget)
    return BoxShadowWrapper(
        frame, shadow_list=shadow_list, smooth=True,
        margins=(14, 14, 14, 14),
    )


def _inset_card(shadow_list: list[dict], content_widget: QtWidgets.QWidget,
                *, corner_radius: int = 16) -> BoxShadowWrapper:
    """Wrap *content_widget* in an inset (pressed) neumorphic card."""
    frame = QFrame()
    frame.setFrameShape(QFrame.Shape.NoFrame)
    p = theme_manager.palette
    frame.setStyleSheet(
        f"QFrame {{ background: {p['card_bg']}; border-radius: {corner_radius}px; }}"
    )
    lay = QtWidgets.QVBoxLayout(frame)
    lay.setContentsMargins(20, 20, 20, 20)
    lay.addWidget(content_widget)
    return BoxShadowWrapper(
        frame, shadow_list=shadow_list, smooth=True,
        margins=(14, 14, 14, 14),
    )


def _label(text: str, *, bold: bool = False, size: int = 13,
           color_key: str = "text") -> QtWidgets.QLabel:
    lbl = QtWidgets.QLabel(text)
    lbl.setWordWrap(True)
    f = lbl.font()
    f.setPointSize(size)
    f.setBold(bold)
    lbl.setFont(f)
    lbl.setStyleSheet(f"color: {theme_manager.palette[color_key]}; background: transparent;")
    return lbl


def create_page() -> QtWidgets.QWidget:
    """Create and return the demo page widget."""
    page = QtWidgets.QWidget()
    scroll = QtWidgets.QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.Shape.NoFrame)

    inner = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(inner)
    layout.setSpacing(20)
    layout.setContentsMargins(24, 24, 24, 24)

    title = QtWidgets.QLabel("Cards")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    desc = QtWidgets.QLabel(
        "Outset (raised) and inset (pressed) card styles. "
    )
    desc.setWordWrap(True)
    desc.setProperty("subheading", True)
    layout.addWidget(desc)

    shadows = theme_manager.shadow_configs()
    p = theme_manager.palette

    # --- Outset cards ---
    layout.addWidget(_label("Outset Cards", bold=True, size=15, color_key="text_heading"))

    outset_row = QtWidgets.QHBoxLayout()
    outset_row.setSpacing(20)

    # Card 1: basic
    c1_content = QtWidgets.QWidget()
    c1_lay = QtWidgets.QVBoxLayout(c1_content)
    c1_lay.setContentsMargins(0, 0, 0, 0)
    c1_lay.addWidget(_label("Basic Card", bold=True, size=14, color_key="text_heading"))
    c1_lay.addWidget(_label("A simple raised neumorphic card with text content.",
                            color_key="text_muted"))
    outset_row.addWidget(_outset_card(shadows["outside_raised"], c1_content))

    # Card 2: with icon
    c2_content = QtWidgets.QWidget()
    c2_lay = QtWidgets.QVBoxLayout(c2_content)
    c2_lay.setContentsMargins(0, 0, 0, 0)
    icon_label = QtWidgets.QLabel()
    icon_label.setPixmap(qta.icon("mdi6.palette-outline", color=p['accent']).pixmap(40, 40))
    c2_lay.addWidget(icon_label)
    c2_lay.addWidget(_label("Accent Card", bold=True, size=14, color_key="text_heading"))
    c2_lay.addWidget(_label("Cards can contain icons, images, or any widget hierarchy.",
                            color_key="text_muted"))
    outset_row.addWidget(_outset_card(shadows["outside_raised"], c2_content))

    # Card 3: accent background
    c3_content = QtWidgets.QWidget()
    c3_lay = QtWidgets.QVBoxLayout(c3_content)
    c3_lay.setContentsMargins(0, 0, 0, 0)
    c3_lay.addWidget(_label("Colored Card", bold=True, size=14, color_key="text_heading"))
    c3_lay.addWidget(_label("Custom corner radius of 20px.",
                            color_key="text_muted"))
    outset_row.addWidget(_outset_card(shadows["outside_raised"], c3_content,
                                      corner_radius=20))

    layout.addLayout(outset_row)

    # --- Inset cards ---
    layout.addSpacing(12)
    layout.addWidget(_label("Inset Cards", bold=True, size=15, color_key="text_heading"))

    inset_row = QtWidgets.QHBoxLayout()
    inset_row.setSpacing(20)

    # Card 1: basic inset
    i1_content = QtWidgets.QWidget()
    i1_lay = QtWidgets.QVBoxLayout(i1_content)
    i1_lay.setContentsMargins(0, 0, 0, 0)
    i1_lay.addWidget(_label("Inset Card", bold=True, size=14, color_key="text_heading"))
    i1_lay.addWidget(_label("A pressed/concave card with inside shadows.",
                            color_key="text_muted"))
    inset_row.addWidget(_inset_card(shadows["inside_pressed"], i1_content))

    # Card 2: inset with icon
    i2_content = QtWidgets.QWidget()
    i2_lay = QtWidgets.QVBoxLayout(i2_content)
    i2_lay.setContentsMargins(0, 0, 0, 0)
    i2_icon = QtWidgets.QLabel()
    i2_icon.setPixmap(qta.icon("mdi6.weather-night", color=p['accent']).pixmap(40, 40))
    i2_lay.addWidget(i2_icon)
    i2_lay.addWidget(_label("Inset with Icon", bold=True, size=14, color_key="text_heading"))
    i2_lay.addWidget(_label("Inside shadows create a recessed visual effect.",
                            color_key="text_muted"))
    inset_row.addWidget(_inset_card(shadows["inside_pressed"], i2_content))

    # Card 3: inset rounded
    i3_content = QtWidgets.QWidget()
    i3_lay = QtWidgets.QVBoxLayout(i3_content)
    i3_lay.setContentsMargins(0, 0, 0, 0)
    i3_lay.addWidget(_label("Rounded Inset", bold=True, size=14, color_key="text_heading"))
    i3_lay.addWidget(_label("Corner radius 20px for softer edges.",
                            color_key="text_muted"))
    inset_row.addWidget(_inset_card(shadows["inside_pressed"], i3_content,
                                    corner_radius=20))

    layout.addLayout(inset_row)

    # --- Nested cards ---
    layout.addSpacing(12)
    layout.addWidget(_label("Nested Cards", bold=True, size=15, color_key="text_heading"))

    nested_content = QtWidgets.QWidget()
    nested_lay = QtWidgets.QVBoxLayout(nested_content)
    nested_lay.setContentsMargins(0, 0, 0, 0)
    nested_lay.setSpacing(12)
    nested_lay.addWidget(_label("Outer Outset Card", bold=True, size=14, color_key="text_heading"))

    inner_content = QtWidgets.QWidget()
    inner_lay = QtWidgets.QVBoxLayout(inner_content)
    inner_lay.setContentsMargins(0, 0, 0, 0)
    inner_lay.addWidget(_label("Inner Inset Card", bold=True, size=13, color_key="text_heading"))
    inner_lay.addWidget(_label(
        "Cards can be nested – outset container with inset child "
        "creates natural depth layering.", color_key="text_muted"))

    inner_card = _inset_card(shadows["inside_pressed"], inner_content)
    nested_lay.addWidget(inner_card)

    outer_card = _outset_card(shadows["outside_raised"], nested_content)
    layout.addWidget(outer_card)

    layout.addStretch()
    scroll.setWidget(inner)

    outer = QtWidgets.QVBoxLayout(page)
    outer.setContentsMargins(0, 0, 0, 0)
    outer.addWidget(scroll)
    return page


def create_about() -> QtWidgets.QWidget:
    """Create and return the about/help page for this demo."""
    page = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(page)
    layout.setContentsMargins(24, 24, 24, 24)

    title = QtWidgets.QLabel("About Cards")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    info = QtWidgets.QLabel(
        "Neumorphic card containers:\n\n"
        "  • Outset (raised) – dual outside box shadows for convex effect\n"
        "  • Inset (pressed) – dual inside box shadows for concave effect\n"
        "  • Nested – combining outset and inset for depth layering\n"
        "  • Custom corner radius for softer or sharper edges\n\n"
    )
    info.setWordWrap(True)
    layout.addWidget(info)
    layout.addStretch()
    return page


registry.register(WidgetDemo(
    id="cards",
    name="Cards",
    create_page=create_page,
    create_about=create_about,
    description="Outset, inset, and nested neumorphic card styles.",
))
