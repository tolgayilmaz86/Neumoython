"""Dialogs demo – custom neumorphic dialog boxes.

Provides a NeuDialog base class and several ready-made variants:
InfoDialog, WarningDialog, ErrorDialog, SuccessDialog,
ConfirmDialog, LoginDialog, InputDialog.
"""

from __future__ import annotations

from typing import Callable

import qtawesome as qta
from PySide6 import QtCore, QtGui, QtWidgets

from widgets.registry import registry, WidgetDemo
from widgets.box_shadow import BoxShadow, BoxShadowWrapper
from styles.theme_manager import theme_manager


def _neu_group(group: QtWidgets.QGroupBox) -> BoxShadowWrapper:
    shadows = theme_manager.shadow_configs()
    return BoxShadowWrapper(
        group, shadow_list=shadows["outside_raised"],
        smooth=True, margins=(12, 12, 12, 12),
    )


# ---------------------------------------------------------------------------
# NeuDialog – base class
# ---------------------------------------------------------------------------

class NeuDialog(QtWidgets.QDialog):
    """Base neumorphic dialog with title bar, icon, message, and action buttons.

    Do not use directly; use the typed subclasses or :meth:`NeuDialog.create`.
    """

    _TYPE_META: dict[str, tuple[str, str]] = {
        "info":    ("mdi6.information-outline",  "#1976D2"),
        "success": ("mdi6.check-circle-outline", "#388E3C"),
        "warning": ("mdi6.alert-outline",        "#F57C00"),
        "error":   ("mdi6.close-circle-outline", "#D32F2F"),
    }

    def __init__(self, parent: QtWidgets.QWidget | None = None,
                 title: str = "Dialog",
                 message: str = "",
                 dialog_type: str = "info",
                 buttons: list[tuple[str, bool]] | None = None) -> None:
        """
        :param parent:      Parent widget (used for positioning).
        :param title:       Dialog window title.
        :param message:     Body message text.
        :param dialog_type: One of 'info', 'success', 'warning', 'error'.
        :param buttons:     List of (label, is_accent) tuples.  Default: [("OK", True)].
        """
        super().__init__(parent, QtCore.Qt.WindowType.FramelessWindowHint |
                         QtCore.Qt.WindowType.Dialog)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setMaximumWidth(520)

        p = theme_manager.palette
        theme = theme_manager.theme
        icon_name, type_color = self._TYPE_META.get(
            dialog_type, self._TYPE_META["info"])

        if buttons is None:
            buttons = [("OK", True)]

        # Lifted card colours – slightly offset from base background
        if theme == "light":
            lifted_bg = "#EDF1F7"
            border_color = "rgba(0, 0, 0, 0.08)"
        else:
            lifted_bg = "#343A3F"
            border_color = "rgba(255, 255, 255, 0.07)"

        # ── outer layout with room for the shadow to render ────────────────
        outer_layout = QtWidgets.QVBoxLayout(self)
        outer_layout.setContentsMargins(28, 28, 28, 28)

        card = QtWidgets.QFrame()
        card.setObjectName("neu_dialog_card")
        card.setStyleSheet(f"""
            QFrame#neu_dialog_card {{
                background: {lifted_bg};
                border-radius: 20px;
                border: 1px solid {border_color};
            }}
        """)
        outer_layout.addWidget(card)

        card_layout = QtWidgets.QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 20)
        card_layout.setSpacing(16)

        # ── title row (icon + title + close) ──────────────────────────────
        title_row = QtWidgets.QHBoxLayout()
        title_row.setSpacing(12)

        icon_lbl = QtWidgets.QLabel()
        icon_lbl.setPixmap(qta.icon(icon_name, color=type_color).pixmap(28, 28))
        title_row.addWidget(icon_lbl)

        title_lbl = QtWidgets.QLabel(title)
        title_lbl.setStyleSheet(
            f"color: {p['text_heading']}; font-size: 16px; font-weight: 700; "
            "background: transparent;"
        )
        title_row.addWidget(title_lbl, stretch=1)

        close_btn = QtWidgets.QPushButton()
        close_btn.setFixedSize(28, 28)
        close_btn.setFlat(True)
        close_btn.setIcon(qta.icon("mdi6.close", color=p["text_muted"]))
        close_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet("background: transparent; border: none;")
        close_btn.setToolTip("Close")
        close_btn.clicked.connect(self.reject)
        title_row.addWidget(close_btn)

        card_layout.addLayout(title_row)

        # ── separator ─────────────────────────────────────────────────────
        sep = QtWidgets.QFrame()
        sep.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        sep.setStyleSheet(f"background: {p['bg_secondary']}; border: none; max-height: 1px;")
        card_layout.addWidget(sep)

        # ── message ───────────────────────────────────────────────────────
        if message:
            msg_lbl = QtWidgets.QLabel(message)
            msg_lbl.setStyleSheet(
                f"color: {p['text']}; font-size: 13px; background: transparent;"
            )
            msg_lbl.setWordWrap(True)
            card_layout.addWidget(msg_lbl)

        # ── extra content (subclasses call _add_content_widget) ───────────
        self._card_layout = card_layout

        # ── button row ────────────────────────────────────────────────────
        btn_row = QtWidgets.QHBoxLayout()
        btn_row.addStretch()
        btn_row.setSpacing(10)
        self._result_button: str = ""
        for label, is_accent in buttons:
            btn = QtWidgets.QPushButton(label)
            if is_accent:
                btn.setProperty("accentButton", True)
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background: {type_color};
                        color: #FFFFFF;
                        border-radius: 10px;
                        padding: 8px 20px;
                        font-weight: 600;
                        font-size: 13px;
                        border: none;
                    }}
                    QPushButton:hover {{
                        background: {type_color}CC;
                    }}
                """)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background: {p['bg_secondary']};
                        color: {p['text']};
                        border-radius: 10px;
                        padding: 8px 20px;
                        font-weight: 600;
                        font-size: 13px;
                        border: none;
                    }}
                    QPushButton:hover {{
                        background: {p['menu_hover']};
                    }}
                """)
            lbl_capture = label
            btn.clicked.connect(lambda checked=False, t=lbl_capture: self._on_btn(t))
            btn_row.addWidget(btn)

        card_layout.addLayout(btn_row)

        # ── drag support ──────────────────────────────────────────────────
        self._drag_pos: QtCore.QPoint | None = None

        # Apply a stronger outside shadow so the dialog "lifts" off the surface
        shadows = theme_manager.shadow_configs()
        if theme == "light":
            dialog_shadow = [
                {"outside": True, "offset": [8, 8], "blur": 20,
                 "color": QtGui.QColor(0, 0, 0, 70)},
                {"outside": True, "offset": [-6, -6], "blur": 16,
                 "color": QtGui.QColor(255, 255, 255, 220)},
            ]
        else:
            dialog_shadow = [
                {"outside": True, "offset": [8, 8], "blur": 20,
                 "color": QtGui.QColor(0, 0, 0, 180)},
                {"outside": True, "offset": [-6, -6], "blur": 16,
                 "color": QtGui.QColor(255, 255, 255, 40)},
            ]
        card.setGraphicsEffect(BoxShadow(dialog_shadow, smooth=True))

    def _add_content_widget(self, widget: QtWidgets.QWidget) -> None:
        """Insert *widget* above the button row."""
        count = self._card_layout.count()
        self._card_layout.insertWidget(count - 1, widget)

    def _on_btn(self, label: str) -> None:
        self._result_button = label
        if label in ("OK", "Yes", "Confirm", "Login", "Submit"):
            self.accept()
        else:
            self.reject()

    def result_label(self) -> str:
        """Return the label of the button that was clicked."""
        return self._result_button

    # Drag frameless window
    def mousePressEvent(self, event) -> None:
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event) -> None:
        if self._drag_pos and event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, event) -> None:
        self._drag_pos = None

    # ── convenience constructors ──────────────────────────────────────────
    @classmethod
    def info(cls, parent, title="Information", message=""):
        return cls(parent, title, message, "info", [("OK", True)])

    @classmethod
    def success(cls, parent, title="Success", message=""):
        return cls(parent, title, message, "success", [("OK", True)])

    @classmethod
    def warning(cls, parent, title="Warning", message=""):
        return cls(parent, title, message, "warning", [("OK", True)])

    @classmethod
    def error(cls, parent, title="Error", message=""):
        return cls(parent, title, message, "error", [("OK", True)])

    @classmethod
    def confirm(cls, parent, title="Confirm", message="Are you sure?"):
        return cls(parent, title, message, "warning",
                   [("Cancel", False), ("Yes", True)])


