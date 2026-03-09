"""Menus demo – nine menu-bar variants (matching Neumorphism.Avalonia),
context menus, and tool bar with neumorphic theming.

Qt's QMenuBar::item ignores per-side borders / gradients, so we build
custom button-bar widgets for the capsule / outlined variants using
QToolButton + BoxShadow, which gives full visual control.
"""

from __future__ import annotations

import qtawesome as qta
from PySide6 import QtCore, QtGui, QtWidgets

from widgets.registry import registry, WidgetDemo
from widgets.box_shadow import BoxShadow, BoxShadowWrapper
from styles.theme_manager import theme_manager


# ── Helpers ──────────────────────────────────────────────────────────────────

def _neu_group(group: QtWidgets.QGroupBox) -> BoxShadowWrapper:
    shadows = theme_manager.shadow_configs()
    return BoxShadowWrapper(
        group, shadow_list=shadows["outside_raised"],
        smooth=True, margins=(12, 12, 12, 12),
    )


def _section_label(text: str) -> QtWidgets.QLabel:
    p = theme_manager.palette
    lbl = QtWidgets.QLabel(text)
    lbl.setStyleSheet(
        f"font-size: 15px; font-weight: 700; color: {p['text_heading']}; "
        "background: transparent; margin-top: 8px; margin-bottom: 2px;"
    )
    return lbl


def _popup_qss() -> str:
    """Shared QSS for QMenu popups."""
    p = theme_manager.palette
    return f"""
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
    """


def _make_menu(parent: QtWidgets.QWidget, log_fn) -> QtWidgets.QMenu:
    """Build a standard File-like context menu attached to *parent*."""
    p = theme_manager.palette
    menu = QtWidgets.QMenu(parent)
    menu.setStyleSheet(_popup_qss())
    for label, ico in [
        ("New", "mdi6.file-plus-outline"),
        ("Open", "mdi6.folder-open-outline"),
        ("Save", "mdi6.content-save-outline"),
    ]:
        act = menu.addAction(qta.icon(ico, color=p["text"]), label)
        act.triggered.connect(lambda c=False, t=label: log_fn(t))
    menu.addSeparator()
    exp = menu.addMenu(qta.icon("mdi6.export", color=p["text"]), "Export")
    exp.setStyleSheet(_popup_qss())
    for fmt in ("PDF", "PNG", "CSV"):
        a = exp.addAction(fmt)
        a.triggered.connect(lambda c=False, t=fmt: log_fn(f"Export {t}"))
    return menu


# ── _MenuButton: a QToolButton capsule with attached QMenu ──────────────────

