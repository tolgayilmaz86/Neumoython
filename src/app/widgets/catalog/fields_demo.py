"""Fields demo – form input fields with floating labels and validation.

Introduces FloatingLabelField: a custom widget with an animated label that
rises when the field is focused or has text.
"""

from __future__ import annotations

import qtawesome as qta
from PySide6 import QtCore, QtGui, QtWidgets

from widgets.registry import registry, WidgetDemo
from widgets.box_shadow import BoxShadowWrapper
from styles.theme_manager import theme_manager


def _neu_group(group: QtWidgets.QGroupBox) -> BoxShadowWrapper:
    shadows = theme_manager.shadow_configs()
    return BoxShadowWrapper(
        group, shadow_list=shadows["outside_raised"],
        smooth=True, margins=(12, 12, 12, 12),
    )


# ---------------------------------------------------------------------------
# FloatingLabelField – custom widget with animated placeholder label
# ---------------------------------------------------------------------------

class FloatingLabelField(QtWidgets.QWidget):
    """QLineEdit wrapped with an animated floating label.

    The label starts inside the field (like a placeholder), then floats
    above when the field is focused or contains text.

    Modes:
        "normal"  – no special styling
        "error"   – red border + error icon
        "success" – green border + check icon
    """

    textChanged = QtCore.Signal(str)

    def __init__(self, label: str = "Label", placeholder: str = "",
                 mode: str = "normal", password: bool = False,
                 parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self._label_text = label
        self._mode = mode
        self._password = password
        self._floated = False

        p = theme_manager.palette

        # --- outer container ---
        outer = QtWidgets.QVBoxLayout(self)
        outer.setContentsMargins(0, 12, 0, 0)  # top margin for the floating label
        outer.setSpacing(0)

        # --- field container (border drawn here) ---
        self._field_frame = QtWidgets.QFrame()
        self._field_frame.setMinimumHeight(52)
        outer.addWidget(self._field_frame)

        field_row = QtWidgets.QHBoxLayout(self._field_frame)
        field_row.setContentsMargins(14, 18, 8, 4)
        field_row.setSpacing(6)

        # --- line edit ---
        self._edit = QtWidgets.QLineEdit()
        self._edit.setPlaceholderText(placeholder)
        self._edit.setStyleSheet("background: transparent; border: none; padding: 0;")
        if password:
            self._edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        field_row.addWidget(self._edit, stretch=1)

        # --- password reveal button ---
        if password:
            self._reveal_btn = QtWidgets.QPushButton()
            self._reveal_btn.setFixedSize(28, 28)
            self._reveal_btn.setFlat(True)
            self._reveal_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            self._reveal_btn.setCheckable(True)
            self._reveal_btn.setIcon(qta.icon("mdi6.eye-off-outline", color=p["text_muted"]))
            self._reveal_btn.setStyleSheet("background: transparent; border: none;")
            self._reveal_btn.setToolTip("Show / hide password")
            self._reveal_btn.toggled.connect(self._toggle_reveal)
            field_row.addWidget(self._reveal_btn)

        # --- validation icon ---
        self._val_icon = QtWidgets.QLabel()
        self._val_icon.setFixedSize(20, 20)
        self._val_icon.hide()
        field_row.addWidget(self._val_icon)

        # --- floating label (drawn as a child widget above field_frame) ---
        self._float_label = QtWidgets.QLabel(label, self)
        self._float_label.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self._label_anim = QtCore.QPropertyAnimation(self._float_label, b"geometry")
        self._label_anim.setDuration(150)
        self._label_anim.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)

        # --- helper text (error/hint) ---
        self._helper = QtWidgets.QLabel()
        self._helper.setStyleSheet(f"font-size: 11px; color: {p['text_muted']}; background: transparent;")
        outer.addWidget(self._helper)

        self._apply_mode(mode)
        self._update_label_pos(floated=False, animate=False)

        # connections
        self._edit.textChanged.connect(self._on_text_changed)
        self._edit.focusInEvent = self._on_focus_in   # type: ignore[assignment]
        self._edit.focusOutEvent = self._on_focus_out  # type: ignore[assignment]
        self._edit.textChanged.connect(self.textChanged)

    # -- public API -------------------------------------------------------
    def text(self) -> str:
        return self._edit.text()

    def setText(self, t: str) -> None:
        self._edit.setText(t)

    def setMode(self, mode: str, helper_text: str = "") -> None:
        self._mode = mode
        self._apply_mode(mode, helper_text)

    def setEnabled(self, enabled: bool) -> None:
        super().setEnabled(enabled)
        self._edit.setEnabled(enabled)
        self._apply_mode(self._mode)

    # -- internal ----------------------------------------------------------
    def _apply_mode(self, mode: str, helper_text: str = "") -> None:
        p = theme_manager.palette
        border_colors = {
            "normal":  p["text_muted"],
            "focus":   p["accent"],
            "error":   "#D32F2F",
            "success": "#388E3C",
        }
        col = border_colors.get(mode, p["text_muted"])

        self._field_frame.setStyleSheet(f"""
            QFrame {{
                background: {p['input_bg']};
                border: 2px solid {col};
                border-radius: 12px;
            }}
        """)

        lbl_col = col if mode in ("error", "success") else p["text_muted"]
        if self._floated:
            lbl_col = border_colors.get(
                mode if mode in ("error", "success") else "focus",
                p["accent"]
            )
        self._float_label.setStyleSheet(
            f"font-size: {'10px' if self._floated else '13px'}; "
            f"color: {lbl_col}; background: transparent;"
        )

        # validation icon
        if mode == "error":
            self._val_icon.setPixmap(
                qta.icon("mdi6.alert-circle-outline", color="#D32F2F").pixmap(20, 20))
            self._val_icon.show()
        elif mode == "success":
            self._val_icon.setPixmap(
                qta.icon("mdi6.check-circle-outline", color="#388E3C").pixmap(20, 20))
            self._val_icon.show()
        else:
            self._val_icon.hide()

        if helper_text:
            col_map = {"error": "#D32F2F", "success": "#388E3C"}
            hc = col_map.get(mode, p["text_muted"])
            self._helper.setStyleSheet(
                f"font-size: 11px; color: {hc}; background: transparent;")
            self._helper.setText(helper_text)
        else:
            self._helper.setText("")

    def _update_label_pos(self, floated: bool, animate: bool = True) -> None:
        self._floated = floated
        ff = self._field_frame
        # floated: small label above the field frame top edge
        # normal : large label sitting inside the field (placeholder-like)
        if floated:
            target = QtCore.QRect(16, 0, ff.width() - 20, 14)
            font_size = "10px"
        else:
            target = QtCore.QRect(16, ff.y() + 16, ff.width() - 20, 20)
            font_size = "13px"

        # update font size immediately so sizeHint is correct
        p = theme_manager.palette
        col = p["accent"] if floated else p["text_muted"]
        self._float_label.setStyleSheet(
            f"font-size: {font_size}; color: {col}; background: transparent;")

        if animate and self._float_label.isVisible():
            self._label_anim.stop()
            self._label_anim.setStartValue(self._float_label.geometry())
            self._label_anim.setEndValue(target)
            self._label_anim.start()
        else:
            self._float_label.setGeometry(target)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._update_label_pos(self._floated, animate=False)

    def _on_text_changed(self, text: str) -> None:
        if text and not self._floated:
            self._update_label_pos(True)
        elif not text and self._floated and not self._edit.hasFocus():
            self._update_label_pos(False)
        self._apply_mode(self._mode)

    def _on_focus_in(self, event) -> None:
        QtWidgets.QLineEdit.focusInEvent(self._edit, event)
        self._update_label_pos(True)
        if self._mode not in ("error", "success"):
            self._apply_mode("focus")

    def _on_focus_out(self, event) -> None:
        QtWidgets.QLineEdit.focusOutEvent(self._edit, event)
        if not self._edit.text():
            self._update_label_pos(False)
        if self._mode not in ("error", "success"):
            self._apply_mode("normal")

    def _toggle_reveal(self, revealed: bool) -> None:
        p = theme_manager.palette
        if revealed:
            self._edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            self._reveal_btn.setIcon(qta.icon("mdi6.eye-outline", color=p["text"]))
        else:
            self._edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self._reveal_btn.setIcon(qta.icon("mdi6.eye-off-outline", color=p["text_muted"]))


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

    title = QtWidgets.QLabel("Fields")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    desc = QtWidgets.QLabel(
        "Form input fields with animated floating labels, validation feedback "
        "states, and password reveal toggle."
    )
    desc.setWordWrap(True)
    desc.setProperty("subheading", True)
    layout.addWidget(desc)

    # --- Floating Label Fields ---
    group1 = QtWidgets.QGroupBox("Floating Label Fields")
    g1 = QtWidgets.QVBoxLayout(group1)
    g1.setContentsMargins(16, 24, 16, 16)
    g1.setSpacing(20)

    form_row1 = QtWidgets.QHBoxLayout()
    form_row1.setSpacing(16)
    first_name = FloatingLabelField("First Name", "John")
    last_name = FloatingLabelField("Last Name", "Doe")
    form_row1.addWidget(first_name)
    form_row1.addWidget(last_name)
    g1.addLayout(form_row1)

    email_field = FloatingLabelField("Email Address", "you@example.com")
    g1.addWidget(email_field)

    pw_field = FloatingLabelField("Password", "", password=True)
    g1.addWidget(pw_field)

    layout.addWidget(_neu_group(group1))

    # --- Validation States ---
    group2 = QtWidgets.QGroupBox("Validation States")
    g2 = QtWidgets.QVBoxLayout(group2)
    g2.setContentsMargins(16, 24, 16, 16)
    g2.setSpacing(20)

    error_field = FloatingLabelField("Username", "")
    error_field.setText("ab")
    error_field.setMode("error", "Username must be at least 3 characters.")
    g2.addWidget(error_field)

    success_field = FloatingLabelField("Email", "")
    success_field.setText("user@example.com")
    success_field.setMode("success", "Email is valid.")
    g2.addWidget(success_field)

    disabled_field = FloatingLabelField("Disabled Field", "")
    disabled_field.setText("Cannot edit")
    disabled_field.setEnabled(False)
    g2.addWidget(disabled_field)

    layout.addWidget(_neu_group(group2))

    # --- Multiline ---
    group3 = QtWidgets.QGroupBox("Multiline / Plain Text")
    g3 = QtWidgets.QVBoxLayout(group3)
    g3.setContentsMargins(16, 24, 16, 16)
    g3.setSpacing(12)

    plain = QtWidgets.QPlainTextEdit()
    plain.setPlaceholderText("Type your message…")
    plain.setMinimumHeight(120)
    g3.addWidget(plain)

    char_counter = QtWidgets.QLabel("0 / 500 characters")
    char_counter.setStyleSheet(f"font-size: 11px; color: {p['text_muted']}; background: transparent;")
    char_counter.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

    def _update_count():
        n = len(plain.toPlainText())
        char_counter.setText(f"{n} / 500 characters")
        if n > 500:
            char_counter.setStyleSheet("font-size: 11px; color: #D32F2F; background: transparent;")
        else:
            char_counter.setStyleSheet(f"font-size: 11px; color: {p['text_muted']}; background: transparent;")

    plain.textChanged.connect(_update_count)
    g3.addWidget(char_counter)

    layout.addWidget(_neu_group(group3))

    # --- Live validation demo ---
    group4 = QtWidgets.QGroupBox("Live Validation")
    g4 = QtWidgets.QVBoxLayout(group4)
    g4.setContentsMargins(16, 24, 16, 16)
    g4.setSpacing(12)

    live_email = FloatingLabelField("Email", "")
    result_lbl = QtWidgets.QLabel("Type a valid email address.")
    result_lbl.setStyleSheet(f"font-size: 12px; color: {p['text_muted']}; background: transparent;")

    def _validate_email(text: str) -> None:
        if not text:
            live_email.setMode("normal", "")
            result_lbl.setText("Type a valid email address.")
            result_lbl.setStyleSheet(f"font-size: 12px; color: {p['text_muted']}; background: transparent;")
        elif "@" in text and "." in text.split("@")[-1]:
            live_email.setMode("success", "Looks good!")
            result_lbl.setText("✓ Valid email format")
            result_lbl.setStyleSheet("font-size: 12px; color: #388E3C; background: transparent;")
        else:
            live_email.setMode("error", "Enter a valid email address.")
            result_lbl.setText("✗ Invalid format")
            result_lbl.setStyleSheet("font-size: 12px; color: #D32F2F; background: transparent;")

    live_email.textChanged.connect(_validate_email)

    submit_btn = QtWidgets.QPushButton("Submit")
    submit_btn.setProperty("accentButton", True)
    submit_btn.setIcon(qta.icon("mdi6.send-outline", color="#FFFFFF"))

    g4.addWidget(live_email)
    g4.addWidget(result_lbl)
    g4.addWidget(submit_btn)
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

    title = QtWidgets.QLabel("About Fields")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    info = QtWidgets.QLabel(
        "Form input field widgets:\n\n"
        "  • FloatingLabelField – animated floating label (rises on focus)\n"
        "  • Password field – with eye-icon reveal toggle\n"
        "  • Validation modes: normal / error / success\n"
        "  • QPlainTextEdit – multiline with character counter\n"
        "  • Live validation – real-time feedback while typing\n\n"
        "FloatingLabelField is a standalone widget importable as:\n"
        "  from widgets.catalog.fields_demo import FloatingLabelField"
    )
    info.setWordWrap(True)
    layout.addWidget(info)
    layout.addStretch()
    return page


registry.register(WidgetDemo(
    id="fields",
    name="Fields",
    create_page=create_page,
    create_about=create_about,
    description="Form input fields with floating labels and validation states.",
))
