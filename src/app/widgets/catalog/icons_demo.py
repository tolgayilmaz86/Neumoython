"""Icons demo – Material Design icon gallery.

Showcases the qtawesome icon library with Material Design 6 icons.
"""

import qtawesome as qta
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QFrame

from widgets.registry import registry, WidgetDemo
from widgets.box_shadow import BoxShadowWrapper
from styles.theme_manager import theme_manager


def _neu_group(group: QtWidgets.QGroupBox) -> BoxShadowWrapper:
    shadows = theme_manager.shadow_configs()
    return BoxShadowWrapper(
        group, shadow_list=shadows["outside_raised"],
        smooth=True, margins=(12, 12, 12, 12),
    )


# Curated set of icons grouped by category
_ICON_CATEGORIES: dict[str, list[tuple[str, str]]] = {
    "Navigation": [
        ("mdi6.home-outline", "Home"),
        ("mdi6.menu", "Menu"),
        ("mdi6.arrow-left", "Back"),
        ("mdi6.arrow-right", "Forward"),
        ("mdi6.chevron-up", "Up"),
        ("mdi6.chevron-down", "Down"),
        ("mdi6.magnify", "Search"),
        ("mdi6.close", "Close"),
    ],
    "Actions": [
        ("mdi6.plus", "Add"),
        ("mdi6.minus", "Remove"),
        ("mdi6.pencil-outline", "Edit"),
        ("mdi6.delete-outline", "Delete"),
        ("mdi6.content-copy", "Copy"),
        ("mdi6.content-paste", "Paste"),
        ("mdi6.download", "Download"),
        ("mdi6.upload", "Upload"),
    ],
    "Communication": [
        ("mdi6.email-outline", "Email"),
        ("mdi6.phone-outline", "Phone"),
        ("mdi6.chat-outline", "Chat"),
        ("mdi6.bell-outline", "Notification"),
        ("mdi6.send", "Send"),
        ("mdi6.share-variant-outline", "Share"),
        ("mdi6.link-variant", "Link"),
        ("mdi6.attachment", "Attach"),
    ],
    "Content": [
        ("mdi6.file-document-outline", "Document"),
        ("mdi6.folder-outline", "Folder"),
        ("mdi6.image-outline", "Image"),
        ("mdi6.video-outline", "Video"),
        ("mdi6.music-note", "Music"),
        ("mdi6.code-tags", "Code"),
        ("mdi6.database-outline", "Database"),
        ("mdi6.cloud-outline", "Cloud"),
    ],
    "User Interface": [
        ("mdi6.cog-outline", "Settings"),
        ("mdi6.account-outline", "Account"),
        ("mdi6.palette-outline", "Theme"),
        ("mdi6.monitor", "Display"),
        ("mdi6.cellphone", "Mobile"),
        ("mdi6.brightness-6", "Brightness"),
        ("mdi6.eye-outline", "Visibility"),
        ("mdi6.lock-outline", "Security"),
    ],
    "Status": [
        ("mdi6.check-circle-outline", "Success"),
        ("mdi6.alert-circle-outline", "Warning"),
        ("mdi6.close-circle-outline", "Error"),
        ("mdi6.information-outline", "Info"),
        ("mdi6.help-circle-outline", "Help"),
        ("mdi6.star-outline", "Favorite"),
        ("mdi6.heart-outline", "Like"),
        ("mdi6.flag-outline", "Flag"),
    ],
}


def _make_icon_tile(icon_name: str, label_text: str,
                    size: int = 28) -> QtWidgets.QWidget:
    """Create a small tile showing an icon and its label."""
    tile = QtWidgets.QWidget()
    lay = QtWidgets.QVBoxLayout(tile)
    lay.setContentsMargins(8, 8, 8, 8)
    lay.setSpacing(4)
    lay.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    p = theme_manager.palette
    icon_label = QtWidgets.QLabel()
    icon_label.setPixmap(qta.icon(icon_name, color=p['text']).pixmap(size, size))
    icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    icon_label.setToolTip(icon_name)
    lay.addWidget(icon_label)

    name_label = QtWidgets.QLabel(label_text)
    name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    name_label.setStyleSheet(
        f"font-size: 10px; color: {p['text_muted']}; background: transparent;")
    lay.addWidget(name_label)

    tile.setFixedSize(90, 72)
    return tile