class _MenuButton(QtWidgets.QToolButton):
    """A QToolButton that opens a QMenu; fully stylable with QSS.

    Set *variant* to apply a dynamic property ``menuVariant`` so that
    QSS selectors like ``QToolButton[menuVariant="flat"]`` can override
    the global QToolButton rules from theme_manager.
    """

    def __init__(self, label: str, icon_name: str, log_fn,
                 qss: str = "", variant: str = "", parent=None):
        super().__init__(parent)
        p = theme_manager.palette
        self.setText(f" {label}")
        self.setIcon(qta.icon(icon_name, color=p["text"]))
        self.setIconSize(QtCore.QSize(16, 16))
        self.setToolButtonStyle(
            QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.setPopupMode(
            QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
        if variant:
            self.setProperty("menuVariant", variant)
        if qss:
            self.setStyleSheet(qss)
        self.setMenu(_make_menu(self, log_fn))


def _menu_buttons(labels: list[tuple[str, str]], log_fn,
                  qss: str, variant: str = "") -> list[_MenuButton]:
    """Create a list of _MenuButton widgets with the same QSS."""
    return [_MenuButton(lbl, ico, log_fn, qss, variant) for lbl, ico in labels]


_MENU_LABELS: list[tuple[str, str]] = [
    ("File", "mdi6.file-outline"),
    ("Edit", "mdi6.pencil-outline"),
    ("View", "mdi6.eye-outline"),
]


# ── Custom menu bar: row of _MenuButton laid out in HBoxLayout ──────────────

def _build_custom_bar(log_fn, buttons: list[_MenuButton],
                      bar_qss: str = "") -> QtWidgets.QFrame:
    """Lay *buttons* out horizontally inside a rounded QFrame."""
    bar = QtWidgets.QFrame()
    bar.setFixedHeight(40)
    if bar_qss:
        bar.setStyleSheet(bar_qss)
    h = QtWidgets.QHBoxLayout(bar)
    h.setContentsMargins(6, 4, 6, 4)
    h.setSpacing(6)
    for btn in buttons:
        h.addWidget(btn)
    h.addStretch()
    return bar


# ── Row-1 variant builders ──────────────────────────────────────────────────

def _build_default_bar(log_fn) -> QtWidgets.QWidget:
    """1) Default neumorphic – a real QMenuBar with basic styling."""
    p = theme_manager.palette
    mb = QtWidgets.QMenuBar()
    qss = f"""
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
    """
    mb.setStyleSheet(qss)

    for label, ico in _MENU_LABELS:
        menu = mb.addMenu(qta.icon(ico, color=p["text"]), f" {label}")
        menu.setStyleSheet(_popup_qss())
        _fill_menu(menu, log_fn)
    return mb


def _fill_menu(menu: QtWidgets.QMenu, log_fn) -> None:
    """Populate a QMenu with sample actions."""
    p = theme_manager.palette
    for lbl, ico in [
        ("New", "mdi6.file-plus-outline"),
        ("Open", "mdi6.folder-open-outline"),
        ("Save", "mdi6.content-save-outline"),
    ]:
        act = menu.addAction(qta.icon(ico, color=p["text"]), lbl)
        act.triggered.connect(lambda c=False, t=lbl: log_fn(t))
    menu.addSeparator()
    dis = menu.addAction("Disabled")
    dis.setEnabled(False)


def _build_capsule_outset_bar(log_fn) -> QtWidgets.QWidget:
    """2) Capsule Outset – each button is a raised neumorphic pill."""
    p = theme_manager.palette
    shadows = theme_manager.shadow_configs()

    bar = QtWidgets.QFrame()
    bar.setObjectName("menuBarOutset")
    bar.setFixedHeight(52)
    bar.setStyleSheet(f"""
        #menuBarOutset {{
            background: {p['bg']};
            border-radius: 16px;
        }}
        #menuBarOutset QToolButton {{
            background: {p['bg']};
            color: {p['text']};
            border: none;
            border-radius: 14px;
            padding: 6px 16px;
            font-size: 13px;
        }}
        #menuBarOutset QToolButton:hover {{
            background: {p['menu_hover']};
            color: {p['text_heading']};
        }}
        #menuBarOutset QToolButton::menu-indicator {{ image: none; }}
    """)
    h = QtWidgets.QHBoxLayout(bar)
    h.setContentsMargins(8, 6, 8, 6)
    h.setSpacing(10)

    for label, ico in _MENU_LABELS:
        btn = _MenuButton(label, ico, log_fn)
        wrapped = BoxShadowWrapper(
            btn, shadow_list=shadows["button_raised"],
            smooth=True, margins=(4, 4, 4, 4),
        )
        h.addWidget(wrapped)
    h.addStretch()
    return bar


def _build_capsule_inset_bar(log_fn) -> QtWidgets.QWidget:
    """3) Capsule Inset – each button appears pressed / sunken."""
    p = theme_manager.palette
    shadows = theme_manager.shadow_configs()

    bar = QtWidgets.QFrame()
    bar.setObjectName("menuBarInset")
    bar.setFixedHeight(52)
    bar.setStyleSheet(f"""
        #menuBarInset {{
            background: {p['bg']};
            border-radius: 16px;
        }}
        #menuBarInset QToolButton {{
            background: {p['bg']};
            color: {p['text']};
            border: none;
            border-radius: 14px;
            padding: 6px 16px;
            font-size: 13px;
        }}
        #menuBarInset QToolButton:hover {{
            color: {p['text_heading']};
        }}
        #menuBarInset QToolButton::menu-indicator {{ image: none; }}
    """)
    h = QtWidgets.QHBoxLayout(bar)
    h.setContentsMargins(8, 6, 8, 6)
    h.setSpacing(10)

    for label, ico in _MENU_LABELS:
        btn = _MenuButton(label, ico, log_fn)
        wrapped = BoxShadowWrapper(
            btn, shadow_list=shadows["button_pressed"],
            smooth=True, margins=(4, 4, 4, 4),
        )
        h.addWidget(wrapped)
    h.addStretch()
    return bar


# ── Row-2 variant builders ──────────────────────────────────────────────────

def _build_capsule_flat_bar(log_fn) -> QtWidgets.QWidget:
    """4) Capsule Flat – no depth, accent tint on hover."""
    p = theme_manager.palette
    bar = QtWidgets.QFrame()
    bar.setObjectName("menuBarFlat")
    bar.setFixedHeight(40)
    bar.setStyleSheet(f"""
        #menuBarFlat {{
            background: {p['bg']};
            border-radius: 20px;
        }}
        #menuBarFlat QToolButton {{
            background: transparent;
            color: {p['text']};
            border: none;
            border-radius: 14px;
            padding: 6px 16px;
            font-size: 13px;
        }}
        #menuBarFlat QToolButton:hover {{
            background: {p['accent']}28;
            color: {p['accent']};
        }}
        #menuBarFlat QToolButton::menu-indicator {{ image: none; }}
    """)
    h = QtWidgets.QHBoxLayout(bar)
    h.setContentsMargins(6, 4, 6, 4)
    h.setSpacing(6)
    for lbl, ico in _MENU_LABELS:
        h.addWidget(_MenuButton(lbl, ico, log_fn))
    h.addStretch()
    return bar


def _build_minimal_bar(log_fn) -> QtWidgets.QWidget:
    """5) Minimal – transparent, accent underline on hover."""
    p = theme_manager.palette
    bar = QtWidgets.QFrame()
    bar.setObjectName("menuBarMinimal")
    bar.setFixedHeight(40)
    bar.setStyleSheet(f"""
        #menuBarMinimal {{
            background: transparent;
        }}
        #menuBarMinimal QToolButton {{
            background: transparent;
            color: {p['text']};
            border: none;
            border-bottom: 2px solid transparent;
            border-radius: 0px;
            padding: 6px 14px 4px 14px;
            font-size: 13px;
        }}
        #menuBarMinimal QToolButton:hover {{
            background: transparent;
            color: {p['accent']};
            border-bottom: 2px solid {p['accent']};
            border-radius: 0px;
        }}
        #menuBarMinimal QToolButton::menu-indicator {{ image: none; }}
    """)
    h = QtWidgets.QHBoxLayout(bar)
    h.setContentsMargins(6, 4, 6, 4)
    h.setSpacing(6)
    for lbl, ico in _MENU_LABELS:
        h.addWidget(_MenuButton(lbl, ico, log_fn))
    h.addStretch()
    return bar


def _build_stroked_bar(log_fn) -> QtWidgets.QWidget:
    """6) Stroked / Outlined – visible border, accent on hover."""
    p = theme_manager.palette
    bar = QtWidgets.QFrame()
    bar.setObjectName("menuBarStroked")
    bar.setFixedHeight(40)
    bar.setStyleSheet(f"""
        #menuBarStroked {{
            background: transparent;
        }}
        #menuBarStroked QToolButton {{
            background: transparent;
            color: {p['text']};
            border: 2px solid {p['text_muted']};
            border-radius: 10px;
            padding: 5px 14px;
            font-size: 13px;
        }}
        #menuBarStroked QToolButton:hover {{
            border: 2px solid {p['accent']};
            color: {p['accent']};
            background: {p['accent']}14;
        }}
        #menuBarStroked QToolButton::menu-indicator {{ image: none; }}
    """)
    h = QtWidgets.QHBoxLayout(bar)
    h.setContentsMargins(6, 4, 6, 4)
    h.setSpacing(6)
    for lbl, ico in _MENU_LABELS:
        h.addWidget(_MenuButton(lbl, ico, log_fn))
    h.addStretch()
    return bar


# ── Row-3 custom button classes ─────────────────────────────────────────────

class _AvatarMenuButton(QtWidgets.QToolButton):
    """Circular avatar button that shows a QMenu on click."""

    def __init__(self, log_fn, parent=None):
        super().__init__(parent)
        p = theme_manager.palette
        self.setFixedSize(64, 64)
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.setPopupMode(
            QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
        self.setToolTip("Avatar profile menu")
        self.setStyleSheet(f"""
            QToolButton {{
                background: {p['accent']};
                border-radius: 32px;
                border: 3px solid {p['bg_secondary']};
            }}
            QToolButton:hover {{
                border-color: {p['accent_hover']};
            }}
            QToolButton::menu-indicator {{ image: none; }}
        """)
        self.setIcon(qta.icon("mdi6.account", color="#FFFFFF"))
        self.setIconSize(QtCore.QSize(32, 32))

        menu = QtWidgets.QMenu(self)
        menu.setStyleSheet(_popup_qss())
        for label, ico in [
            ("Hello !", "mdi6.hand-wave-outline"),
            (None, None),
            ("Follow us", "mdi6.share-variant-outline"),
            (None, None),
            ("About", "mdi6.information-outline"),
            (None, None),
            ("Goodbye", "mdi6.exit-to-app"),
        ]:
            if label is None:
                menu.addSeparator()
                continue
            act = menu.addAction(qta.icon(ico, color=p["text"]), label)
            act.triggered.connect(
                lambda c=False, t=label: log_fn(f"Avatar: {t}"))

        follow_items = menu.actions()
        follow_action = follow_items[2]
        follow_sub = QtWidgets.QMenu("Follow us", menu)
        follow_sub.setStyleSheet(_popup_qss())
        for soc in ("Twitter", "Instagram", "Facebook"):
            a = follow_sub.addAction(
                qta.icon(f"mdi6.{soc.lower()}", color=p["text"]), soc)
            a.triggered.connect(
                lambda c=False, t=soc: log_fn(f"Follow: {t}"))
        follow_action.setMenu(follow_sub)
        self.setMenu(menu)


class _HamburgerMenuButton(QtWidgets.QToolButton):
    """Hamburger icon that opens a dropdown menu."""

    def __init__(self, log_fn, parent=None):
        super().__init__(parent)
        p = theme_manager.palette
        self.setFixedSize(40, 40)
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.setPopupMode(
            QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
        self.setToolTip("Hamburger menu")
        self.setIcon(qta.icon("mdi6.menu", color=p["text"]))
        self.setIconSize(QtCore.QSize(24, 24))
        self.setStyleSheet(f"""
            QToolButton {{
                background: transparent;
                border: 2px solid {p['text_muted']};
                border-radius: 8px;
            }}
            QToolButton:hover {{
                background: {p['menu_hover']};
                border-color: {p['accent']};
            }}
            QToolButton::menu-indicator {{ image: none; }}
        """)
        menu = QtWidgets.QMenu(self)
        menu.setStyleSheet(_popup_qss())
        for label, ico in [
            ("Hello !", "mdi6.hand-wave-outline"),
            (None, None),
            ("About", "mdi6.information-outline"),
            (None, None),
            ("Goodbye", "mdi6.exit-to-app"),
        ]:
            if label is None:
                menu.addSeparator()
                continue
            act = menu.addAction(qta.icon(ico, color=p["text"]), label)
            act.triggered.connect(
                lambda c=False, t=label: log_fn(f"Hamburger: {t}"))
        self.setMenu(menu)


class _IconNavButton(QtWidgets.QToolButton):
    """Large icon button with a dropdown (used in icon-nav bar)."""

    def __init__(self, icon_name: str, items: list[tuple[str, str]],
                 log_fn, parent=None):
        super().__init__(parent)
        p = theme_manager.palette
        self.setFixedSize(48, 48)
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.setPopupMode(
            QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
        self.setIcon(qta.icon(icon_name, color=p["text_muted"]))
        self.setIconSize(QtCore.QSize(30, 30))
        self.setStyleSheet(f"""
            QToolButton {{
                background: transparent;
                border: none;
                border-radius: 8px;
            }}
            QToolButton:hover {{
                background: {p['menu_hover']};
            }}
            QToolButton::menu-indicator {{ image: none; }}
        """)
        menu = QtWidgets.QMenu(self)
        menu.setStyleSheet(_popup_qss())
        first = True
        for label, ico in items:
            if not first:
                menu.addSeparator()
            first = False
            act = menu.addAction(qta.icon(ico, color=p["text"]), label)
            act.triggered.connect(
                lambda c=False, t=label: log_fn(f"NavIcon: {t}"))
        self.setMenu(menu)


# ---------------------------------------------------------------------------
# Page builder
# ---------------------------------------------------------------------------

def create_page() -> QtWidgets.QWidget:
    page = QtWidgets.QWidget()
    scroll = QtWidgets.QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

    inner = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(inner)
    layout.setSpacing(16)
    layout.setContentsMargins(24, 24, 24, 24)

    p = theme_manager.palette

    title = QtWidgets.QLabel("Menus")
    title.setProperty("heading", True)
    f = title.font()
    f.setPointSize(20)
    title.setFont(f)
    layout.addWidget(title)

    desc = QtWidgets.QLabel(
        "Nine menu-bar variants inspired by Neumorphism.Avalonia, "
        "plus context menus and a tool bar.  Capsule Outset / Inset "
        "use real BoxShadow effects for neumorphic depth."
    )
    desc.setWordWrap(True)
    desc.setProperty("subheading", True)
    layout.addWidget(desc)

    action_log = QtWidgets.QLabel("Action: —")
    action_log.setStyleSheet(
        f"color: {p['accent']}; font-size: 12px; "
        "background: transparent; font-weight: 600;"
    )

    def _log(text: str) -> None:
        action_log.setText(f"Action: {text}")

    # ── Row 1 ───────────────────────────────────────────────────────────
    layout.addWidget(
        _section_label("Row 1 — Default · Capsule Outset · Capsule Inset"))
    row1 = QtWidgets.QHBoxLayout()
    row1.setSpacing(16)

    # 1) Default
    g1 = QtWidgets.QGroupBox("Default")
    v1 = QtWidgets.QVBoxLayout(g1)
    v1.setContentsMargins(12, 20, 12, 12)
    v1.addWidget(_build_default_bar(_log))
    row1.addWidget(_neu_group(g1))

    # 2) Capsule Outset (raised pills with BoxShadow)
    g2 = QtWidgets.QGroupBox("Capsule Outset")
    v2 = QtWidgets.QVBoxLayout(g2)
    v2.setContentsMargins(12, 20, 12, 12)
    v2.addWidget(_build_capsule_outset_bar(_log))
    row1.addWidget(_neu_group(g2))

    # 3) Capsule Inset (sunken pills with BoxShadow)
    g3 = QtWidgets.QGroupBox("Capsule Inset")
    v3 = QtWidgets.QVBoxLayout(g3)
    v3.setContentsMargins(12, 20, 12, 12)
    v3.addWidget(_build_capsule_inset_bar(_log))
    row1.addWidget(_neu_group(g3))

    layout.addLayout(row1)

    # ── Row 2 ───────────────────────────────────────────────────────────
    layout.addWidget(
        _section_label("Row 2 — Capsule Flat · Minimal · Stroked"))
    row2 = QtWidgets.QHBoxLayout()
    row2.setSpacing(16)

    # 4) Capsule Flat
    g4 = QtWidgets.QGroupBox("Capsule Flat")
    v4 = QtWidgets.QVBoxLayout(g4)
    v4.setContentsMargins(12, 20, 12, 12)
    v4.addWidget(_build_capsule_flat_bar(_log))
    row2.addWidget(_neu_group(g4))

    # 5) Minimal
    g5 = QtWidgets.QGroupBox("Minimal")
    v5 = QtWidgets.QVBoxLayout(g5)
    v5.setContentsMargins(12, 20, 12, 12)
    v5.addWidget(_build_minimal_bar(_log))
    row2.addWidget(_neu_group(g5))

    # 6) Outlined / Stroked
    g6 = QtWidgets.QGroupBox("Outlined / Stroked")
    v6 = QtWidgets.QVBoxLayout(g6)
    v6.setContentsMargins(12, 20, 12, 12)
    v6.addWidget(_build_stroked_bar(_log))
    row2.addWidget(_neu_group(g6))

    layout.addLayout(row2)

    # ── Row 3 ───────────────────────────────────────────────────────────
    layout.addWidget(
        _section_label("Row 3 — Avatar · Hamburger · Icon Nav Bar"))
    row3 = QtWidgets.QHBoxLayout()
    row3.setSpacing(16)

    # 7) Avatar
    g7 = QtWidgets.QGroupBox("Avatar Profile Menu")
    v7 = QtWidgets.QVBoxLayout(g7)
    v7.setContentsMargins(12, 20, 12, 12)
    v7.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    avatar = _AvatarMenuButton(_log)
    shadows = theme_manager.shadow_configs()
    avatar.setGraphicsEffect(BoxShadow(shadows["outside_raised"], smooth=True))
    v7.addWidget(avatar, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
    tip7 = QtWidgets.QLabel("Circular avatar with dropdown")
    tip7.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    tip7.setStyleSheet(
        f"color: {p['text_muted']}; font-size: 11px; background: transparent;")
    v7.addWidget(tip7)
    row3.addWidget(_neu_group(g7))

    # 8) Hamburger
    g8 = QtWidgets.QGroupBox("Hamburger Menu")
    v8 = QtWidgets.QVBoxLayout(g8)
    v8.setContentsMargins(12, 20, 12, 12)
    v8.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    hamburger = _HamburgerMenuButton(_log)
    v8.addWidget(hamburger, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
    tip8 = QtWidgets.QLabel("Icon button \u2261 opens dropdown")
    tip8.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    tip8.setStyleSheet(
        f"color: {p['text_muted']}; font-size: 11px; background: transparent;")
    v8.addWidget(tip8)
    row3.addWidget(_neu_group(g8))

    # 9) Icon Navigation Bar
    g9 = QtWidgets.QGroupBox("Icon Nav Bar")
    v9 = QtWidgets.QVBoxLayout(g9)
    v9.setContentsMargins(12, 20, 12, 12)
    nav_row = QtWidgets.QHBoxLayout()
    nav_row.setSpacing(12)
    nav_row.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    icon_nav_items = [
        ("mdi6.rocket-launch-outline", [
            ("Go to the Moon !", "mdi6.space-invaders"),
            ("Go to Mars !", "mdi6.space-invaders"),
            ("Go to Saturn !", "mdi6.space-invaders"),
        ]),
        ("mdi6.account-outline", [
            ("Create", "mdi6.pencil-outline"),
            ("Disable", "mdi6.stop-circle-outline"),
            ("Lock", "mdi6.lock-outline"),
        ]),
        ("mdi6.shield-account-outline", [
            ("Allow", "mdi6.account-plus-outline"),
            ("Deny", "mdi6.account-remove-outline"),
            ("Default", "mdi6.account-group-outline"),
        ]),
    ]
    for icon_name, items in icon_nav_items:
        nav_row.addWidget(_IconNavButton(icon_name, items, _log))
    v9.addLayout(nav_row)
    tip9 = QtWidgets.QLabel("Multiple icon buttons, each with their own menu")
    tip9.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    tip9.setStyleSheet(
        f"color: {p['text_muted']}; font-size: 11px; background: transparent;")
    v9.addWidget(tip9)
    row3.addWidget(_neu_group(g9))

    layout.addLayout(row3)

    # ── Action log ──────────────────────────────────────────────────────
    layout.addWidget(action_log)

    # ── Context menu ────────────────────────────────────────────────────
    layout.addWidget(_section_label("Context Menu"))
    group_ctx = QtWidgets.QGroupBox("Right-click the area below")
    gc = QtWidgets.QVBoxLayout(group_ctx)
    gc.setContentsMargins(16, 24, 16, 16)

    ctx_area = QtWidgets.QLabel(
        "Right-click anywhere here to open the context menu.")
    ctx_area.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    ctx_area.setMinimumHeight(70)
    ctx_area.setStyleSheet(f"""
        background: {p['input_bg']};
        border: 2px dashed {p['text_muted']};
        border-radius: 12px;
        color: {p['text_muted']};
        font-size: 12px; padding: 8px;
    """)
    ctx_area.setContextMenuPolicy(
        QtCore.Qt.ContextMenuPolicy.CustomContextMenu)

    def _show_context(pos: QtCore.QPoint) -> None:
        menu = QtWidgets.QMenu(ctx_area)
        menu.setStyleSheet(_popup_qss())
        for label, ico in [
            ("Cut", "mdi6.scissors-cutting"),
            ("Copy", "mdi6.content-copy"),
            ("Paste", "mdi6.content-paste"),
        ]:
            act = menu.addAction(qta.icon(ico, color=p["text"]), label)
            act.triggered.connect(
                lambda c=False, t=label: _log(f"Context: {t}"))
        menu.addSeparator()
        menu.addAction(
            qta.icon("mdi6.information-outline", color=p["text"]),
            "Properties…").triggered.connect(
                lambda: _log("Context: Properties"))
        dis_ctx = menu.addAction("Not Available")
        dis_ctx.setEnabled(False)
        menu.addSeparator()
        sub = menu.addMenu(
            qta.icon("mdi6.sort-ascending", color=p["text"]), "Sort By")
        sub.setStyleSheet(_popup_qss())
        for key in ("Name", "Date", "Size", "Type"):
            sa = sub.addAction(key)
            sa.triggered.connect(
                lambda c=False, k=key: _log(f"Sort: {k}"))
        menu.exec(ctx_area.mapToGlobal(pos))

    ctx_area.customContextMenuRequested.connect(_show_context)
    gc.addWidget(ctx_area)
    layout.addWidget(_neu_group(group_ctx))

    # ── Toolbar ─────────────────────────────────────────────────────────
    layout.addWidget(_section_label("Tool Bar"))
    group_tb = QtWidgets.QGroupBox("Toolbar with formatting actions")
    gt = QtWidgets.QVBoxLayout(group_tb)
    gt.setContentsMargins(16, 24, 16, 16)

    toolbar = QtWidgets.QToolBar()
    toolbar.setIconSize(QtCore.QSize(20, 20))
    toolbar.setToolButtonStyle(
        QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    toolbar.setStyleSheet(f"""
        QToolBar {{
            background: {p['bg_secondary']};
            border: none; border-radius: 12px;
            spacing: 4px; padding: 4px 8px;
        }}
        QToolBar::separator {{
            background: {p['bg']}; width: 1px; margin: 6px 4px;
        }}
        QToolButton {{
            background: transparent; border: none;
            border-radius: 8px; padding: 6px; color: {p['text']};
        }}
        QToolButton:hover {{ background: {p['menu_hover']}; }}
        QToolButton:pressed {{ background: {p['menu_active']}; }}
        QToolButton:checked {{
            background: {p['accent']}30; color: {p['accent']};
        }}
    """)

    for ico, label in [
        ("mdi6.file-plus-outline", "New"),
        ("mdi6.folder-open-outline", "Open"),
        ("mdi6.content-save-outline", "Save"),
    ]:
        act = QtGui.QAction(qta.icon(ico, color=p["text"]), label)
        act.triggered.connect(
            lambda c=False, t=label: _log(f"Toolbar: {t}"))
        toolbar.addAction(act)
    toolbar.addSeparator()
    for ico, label in [
        ("mdi6.format-bold", "Bold"),
        ("mdi6.format-italic", "Italic"),
        ("mdi6.format-underline", "Underline"),
    ]:
        act = QtGui.QAction(qta.icon(ico, color=p["text"]), label)
        act.setCheckable(True)
        act.triggered.connect(lambda c, t=label: _log(f"Toolbar: {t}"))
        toolbar.addAction(act)
    toolbar.addSeparator()
    for ico, label in [
        ("mdi6.format-align-left", "Left"),
        ("mdi6.format-align-center", "Center"),
        ("mdi6.format-align-right", "Right"),
    ]:
        act = QtGui.QAction(qta.icon(ico, color=p["text"]), label)
        act.setCheckable(True)
        act.triggered.connect(lambda c, t=label: _log(f"Align: {t}"))
        toolbar.addAction(act)
    gt.addWidget(toolbar)
    layout.addWidget(_neu_group(group_tb))

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

    title = QtWidgets.QLabel("About Menus")
    title.setProperty("heading", True)
    f = title.font()
    f.setPointSize(20)
    title.setFont(f)
    layout.addWidget(title)

    info = QtWidgets.QLabel(
        "Nine menu-bar variants (matching Neumorphism.Avalonia):\n\n"
        "  Row 1\n"
        "  \u2022 Default \u2013 standard neumorphic raised menu bar\n"
        "  \u2022 Capsule Outset \u2013 pill buttons with raised BoxShadow\n"
        "  \u2022 Capsule Inset \u2013 pill buttons with inset BoxShadow\n\n"
        "  Row 2\n"
        "  \u2022 Capsule Flat \u2013 flat pills, accent tint on hover\n"
        "  \u2022 Minimal \u2013 transparent bar with underline on hover\n"
        "  \u2022 Stroked \u2013 outlined / bordered menu items\n\n"
        "  Row 3\n"
        "  \u2022 Avatar Profile \u2013 circular button with raised shadow\n"
        "  \u2022 Hamburger \u2013 bordered \u2261 icon\n"
        "  \u2022 Icon Nav Bar \u2013 multiple icon buttons, each with a menu\n\n"
        "Plus:\n"
        "  \u2022 Context Menu \u2013 right-click area with icons & submenus\n"
        "  \u2022 Tool Bar \u2013 icon + text toolbar with checkable buttons\n\n"
        "Capsule Outset/Inset use real BoxShadow (not QSS borders) for\n"
        "genuine neumorphic depth.  All variants read from ThemeManager."
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
    description="Nine menu-bar styles, context menus, and toolbar with neumorphic theming.",
))