class LoginDialog(NeuDialog):
    """NeuDialog variant with username + password fields."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent, title="Sign In",
                         message="Please enter your credentials.",
                         dialog_type="info",
                         buttons=[("Cancel", False), ("Login", True)])

        p = theme_manager.palette
        form = QtWidgets.QFormLayout()
        form.setSpacing(12)
        form.setContentsMargins(0, 4, 0, 4)

        self._user = QtWidgets.QLineEdit()
        self._user.setPlaceholderText("Username or email")
        self._user.setAccessibleName("Username")

        self._pwd = QtWidgets.QLineEdit()
        self._pwd.setPlaceholderText("Password")
        self._pwd.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self._pwd.setAccessibleName("Password")

        form.addRow("Username:", self._user)
        form.addRow("Password:", self._pwd)

        wrapper = QtWidgets.QWidget()
        wrapper.setStyleSheet("background: transparent;")
        wrapper.setLayout(form)
        self._add_content_widget(wrapper)
        QtWidgets.QWidget.setTabOrder(self._user, self._pwd)

    def credentials(self) -> tuple[str, str]:
        return self._user.text(), self._pwd.text()


class InputDialog(NeuDialog):
    """NeuDialog variant with a single QLineEdit for user input."""

    def __init__(self, parent=None, title="Enter Value",
                 prompt="Value:", placeholder="") -> None:
        super().__init__(parent, title=title, message="",
                         dialog_type="info",
                         buttons=[("Cancel", False), ("Submit", True)])
        p = theme_manager.palette
        row = QtWidgets.QHBoxLayout()
        row.setSpacing(10)
        lbl = QtWidgets.QLabel(prompt)
        lbl.setStyleSheet(f"color: {p['text']}; background: transparent;")
        self._input = QtWidgets.QLineEdit()
        self._input.setPlaceholderText(placeholder)
        row.addWidget(lbl)
        row.addWidget(self._input, stretch=1)
        wrapper = QtWidgets.QWidget()
        wrapper.setStyleSheet("background: transparent;")
        wrapper.setLayout(row)
        self._add_content_widget(wrapper)

    def value(self) -> str:
        return self._input.text()


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

    title = QtWidgets.QLabel("Dialogs")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    desc = QtWidgets.QLabel(
        "Custom neumorphic dialog boxes for info, confirmation, login, "
        "and freeform input. All dialogs are frameless and support drag-to-move."
    )
    desc.setWordWrap(True)
    desc.setProperty("subheading", True)
    layout.addWidget(desc)

    result_lbl = QtWidgets.QLabel("Dialog result will appear here.")
    result_lbl.setStyleSheet(
        f"color: {p['text_muted']}; font-size: 12px; background: transparent; "
        "font-style: italic;"
    )

    def _show(dlg: NeuDialog, result_fmt: Callable[[], str] = lambda: "") -> None:
        if dlg.exec():
            extra = result_fmt()
            result_lbl.setText(
                f"Accepted — button: '{dlg.result_label()}'" + (f"  {extra}" if extra else ""))
        else:
            result_lbl.setText(f"Rejected — button: '{dlg.result_label()}'")

    # --- Type variants ---
    group1 = QtWidgets.QGroupBox("Dialog Types")
    g1 = QtWidgets.QHBoxLayout(group1)
    g1.setContentsMargins(16, 24, 16, 16)
    g1.setSpacing(12)

    for dlg_type, lbl, ico, color in [
        ("info",    "Info",    "mdi6.information-outline",  "#1976D2"),
        ("success", "Success", "mdi6.check-circle-outline", "#388E3C"),
        ("warning", "Warning", "mdi6.alert-outline",        "#F57C00"),
        ("error",   "Error",   "mdi6.close-circle-outline", "#D32F2F"),
    ]:
        t = dlg_type
        btn = QtWidgets.QPushButton(lbl)
        btn.setIcon(qta.icon(ico, color=color))
        btn.setStyleSheet(f"""
            QPushButton {{
                color: {color};
                border: 2px solid {color};
                border-radius: 10px;
                padding: 8px 18px;
                font-weight: 600;
                background: transparent;
            }}
            QPushButton:hover {{
                background: {color};
                color: #FFFFFF;
            }}
        """)
        btn.clicked.connect(lambda checked=False, dt=t: _show(NeuDialog(
            inner.window(), dt.capitalize(),
            f"This is a {dt} message. Check your settings or try again.",
            dt,
        )))
        g1.addWidget(btn)
    g1.addStretch()

    layout.addWidget(_neu_group(group1))

    # --- Confirm dialog ---
    group2 = QtWidgets.QGroupBox("Confirmation Dialog")
    g2 = QtWidgets.QHBoxLayout(group2)
    g2.setContentsMargins(16, 24, 16, 16)
    g2.setSpacing(12)

    confirm_btn = QtWidgets.QPushButton("Delete Item")
    confirm_btn.setIcon(qta.icon("mdi6.delete-outline", color="#D32F2F"))
    confirm_btn.setStyleSheet(f"""
        QPushButton {{
            color: #D32F2F;
            border: 2px solid #D32F2F;
            border-radius: 10px;
            padding: 8px 18px;
            font-weight: 600;
            background: transparent;
        }}
        QPushButton:hover {{
            background: #D32F2F;
            color: #FFFFFF;
        }}
    """)
    confirm_btn.clicked.connect(lambda: _show(
        NeuDialog.confirm(inner.window(),
                          "Delete Item?",
                          "This action cannot be undone. The item will be permanently removed.")
    ))

    g2.addWidget(confirm_btn)
    g2.addStretch()
    layout.addWidget(_neu_group(group2))

    # --- Login + Input dialogs ---
    group3 = QtWidgets.QGroupBox("Specialized Dialogs")
    g3 = QtWidgets.QHBoxLayout(group3)
    g3.setContentsMargins(16, 24, 16, 16)
    g3.setSpacing(12)

    login_btn = QtWidgets.QPushButton("Login Dialog")
    login_btn.setIcon(qta.icon("mdi6.account-key-outline", color=p["text"]))

    def _show_login():
        d = LoginDialog(inner.window())
        if d.exec():
            user, _ = d.credentials()
            result_lbl.setText(f"Login accepted — user: '{user}'")
        else:
            result_lbl.setText("Login cancelled.")

    login_btn.clicked.connect(_show_login)

    input_btn = QtWidgets.QPushButton("Input Dialog")
    input_btn.setIcon(qta.icon("mdi6.form-textbox", color=p["text"]))

    def _show_input():
        d = InputDialog(inner.window(),
                        title="Rename Item",
                        prompt="New name:",
                        placeholder="Enter name…")
        if d.exec():
            result_lbl.setText(f"Input value: '{d.value()}'")
        else:
            result_lbl.setText("Input cancelled.")

    input_btn.clicked.connect(_show_input)

    g3.addWidget(login_btn)
    g3.addWidget(input_btn)
    g3.addStretch()
    layout.addWidget(_neu_group(group3))

    # --- Result display ---
    layout.addWidget(result_lbl)

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

    title = QtWidgets.QLabel("About Dialogs")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    info = QtWidgets.QLabel(
        "Custom neumorphic dialog widgets:\n\n"
        "  • NeuDialog – frameless base class (draggable)\n"
        "  • Info / Success / Warning / Error – typed variants\n"
        "  • ConfirmDialog – Yes / Cancel confirmation\n"
        "  • LoginDialog – username + password fields\n"
        "  • InputDialog – single text input\n\n"
        "NeuDialog is a fully standalone QDialog subclass importable as:\n"
        "  from widgets.catalog.dialogs_demo import NeuDialog, LoginDialog"
    )
    info.setWordWrap(True)
    layout.addWidget(info)
    layout.addStretch()
    return page


registry.register(WidgetDemo(
    id="dialogs",
    name="Dialogs",
    create_page=create_page,
    create_about=create_about,
    description="Custom neumorphic dialog boxes with typed variants.",
))
