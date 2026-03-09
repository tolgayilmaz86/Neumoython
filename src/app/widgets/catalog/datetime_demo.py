"""DateTime demo – date / time / calendar pickers with neumorphic theming.
"""

from __future__ import annotations

import qtawesome as qta
from PySide6 import QtCore, QtWidgets

from widgets.registry import registry, WidgetDemo
from widgets.box_shadow import BoxShadowWrapper
from widgets.popup_datetime_field import PopupDateTimeField
from styles.theme_manager import theme_manager
from styles.snippets import (
    value_label as _value_label_qss, calendar_qss, transparent_label,
)


def _neu_group(group: QtWidgets.QGroupBox) -> BoxShadowWrapper:
    shadows = theme_manager.shadow_configs()
    return BoxShadowWrapper(
        group, shadow_list=shadows["outside_raised"],
        smooth=True, margins=(12, 12, 12, 12),
    )


def _value_label(text: str) -> QtWidgets.QLabel:
    lbl = QtWidgets.QLabel(text)
    lbl.setStyleSheet(_value_label_qss())
    return lbl


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

    title = QtWidgets.QLabel("Date & Time")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    desc = QtWidgets.QLabel(
        "Date, time, and calendar picker widgets styled with the neumorphic theme."
    )
    desc.setWordWrap(True)
    desc.setProperty("subheading", True)
    layout.addWidget(desc)

    # --- Date & Time Editors ---
    group1 = QtWidgets.QGroupBox("Date & Time Pickers")
    g1 = QtWidgets.QFormLayout(group1)
    g1.setContentsMargins(16, 24, 16, 16)
    g1.setSpacing(16)

    # QDateEdit
    date_edit = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
    date_edit.setCalendarPopup(True)
    date_edit.setDisplayFormat("dd MMMM yyyy")
    date_edit.setMinimumWidth(200)
    date_val = _value_label(date_edit.date().toString("dd MMMM yyyy"))
    date_edit.dateChanged.connect(
        lambda d: date_val.setText(d.toString("dd MMMM yyyy")))
    row1 = QtWidgets.QHBoxLayout()
    row1.addWidget(date_edit)
    row1.addWidget(date_val)
    row1.addStretch()
    g1.addRow("Date:", row1)

    # QTimeEdit
    time_edit = QtWidgets.QTimeEdit(QtCore.QTime.currentTime())
    time_edit.setDisplayFormat("HH:mm:ss")
    time_edit.setMinimumWidth(150)
    time_val = _value_label(time_edit.time().toString("HH:mm:ss"))
    time_edit.timeChanged.connect(
        lambda t: time_val.setText(t.toString("HH:mm:ss")))
    row2 = QtWidgets.QHBoxLayout()
    row2.addWidget(time_edit)
    row2.addWidget(time_val)
    row2.addStretch()
    g1.addRow("Time:", row2)

    # QDateTimeEdit
    dt_edit = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime())
    dt_edit.setCalendarPopup(True)
    dt_edit.setDisplayFormat("dd/MM/yyyy HH:mm")
    dt_edit.setMinimumWidth(220)
    dt_val = _value_label(dt_edit.dateTime().toString("dd/MM/yyyy HH:mm"))
    dt_edit.dateTimeChanged.connect(
        lambda dt: dt_val.setText(dt.toString("dd/MM/yyyy HH:mm")))
    row3 = QtWidgets.QHBoxLayout()
    row3.addWidget(dt_edit)
    row3.addWidget(dt_val)
    row3.addStretch()
    g1.addRow("Date & Time:", row3)

    # Popup date-time field (text field + popup picker)
    popup_field = PopupDateTimeField(
        display_format="dd MMM yyyy, HH:mm",
    )
    popup_field.setMinimumWidth(280)
    popup_val = _value_label(popup_field.date_time().toString("yyyy-MM-dd HH:mm"))
    popup_field.dateTimeChanged.connect(
        lambda dt: popup_val.setText(dt.toString("yyyy-MM-dd HH:mm"))
    )
    row_popup = QtWidgets.QHBoxLayout()
    row_popup.addWidget(popup_field)
    row_popup.addWidget(popup_val)
    row_popup.addStretch()
    g1.addRow("Popup Field:", row_popup)

    # Range-constrained date
    min_date_edit = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
    min_date_edit.setCalendarPopup(True)
    min_date_edit.setDisplayFormat("dd MMM yyyy")
    min_date_edit.setDateRange(
        QtCore.QDate.currentDate().addDays(-90),
        QtCore.QDate.currentDate().addDays(90),
    )
    min_date_edit.setMinimumWidth(200)
    row4 = QtWidgets.QHBoxLayout()
    row4.addWidget(min_date_edit)
    range_lbl = QtWidgets.QLabel("(±90 days from today)")
    range_lbl.setStyleSheet(transparent_label("text_muted", 11))
    row4.addWidget(range_lbl)
    row4.addStretch()
    g1.addRow("Date (range):", row4)

    layout.addWidget(_neu_group(group1))

    # --- Inline Calendar ---
    group2 = QtWidgets.QGroupBox("Inline Calendar")
    g2 = QtWidgets.QVBoxLayout(group2)
    g2.setContentsMargins(16, 24, 16, 16)
    g2.setSpacing(12)

    calendar = QtWidgets.QCalendarWidget()
    calendar.setStyleSheet(calendar_qss())
    calendar.setGridVisible(False)
    calendar.setNavigationBarVisible(True)
    calendar.setMaximumWidth(380)

    cal_label = _value_label(
        "Selected: " + calendar.selectedDate().toString("dd MMMM yyyy"))
    calendar.selectionChanged.connect(
        lambda: cal_label.setText(
            "Selected: " + calendar.selectedDate().toString("dd MMMM yyyy")))

    g2.addWidget(calendar)
    g2.addWidget(cal_label)
    layout.addWidget(_neu_group(group2))

    # --- Range Selector ---
    group3 = QtWidgets.QGroupBox("Date Range Selector")
    g3 = QtWidgets.QFormLayout(group3)
    g3.setContentsMargins(16, 24, 16, 16)
    g3.setSpacing(16)

    today = QtCore.QDate.currentDate()
    from_edit = QtWidgets.QDateEdit(today)
    from_edit.setCalendarPopup(True)
    from_edit.setDisplayFormat("dd MMM yyyy")
    from_edit.setMinimumWidth(180)

    to_edit = QtWidgets.QDateEdit(today.addDays(7))
    to_edit.setCalendarPopup(True)
    to_edit.setDisplayFormat("dd MMM yyyy")
    to_edit.setMinimumWidth(180)

    range_result = _value_label("")

    def _update_range():
        f = from_edit.date()
        t = to_edit.date()
        delta = f.daysTo(t)
        if delta < 0:
            to_edit.setDate(f)
            delta = 0
        range_result.setText(f"{delta} day{'s' if delta != 1 else ''} selected")

    from_edit.dateChanged.connect(lambda _: _update_range())
    to_edit.dateChanged.connect(lambda _: _update_range())
    _update_range()

    row_from = QtWidgets.QHBoxLayout()
    row_from.addWidget(from_edit)
    row_from.addStretch()
    row_to = QtWidgets.QHBoxLayout()
    row_to.addWidget(to_edit)
    row_to.addStretch()

    g3.addRow("From:", row_from)
    g3.addRow("To:", row_to)
    g3.addRow("Duration:", range_result)

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

    title = QtWidgets.QLabel("About Date & Time")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    info = QtWidgets.QLabel(
        "Date and time picker widgets:\n\n"
        "  • QDateEdit – date picker with optional calendar popup\n"
        "  • QTimeEdit – time spinner with HH:mm:ss display\n"
        "  • QDateTimeEdit – combined date + time picker\n"
        "  • PopupDateTimeField – text field that opens a popup date-time picker\n"
        "  • QCalendarWidget – inline month calendar view\n"
        "  • Date range selector – from / to with duration calculation\n\n"
        "All widgets are styled via the ThemeManager QSS generator "
        "and include neumorphic inset borders on focus."
    )
    info.setWordWrap(True)
    layout.addWidget(info)
    layout.addStretch()
    return page


registry.register(WidgetDemo(
    id="datetime",
    name="Date & Time",
    create_page=create_page,
    create_about=create_about,
    description="Date, time, and calendar pickers with neumorphic styling.",
))
