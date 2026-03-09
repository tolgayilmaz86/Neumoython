"""Legacy widget showcase helpers kept for compatibility."""

from __future__ import annotations

from PySide6 import QtCore, QtWidgets

from widgets.progress_widgets import roundProgressBar, spiralProgressBar


def install_widget_showcase(main_window) -> None:
    """Attach a new Widgets menu button and showcase pages to the existing UI."""
    ui = main_window.ui

    frame_widgets = QtWidgets.QFrame(ui.frame_bottom_west)
    frame_widgets.setObjectName("frame_widgets")
    frame_widgets.setMinimumSize(QtCore.QSize(80, 55))
    frame_widgets.setMaximumSize(QtCore.QSize(160, 55))
    frame_widgets.setFrameShape(QtWidgets.QFrame.NoFrame)
    frame_widgets.setFrameShadow(QtWidgets.QFrame.Plain)

    frame_layout = QtWidgets.QHBoxLayout(frame_widgets)
    frame_layout.setSpacing(0)
    frame_layout.setContentsMargins(0, 0, 0, 0)

    bn_widgets = QtWidgets.QPushButton(frame_widgets)
    bn_widgets.setObjectName("bn_widgets")
    bn_widgets.setMinimumSize(QtCore.QSize(80, 55))
    bn_widgets.setMaximumSize(QtCore.QSize(160, 55))
    bn_widgets.setToolTip("Widgets")
    bn_widgets.setFlat(True)
    bn_widgets.setText("")
    bn_widgets.setIcon(main_window.style().standardIcon(QtWidgets.QStyle.SP_FileDialogContentsView))
    bn_widgets.setIconSize(QtCore.QSize(20, 20))
    frame_layout.addWidget(bn_widgets)

    insert_idx = ui.verticalLayout_3.indexOf(ui.frame_8)
    if insert_idx < 0:
        ui.verticalLayout_3.addWidget(frame_widgets)
    else:
        ui.verticalLayout_3.insertWidget(insert_idx, frame_widgets)

    page_widgets = QtWidgets.QWidget()
    page_widgets.setObjectName("page_widgets")
    page_layout = QtWidgets.QVBoxLayout(page_widgets)
    page_layout.setSpacing(8)
    page_layout.setContentsMargins(8, 8, 8, 8)

    title = QtWidgets.QLabel("Widget Showcase: Progress Bars")
    title_font = title.font()
    title_font.setPointSize(20)
    title.setFont(title_font)
    page_layout.addWidget(title)

    desc = QtWidgets.QLabel("Round and spiral progress bars inspired by PySide2extn. Use the slider to animate all widgets.")
    desc.setWordWrap(True)
    page_layout.addWidget(desc)

    row = QtWidgets.QHBoxLayout()
    row.setSpacing(12)

    rpb1 = roundProgressBar()
    rpb1.rpb_setBarStyle("Donet")
    rpb1.rpb_setValue(72)
    row.addWidget(rpb1)

    rpb2 = roundProgressBar()
    rpb2.rpb_setBarStyle("Pizza")
    rpb2.rpb_setTextFormat("Value")
    rpb2.rpb_setRange(0, 360)
    rpb2.rpb_setValue(220)
    row.addWidget(rpb2)

    spb1 = spiralProgressBar()
    spb1.spb_setNoProgressBar(3)
    spb1.spb_setValue((65, 42, 80))
    row.addWidget(spb1)

    page_layout.addLayout(row)

    slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    slider.setRange(0, 100)
    slider.setValue(65)
    page_layout.addWidget(slider)

    value_label = QtWidgets.QLabel("Showcase Value: 65")
    page_layout.addWidget(value_label)

    page_about_widgets = QtWidgets.QWidget()
    page_about_widgets.setObjectName("page_about_widgets")
    about_layout = QtWidgets.QVBoxLayout(page_about_widgets)
    about_layout.setContentsMargins(8, 8, 8, 8)
    about_title = QtWidgets.QLabel("About > Widgets")
    about_title_font = about_title.font()
    about_title_font.setPointSize(20)
    about_title.setFont(about_title_font)
    about_text = QtWidgets.QLabel(
        "This page is reserved for documentation and controls of custom widgets. "
        "You can add more widget demos here without touching generated UI files."
    )
    about_text.setWordWrap(True)
    about_layout.addWidget(about_title)
    about_layout.addWidget(about_text)

    def on_value_changed(value: int) -> None:
        value_label.setText(f"Showcase Value: {value}")
        rpb1.rpb_setValue(value)
        rpb2.rpb_setValue(int(value * 3.6))
        spb1.spb_setValue((value, min(100, value + 15), max(0, value - 20)))

    slider.valueChanged.connect(on_value_changed)

    ui.stackedWidget.addWidget(page_widgets)
    ui.stackedWidget.addWidget(page_about_widgets)

    ui.frame_widgets = frame_widgets
    ui.bn_widgets = bn_widgets
    ui.page_widgets = page_widgets
    ui.page_about_widgets = page_about_widgets
