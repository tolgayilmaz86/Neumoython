"""Toggles demo – toggle switches, checkboxes, and radio buttons.
"""

import qtawesome as qta
from PySide6 import QtCore, QtWidgets

from widgets.registry import registry, WidgetDemo
from widgets.box_shadow import BoxShadowWrapper
from widgets.toggle_switch import ToggleSwitch
from styles.theme_manager import theme_manager


def _neu_group(group: QtWidgets.QGroupBox) -> BoxShadowWrapper:
    shadows = theme_manager.shadow_configs()
    return BoxShadowWrapper(
        group, shadow_list=shadows["outside_raised"],
        smooth=True, margins=(12, 12, 12, 12),
    )


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

    title = QtWidgets.QLabel("Toggles")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    desc = QtWidgets.QLabel(
        "Toggle switches, checkboxes, and radio buttons "
        "with neumorphic styling."
    )
    desc.setWordWrap(True)
    desc.setProperty("subheading", True)
    layout.addWidget(desc)

    # --- Toggle Switches ---
    group1 = QtWidgets.QGroupBox("Toggle Switches")
    g1 = QtWidgets.QVBoxLayout(group1)
    g1.setContentsMargins(16, 24, 16, 16)
    g1.setSpacing(12)

    row1 = QtWidgets.QHBoxLayout()
    row1.setSpacing(24)

    t1 = ToggleSwitch(checked=False, label="Default Off")
    t2 = ToggleSwitch(checked=True, label="Default On")
    t3 = ToggleSwitch(checked=False, label="Disabled")
    t3.setEnabled(False)
    t4 = ToggleSwitch(checked=True, label="Disabled On")
    t4.setEnabled(False)

    for t in (t1, t2, t3, t4):
        row1.addWidget(t)
    row1.addStretch()
    g1.addLayout(row1)

    # Status label linked to a toggle
    status_row = QtWidgets.QHBoxLayout()
    status_toggle = ToggleSwitch(checked=False, label="")
    status_label = QtWidgets.QLabel("OFF")
    status_label.setStyleSheet(f"font-weight: 600; font-size: 13px;")

    def on_status(checked: bool) -> None:
        status_label.setText("ON" if checked else "OFF")
        color = theme_manager.palette["accent"] if checked else theme_manager.palette["text_muted"]
        status_label.setStyleSheet(f"color: {color}; font-weight: 600; font-size: 13px;")

    status_toggle.toggled.connect(on_status)
    status_row.addWidget(status_toggle)
    status_row.addWidget(status_label)
    status_row.addStretch()
    g1.addLayout(status_row)

    layout.addWidget(_neu_group(group1))

    # --- Checkboxes ---
    group2 = QtWidgets.QGroupBox("Checkboxes")
    g2 = QtWidgets.QVBoxLayout(group2)
    g2.setContentsMargins(16, 24, 16, 16)
    g2.setSpacing(12)

    cb_row1 = QtWidgets.QHBoxLayout()
    cb_row1.setSpacing(24)
    for label, checked, enabled in [
        ("Default", False, True),
        ("Checked", True, True),
        ("Indeterminate", False, True),
        ("Disabled", False, False),
        ("Disabled Checked", True, False),
    ]:
        cb = QtWidgets.QCheckBox(label)
        cb.setChecked(checked)
        cb.setEnabled(enabled)
        if label == "Indeterminate":
            cb.setTristate(True)
            cb.setCheckState(QtCore.Qt.CheckState.PartiallyChecked)
        cb_row1.addWidget(cb)
    cb_row1.addStretch()
    g2.addLayout(cb_row1)

    # Accent row
    cb_row2 = QtWidgets.QHBoxLayout()
    cb_row2.setSpacing(24)
    for label in ("Option A", "Option B", "Option C"):
        cb = QtWidgets.QCheckBox(label)
        cb.setProperty("accentCheckbox", True)
        cb_row2.addWidget(cb)
    cb_row2.addStretch()
    g2.addLayout(cb_row2)

    layout.addWidget(_neu_group(group2))

    # --- Radio Buttons ---
    group3 = QtWidgets.QGroupBox("Radio Buttons")
    g3 = QtWidgets.QVBoxLayout(group3)
    g3.setContentsMargins(16, 24, 16, 16)
    g3.setSpacing(12)

    rb_row1 = QtWidgets.QHBoxLayout()
    rb_row1.setSpacing(24)
    radio_group1 = QtWidgets.QButtonGroup(group3)
    for i, label in enumerate(("Option 1", "Option 2", "Option 3")):
        rb = QtWidgets.QRadioButton(label)
        if i == 0:
            rb.setChecked(True)
        radio_group1.addButton(rb)
        rb_row1.addWidget(rb)

    rb_disabled = QtWidgets.QRadioButton("Disabled")
    rb_disabled.setEnabled(False)
    rb_row1.addWidget(rb_disabled)
    rb_row1.addStretch()
    g3.addLayout(rb_row1)

    # Second group
    rb_row2 = QtWidgets.QHBoxLayout()
    rb_row2.setSpacing(24)
    radio_group2 = QtWidgets.QButtonGroup(group3)
    for i, (label, icon_name) in enumerate([
        ("Left Align", "mdi6.format-align-left"),
        ("Center", "mdi6.format-align-center"),
        ("Right Align", "mdi6.format-align-right"),
        ("Justify", "mdi6.format-align-justify"),
    ]):
        rb = QtWidgets.QRadioButton(label)
        rb.setIcon(qta.icon(icon_name, color=theme_manager.palette['text']))
        if i == 0:
            rb.setChecked(True)
        radio_group2.addButton(rb)
        rb_row2.addWidget(rb)
    rb_row2.addStretch()
    g3.addLayout(rb_row2)

    layout.addWidget(_neu_group(group3))

    # --- Toggle Buttons (QPushButton checkable styled as toggles) ---
    group4 = QtWidgets.QGroupBox("Toggle Buttons")
    g4 = QtWidgets.QHBoxLayout(group4)
    g4.setContentsMargins(16, 24, 16, 16)
    g4.setSpacing(16)

    for label, icon_name, checked in [
        ("Wi-Fi", "mdi6.wifi", True),
        ("Bluetooth", "mdi6.bluetooth", False),
        ("Airplane", "mdi6.airplane", False),
        ("Location", "mdi6.map-marker-outline", True),
    ]:
        btn = QtWidgets.QPushButton(label)
        btn.setCheckable(True)
        btn.setChecked(checked)
        btn.setIcon(qta.icon(icon_name, color=theme_manager.palette['text']))
        g4.addWidget(btn)
    g4.addStretch()

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

    title = QtWidgets.QLabel("About Toggles")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    info = QtWidgets.QLabel(
        "Toggle controls for on/off states:\n\n"
        "  • ToggleSwitch – custom-painted sliding switch with animation\n"
        "  • QCheckBox – standard checkbox with tri-state support\n"
        "  • QRadioButton – mutually exclusive selection\n"
        "  • Toggle buttons – checkable QPushButtons\n\n"
        "The ToggleSwitch widget is a custom PySide6 implementation\n"
    )
    info.setWordWrap(True)
    layout.addWidget(info)
    layout.addStretch()
    return page


registry.register(WidgetDemo(
    id="toggles",
    name="Toggles",
    create_page=create_page,
    create_about=create_about,
    description="Toggle switches, checkboxes, and radio buttons.",
))
