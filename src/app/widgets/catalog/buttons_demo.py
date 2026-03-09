"""Buttons demo – matching Neumorphism.Avalonia button showcase.

Sections: Regular, Outline, Icon, Floating (FAB), Extended FAB, Custom.
"""

import qtawesome as qta
from PySide6 import QtCore, QtWidgets

from widgets.registry import registry, WidgetDemo
from widgets.box_shadow import BoxShadow, BoxShadowWrapper
from styles.theme_manager import theme_manager
from styles.snippets import section_heading


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


def _neu_fab(btn: QtWidgets.QPushButton) -> BoxShadowWrapper:
    """Wrap a FAB in a bigger neumorphic raised shadow."""
    shadows = theme_manager.shadow_configs()
    return BoxShadowWrapper(
        btn,
        shadow_list=shadows["outside_raised"],
        smooth=True,
        margins=(10, 10, 10, 10),
    )


def _section_label(text: str) -> QtWidgets.QLabel:
    lbl = QtWidgets.QLabel(text)
    lbl.setStyleSheet(section_heading())
    return lbl


def create_page() -> QtWidgets.QWidget:
    """Create and return the demo page widget."""
    p = theme_manager.palette
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

    desc = QtWidgets.QLabel(
        "Neumorphic button variants: regular, outline, icon, "
        "floating action buttons (FAB), extended FAB, and custom."
    )
    desc.setWordWrap(True)
    desc.setProperty("subheading", True)
    layout.addWidget(desc)

    # ── 1. Regular buttons ────────────────────────────────────────────────
    layout.addWidget(_section_label("Regular buttons"))
    group1 = QtWidgets.QGroupBox("Regular Buttons")
    g1 = QtWidgets.QHBoxLayout(group1)
    g1.setSpacing(14)
    g1.setContentsMargins(16, 24, 16, 16)

    btn_default = QtWidgets.QPushButton("Default")
    btn_default.setToolTip("Regular button with default theme")

    btn_icon_heart = QtWidgets.QPushButton()
    btn_icon_heart.setIcon(qta.icon("mdi6.heart", color="red"))
    btn_icon_heart.setIconSize(QtCore.QSize(24, 24))
    btn_icon_heart.setToolTip("Regular button with icon")

    btn_light = QtWidgets.QPushButton("Light")
    btn_light.setProperty("buttonVariant", "light")
    btn_light.setToolTip('Regular button class "Light"')

    btn_dark = QtWidgets.QPushButton("Dark")
    btn_dark.setProperty("buttonVariant", "dark")
    btn_dark.setToolTip('Regular button class "Dark"')

    btn_accent = QtWidgets.QPushButton("Accent")
    btn_accent.setProperty("accentButton", True)
    btn_accent.setToolTip('Regular button class "Accent"')

    btn_gradient = QtWidgets.QPushButton("Gradient")
    btn_gradient.setProperty("buttonVariant", "gradient")
    btn_gradient.setToolTip('Regular button class "Gradient"')

    btn_disabled = QtWidgets.QPushButton("Disabled")
    btn_disabled.setEnabled(False)
    btn_disabled.setToolTip("Disabled regular button")

    for btn in (btn_default, btn_icon_heart, btn_light, btn_dark,
                btn_accent, btn_gradient):
        g1.addWidget(_neu_button(btn))
    g1.addWidget(btn_disabled)

    layout.addWidget(_neu_group(group1))

    # ── 2. Outline buttons ───────────────────────────────────────────────
    layout.addWidget(_section_label("Outline buttons"))
    group2 = QtWidgets.QGroupBox("Outline Buttons")
    g2 = QtWidgets.QHBoxLayout(group2)
    g2.setSpacing(14)
    g2.setContentsMargins(16, 24, 16, 16)

    outline_default = QtWidgets.QPushButton("Default")
    outline_default.setProperty("buttonVariant", "outline")

    outline_heart = QtWidgets.QPushButton()
    outline_heart.setProperty("buttonVariant", "outline")
    outline_heart.setIcon(qta.icon("mdi6.heart", color="red"))
    outline_heart.setIconSize(QtCore.QSize(24, 24))

    outline_light = QtWidgets.QPushButton("Light")
    outline_light.setProperty("buttonVariant", "outline-light")

    outline_dark = QtWidgets.QPushButton("Dark")
    outline_dark.setProperty("buttonVariant", "outline-dark")

    outline_accent = QtWidgets.QPushButton("Accent")
    outline_accent.setProperty("buttonVariant", "outline-accent")

    outline_disabled = QtWidgets.QPushButton("Disabled")
    outline_disabled.setProperty("buttonVariant", "outline")
    outline_disabled.setEnabled(False)

    for btn in (outline_default, outline_heart, outline_light,
                outline_dark, outline_accent):
        g2.addWidget(_neu_button(btn))
    g2.addWidget(outline_disabled)

    layout.addWidget(_neu_group(group2))

    # ── 3. Icon buttons ──────────────────────────────────────────────────
    layout.addWidget(_section_label("Icon buttons"))
    group3 = QtWidgets.QGroupBox("Icon Buttons")
    g3 = QtWidgets.QHBoxLayout(group3)
    g3.setSpacing(14)
    g3.setContentsMargins(16, 24, 16, 16)

    icon_heart = QtWidgets.QPushButton()
    icon_heart.setProperty("buttonVariant", "icon")
    icon_heart.setIcon(qta.icon("mdi6.heart", color="red"))
    icon_heart.setIconSize(QtCore.QSize(22, 22))
    icon_heart.setToolTip("Icon button")

    icon_light = QtWidgets.QPushButton()
    icon_light.setProperty("buttonVariant", "icon-light")
    icon_light.setIcon(qta.icon("mdi6.close", color=p['text']))
    icon_light.setIconSize(QtCore.QSize(22, 22))
    icon_light.setToolTip('Icon button "Light"')

    icon_dark = QtWidgets.QPushButton()
    icon_dark.setProperty("buttonVariant", "icon-dark")
    icon_dark.setIcon(qta.icon("mdi6.close", color="#FFFFFF"))
    icon_dark.setIconSize(QtCore.QSize(22, 22))
    icon_dark.setToolTip('Icon button "Dark"')

    icon_accent = QtWidgets.QPushButton()
    icon_accent.setProperty("buttonVariant", "icon-accent")
    icon_accent.setIcon(qta.icon("mdi6.close", color="#FFFFFF"))
    icon_accent.setIconSize(QtCore.QSize(22, 22))
    icon_accent.setToolTip('Icon button "Accent"')

    for btn in (icon_heart, icon_light, icon_dark, icon_accent):
        g3.addWidget(_neu_button(btn))
    g3.addStretch()

    layout.addWidget(_neu_group(group3))

    # ── 4. Floating buttons with icon (FAB) ──────────────────────────────
    layout.addWidget(_section_label("Floating buttons with icon"))
    group4 = QtWidgets.QGroupBox("Floating Action Buttons")
    g4 = QtWidgets.QHBoxLayout(group4)
    g4.setSpacing(14)
    g4.setContentsMargins(16, 24, 16, 16)

    fab_specs = [
        ("fab",              "mdi6.plus",      p['text'],   "Default FAB"),
        ("fab-mini",         "mdi6.cog",       p['text'],   "Mini FAB"),
        ("fab-light-mini",   "mdi6.bell",      "#FFFFFF",   "Light Mini FAB"),
        ("fab-light",        "mdi6.speaker",   "#FFFFFF",   "Light FAB"),
        ("fab-dark-mini",    "mdi6.thumb-up",  "#FFFFFF",   "Dark Mini FAB"),
        ("fab-dark",         "mdi6.heart",     "#FFFFFF",   "Dark FAB"),
        ("fab-accent-mini",  "mdi6.heart",     "#FFFFFF",   "Accent Mini FAB"),
        ("fab-accent",       "mdi6.heart",     "#FFFFFF",   "Accent FAB"),
    ]
    for variant, icon_name, icon_color, tip in fab_specs:
        btn = QtWidgets.QPushButton()
        btn.setProperty("buttonVariant", variant)
        btn.setIcon(qta.icon(icon_name, color=icon_color))
        btn.setIconSize(QtCore.QSize(22, 22))
        btn.setToolTip(tip)
        g4.addWidget(_neu_fab(btn))

    fab_disabled = QtWidgets.QPushButton()
    fab_disabled.setProperty("buttonVariant", "fab-accent")
    fab_disabled.setIcon(qta.icon("mdi6.heart", color="#FFFFFF"))
    fab_disabled.setIconSize(QtCore.QSize(24, 24))
    fab_disabled.setEnabled(False)
    fab_disabled.setToolTip("Disabled Accent FAB")
    g4.addWidget(fab_disabled)

    layout.addWidget(_neu_group(group4))

    # ── 5. Extended floating buttons ─────────────────────────────────────
    layout.addWidget(_section_label("Extended floating buttons"))
    group5 = QtWidgets.QGroupBox("Extended FAB")
    g5 = QtWidgets.QHBoxLayout(group5)
    g5.setSpacing(14)
    g5.setContentsMargins(16, 24, 16, 16)

    ext_specs = [
        ("fab-extended",        p['text'],   "Default"),
        ("fab-extended-light",  p['text'],   "Light"),
        ("fab-extended-dark",   "#FFFFFF",   "Dark"),
        ("fab-extended-accent", "#FFFFFF",   "Accent"),
    ]
    for variant, icon_col, label_text in ext_specs:
        btn = QtWidgets.QPushButton(f"  {label_text}")
        btn.setProperty("buttonVariant", variant)
        btn.setIcon(qta.icon("mdi6.plus", color=icon_col))
        btn.setIconSize(QtCore.QSize(20, 20))
        g5.addWidget(_neu_fab(btn))

    g5.addStretch()
    layout.addWidget(_neu_group(group5))

    # ── 6. Custom buttons ────────────────────────────────────────────────
    layout.addWidget(_section_label("Custom buttons"))
    group6 = QtWidgets.QGroupBox("Custom Buttons")
    g6 = QtWidgets.QHBoxLayout(group6)
    g6.setSpacing(14)
    g6.setContentsMargins(16, 24, 16, 16)

    custom1 = QtWidgets.QPushButton("Custom")
    custom1.setProperty("buttonVariant", "custom-gradient")
    custom1.setToolTip("Custom button with gradient background")
    custom1.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

    custom2 = QtWidgets.QPushButton("Custom\noutline")
    custom2.setProperty("buttonVariant", "custom-outline-gradient")
    custom2.setToolTip("Custom outline button with gradient background")
    custom2.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

    custom_fab = QtWidgets.QPushButton()
    custom_fab.setProperty("buttonVariant", "fab")
    custom_fab.setIcon(qta.icon("mdi6.plus", color="#FFFFFF"))
    custom_fab.setIconSize(QtCore.QSize(22, 22))
    custom_fab.setToolTip("Custom floating button")
    custom_fab.setStyleSheet(
        f"background: SteelBlue; border: 3px solid white; "
        f"border-radius: 28px; min-width:56px; max-width:56px; "
        f"min-height:56px; max-height:56px; padding:0px;"
    )

    for btn in (custom1, custom2):
        g6.addWidget(_neu_button(btn))
    g6.addWidget(_neu_fab(custom_fab))
    g6.addStretch()

    layout.addWidget(_neu_group(group6))

    # ── 7. Interactive click counter ─────────────────────────────────────
    layout.addWidget(_section_label("Interactive"))
    group7 = QtWidgets.QGroupBox("Click Counter")
    g7 = QtWidgets.QHBoxLayout(group7)
    g7.setSpacing(16)
    g7.setContentsMargins(16, 24, 16, 16)

    counter_label = QtWidgets.QLabel("Clicks: 0")
    clicks = [0]

    def on_click() -> None:
        clicks[0] += 1
        counter_label.setText(f"Clicks: {clicks[0]}")

    btn_count = QtWidgets.QPushButton("Click Counter")
    btn_count.clicked.connect(on_click)
    g7.addWidget(_neu_button(btn_count))
    g7.addWidget(counter_label)
    g7.addStretch()

    layout.addWidget(_neu_group(group7))

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
        "Neumorphic button variants matching the Neumorphism.Avalonia showcase:\n\n"
        "  • Regular – Default, Light, Dark, Accent, Gradient, Disabled\n"
        "  • Outline – Default, Light, Dark, Accent, Disabled\n"
        "  • Icon    – circular icon-only buttons in 4 colour variants\n"
        "  • FAB     – Floating Action Buttons in standard and mini sizes\n"
        "  • Extended FAB – FAB with icon + label text\n"
        "  • Custom  – gradient, outline-gradient, custom-styled FAB\n\n"
        "Each variant is driven by the 'buttonVariant' dynamic property and "
        "styled via the global neumorphic QSS theme."
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
    description="Regular, outline, icon, FAB, extended FAB, and custom buttons.",
))
