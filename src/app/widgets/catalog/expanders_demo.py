"""Expanders demo – collapsible sections in various styles.

Uses QToolBox for collapsible sections since PySide6 doesn't have a
native Expander control.
"""

import qtawesome as qta
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QFrame

from widgets.registry import registry, WidgetDemo
from widgets.box_shadow import BoxShadowWrapper
from widgets.collapsible_section import CollapsibleSection
from styles.theme_manager import theme_manager


def _neu_group(group: QtWidgets.QGroupBox) -> BoxShadowWrapper:
    shadows = theme_manager.shadow_configs()
    return BoxShadowWrapper(
        group, shadow_list=shadows["outside_raised"],
        smooth=True, margins=(12, 12, 12, 12),
    )


def _toolbox_page(text: str) -> QtWidgets.QWidget:
    """Build a padded QToolBox page with wrapping content text."""
    page = QtWidgets.QWidget()
    page.setMinimumHeight(60)
    layout = QtWidgets.QVBoxLayout(page)
    layout.setContentsMargins(12, 12, 12, 12)
    layout.setSpacing(0)

    label = QtWidgets.QLabel(text)
    label.setWordWrap(True)
    label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
    label.setSizePolicy(
        QtWidgets.QSizePolicy.Policy.Expanding,
        QtWidgets.QSizePolicy.Policy.Preferred,
    )
    layout.addWidget(label)
    return page


# ---------------------------------------------------------------------------
# Page builder
# ---------------------------------------------------------------------------

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

    title = QtWidgets.QLabel("Expanders")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    desc = QtWidgets.QLabel(
        "Collapsible sections with animated reveal. "
    )
    desc.setWordWrap(True)
    desc.setProperty("subheading", True)
    layout.addWidget(desc)

    p = theme_manager.palette

    # --- Vertical Expanders ---
    group1 = QtWidgets.QGroupBox("Collapsible Sections")
    g1 = QtWidgets.QVBoxLayout(group1)
    g1.setContentsMargins(16, 24, 16, 16)
    g1.setSpacing(8)

    sections = [
        ("General Settings", "mdi6.cog-outline",
         "Configure general application preferences including language, timezone, "
         "and notification settings."),
        ("Appearance", "mdi6.palette-outline",
         "Customize the look and feel of the application. Choose between light "
         "and dark neumorphic themes."),
        ("Privacy & Security", "mdi6.shield-lock-outline",
         "Manage privacy settings, two-factor authentication, and data "
         "export options."),
        ("About", "mdi6.information-outline",
         "View application version, license information, and credits."),
    ]

    for i, (sec_title, icon_name, body_text) in enumerate(sections):
        sec = CollapsibleSection(sec_title, icon_name)
        content_label = QtWidgets.QLabel(body_text)
        content_label.setWordWrap(True)
        content_label.setStyleSheet(f"color: {p['text']}; background: transparent;")
        sec.addContent(content_label)
        if i == 0:
            sec.setExpanded(True)
        g1.addWidget(sec)

    layout.addWidget(_neu_group(group1))

    # --- QToolBox (built-in Qt collapsible) ---
    group2 = QtWidgets.QGroupBox("QToolBox")
    g2 = QtWidgets.QVBoxLayout(group2)
    g2.setContentsMargins(16, 10, 16, 16)
    g2.setSpacing(10)

    toolbox = QtWidgets.QToolBox()
    toolbox.setSizePolicy(
        QtWidgets.QSizePolicy.Policy.Expanding,
        QtWidgets.QSizePolicy.Policy.MinimumExpanding,
    )
    toolbox.setMinimumHeight(200)
    for sec_title, icon_name, body_text in [
        ("Account", "mdi6.account-outline", "Manage your account details and preferences."),
        ("Notifications", "mdi6.bell-outline", "Configure notification channels and frequency."),
        ("Storage", "mdi6.database-outline", "View storage usage and manage your files."),
    ]:
        content = _toolbox_page(body_text)
        toolbox.addItem(content, qta.icon(icon_name, color=p['text']), sec_title)

    g2.addWidget(toolbox)
    layout.addWidget(_neu_group(group2))

    # --- Nested expanders ---
    group3 = QtWidgets.QGroupBox("Nested Expanders")
    g3 = QtWidgets.QVBoxLayout(group3)
    g3.setContentsMargins(16, 24, 16, 16)
    g3.setSpacing(8)

    outer_sec = CollapsibleSection("Parent Section", "mdi6.folder-outline")

    child1 = CollapsibleSection("Child Section A", "mdi6.file-outline")
    child1_label = QtWidgets.QLabel("Content inside child A.")
    child1_label.setStyleSheet(f"color: {p['text']}; background: transparent;")
    child1.addContent(child1_label)

    child2 = CollapsibleSection("Child Section B", "mdi6.file-outline")
    child2_label = QtWidgets.QLabel("Content inside child B.")
    child2_label.setStyleSheet(f"color: {p['text']}; background: transparent;")
    child2.addContent(child2_label)

    outer_sec.addContent(child1)
    outer_sec.addContent(child2)
    outer_sec.setExpanded(True)

    g3.addWidget(outer_sec)
    layout.addWidget(_neu_group(group3))

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

    title = QtWidgets.QLabel("About Expanders")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    info = QtWidgets.QLabel(
        "Collapsible container controls:\n\n"
        "  • CollapsibleSection – custom animated expand/collapse widget\n"
        "  • QToolBox – built-in Qt collapsible panel widget\n"
        "  • Nested expanders – sections within sections\n\n"
        "Provides three expander themes:\n"
        "  – Default (flat header)\n"
        "  – ExpanderCircle (circular toggle button)\n"
        "  – ExpanderStroke (outlined toggle)"
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
