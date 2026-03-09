"""Buttons demo – push buttons, tool buttons, and checkable buttons."""

import qtawesome as qta
from PySide6 import QtCore, QtWidgets

from widgets.registry import registry, WidgetDemo
from widgets.box_shadow import BoxShadow, BoxShadowWrapper
from styles.theme_manager import theme_manager


def _neu_group(group: QtWidgets.QGroupBox) -> BoxShadowWrapper:
    """Wrap a QGroupBox in a neumorphic raised shadow."""
    shadows = theme_manager.shadow_configs()
    return BoxShadowWrapper(
        group,
        shadow_list=shadows["outside_raised"],
        smooth=True,
        margins=(12, 12, 12, 12),
    )


def _neu_button(btn: QtWidgets.QPushButton) -> BoxShadowWrapper:
    """Wrap a QPushButton in a neumorphic raised shadow."""
    shadows = theme_manager.shadow_configs()
    return BoxShadowWrapper(
        btn,
        shadow_list=shadows["button_raised"],
        smooth=True,
        margins=(8, 8, 8, 8),
    )


def create_page() -> QtWidgets.QWidget:
    """Create and return the demo page widget."""
    page = QtWidgets.QWidget()
    scroll = QtWidgets.QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

    inner = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(inner)
    layout.setSpacing(16)
    layout.setContentsMargins(24, 24, 24, 24)

    title = QtWidgets.QLabel("Buttons")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    desc = QtWidgets.QLabel("Various button styles and states with neumorphic shadows.")
    desc.setWordWrap(True)
    desc.setProperty("subheading", True)
    layout.addWidget(desc)

    # --- Push buttons (raised neumorphic) ---
    group1 = QtWidgets.QGroupBox("Push Buttons")
    g1_layout = QtWidgets.QHBoxLayout(group1)
    g1_layout.setSpacing(16)
    g1_layout.setContentsMargins(16, 24, 16, 16)

    btn_default = QtWidgets.QPushButton("Default")
    btn_flat = QtWidgets.QPushButton("Flat")
    btn_flat.setFlat(True)
    btn_disabled = QtWidgets.QPushButton("Disabled")
    btn_disabled.setEnabled(False)
    btn_icon = QtWidgets.QPushButton("With Icon")
    btn_icon.setIcon(qta.icon("mdi6.check", color=theme_manager.palette['text']))

    btn_accent = QtWidgets.QPushButton("Accent")
    btn_accent.setProperty("accentButton", True)

    # Wrap individual buttons in neumorphic shadows
    for btn in (btn_default, btn_icon, btn_accent):
        g1_layout.addWidget(_neu_button(btn))
    # Flat and disabled stay unwrapped (flat = no shadow, disabled = subdued)
    g1_layout.addWidget(btn_flat)
    g1_layout.addWidget(btn_disabled)

    layout.addWidget(_neu_group(group1))

    # --- Tool buttons ---
    group2 = QtWidgets.QGroupBox("Tool Buttons")
    g2_layout = QtWidgets.QHBoxLayout(group2)
    g2_layout.setSpacing(16)
    g2_layout.setContentsMargins(16, 24, 16, 16)

    for style_name, style, icon_name in [
        ("Icon Only", QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly, "mdi6.file-outline"),
        ("Text Only", QtCore.Qt.ToolButtonStyle.ToolButtonTextOnly, "mdi6.file-outline"),
        ("Text Beside", QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon, "mdi6.folder-outline"),
        ("Text Under", QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon, "mdi6.star-outline"),
    ]:
        tb = QtWidgets.QToolButton()
        tb.setText(style_name)
        tb.setIcon(qta.icon(icon_name, color=theme_manager.palette['text']))
        tb.setToolButtonStyle(style)
        g2_layout.addWidget(_neu_button(tb))

    layout.addWidget(_neu_group(group2))

    # --- Checkable push buttons ---
    group3 = QtWidgets.QGroupBox("Checkable Push Buttons")
    g3_layout = QtWidgets.QHBoxLayout(group3)
    g3_layout.setSpacing(16)
    g3_layout.setContentsMargins(16, 24, 16, 16)

    btn_check = QtWidgets.QPushButton("Toggle Me")
    btn_check.setCheckable(True)
    btn_check2 = QtWidgets.QPushButton("Toggle B")
    btn_check2.setCheckable(True)
    btn_check2.setChecked(True)
    btn_check_d = QtWidgets.QPushButton("Disabled")
    btn_check_d.setCheckable(True)
    btn_check_d.setEnabled(False)

    for btn in (btn_check, btn_check2, btn_check_d):
        g3_layout.addWidget(_neu_button(btn))

    layout.addWidget(_neu_group(group3))

    # --- Click counter ---
    group4 = QtWidgets.QGroupBox("Interactive")
    g4_layout = QtWidgets.QHBoxLayout(group4)
    g4_layout.setSpacing(16)
    g4_layout.setContentsMargins(16, 24, 16, 16)

    counter_label = QtWidgets.QLabel("Clicks: 0")
    clicks = [0]

    def on_click() -> None:
        clicks[0] += 1
        counter_label.setText(f"Clicks: {clicks[0]}")

    btn_count = QtWidgets.QPushButton("Click Counter")
    btn_count.clicked.connect(on_click)

    g4_layout.addWidget(_neu_button(btn_count))
    g4_layout.addWidget(counter_label)
    g4_layout.addStretch()

    layout.addWidget(_neu_group(group4))

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

    title = QtWidgets.QLabel("About Buttons")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    info = QtWidgets.QLabel(
        "Standard Qt button widgets:\n"
        "  QPushButton, QToolButton, QRadioButton, QCheckBox.\n\n"
        "Demonstrates different styles, states, and click handling."
    )
    info.setWordWrap(True)
    layout.addWidget(info)
    layout.addStretch()
    return page


registry.register(WidgetDemo(
    id="buttons",
    name="Buttons",
    create_page=create_page,
    create_about=create_about,
    description="Push buttons, tool buttons, radio buttons, and checkboxes.",
))
