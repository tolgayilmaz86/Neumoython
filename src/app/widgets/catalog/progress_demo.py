"""Progress bars demo – neumorphic linear, circular, and spiral progress widgets."""

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt

from widgets.progress_widgets import (
    roundProgressBar,
    spiralProgressBar,
    NeuProgressBar,
    NeuProgressBarOutset,
    NeuProgressBarDeepInset,
)
from widgets.registry import registry, WidgetDemo
from widgets.box_shadow import BoxShadowWrapper
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


def _label(text: str) -> QtWidgets.QLabel:
    p = theme_manager.palette
    lbl = QtWidgets.QLabel(text)
    lbl.setStyleSheet(
        f"color: {p['text_muted']}; font-size: 11px; background: transparent;"
    )
    return lbl


def _accent_label(text: str) -> QtWidgets.QLabel:
    p = theme_manager.palette
    lbl = QtWidgets.QLabel(text)
    lbl.setStyleSheet(
        f"color: {p['accent']}; font-weight: 600; font-size: 13px; background: transparent;"
    )
    return lbl


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

    title = QtWidgets.QLabel("Progress Bars")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    desc = QtWidgets.QLabel(
        "Neumorphic progress bars in inset, deep-inset, and outset styles. "
        "Supports horizontal, vertical, indeterminate, gradient, and accent variants."
    )
    desc.setWordWrap(True)
    desc.setProperty("subheading", True)
    layout.addWidget(desc)

    # ================================================================
    # Global slider to drive all progress bars
    # ================================================================
    slider_row = QtWidgets.QHBoxLayout()
    slider_label = _accent_label("Value: 50")
    slider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
    slider.setRange(0, 100)
    slider.setValue(50)
    slider_row.addWidget(QtWidgets.QLabel("Control:"))
    slider_row.addWidget(slider, 1)
    slider_row.addWidget(slider_label)
    layout.addLayout(slider_row)

    # Collect all bars to update from slider
    all_bars: list = []

    # ================================================================
    # 1) Inset Linear Progress Bars
    # ================================================================
    group1 = QtWidgets.QGroupBox("Inset Linear Progress Bars")
    g1 = QtWidgets.QVBoxLayout(group1)
    g1.setContentsMargins(16, 24, 16, 16)
    g1.setSpacing(12)

    # Default inset
    g1.addWidget(_label("Default inset"))
    bar1 = NeuProgressBar()
    bar1.setValue(50)
    g1.addWidget(bar1)
    all_bars.append(bar1)

    # Inset with percentage text
    g1.addWidget(_label("With percentage text"))
    bar2 = NeuProgressBar()
    bar2.setValue(50)
    bar2.setShowText(True)
    bar2.setBarHeight(20)
    g1.addWidget(bar2)
    all_bars.append(bar2)

    # Accent colour override
    g1.addWidget(_label("Accent color (blue)"))
    bar3 = NeuProgressBar()
    bar3.setValue(50)
    bar3.setAccentColor("#1976D2")
    g1.addWidget(bar3)
    all_bars.append(bar3)

    # Gradient fill
    g1.addWidget(_label("Gradient fill"))
    bar4 = NeuProgressBar()
    bar4.setValue(50)
    bar4.setGradientColors(["#5cbcd6", "#77dbf0"])
    g1.addWidget(bar4)
    all_bars.append(bar4)

    # Indeterminate
    g1.addWidget(_label("Indeterminate"))
    bar5 = NeuProgressBar()
    bar5.setIndeterminate(True)
    g1.addWidget(bar5)

    layout.addWidget(_neu_group(group1))

    # ================================================================
    # 2) Deep Inset Linear Progress Bars
    # ================================================================
    group2 = QtWidgets.QGroupBox("Deep Inset Linear Progress Bars")
    g2 = QtWidgets.QVBoxLayout(group2)
    g2.setContentsMargins(16, 24, 16, 16)
    g2.setSpacing(12)

    # Default deep inset (shows text by default)
    g2.addWidget(_label("Default deep inset (with text)"))
    bar6 = NeuProgressBarDeepInset()
    bar6.setValue(50)
    g2.addWidget(bar6)
    all_bars.append(bar6)

    # Deep inset accent
    g2.addWidget(_label("Accent color (coral)"))
    bar7 = NeuProgressBarDeepInset()
    bar7.setValue(50)
    bar7.setAccentColor("#E64A19")
    g2.addWidget(bar7)
    all_bars.append(bar7)

    # Deep inset indeterminate
    g2.addWidget(_label("Indeterminate"))
    bar8 = NeuProgressBarDeepInset()
    bar8.setIndeterminate(True)
    g2.addWidget(bar8)

    layout.addWidget(_neu_group(group2))

    # ================================================================
    # 3) Outset Linear Progress Bars
    # ================================================================
    group3 = QtWidgets.QGroupBox("Outset Linear Progress Bars")
    g3 = QtWidgets.QVBoxLayout(group3)
    g3.setContentsMargins(16, 24, 16, 16)
    g3.setSpacing(12)

    # Default outset
    g3.addWidget(_label("Default outset"))
    bar9 = NeuProgressBarOutset()
    bar9.setValue(50)
    g3.addWidget(bar9)
    all_bars.append(bar9)

    # Outset with text
    g3.addWidget(_label("With percentage text"))
    bar10 = NeuProgressBarOutset()
    bar10.setValue(50)
    bar10.setShowText(True)
    bar10.setBarHeight(22)
    g3.addWidget(bar10)
    all_bars.append(bar10)

    # Outset gradient
    g3.addWidget(_label("Gradient fill (teal)"))
    bar11 = NeuProgressBarOutset()
    bar11.setValue(50)
    bar11.setGradientColors(["#00897B", "#4DB6AC"])
    g3.addWidget(bar11)
    all_bars.append(bar11)

    # Outset indeterminate
    g3.addWidget(_label("Indeterminate"))
    bar12 = NeuProgressBarOutset()
    bar12.setIndeterminate(True)
    g3.addWidget(bar12)

    layout.addWidget(_neu_group(group3))

    # ================================================================
    # 4) Vertical Progress Bars
    # ================================================================
    group4 = QtWidgets.QGroupBox("Vertical Progress Bars")
    g4 = QtWidgets.QHBoxLayout(group4)
    g4.setContentsMargins(16, 24, 16, 16)
    g4.setSpacing(20)

    vert_data = [
        ("Inset", NeuProgressBar, {}),
        ("Deep\nInset", NeuProgressBarDeepInset, {"bar_height": 24}),
        ("Outset", NeuProgressBarOutset, {}),
        ("Accent", NeuProgressBar, {"accent": "#1976D2"}),
        ("Gradient", NeuProgressBarOutset, {"gradient": ["#E64A19", "#FF8A65"]}),
        ("Indeterm.", NeuProgressBar, {"indeterm": True}),
    ]

    for label_text, cls, opts in vert_data:
        col = QtWidgets.QVBoxLayout()
        col.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        vbar = cls(orientation=Qt.Orientation.Vertical)
        vbar.setFixedHeight(180)
        vbar.setValue(50)
        if "bar_height" in opts:
            vbar.setBarHeight(opts["bar_height"])
        if "accent" in opts:
            vbar.setAccentColor(opts["accent"])
        if "gradient" in opts:
            vbar.setGradientColors(opts["gradient"])
        if "indeterm" in opts:
            vbar.setIndeterminate(True)
        else:
            all_bars.append(vbar)
        col.addWidget(vbar, 1, Qt.AlignmentFlag.AlignHCenter)
        lbl = _label(label_text)
        lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        col.addWidget(lbl)
        g4.addLayout(col)

    layout.addWidget(_neu_group(group4))

    # ================================================================
    # 5) Round & Spiral (existing widgets)
    # ================================================================
    group5 = QtWidgets.QGroupBox("Circular & Spiral Progress")
    g5 = QtWidgets.QVBoxLayout(group5)
    g5.setContentsMargins(16, 24, 16, 16)

    row = QtWidgets.QHBoxLayout()
    row.setSpacing(16)

    rpb1 = roundProgressBar()
    rpb1.rpb_setBarStyle("Donet")
    rpb1.rpb_setValue(50)
    row.addWidget(rpb1)

    rpb2 = roundProgressBar()
    rpb2.rpb_setBarStyle("Pizza")
    rpb2.rpb_setTextFormat("Value")
    rpb2.rpb_setRange(0, 360)
    rpb2.rpb_setValue(180)
    row.addWidget(rpb2)

    spb1 = spiralProgressBar()
    spb1.spb_setNoProgressBar(3)
    spb1.spb_setValue((50, 65, 30))
    row.addWidget(spb1)

    g5.addLayout(row)
    layout.addWidget(_neu_group(group5))

    layout.addStretch()

    # ================================================================
    # Slider → update all bars
    # ================================================================
    def on_value_changed(value: int) -> None:
        slider_label.setText(f"Value: {value}")
        for bar in all_bars:
            bar.setValue(value)
        rpb1.rpb_setValue(value)
        rpb2.rpb_setValue(int(value * 3.6))
        spb1.spb_setValue((value, min(100, value + 15), max(0, value - 20)))

    slider.valueChanged.connect(on_value_changed)

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

    title = QtWidgets.QLabel("About Progress Bars")
    title.setProperty("heading", True)
    layout.addWidget(title)

    info = QtWidgets.QLabel(
        "Neumorphic progress bar widgets for PySide6.\n\n"
        "NeuProgressBar (Inset):\n"
        "  - Sunken groove with inner shadows\n"
        "  - Accent colour or gradient fill\n"
        "  - Horizontal / vertical orientation\n"
        "  - Determinate and indeterminate modes\n\n"
        "NeuProgressBarDeepInset:\n"
        "  - Thicker groove with stronger inner shadows\n"
        "  - Built-in percentage text display\n\n"
        "NeuProgressBarOutset:\n"
        "  - Raised groove with outer shadows\n"
        "  - Same configuration options as inset\n\n"
        "roundProgressBar:\n"
        "  - Bar styles: Donet, Pizza, Pie\n"
        "  - Text formats: Percentage, Value\n\n"
        "spiralProgressBar:\n"
        "  - 2\u20136 concentric progress rings\n"
        "  - Per-ring colors and direction\n\n"
        "Import:\n"
        "  from widgets.progress_widgets import (\n"
        "      NeuProgressBar, NeuProgressBarOutset,\n"
        "      NeuProgressBarDeepInset,\n"
        "      roundProgressBar, spiralProgressBar\n"
        "  )"
    )
    info.setWordWrap(True)
    layout.addWidget(info)
    layout.addStretch()
    return page


registry.register(WidgetDemo(
    id="progress_bars",
    name="Progress Bars",
    create_page=create_page,
    create_about=create_about,
    description="Neumorphic linear, circular, and spiral progress bars.",
))
