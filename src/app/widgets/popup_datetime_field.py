"""Popup date-time field with a neumorphic picker surface.

This widget pairs a read-only text field with a popup picker. Clicking the field
(or its button) opens a neumorphic popup containing a calendar + time picker.
"""

from __future__ import annotations

import qtawesome as qta
from PySide6 import QtCore, QtGui, QtWidgets

from styles.theme_manager import theme_manager
from styles.snippets import calendar_qss
from widgets.box_shadow import BoxShadow


class _DateTimePopup(QtWidgets.QFrame):
    """Floating popup that hosts calendar/time controls."""

    accepted = QtCore.Signal(QtCore.QDateTime)

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup | QtCore.Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        outer = QtWidgets.QVBoxLayout(self)
        outer.setContentsMargins(10, 10, 10, 10)

        self._card = QtWidgets.QFrame()
        self._card.setObjectName("popupDateTimeCard")
        card_layout = QtWidgets.QVBoxLayout(self._card)
        card_layout.setContentsMargins(14, 14, 14, 14)
        card_layout.setSpacing(10)

        self._title = QtWidgets.QLabel("Choose Date & Time")
        title_font = self._title.font()
        title_font.setPointSize(11)
        title_font.setBold(True)
        self._title.setFont(title_font)
        card_layout.addWidget(self._title)

        self._calendar = QtWidgets.QCalendarWidget()
        self._calendar.setGridVisible(False)
        self._calendar.setNavigationBarVisible(True)
        card_layout.addWidget(self._calendar)

        self._time = QtWidgets.QTimeEdit()
        self._time.setDisplayFormat("HH:mm")
        self._time.setMinimumWidth(120)
        card_layout.addWidget(self._time, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

        buttons = QtWidgets.QHBoxLayout()
        buttons.addStretch(1)
        self._btn_now = QtWidgets.QPushButton("Now")
        self._btn_cancel = QtWidgets.QPushButton("Cancel")
        self._btn_apply = QtWidgets.QPushButton("Apply")
        self._btn_apply.setProperty("accent", True)
        buttons.addWidget(self._btn_now)
        buttons.addWidget(self._btn_cancel)
        buttons.addWidget(self._btn_apply)
        card_layout.addLayout(buttons)

        outer.addWidget(self._card)

        shadows = theme_manager.shadow_configs()
        self._card.setGraphicsEffect(
            BoxShadow(shadow_list=shadows["outside_raised"], smooth=True)
        )

        self._btn_now.clicked.connect(self._set_now)
        self._btn_cancel.clicked.connect(self.hide)
        self._btn_apply.clicked.connect(self._accept)

        self._apply_styles()

    def set_date_time(self, value: QtCore.QDateTime) -> None:
        self._calendar.setSelectedDate(value.date())
        self._time.setTime(value.time())

    def selected_date_time(self) -> QtCore.QDateTime:
        return QtCore.QDateTime(self._calendar.selectedDate(), self._time.time())

    def _set_now(self) -> None:
        now = QtCore.QDateTime.currentDateTime()
        self.set_date_time(now)

    def _accept(self) -> None:
        self.accepted.emit(self.selected_date_time())
        self.hide()

    def _apply_styles(self) -> None:
        p = theme_manager.palette
        self._card.setStyleSheet(
            f"""
            QFrame#popupDateTimeCard {{
                background: {p['card_bg']};
                border: 1px solid {p['bg_secondary']};
                border-radius: 14px;
            }}
            QLabel {{
                color: {p['text']};
                background: transparent;
            }}
            QPushButton {{
                background: {p['input_bg']};
                color: {p['text']};
                border: 1px solid {p['bg_secondary']};
                border-radius: 8px;
                padding: 6px 10px;
            }}
            QPushButton:hover {{
                background: {p['menu_hover']};
            }}
            QPushButton[accent='true'] {{
                background: {p['accent']};
                color: #FFFFFF;
                border: 1px solid {p['accent']};
                font-weight: 600;
            }}
            QPushButton[accent='true']:hover {{
                background: {p['accent_hover']};
            }}
            QTimeEdit {{
                background: {p['input_bg']};
                color: {p['text']};
                border: 1px solid {p['bg_secondary']};
                border-radius: 8px;
                padding: 4px 8px;
            }}
            """
        )

        self._calendar.setStyleSheet(calendar_qss())


class PopupDateTimeField(QtWidgets.QWidget):
    """Text-field style date-time input that opens a popup picker on click."""

    dateTimeChanged = QtCore.Signal(QtCore.QDateTime)

    def __init__(
        self,
        value: QtCore.QDateTime | None = None,
        display_format: str = "dd MMM yyyy HH:mm",
        parent: QtWidgets.QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._display_format = display_format
        self._value = value or QtCore.QDateTime.currentDateTime()

        p = theme_manager.palette

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self._edit = QtWidgets.QLineEdit()
        self._edit.setReadOnly(True)
        self._edit.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self._edit.installEventFilter(self)
        self._edit.setStyleSheet(
            f"""
            QLineEdit {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 {p['bg_secondary']},
                    stop:1 {p['input_bg']}
                );
                color: {p['text']};
                border: 1px solid {p['bg_secondary']};
                border-top-color: {p['bg_secondary']};
                border-left-color: {p['bg_secondary']};
                border-right-color: {p['menu_hover']};
                border-bottom-color: {p['menu_hover']};
                border-radius: 10px;
                padding: 8px 10px;
                min-height: 34px;
            }}
            QLineEdit:hover {{
                border-top-color: {p['menu_hover']};
                border-left-color: {p['menu_hover']};
                border-right-color: {p['bg_secondary']};
                border-bottom-color: {p['bg_secondary']};
            }}
            """
        )

        self._button = QtWidgets.QToolButton()
        self._button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self._button.setIcon(qta.icon("mdi6.calendar-clock", color=p["text_muted"]))
        self._button.setIconSize(QtCore.QSize(18, 18))
        self._button.setToolTip("Open date and time picker")
        self._button.setStyleSheet(
            f"""
            QToolButton {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 {p['bg_secondary']},
                    stop:1 {p['input_bg']}
                );
                border: 1px solid {p['bg_secondary']};
                border-top-color: {p['bg_secondary']};
                border-left-color: {p['bg_secondary']};
                border-right-color: {p['menu_hover']};
                border-bottom-color: {p['menu_hover']};
                border-radius: 10px;
                min-width: 36px;
                min-height: 34px;
            }}
            QToolButton:hover {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 {p['input_bg']},
                    stop:1 {p['menu_hover']}
                );
                border-top-color: {p['menu_hover']};
                border-left-color: {p['menu_hover']};
                border-right-color: {p['bg_secondary']};
                border-bottom-color: {p['bg_secondary']};
            }}
            """
        )

        layout.addWidget(self._edit, 1)
        layout.addWidget(self._button)

        self._popup = _DateTimePopup(self)
        self._popup.accepted.connect(self.set_date_time)
        self._button.clicked.connect(self.open_popup)

        self._sync_text()

    def date_time(self) -> QtCore.QDateTime:
        return QtCore.QDateTime(self._value)

    def set_date_time(self, value: QtCore.QDateTime) -> None:
        if not value.isValid():
            return
        if value == self._value:
            return
        self._value = QtCore.QDateTime(value)
        self._sync_text()
        self.dateTimeChanged.emit(self._value)

    def set_display_format(self, display_format: str) -> None:
        self._display_format = display_format
        self._sync_text()

    def open_popup(self) -> None:
        self._popup.set_date_time(self._value)
        self._popup.adjustSize()

        anchor = self.mapToGlobal(QtCore.QPoint(0, self.height() + 4))
        popup_size = self._popup.sizeHint()
        screen = QtGui.QGuiApplication.screenAt(anchor) or QtGui.QGuiApplication.primaryScreen()
        if screen:
            available = screen.availableGeometry()
            x = max(available.left(), min(anchor.x(), available.right() - popup_size.width()))
            y = anchor.y()
            if y + popup_size.height() > available.bottom():
                y = self.mapToGlobal(QtCore.QPoint(0, -popup_size.height() - 4)).y()
            anchor = QtCore.QPoint(x, y)

        self._popup.move(anchor)
        self._popup.show()

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if watched is self._edit and event.type() == QtCore.QEvent.Type.MouseButtonPress:
            self.open_popup()
            return True
        return super().eventFilter(watched, event)

    def _sync_text(self) -> None:
        self._edit.setText(self._value.toString(self._display_format))
