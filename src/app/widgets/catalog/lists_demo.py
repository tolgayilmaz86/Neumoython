"""Lists demo – list boxes with regular, outset, and inset item styles.
"""

import qtawesome as qta
from PySide6 import QtCore, QtGui, QtWidgets

from widgets.registry import registry, WidgetDemo
from widgets.box_shadow import BoxShadowWrapper
from styles.theme_manager import theme_manager


def _neu_group(group: QtWidgets.QGroupBox) -> BoxShadowWrapper:
    shadows = theme_manager.shadow_configs()
    return BoxShadowWrapper(
        group, shadow_list=shadows["outside_raised"],
        smooth=True, margins=(12, 12, 12, 12),
    )


def _make_list(items: list[str], *, parent=None) -> QtWidgets.QListWidget:
    lw = QtWidgets.QListWidget(parent)
    lw.setMinimumHeight(180)
    for text in items:
        lw.addItem(text)
    return lw


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

    title = QtWidgets.QLabel("Lists")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    desc = QtWidgets.QLabel(
        "List boxes with different item styles. "
    )
    desc.setWordWrap(True)
    desc.setProperty("subheading", True)
    layout.addWidget(desc)

    fruit_items = ["Apple", "Banana", "Cherry", "Dragonfruit", "Elderberry", "Fig"]

    cols = QtWidgets.QHBoxLayout()
    cols.setSpacing(20)

    # --- Regular list ---
    group1 = QtWidgets.QGroupBox("Regular")
    g1 = QtWidgets.QVBoxLayout(group1)
    g1.setContentsMargins(16, 24, 16, 16)
    g1.addWidget(_make_list(fruit_items))
    cols.addWidget(_neu_group(group1))

    # --- List with icons ---
    group2 = QtWidgets.QGroupBox("With Icons")
    g2 = QtWidgets.QVBoxLayout(group2)
    g2.setContentsMargins(16, 24, 16, 16)

    lw2 = QtWidgets.QListWidget()
    lw2.setMinimumHeight(180)
    p = theme_manager.palette
    icon_names = ["mdi6.folder-outline", "mdi6.file-document-outline",
                  "mdi6.image-outline", "mdi6.music-note",
                  "mdi6.video-outline", "mdi6.archive-outline"]
    for text, icon_name in zip(fruit_items, icon_names):
        item = QtWidgets.QListWidgetItem(
            qta.icon(icon_name, color=p['text']), text)
        lw2.addItem(item)
    g2.addWidget(lw2)
    cols.addWidget(_neu_group(group2))

    # --- Checkable list ---
    group3 = QtWidgets.QGroupBox("Checkable")
    g3 = QtWidgets.QVBoxLayout(group3)
    g3.setContentsMargins(16, 24, 16, 16)

    lw3 = QtWidgets.QListWidget()
    lw3.setMinimumHeight(180)
    for i, text in enumerate(fruit_items):
        item = QtWidgets.QListWidgetItem(text)
        item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.CheckState.Checked if i < 2
                           else QtCore.Qt.CheckState.Unchecked)
        lw3.addItem(item)
    g3.addWidget(lw3)
    cols.addWidget(_neu_group(group3))

    layout.addLayout(cols)

    # --- Selection info ---
    group4 = QtWidgets.QGroupBox("Interactive Selection")
    g4 = QtWidgets.QVBoxLayout(group4)
    g4.setContentsMargins(16, 24, 16, 16)
    g4.setSpacing(12)

    info_label = QtWidgets.QLabel("Select an item below:")
    g4.addWidget(info_label)

    lw4 = QtWidgets.QListWidget()
    lw4.setMinimumHeight(120)
    lw4.setMaximumHeight(160)
    menu_items = [
        ("Dashboard", "mdi6.view-dashboard-outline"),
        ("Settings", "mdi6.cog-outline"),
        ("Profile", "mdi6.account-outline"),
        ("Messages", "mdi6.email-outline"),
        ("Help", "mdi6.help-circle-outline"),
    ]
    for text, icon_name in menu_items:
        item = QtWidgets.QListWidgetItem(
            qta.icon(icon_name, color=p['text']), text)
        lw4.addItem(item)

    selection_label = QtWidgets.QLabel("Selected: None")
    selection_label.setStyleSheet("font-weight: 600; font-size: 13px;")

    def on_selection(current, _previous) -> None:
        if current:
            selection_label.setText(f"Selected: {current.text()}")

    lw4.currentItemChanged.connect(on_selection)
    g4.addWidget(lw4)
    g4.addWidget(selection_label)

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

    title = QtWidgets.QLabel("About Lists")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    info = QtWidgets.QLabel(
        "List box variants:\n\n"
        "  • Regular – plain text items\n"
        "  • With Icons – items with Material Design icons\n"
        "  • Checkable – items with checkboxes\n"
        "  • Interactive – selection change tracking\n\n"
        "Provides ListBoxItemOutset (raised) and\n"
        "ListBoxItemInset (sunken) item themes with pill-shaped variants."
    )
    info.setWordWrap(True)
    layout.addWidget(info)
    layout.addStretch()
    return page


registry.register(WidgetDemo(
    id="lists",
    name="Lists",
    create_page=create_page,
    create_about=create_about,
    description="List boxes with regular, icon, and checkable items.",
))
