"""Tabs demo – tab controls with different placements and styles.
"""

import qtawesome as qta
from PySide6 import QtCore, QtWidgets

from widgets.registry import registry, WidgetDemo
from widgets.box_shadow import BoxShadowWrapper
from styles.theme_manager import theme_manager


def _neu_group(group: QtWidgets.QGroupBox) -> BoxShadowWrapper:
    shadows = theme_manager.shadow_configs()
    return BoxShadowWrapper(
        group, shadow_list=shadows["outside_raised"],
        smooth=True, margins=(12, 12, 12, 12),
    )


def _sample_tab_content(label_text: str) -> QtWidgets.QWidget:
    """Return a simple content widget for a tab page."""
    w = QtWidgets.QWidget()
    lay = QtWidgets.QVBoxLayout(w)
    lay.setContentsMargins(16, 16, 16, 16)
    lbl = QtWidgets.QLabel(label_text)
    lbl.setWordWrap(True)
    lay.addWidget(lbl)
    lay.addStretch()
    return w


def _make_tab_widget(placement: QtWidgets.QTabWidget.TabPosition,
                     tabs: list[tuple[str, str]]) -> QtWidgets.QTabWidget:
    """Create a QTabWidget with icon+text tabs."""
    tw = QtWidgets.QTabWidget()
    tw.setTabPosition(placement)
    tw.setMinimumHeight(200)
    p = theme_manager.palette
    for name, icon_name in tabs:
        icon = qta.icon(icon_name, color=p['text'])
        tw.addTab(_sample_tab_content(f'Content area for "{name}" tab.'),
                  icon, name)
    return tw


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

    title = QtWidgets.QLabel("Tabs")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    desc = QtWidgets.QLabel(
        "Tab controls with top, bottom, left, and right placements. "
    )
    desc.setWordWrap(True)
    desc.setProperty("subheading", True)
    layout.addWidget(desc)

    tab_items = [
        ("Home", "mdi6.home-outline"),
        ("Profile", "mdi6.account-outline"),
        ("Settings", "mdi6.cog-outline"),
    ]

    # --- Top tabs ---
    group1 = QtWidgets.QGroupBox("Top Tabs")
    g1 = QtWidgets.QVBoxLayout(group1)
    g1.setContentsMargins(16, 24, 16, 16)
    g1.addWidget(_make_tab_widget(QtWidgets.QTabWidget.TabPosition.North, tab_items))
    layout.addWidget(_neu_group(group1))

    # --- Bottom tabs ---
    group2 = QtWidgets.QGroupBox("Bottom Tabs")
    g2 = QtWidgets.QVBoxLayout(group2)
    g2.setContentsMargins(16, 24, 16, 16)
    g2.addWidget(_make_tab_widget(QtWidgets.QTabWidget.TabPosition.South, tab_items))
    layout.addWidget(_neu_group(group2))

    # --- Left / Right side by side ---
    side_row = QtWidgets.QHBoxLayout()
    side_row.setSpacing(20)

    group3 = QtWidgets.QGroupBox("Left Tabs")
    g3 = QtWidgets.QVBoxLayout(group3)
    g3.setContentsMargins(16, 24, 16, 16)
    g3.addWidget(_make_tab_widget(QtWidgets.QTabWidget.TabPosition.West, tab_items))
    side_row.addWidget(_neu_group(group3))

    group4 = QtWidgets.QGroupBox("Right Tabs")
    g4 = QtWidgets.QVBoxLayout(group4)
    g4.setContentsMargins(16, 24, 16, 16)
    g4.addWidget(_make_tab_widget(QtWidgets.QTabWidget.TabPosition.East, tab_items))
    side_row.addWidget(_neu_group(group4))

    layout.addLayout(side_row)

    # --- Dynamic tabs ---
    group5 = QtWidgets.QGroupBox("Dynamic Tabs")
    g5 = QtWidgets.QVBoxLayout(group5)
    g5.setContentsMargins(16, 24, 16, 16)
    g5.setSpacing(12)

    dynamic_tw = QtWidgets.QTabWidget()
    dynamic_tw.setTabsClosable(True)
    dynamic_tw.setMinimumHeight(180)
    p = theme_manager.palette

    for i in range(1, 4):
        dynamic_tw.addTab(
            _sample_tab_content(f"This is dynamic tab #{i}."),
            qta.icon("mdi6.file-document-outline", color=p['text']),
            f"Tab {i}",
        )

    tab_counter = [3]

    def add_tab() -> None:
        tab_counter[0] += 1
        n = tab_counter[0]
        dynamic_tw.addTab(
            _sample_tab_content(f"This is dynamic tab #{n}."),
            qta.icon("mdi6.file-document-outline", color=p['text']),
            f"Tab {n}",
        )
        dynamic_tw.setCurrentIndex(dynamic_tw.count() - 1)

    def close_tab(index: int) -> None:
        if dynamic_tw.count() > 1:
            dynamic_tw.removeTab(index)

    dynamic_tw.tabCloseRequested.connect(close_tab)

    btn_row = QtWidgets.QHBoxLayout()
    add_btn = QtWidgets.QPushButton("Add Tab")
    add_btn.setIcon(qta.icon("mdi6.plus", color=p['text']))
    add_btn.clicked.connect(add_tab)
    btn_row.addWidget(add_btn)
    btn_row.addStretch()

    g5.addWidget(dynamic_tw)
    g5.addLayout(btn_row)
    layout.addWidget(_neu_group(group5))

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

    title = QtWidgets.QLabel("About Tabs")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    info = QtWidgets.QLabel(
        "Tab widget variants:\n\n"
        "  • Top / Bottom / Left / Right tab placement\n"
        "  • Icon + text tab headers\n"
        "  • Closable tabs with dynamic add/remove\n\n"
        "QSS provides neumorphic panel\n"
        "backgrounds and accent-colored selected tab indicators."
    )
    info.setWordWrap(True)
    layout.addWidget(info)
    layout.addStretch()
    return page


registry.register(WidgetDemo(
    id="tabs",
    name="Tabs",
    create_page=create_page,
    create_about=create_about,
    description="Tab controls with various placements and dynamic tabs.",
))
