"""Sliders demo – horizontal, vertical, and neumorphic outset sliders.
"""

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


def _slider_with_label(orientation, *, value: int = 50,
                       tick_interval: int = 0,
                       enabled: bool = True) -> QtWidgets.QWidget:
    """Create a slider + value label pair."""
    container = QtWidgets.QWidget()
    is_horiz = (orientation == QtCore.Qt.Orientation.Horizontal)

    if is_horiz:
        lay = QtWidgets.QVBoxLayout(container)
    else:
        lay = QtWidgets.QHBoxLayout(container)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(6)

    slider = QtWidgets.QSlider(orientation)
    slider.setRange(0, 100)
    slider.setValue(value)
    slider.setEnabled(enabled)
    if tick_interval > 0:
        slider.setTickInterval(tick_interval)
        if is_horiz:
            slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        else:
            slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksRight)

    if not is_horiz:
        slider.setMinimumHeight(120)

    label = QtWidgets.QLabel(str(value))
    label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    label.setFixedWidth(32)
    slider.valueChanged.connect(lambda v: label.setText(str(v)))

    lay.addWidget(slider)
    lay.addWidget(label)
    return container


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

    title = QtWidgets.QLabel("Sliders")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    desc = QtWidgets.QLabel(
        "Horizontal and vertical sliders with various configurations. "
        "Neumorphic track styling via QSS."
    )
    desc.setWordWrap(True)
    desc.setProperty("subheading", True)
    layout.addWidget(desc)

    # --- Horizontal sliders ---
    group1 = QtWidgets.QGroupBox("Horizontal Sliders")
    g1 = QtWidgets.QVBoxLayout(group1)
    g1.setContentsMargins(16, 24, 16, 16)
    g1.setSpacing(16)

    g1.addWidget(QtWidgets.QLabel("Default"))
    g1.addWidget(_slider_with_label(QtCore.Qt.Orientation.Horizontal, value=40))

    g1.addWidget(QtWidgets.QLabel("With Tick Marks"))
    g1.addWidget(_slider_with_label(QtCore.Qt.Orientation.Horizontal, value=60,
                                    tick_interval=10))

    g1.addWidget(QtWidgets.QLabel("Disabled"))
    g1.addWidget(_slider_with_label(QtCore.Qt.Orientation.Horizontal, value=30,
                                    enabled=False))

    layout.addWidget(_neu_group(group1))

    # --- Vertical sliders ---
    group2 = QtWidgets.QGroupBox("Vertical Sliders")
    g2 = QtWidgets.QHBoxLayout(group2)
    g2.setContentsMargins(16, 24, 16, 16)
    g2.setSpacing(24)

    for val, ticks in [(50, 0), (75, 20), (25, 0), (60, 10)]:
        g2.addWidget(_slider_with_label(
            QtCore.Qt.Orientation.Vertical, value=val, tick_interval=ticks))
    g2.addStretch()

    layout.addWidget(_neu_group(group2))

    # --- Range demonstration ---
    group3 = QtWidgets.QGroupBox("Interactive Range")
    g3 = QtWidgets.QVBoxLayout(group3)
    g3.setContentsMargins(16, 24, 16, 16)
    g3.setSpacing(12)

    range_label = QtWidgets.QLabel("Value: 50")
    range_label.setStyleSheet("font-size: 14px; font-weight: 600;")

    range_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
    range_slider.setRange(0, 100)
    range_slider.setValue(50)

    progress = QtWidgets.QProgressBar()
    progress.setRange(0, 100)
    progress.setValue(50)
    progress.setTextVisible(True)

    def on_range_changed(v: int) -> None:
        range_label.setText(f"Value: {v}")
        progress.setValue(v)

    range_slider.valueChanged.connect(on_range_changed)

    g3.addWidget(range_label)
    g3.addWidget(range_slider)
    g3.addWidget(QtWidgets.QLabel("Linked Progress Bar:"))
    g3.addWidget(progress)

    layout.addWidget(_neu_group(group3))

    # --- Dial section ---
    group4 = QtWidgets.QGroupBox("Dials")
    g4 = QtWidgets.QHBoxLayout(group4)
    g4.setContentsMargins(16, 24, 16, 16)
    g4.setSpacing(24)

    for val in (25, 50, 75):
        col = QtWidgets.QVBoxLayout()
        col.setSpacing(4)
        dial = QtWidgets.QDial()
        dial.setRange(0, 100)
        dial.setValue(val)
        dial.setMaximumSize(80, 80)
        dial.setNotchesVisible(True)
        d_label = QtWidgets.QLabel(str(val))
        d_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        dial.valueChanged.connect(lambda v, lb=d_label: lb.setText(str(v)))
        col.addWidget(dial, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        col.addWidget(d_label)
        g4.addLayout(col)
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

    title = QtWidgets.QLabel("About Sliders")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    info = QtWidgets.QLabel(
        "Slider and dial controls:\n\n"
        "  • QSlider – horizontal & vertical with tick marks\n"
        "  • QDial – rotary knob with notches\n"
        "  • QProgressBar – linked progress visualization\n\n"
        "Our QSS provides neumorphic groove and accent-colored handles."
    )
    info.setWordWrap(True)
    layout.addWidget(info)
    layout.addStretch()
    return page


registry.register(WidgetDemo(
    id="sliders",
    name="Sliders",
    create_page=create_page,
    create_about=create_about,
    description="Horizontal, vertical sliders and rotary dials.",
))
