"""Menus demo – QMenuBar, context menus, and QToolBar with neumorphic theming.
"""

from __future__ import annotations

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


def _menu_qss() -> str:
    p = theme_manager.palette
    return f"""
        QMenuBar {{
            background: {p['bg_secondary']};
            color: {p['text']};
            padding: 2px 4px;
            border-radius: 10px;
        }}
        QMenuBar::item {{
            background: transparent;
            padding: 6px 14px;
            border-radius: 8px;
        }}
        QMenuBar::item:selected {{
            background: {p['menu_hover']};
            color: {p['text_heading']};
        }}
        QMenuBar::item:pressed {{
            background: {p['menu_active']};
        }}
        QMenu {{
            background: {p['card_bg']};
            color: {p['text']};
            border: none;
            border-radius: 12px;
            padding: 6px 0;
        }}
        QMenu::item {{
            padding: 8px 32px 8px 16px;
            border-radius: 8px;
            margin: 2px 6px;
        }}
        QMenu::item:selected {{
            background: {p['accent']};
            color: #FFFFFF;
        }}
        QMenu::item:disabled {{
            color: {p['text_muted']};
        }}
        QMenu::separator {{
            height: 1px;
            background: {p['bg_secondary']};
            margin: 4px 10px;
        }}
        QMenu::indicator {{
            width: 16px;
            height: 16px;
            left: 8px;
        }}
        QMenu::indicator:checked {{
            image: none;
        }}
        QMenu::right-arrow {{
            width: 14px;
            height: 14px;
        }}
        QToolBar {{
            background: {p['bg_secondary']};
            border: none;
            border-radius: 12px;
            spacing: 4px;
            padding: 4px 8px;
        }}
        QToolBar::separator {{
            background: {p['bg']};
            width: 1px;
            margin: 6px 4px;
        }}
        QToolButton {{
            background: transparent;
            border: none;
            border-radius: 8px;
            padding: 6px;
        }}
        QToolButton:hover {{
            background: {p['menu_hover']};
        }}
        QToolButton:pressed {{
            background: {p['menu_active']};
        }}
        QToolButton:checked {{
            background: {p['accent']}30;
            color: {p['accent']};
        }}
    """


