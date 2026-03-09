"""Snackbars demo – toast / snackbar notification widget.
All snack types + action-button variant demonstrated.
"""

import qtawesome as qta
from PySide6 import QtCore, QtWidgets

from widgets.registry import registry, WidgetDemo
from widgets.box_shadow import BoxShadowWrapper
from widgets.snackbar import Snackbar
from styles.theme_manager import theme_manager


def _neu_group(group: QtWidgets.QGroupBox) -> BoxShadowWrapper:
    shadows = theme_manager.shadow_configs()
    return BoxShadowWrapper(
        group, shadow_list=shadows["outside_raised"],
        smooth=True, margins=(12, 12, 12, 12),
    )


def _accent_btn(label: str, icon: str, accent: str = "") -> QtWidgets.QPushButton:
    btn = QtWidgets.QPushButton(label)
    ic_color = accent if accent else theme_manager.palette["text"]
    btn.setIcon(qta.icon(icon, color=ic_color))
    if accent:
        btn.setStyleSheet(f"""
            QPushButton {{
                color: {accent};
                border: 2px solid {accent};
                border-radius: 10px;
                padding: 8px 18px;
                font-weight: 600;
                background: transparent;
            }}
            QPushButton:hover {{
                background: {accent};
                color: #FFFFFF;
            }}
        """)
    return btn


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

    title = QtWidgets.QLabel("Snackbars")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    desc = QtWidgets.QLabel(
        "Brief notification overlays (toasts) that slide in from the bottom "
        "and auto-dismiss after a set duration. Supports info, success, "
        "warning, and error variants with an optional action button."
    )
    desc.setWordWrap(True)
    desc.setProperty("subheading", True)
    layout.addWidget(desc)

    # helper: find the top-level window at click time
    def _top(w: QtWidgets.QWidget) -> QtWidgets.QWidget:
        top = w.window()
        return top if top else w

    # --- Type variants ---
    group1 = QtWidgets.QGroupBox("Notification Types")
    g1 = QtWidgets.QHBoxLayout(group1)
    g1.setContentsMargins(16, 24, 16, 16)
    g1.setSpacing(12)

    for label, icon_name, snack_t, color in [
        ("Default",  "mdi6.bell-outline",            "default", ""),
        ("Info",     "mdi6.information-outline",      "info",    "#1976D2"),
        ("Success",  "mdi6.check-circle-outline",     "success", "#388E3C"),
        ("Warning",  "mdi6.alert-outline",            "warning", "#F57C00"),
        ("Error",    "mdi6.close-circle-outline",     "error",   "#D32F2F"),
    ]:
        btn = _accent_btn(label, icon_name, color)
        msg = f"This is a {label.lower()} notification."
        t = snack_t  # capture loop variable
        btn.clicked.connect(lambda checked=False, m=msg, st=t: Snackbar.show(
            _top(inner), m, snack_type=st))
        g1.addWidget(btn)

    g1.addStretch()
    layout.addWidget(_neu_group(group1))

    # --- With action button ---
    group2 = QtWidgets.QGroupBox("With Action Button")
    g2 = QtWidgets.QVBoxLayout(group2)
    g2.setContentsMargins(16, 24, 16, 16)
    g2.setSpacing(12)

    undo_label = QtWidgets.QLabel("Action result appears here.")
    undo_label.setStyleSheet(f"color: {theme_manager.palette['text_muted']}; font-size: 12px;")

    def _simulate_delete():
        undo_label.setText("Item deleted. Click below to undo.")
        Snackbar.show(
            _top(inner), "Item deleted",
            action_label="Undo",
            on_action=lambda: undo_label.setText("Undo performed — item restored."),
            snack_type="warning",
            duration=5000,
        )

    delete_btn = QtWidgets.QPushButton("Delete Item")
    delete_btn.setIcon(qta.icon("mdi6.delete-outline", color=theme_manager.palette["text"]))
    delete_btn.clicked.connect(_simulate_delete)

    g2.addWidget(delete_btn)
    g2.addWidget(undo_label)
    layout.addWidget(_neu_group(group2))

    # --- Custom duration ---
    group3 = QtWidgets.QGroupBox("Custom Duration")
    g3 = QtWidgets.QHBoxLayout(group3)
    g3.setContentsMargins(16, 24, 16, 16)
    g3.setSpacing(12)

    dur_label = QtWidgets.QLabel("Duration (ms):")
    dur_spin = QtWidgets.QSpinBox()
    dur_spin.setRange(500, 10000)
    dur_spin.setSingleStep(500)
    dur_spin.setValue(3000)
    dur_spin.setSuffix(" ms")

    show_btn = QtWidgets.QPushButton("Show Toast")
    show_btn.setIcon(qta.icon("mdi6.bell-ring-outline", color=theme_manager.palette["accent"]))
    show_btn.setProperty("accentButton", True)

    show_btn.clicked.connect(lambda: Snackbar.show(
        _top(inner),
        f"Toast visible for {dur_spin.value()} ms.",
        duration=dur_spin.value(),
        snack_type="info",
    ))

    g3.addWidget(dur_label)
    g3.addWidget(dur_spin)
    g3.addSpacing(8)
    g3.addWidget(show_btn)
    g3.addStretch()
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

    title = QtWidgets.QLabel("About Snackbars")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    info = QtWidgets.QLabel(
        "Snackbar is a lightweight overlay toast notification:\n\n"
        "  • Slides in from the bottom of the parent window\n"
        "  • Auto-dismisses after a configurable duration\n"
        "  • Supports info / success / warning / error icon variants\n"
        "  • Optional action button (e.g. Undo)\n"
        "  • Manual close via × button\n"
        "  • At most one toast visible at a time (new replaces old)\n\n"
        "API:  Snackbar.show(parent, message, duration=3000,\n"
        "        action_label=None, on_action=None, snack_type='default')"
    )
    info.setWordWrap(True)
    layout.addWidget(info)
    layout.addStretch()
    return page


registry.register(WidgetDemo(
    id="snackbars",
    name="Snackbars",
    create_page=create_page,
    create_about=create_about,
    description="Toast notifications that slide in from the bottom.",
))
