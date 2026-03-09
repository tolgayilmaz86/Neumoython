"""Dynamic showcase builder – reads from the widget registry and installs
menu buttons, stacked-widget pages, and a welcome home page.

Applies neumorphic BoxShadow effects to cards and key UI elements."""

from __future__ import annotations

import qtawesome as qta

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QVBoxLayout, QLabel

from widgets.registry import registry
from widgets.box_shadow import BoxShadowWrapper
from styles.theme_manager import theme_manager, ACCENT_PURPLE, ACCENT_BLUE, ACCENT_TEAL, ACCENT_CORAL, ACCENT_PINK

# ---------------------------------------------------------------------------
# Page transition helpers
# ---------------------------------------------------------------------------

def _fade_to(widget: QtWidgets.QWidget, start: float, end: float,
             duration: int = 140) -> None:
    """Fade *widget* opacity from *start* to *end* over *duration* ms."""
    effect = QtWidgets.QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)
    anim = QtCore.QPropertyAnimation(effect, b"opacity", widget)
    anim.setStartValue(start)
    anim.setEndValue(end)
    anim.setDuration(duration)
    anim.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
    anim.finished.connect(lambda: widget.setGraphicsEffect(None))
    anim.start(QtCore.QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_showcase(main_window) -> None:
    """Build the entire showcase UI from the widget registry."""
    ui = main_window.ui

    # Hide the old hardcoded menu frames (Home, Bug, Cloud, Android)
    for name in ("frame_home", "frame_bug", "frame_cloud", "frame_android"):
        frame = getattr(ui, name, None)
        if frame:
            frame.hide()

    # Also hide the dynamically-added frame_widgets from the old showcase
    frame_widgets_old = getattr(ui, "frame_widgets", None)
    if frame_widgets_old:
        frame_widgets_old.hide()

    # Bookkeeping dicts stored on ui for runtime lookup
    ui._showcase_pages = {}   # demo_id -> (page_widget, about_widget | None)
    ui._showcase_frames = {}  # demo_id -> menu QFrame
    ui._showcase_nav_btns = {}  # demo_id -> nav QPushButton
    ui._current_demo_id = "home"

    # Locate the spacer frame for insertion order
    spacer_frame = getattr(ui, "frame_8", None)
    spacer_idx = ui.verticalLayout_3.indexOf(spacer_frame) if spacer_frame else -1

    # Install home button + page first
    _install_home(main_window, spacer_idx)

    # Install one button + page per registered demo
    insert_pos = (spacer_idx + 1) if spacer_idx >= 0 else -1
    for demo in registry.all():
        _install_demo(main_window, demo, insert_pos)
        if insert_pos >= 0:
            insert_pos += 1

    # Start on the home page
    ui.stackedWidget.setCurrentWidget(ui._showcase_pages["home"][0])
    ui.lab_tab.setText("Home")
    ui._showcase_frames["home"].setProperty("menuState", "active")
    _apply_nav_label_mode(ui, compact=(ui.frame_bottom_west.width() <= 80))


def navigate(main_window, demo_id: str, *, about: bool | None = None) -> None:
    """Navigate to a demo page.

    *about* controls which variant is shown:
      - ``None``  – auto-detect from sidebar width (collapsed → page, expanded → about)
      - ``True``  – force the about/documentation page
      - ``False`` – force the regular demo page
    """
    from windows.window_logic import UIFunction

    ui = main_window.ui
    pages = ui._showcase_pages.get(demo_id)
    frame = ui._showcase_frames.get(demo_id)
    if not pages:
        return

    page, about_page = pages
    if about is None:
        about = ui.frame_bottom_west.width() != 80

    # Clear all menu highlights then activate current
    UIFunction._set_group_state(ui.frame_bottom_west, "menuState")
    if frame:
        frame.setProperty("menuState", "active")
        UIFunction._repolish(frame)

    # Update nav icons: active item gets accent color, others get muted
    _refresh_nav_icons(ui, demo_id)

    if about and about_page:
        ui.stackedWidget.setCurrentWidget(about_page)
        _fade_to(about_page, 0.0, 1.0)
        label = f"About > {_display_name(demo_id)}"
    else:
        ui.stackedWidget.setCurrentWidget(page)
        _fade_to(page, 0.0, 1.0)
        label = _display_name(demo_id)

    ui.lab_tab.setText(label)
    ui._current_demo_id = demo_id


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_ICON_MAP: dict[str, str] = {
    "home":          "mdi6.home-outline",
    "buttons":       "mdi6.gesture-tap-button",
    "toggles":      "mdi6.toggle-switch-outline",
    "inputs":        "mdi6.form-textbox",
    "sliders":      "mdi6.tune-vertical",
    "progress_bars": "mdi6.poll",
    "cards":        "mdi6.card-outline",
    "lists":        "mdi6.format-list-bulleted",
    "tabs":         "mdi6.tab",
    "expanders":    "mdi6.arrow-expand-vertical",
    "icons":        "mdi6.material-design",
    # Phase 3 additions
    "snackbars":    "mdi6.bell-outline",
    "fields":       "mdi6.form-textbox-password",
    "datetime":     "mdi6.calendar-outline",
    "comboboxes":   "mdi6.chevron-down-box-outline",
    "dialogs":      "mdi6.message-outline",
    "menus":        "mdi6.menu",
}

_DEFAULT_ICON = "mdi6.file-document-outline"


def _refresh_nav_icons(ui, active_demo_id: str) -> None:
    """Update all sidebar nav button icons – accent for active, muted for rest."""
    nav_btns = getattr(ui, "_showcase_nav_btns", {})
    for did, btn in nav_btns.items():
        is_active = (did == active_demo_id)
        btn.setIcon(_get_nav_icon(did, active=is_active))
        btn.setIconSize(QtCore.QSize(22, 22))


def _display_name(demo_id: str) -> str:
    if demo_id == "home":
        return "Home"
    demo = registry.get(demo_id)
    return demo.name if demo else demo_id


def _get_nav_icon(demo_id: str, active: bool = False, size: int = 20) -> QtGui.QIcon:
    """Get a qtawesome Material Design icon for a demo_id."""
    icon_name = _ICON_MAP.get(demo_id, _DEFAULT_ICON)
    p = theme_manager.palette
    color = p["accent"] if active else p["text_muted"]
    return qta.icon(icon_name, color=color)


def _make_menu_frame(parent, object_suffix: str, tooltip: str,
                     icon: QtGui.QIcon, label_text: str = "") -> tuple[QFrame, QPushButton]:
    """Create a sidebar nav item with icon and label text."""
    frame = QFrame(parent)
    frame.setObjectName(f"frame_{object_suffix}")
    frame.setMinimumSize(QtCore.QSize(80, 48))
    frame.setMaximumSize(QtCore.QSize(16777215, 48))
    frame.setFrameShape(QFrame.Shape.NoFrame)

    layout = QHBoxLayout(frame)
    layout.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 0)

    btn = QPushButton(frame)
    btn.setObjectName(f"bn_{object_suffix}")
    btn.setMinimumSize(QtCore.QSize(80, 48))
    btn.setMaximumSize(QtCore.QSize(16777215, 48))
    btn.setToolTip(tooltip)
    btn.setFlat(True)
    btn.setProperty("fullLabel", label_text)
    btn.setText(f"  {label_text}" if label_text else "")
    btn.setIcon(icon)
    btn.setIconSize(QtCore.QSize(22, 22))
    layout.addWidget(btn)
    return frame, btn