# ---------------------------------------------------------------------------
# Page builder
# ---------------------------------------------------------------------------

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

    p = theme_manager.palette

    # Apply menu QSS to the inner widget (so sub-widgets inherit)
    inner.setStyleSheet(inner.styleSheet() + _menu_qss())

    title = QtWidgets.QLabel("Menus")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    desc = QtWidgets.QLabel(
        "Menu bar, context menus, and tool bar with neumorphic theming. "
        "Supports icons, checkable items, submenus, separators, and disabled items."
    )
    desc.setWordWrap(True)
    desc.setProperty("subheading", True)
    layout.addWidget(desc)

    action_log = QtWidgets.QLabel("Action: —")
    action_log.setStyleSheet(
        f"color: {p['accent']}; font-size: 12px; background: transparent; font-weight: 600;"
    )

    def _log(text: str) -> None:
        action_log.setText(f"Action: {text}")

    # --- MenuBar ---
    group1 = QtWidgets.QGroupBox("Menu Bar")
    g1 = QtWidgets.QVBoxLayout(group1)
    g1.setContentsMargins(16, 24, 16, 16)
    g1.setSpacing(12)

    menubar = QtWidgets.QMenuBar()

    # File menu
    file_menu = menubar.addMenu(
        qta.icon("mdi6.file-outline", color=p["text"]), " File")
    for label, ico in [
        ("New",   "mdi6.file-plus-outline"),
        ("Open",  "mdi6.folder-open-outline"),
        ("Save",  "mdi6.content-save-outline"),
        ("Save As…", "mdi6.content-save-edit-outline"),
    ]:
        act = QtGui.QAction(qta.icon(ico, color=p["text"]), label, menubar)
        act.triggered.connect(lambda checked=False, t=label: _log(t))
        file_menu.addAction(act)
    file_menu.addSeparator()
    export = file_menu.addMenu(
        qta.icon("mdi6.export", color=p["text"]), "Export")
    for fmt in ("PDF", "PNG", "CSV"):
        sub_act = QtGui.QAction(fmt, menubar)
        sub_act.triggered.connect(lambda checked=False, t=fmt: _log(f"Export {t}"))
        export.addAction(sub_act)
    file_menu.addSeparator()
    quit_act = QtGui.QAction(
        qta.icon("mdi6.exit-to-app", color="#D32F2F"), "Exit", menubar)
    quit_act.triggered.connect(lambda: _log("Exit"))
    file_menu.addAction(quit_act)

    # Edit menu
    edit_menu = menubar.addMenu(
        qta.icon("mdi6.pencil-outline", color=p["text"]), " Edit")
    for label, ico, shortcut in [
        ("Cut",    "mdi6.scissors-cutting", "Ctrl+X"),
        ("Copy",   "mdi6.content-copy",     "Ctrl+C"),
        ("Paste",  "mdi6.content-paste",    "Ctrl+V"),
    ]:
        act = QtGui.QAction(qta.icon(ico, color=p["text"]), label, menubar)
        act.setShortcut(shortcut)
        act.triggered.connect(lambda checked=False, t=label: _log(t))
        edit_menu.addAction(act)
    edit_menu.addSeparator()
    disabled_act = QtGui.QAction("Undo (disabled)", menubar)
    disabled_act.setEnabled(False)
    edit_menu.addAction(disabled_act)

    # View menu (checkable items)
    view_menu = menubar.addMenu(
        qta.icon("mdi6.eye-outline", color=p["text"]), " View")
    for label in ("Show Toolbar", "Show Status Bar", "Show Sidebar"):
        act = QtGui.QAction(label, menubar)
        act.setCheckable(True)
        act.setChecked(True)
        act.triggered.connect(
            lambda checked, t=label: _log(
                f"{'Show' if checked else 'Hide'} {t.split()[-1]}"))
        view_menu.addAction(act)

    g1.addWidget(menubar)
    g1.addWidget(action_log)
    layout.addWidget(_neu_group(group1))

    # --- Context menu ---
    group2 = QtWidgets.QGroupBox("Context Menu (right-click the box below)")
    g2 = QtWidgets.QVBoxLayout(group2)
    g2.setContentsMargins(16, 24, 16, 16)
    g2.setSpacing(12)

    ctx_area = QtWidgets.QLabel("Right-click anywhere here to open the context menu.")
    ctx_area.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    ctx_area.setMinimumHeight(80)
    ctx_area.setStyleSheet(f"""
        background: {p['input_bg']};
        border: 2px dashed {p['text_muted']};
        border-radius: 12px;
        color: {p['text_muted']};
        font-size: 12px;
        padding: 8px;
    """)
    ctx_area.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)

    def _show_context(pos: QtCore.QPoint) -> None:
        menu = QtWidgets.QMenu(ctx_area)
        menu.setStyleSheet(_menu_qss())
        for label, ico in [
            ("Cut",    "mdi6.scissors-cutting"),
            ("Copy",   "mdi6.content-copy"),
            ("Paste",  "mdi6.content-paste"),
        ]:
            act = menu.addAction(qta.icon(ico, color=p["text"]), label)
            act.triggered.connect(lambda checked=False, t=label: _log(f"Context: {t}"))
        menu.addSeparator()
        prop_act = menu.addAction(
            qta.icon("mdi6.information-outline", color=p["text"]), "Properties…")
        prop_act.triggered.connect(lambda: _log("Context: Properties"))
        disabled_ctx = menu.addAction("Not Available")
        disabled_ctx.setEnabled(False)
        menu.addSeparator()
        submenu = menu.addMenu(
            qta.icon("mdi6.sort-ascending", color=p["text"]), "Sort By")
        for key in ("Name", "Date", "Size", "Type"):
            sub_act = submenu.addAction(key)
            sub_act.triggered.connect(lambda checked=False, k=key: _log(f"Sort: {k}"))
        menu.exec(ctx_area.mapToGlobal(pos))

    ctx_area.customContextMenuRequested.connect(_show_context)

    g2.addWidget(ctx_area)
    layout.addWidget(_neu_group(group2))

    # --- ToolBar ---
    group3 = QtWidgets.QGroupBox("Tool Bar")
    g3 = QtWidgets.QVBoxLayout(group3)
    g3.setContentsMargins(16, 24, 16, 16)
    g3.setSpacing(12)

    toolbar = QtWidgets.QToolBar()
    toolbar.setIconSize(QtCore.QSize(20, 20))
    toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

    for ico, label in [
        ("mdi6.file-plus-outline",       "New"),
        ("mdi6.folder-open-outline",     "Open"),
        ("mdi6.content-save-outline",    "Save"),
    ]:
        act = QtGui.QAction(qta.icon(ico, color=p["text"]), label)
        act.triggered.connect(lambda checked=False, t=label: _log(f"Toolbar: {t}"))
        toolbar.addAction(act)

    toolbar.addSeparator()

    for ico, label, checkable in [
        ("mdi6.format-bold",    "Bold",    True),
        ("mdi6.format-italic",  "Italic",  True),
        ("mdi6.format-underline", "Underline", True),
    ]:
        act = QtGui.QAction(qta.icon(ico, color=p["text"]), label)
        act.setCheckable(checkable)
        act.triggered.connect(lambda checked, t=label: _log(f"Toolbar: {t}"))
        toolbar.addAction(act)

    toolbar.addSeparator()

    for ico, label in [
        ("mdi6.format-align-left",   "Left"),
        ("mdi6.format-align-center", "Center"),
        ("mdi6.format-align-right",  "Right"),
    ]:
        act = QtGui.QAction(qta.icon(ico, color=p["text"]), label)
        act.setCheckable(True)
        act.triggered.connect(lambda checked, t=label: _log(f"Align: {t}"))
        toolbar.addAction(act)

    g3.addWidget(toolbar)
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

    title = QtWidgets.QLabel("About Menus")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    info = QtWidgets.QLabel(
        "Menu and toolbar widgets:\n\n"
        "  • QMenuBar – application menu bar with File / Edit / View menus\n"
        "  • QMenu – context menu with icons, separators, submenus\n"
        "  • Checkable items – toggle state persists across opens\n"
        "  • Disabled items – greyed-out non-interactive entries\n"
        "  • QToolBar – icon + text buttons with separator and checkable actions\n\n"
        "All styled via _menu_qss() which reads from ThemeManager.palette "
        "to match the active light/dark theme."
    )
    info.setWordWrap(True)
    layout.addWidget(info)
    layout.addStretch()
    return page


registry.register(WidgetDemo(
    id="menus",
    name="Menus",
    create_page=create_page,
    create_about=create_about,
    description="Menu bar, context menus, and toolbar with neumorphic theming.",
))
