"""Input widgets demo – text, numeric, and selector inputs."""

from PySide6 import QtCore, QtWidgets

from widgets.registry import registry, WidgetDemo
from widgets.box_shadow import BoxShadowWrapper
from widgets.catalog.sliders_demo import _NeuSlider
from styles.theme_manager import theme_manager


def _neu_group(group: QtWidgets.QGroupBox) -> BoxShadowWrapper:
    """Wrap a QGroupBox in a neumorphic raised shadow."""
    shadows = theme_manager.shadow_configs()
    return BoxShadowWrapper(
        group,
        shadow_list=shadows["outside_raised"],
        smooth=True,
        margins=(12, 12, 12, 12),
    )


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

    title = QtWidgets.QLabel("Input Widgets")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    desc = QtWidgets.QLabel(
        "Text inputs, combo boxes, spin boxes, sliders, and date pickers."
    )
    desc.setWordWrap(True)
    desc.setProperty("subheading", True)
    layout.addWidget(desc)

    # --- Text inputs ---
    group1 = QtWidgets.QGroupBox("Text Input")
    g1 = QtWidgets.QFormLayout(group1)
    g1.setContentsMargins(16, 24, 16, 16)
    g1.setVerticalSpacing(12)
    line = QtWidgets.QLineEdit()
    line.setPlaceholderText("Type here\u2026")
    g1.addRow("Line Edit:", line)

    pwd = QtWidgets.QLineEdit()
    pwd.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
    pwd.setPlaceholderText("Password")
    g1.addRow("Password:", pwd)

    text = QtWidgets.QTextEdit()
    text.setPlaceholderText("Multi-line text\u2026")
    text.setMaximumHeight(80)
    g1.addRow("Text Edit:", text)
    layout.addWidget(_neu_group(group1))

    # --- Numeric inputs ---
    group2 = QtWidgets.QGroupBox("Numeric Input")
    g2 = QtWidgets.QFormLayout(group2)
    g2.setContentsMargins(16, 24, 16, 16)
    g2.setVerticalSpacing(12)
    spin = QtWidgets.QSpinBox()
    spin.setRange(0, 100)
    g2.addRow("Spin Box:", spin)

    dspin = QtWidgets.QDoubleSpinBox()
    dspin.setRange(0.0, 1.0)
    dspin.setSingleStep(0.1)
    dspin.setDecimals(2)
    g2.addRow("Double Spin:", dspin)

    slider = _NeuSlider(QtCore.Qt.Orientation.Horizontal)
    slider.setRange(0, 100)
    g2.addRow("Slider:", slider)

    dial = QtWidgets.QDial()
    dial.setRange(0, 100)
    dial.setMaximumSize(80, 80)
    g2.addRow("Dial:", dial)
    layout.addWidget(_neu_group(group2))

    # --- Selectors ---
    group3 = QtWidgets.QGroupBox("Selectors")
    g3 = QtWidgets.QFormLayout(group3)
    g3.setContentsMargins(16, 24, 16, 16)
    g3.setVerticalSpacing(12)
    combo = QtWidgets.QComboBox()
    combo.addItems(["Option 1", "Option 2", "Option 3"])
    g3.addRow("Combo Box:", combo)

    date = QtWidgets.QDateEdit()
    date.setCalendarPopup(True)
    g3.addRow("Date:", date)

    time = QtWidgets.QTimeEdit()
    g3.addRow("Time:", time)
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

    title = QtWidgets.QLabel("About Input Widgets")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    info = QtWidgets.QLabel(
        "Standard Qt input widgets showcasing text, numeric, and selection inputs.\n\n"
        "Widgets: QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QSlider, QDial, "
        "QComboBox, QDateEdit, QTimeEdit."
    )
    info.setWordWrap(True)
    layout.addWidget(info)
    layout.addStretch()
    return page


registry.register(WidgetDemo(
    id="inputs",
    name="Input Widgets",
    create_page=create_page,
    create_about=create_about,
    description="Line edits, spin boxes, sliders, combo boxes, and date/time pickers.",
))