def _apply_nav_label_mode(ui, compact: bool) -> None:
    """Toggle nav button labels for compact (icon-only) vs expanded mode."""
    for btn in getattr(ui, "_showcase_nav_btns", {}).values():
        full_label = btn.property("fullLabel") or ""
        btn.setText("" if compact else f"  {full_label}")


def set_nav_compact(main_window, compact: bool) -> None:
    """Public helper used by window logic when sidebar is collapsed/expanded."""
    _apply_nav_label_mode(main_window.ui, compact)


def _install_home(main_window, spacer_idx: int) -> None:
    ui = main_window.ui
    icon = _get_nav_icon("home", active=True)
    frame, btn = _make_menu_frame(ui.frame_bottom_west, "showcase_home", "Home", icon, "Home")

    if spacer_idx >= 0:
        ui.verticalLayout_3.insertWidget(spacer_idx, frame)
    else:
        ui.verticalLayout_3.addWidget(frame)

    page = _build_home_page(main_window)
    page.setObjectName("page_showcase_home")
    ui.stackedWidget.addWidget(page)

    about = _build_about_home_page()
    about.setObjectName("page_about_showcase_home")
    ui.stackedWidget.addWidget(about)

    btn.clicked.connect(lambda: navigate(main_window, "home"))

    ui._showcase_frames["home"] = frame
    ui._showcase_nav_btns["home"] = btn
    ui._showcase_pages["home"] = (page, about)