def create_page() -> QtWidgets.QWidget:
    """Create and return the demo page widget."""
    page = QtWidgets.QWidget()
    scroll = QtWidgets.QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.Shape.NoFrame)

    inner = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(inner)
    layout.setSpacing(16)
    layout.setContentsMargins(24, 24, 24, 24)

    title = QtWidgets.QLabel("Icons")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    desc = QtWidgets.QLabel(
        "Material Design icons from the qtawesome library (mdi6 prefix). "
        "Hover over an icon to see its identifier."
    )
    desc.setWordWrap(True)
    desc.setProperty("subheading", True)
    layout.addWidget(desc)

    p = theme_manager.palette

    for category, icons in _ICON_CATEGORIES.items():
        group = QtWidgets.QGroupBox(category)
        g_lay = QtWidgets.QVBoxLayout(group)
        g_lay.setContentsMargins(16, 24, 16, 12)

        flow = QtWidgets.QWidget()
        flow_layout = QtWidgets.QGridLayout(flow)
        flow_layout.setSpacing(4)
        flow_layout.setContentsMargins(0, 0, 0, 0)

        cols = 8
        for i, (icon_name, label_text) in enumerate(icons):
            flow_layout.addWidget(
                _make_icon_tile(icon_name, label_text),
                i // cols, i % cols,
            )

        g_lay.addWidget(flow)
        layout.addWidget(_neu_group(group))

    # --- Size variants ---
    group_sizes = QtWidgets.QGroupBox("Size Variants")
    gs_lay = QtWidgets.QHBoxLayout(group_sizes)
    gs_lay.setContentsMargins(16, 24, 16, 16)
    gs_lay.setSpacing(24)

    for size in (16, 24, 32, 48, 64):
        col = QtWidgets.QVBoxLayout()
        col.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        icon_label = QtWidgets.QLabel()
        icon_label.setPixmap(
            qta.icon("mdi6.star", color=p['accent']).pixmap(size, size))
        icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        size_label = QtWidgets.QLabel(f"{size}px")
        size_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        size_label.setStyleSheet(f"font-size: 11px; color: {p['text_muted']};")
        col.addWidget(icon_label)
        col.addWidget(size_label)
        gs_lay.addLayout(col)
    gs_lay.addStretch()

    layout.addWidget(_neu_group(group_sizes))

    # --- Colored icons ---
    group_colors = QtWidgets.QGroupBox("Colored Icons")
    gc_lay = QtWidgets.QHBoxLayout(group_colors)
    gc_lay.setContentsMargins(16, 24, 16, 16)
    gc_lay.setSpacing(16)

    for color, name in [
        (p['accent'], "Accent"),
        ("#E04848", "Red"),
        ("#4CAF50", "Green"),
        ("#2196F3", "Blue"),
        ("#FF9800", "Orange"),
        (p['text'], "Default"),
    ]:
        col = QtWidgets.QVBoxLayout()
        col.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        icon_label = QtWidgets.QLabel()
        icon_label.setPixmap(
            qta.icon("mdi6.heart", color=color).pixmap(32, 32))
        icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        c_label = QtWidgets.QLabel(name)
        c_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        c_label.setStyleSheet(f"font-size: 11px; color: {p['text_muted']};")
        col.addWidget(icon_label)
        col.addWidget(c_label)
        gc_lay.addLayout(col)
    gc_lay.addStretch()

    layout.addWidget(_neu_group(group_colors))

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

    title = QtWidgets.QLabel("About Icons")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    info = QtWidgets.QLabel(
        "Material Design icons via the qtawesome library:\n\n"
        "  • 7000+ icons from @mdi/font (mdi6 prefix)\n"
        "  • Scalable to any size\n"
        "  • Colorable via the color parameter\n"
        "  • Usage: qta.icon('mdi6.icon-name', color='#hex')\n\n"
    )
    info.setWordWrap(True)
    layout.addWidget(info)
    layout.addStretch()
    return page


registry.register(WidgetDemo(
    id="icons",
    name="Icons",
    create_page=create_page,
    create_about=create_about,
    description="Material Design icon gallery with size and color variants.",
))