def _install_demo(main_window, demo, insert_idx: int) -> None:
    ui = main_window.ui
    icon = _get_nav_icon(demo.id)
    frame, btn = _make_menu_frame(ui.frame_bottom_west,
                                  f"demo_{demo.id}", demo.name, icon, demo.name)

    if insert_idx >= 0:
        ui.verticalLayout_3.insertWidget(insert_idx, frame)
    else:
        ui.verticalLayout_3.addWidget(frame)

    page = demo.create_page()
    page.setObjectName(f"page_demo_{demo.id}")
    ui.stackedWidget.addWidget(page)

    about = None
    if demo.create_about:
        about = demo.create_about()
        about.setObjectName(f"page_about_demo_{demo.id}")
        ui.stackedWidget.addWidget(about)

    btn.clicked.connect(lambda checked=False, d=demo.id: navigate(main_window, d))

    ui._showcase_frames[demo.id] = frame
    ui._showcase_nav_btns[demo.id] = btn
    ui._showcase_pages[demo.id] = (page, about)


# ---------------------------------------------------------------------------
# Home page builders
# ---------------------------------------------------------------------------

def _build_home_page(main_window) -> QtWidgets.QWidget:
    """Welcome page with clickable cards for each registered demo."""
    page = QtWidgets.QWidget()
    outer = QVBoxLayout(page)
    outer.setSpacing(20)
    outer.setContentsMargins(32, 28, 32, 24)

    p = theme_manager.palette

    title = QtWidgets.QLabel("Neumorphism Widget Showcase")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(22)
    font.setBold(True)
    title.setFont(font)
    outer.addWidget(title)

    subtitle = QtWidgets.QLabel(
        "A template library of reusable PySide6 widgets with "
        "soft neumorphic design.\nSelect a category below to explore."
    )
    subtitle.setWordWrap(True)
    subtitle.setProperty("subheading", True)
    sub_font = subtitle.font()
    sub_font.setPointSize(11)
    subtitle.setFont(sub_font)
    outer.addWidget(subtitle)

    outer.addSpacing(8)

    # --- Accent colour picker row ---
    accent_row = QtWidgets.QWidget()
    accent_layout = QtWidgets.QHBoxLayout(accent_row)
    accent_layout.setContentsMargins(0, 0, 0, 0)
    accent_layout.setSpacing(10)

    accent_label = QtWidgets.QLabel("Accent colour:")
    accent_label.setStyleSheet("font-size: 12px; font-weight: 600;")
    accent_layout.addWidget(accent_label)

    _ACCENT_PRESETS = [
        ("Purple",  ACCENT_PURPLE,  "#9C27B0"),
        ("Blue",    ACCENT_BLUE,    "#1976D2"),
        ("Teal",    ACCENT_TEAL,    "#00897B"),
        ("Coral",   ACCENT_CORAL,   "#E64A19"),
        ("Pink",    ACCENT_PINK,    "#E91E63"),
    ]
    for label_text, color_hex, _ in _ACCENT_PRESETS:
        dot = QPushButton()
        dot.setFixedSize(28, 28)
        dot.setToolTip(f"{label_text}  {color_hex}")
        dot.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        dot.setStyleSheet(
            f"QPushButton {{ background: {color_hex}; border-radius: 14px; border: none; }}"
            f"QPushButton:hover {{ border: 2px solid #FFFFFF; }}"
        )
        dot.clicked.connect(
            lambda checked=False, c=color_hex, mw=main_window: _apply_accent(c, mw)
        )
        accent_layout.addWidget(dot)

    accent_layout.addStretch()
    outer.addWidget(accent_row)

    outer.addSpacing(12)

    scroll = QtWidgets.QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.Shape.NoFrame)

    grid_widget = QtWidgets.QWidget()
    grid = QtWidgets.QGridLayout(grid_widget)
    grid.setSpacing(24)
    grid.setContentsMargins(4, 4, 4, 4)

    demos = registry.all()
    cols = 3
    for i, demo in enumerate(demos):
        card = _make_card(demo, main_window)
        grid.addWidget(card, i // cols, i % cols)

    # Fill remainder of last row so cards don't stretch
    remainder = len(demos) % cols
    if remainder:
        for j in range(remainder, cols):
            spacer = QtWidgets.QWidget()
            grid.addWidget(spacer, (len(demos) - 1) // cols, j)

    grid.setRowStretch(len(demos) // cols + 1, 1)
    scroll.setWidget(grid_widget)
    outer.addWidget(scroll)
    return page


def _make_card(demo, main_window) -> QtWidgets.QWidget:
    card = QFrame()
    card.setObjectName("showcase_card")
    card.setFrameShape(QFrame.Shape.NoFrame)
    card.setMinimumSize(220, 150)
    card.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

    p = theme_manager.palette

    layout = QVBoxLayout(card)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(10)

    # Icon in an accent circle
    icon_name = _ICON_MAP.get(demo.id, _DEFAULT_ICON)
    icon_widget = QtWidgets.QLabel()
    icon_widget.setPixmap(qta.icon(icon_name, color=p['accent']).pixmap(36, 36))
    icon_widget.setFixedSize(52, 52)
    icon_widget.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    icon_widget.setStyleSheet(
        f"background: {p['bg']}; border-radius: 26px;"
    )
    layout.addWidget(icon_widget)

    layout.addSpacing(4)

    name_label = QtWidgets.QLabel(demo.name)
    name_label.setProperty("heading", True)
    name_font = name_label.font()
    name_font.setPointSize(14)
    name_font.setBold(True)
    name_label.setFont(name_font)
    layout.addWidget(name_label)

    if demo.description:
        desc = QtWidgets.QLabel(demo.description)
        desc.setWordWrap(True)
        desc.setProperty("subheading", True)
        desc_font = desc.font()
        desc_font.setPointSize(10)
        desc.setFont(desc_font)
        layout.addWidget(desc)

    layout.addStretch()

    # "Explore →" link
    explore = QtWidgets.QLabel(f"Explore  →")
    explore.setStyleSheet(f"color: {p['accent']}; background: transparent; font-size: 12px; font-weight: 600;")
    layout.addWidget(explore)

    # Wrap in BoxShadowWrapper for neumorphic raised effect
    shadows = theme_manager.shadow_configs()
    wrapper = BoxShadowWrapper(
        card,
        shadow_list=shadows["outside_raised"],
        smooth=True,
        margins=(14, 14, 14, 14),
    )

    demo_id = demo.id
    card.mousePressEvent = lambda event, d=demo_id: navigate(main_window, d, about=False)
    return wrapper


def _apply_accent(color_hex: str, main_window) -> None:
    """Change the global accent colour and re-apply QSS + refresh nav icons."""
    theme_manager.set_accent(color_hex)
    theme_manager.apply()
    _refresh_nav_icons(main_window.ui, main_window.ui._current_demo_id)


def _build_about_home_page() -> QtWidgets.QWidget:
    page = QtWidgets.QWidget()
    layout = QVBoxLayout(page)
    layout.setContentsMargins(32, 28, 32, 24)

    title = QtWidgets.QLabel("About Widget Showcase")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    text = QtWidgets.QLabel(
        "This application is a showcase and template library for PySide6 widgets.\n\n"
        "Adding a new widget demo:\n"
        "  1. Create your widget class in  widgets/\n"
        "  2. Create a demo module in  widgets/catalog/\n"
        "  3. Register it with the WidgetRegistry\n"
        "  4. Restart the app \u2014 it appears automatically!\n\n"
        "Users can import any widget independently:\n"
        "  from widgets.progress_widgets import roundProgressBar"
    )
    text.setWordWrap(True)
    layout.addWidget(text)
    layout.addStretch()
    return page
