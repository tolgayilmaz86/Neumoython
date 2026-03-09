"""Fields demo – form input fields matching Neumorphism.Avalonia themes.

Covers Classic (inset), Filled (filled bg + inset), Outline (outset + inset),
Header (icon slots), and NumericUpDown field themes.
"""

from __future__ import annotations

import qtawesome as qta
from PySide6 import QtCore, QtGui, QtWidgets

from widgets.registry import registry, WidgetDemo
from widgets.box_shadow import BoxShadow, BoxShadowWrapper
from styles.theme_manager import theme_manager


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _neu_group(group: QtWidgets.QGroupBox) -> BoxShadowWrapper:
    shadows = theme_manager.shadow_configs()
    return BoxShadowWrapper(
        group, shadow_list=shadows["outside_raised"],
        smooth=True, margins=(12, 12, 12, 12),
    )


def _theme_props(theme: str) -> dict:
    """Return bg / shadow-key / border colour for a field theme."""
    p = theme_manager.palette
    if theme == "filled":
        return {"bg": p["bg_secondary"], "shadow": "input_inset",
                "border": p["bg_secondary"]}
    if theme == "outline":
        return {"bg": p["card_bg"], "shadow": "input_outline",
                "border": p["text_muted"]}
    # classic (default)
    return {"bg": p["input_bg"], "shadow": "input_inset",
            "border": p["input_bg"]}


def _sub_label(text: str) -> QtWidgets.QLabel:
    p = theme_manager.palette
    lbl = QtWidgets.QLabel(text)
    lbl.setStyleSheet(
        f"font-size: 13px; font-weight: 600; color: {p['text_muted']}; "
        "background: transparent; margin-top: 6px;")
    return lbl


# ---------------------------------------------------------------------------
# FloatingLabelField – custom widget with animated placeholder label
# ---------------------------------------------------------------------------

class FloatingLabelField(QtWidgets.QWidget):
    """QLineEdit wrapped with an animated floating label.

    Modes: "normal", "error", "success"
    Themes: "classic" (inset), "filled" (darker bg + inset),
            "outline" (outset + inset + visible border)
    """

    textChanged = QtCore.Signal(str)

    def __init__(self, label: str = "Label", placeholder: str = "",
                 mode: str = "normal", password: bool = False,
                 theme: str = "classic", clear_button: bool = False,
                 floating: bool = True,
                 parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self._label_text = label
        self._mode = mode
        self._password = password
        self._floated = False
        self._theme = theme
        self._floating = floating

        p = theme_manager.palette

        # --- outer container ---
        outer = QtWidgets.QVBoxLayout(self)
        top_margin = 12 if floating else 4
        side = 10 if theme == "outline" else 0
        outer.setContentsMargins(side, top_margin, side, 0)
        outer.setSpacing(0)

        # --- field container (border drawn here) ---
        self._field_frame = QtWidgets.QFrame()
        self._field_frame.setMinimumHeight(52)
        outer.addWidget(self._field_frame)

        # Neumorphic shadow
        shadows = theme_manager.shadow_configs()
        tp = _theme_props(theme)
        self._shadow = BoxShadow(shadows[tp["shadow"]], smooth=True)
        self._field_frame.setGraphicsEffect(self._shadow)

        field_row = QtWidgets.QHBoxLayout(self._field_frame)
        field_row.setContentsMargins(14, 18 if floating else 10, 8, 4 if floating else 10)
        field_row.setSpacing(6)

        # --- line edit ---
        self._edit = QtWidgets.QLineEdit()
        self._edit.setPlaceholderText(placeholder if not floating else placeholder)
        self._edit.setStyleSheet(
            "background: transparent; border: none; padding: 0;")
        if password:
            self._edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        field_row.addWidget(self._edit, stretch=1)

        # --- clear button ---
        self._clear_btn: QtWidgets.QPushButton | None = None
        if clear_button:
            self._clear_btn = QtWidgets.QPushButton()
            self._clear_btn.setFixedSize(24, 24)
            self._clear_btn.setFlat(True)
            self._clear_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            self._clear_btn.setIcon(
                qta.icon("mdi6.close-circle-outline", color=p["text_muted"]))
            self._clear_btn.setStyleSheet(
                "background: transparent; border: none;")
            self._clear_btn.setToolTip("Clear")
            self._clear_btn.clicked.connect(lambda: self._edit.clear())
            self._clear_btn.hide()
            field_row.addWidget(self._clear_btn)

        # --- password reveal button ---
        if password:
            self._reveal_btn = QtWidgets.QPushButton()
            self._reveal_btn.setFixedSize(28, 28)
            self._reveal_btn.setFlat(True)
            self._reveal_btn.setCursor(
                QtCore.Qt.CursorShape.PointingHandCursor)
            self._reveal_btn.setCheckable(True)
            self._reveal_btn.setIcon(
                qta.icon("mdi6.eye-off-outline", color=p["text_muted"]))
            self._reveal_btn.setStyleSheet(
                "background: transparent; border: none;")
            self._reveal_btn.setToolTip("Show / hide password")
            self._reveal_btn.toggled.connect(self._toggle_reveal)
            field_row.addWidget(self._reveal_btn)

        # --- validation icon ---
        self._val_icon = QtWidgets.QLabel()
        self._val_icon.setFixedSize(20, 20)
        self._val_icon.hide()
        field_row.addWidget(self._val_icon)

        # --- floating label ---
        if floating:
            self._float_label = QtWidgets.QLabel(label, self)
            self._float_label.setAttribute(
                QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            self._label_anim = QtCore.QPropertyAnimation(
                self._float_label, b"geometry")
            self._label_anim.setDuration(150)
            self._label_anim.setEasingCurve(
                QtCore.QEasingCurve.Type.OutCubic)
        else:
            self._float_label = None  # type: ignore[assignment]
            self._label_anim = None  # type: ignore[assignment]

        # --- helper text ---
        self._helper = QtWidgets.QLabel()
        self._helper.setStyleSheet(
            f"font-size: 11px; color: {p['text_muted']}; "
            "background: transparent;")
        outer.addWidget(self._helper)

        self._apply_mode(mode)
        if floating:
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
        tp = _theme_props(self._theme)

        border_map = {
            "normal":  tp["border"],
            "focus":   p["accent"],
            "error":   "#D32F2F",
            "success": "#388E3C",
        }
        col = border_map.get(mode, tp["border"])
        bw = 3 if (self._theme == "outline" and mode == "focus") else 2

        self._field_frame.setStyleSheet(f"""
            QFrame {{
                background: {tp['bg']};
                border: {bw}px solid {col};
                border-radius: 12px;
            }}
        """)

        if self._floating and self._float_label is not None:
            lbl_col = col if mode in ("error", "success") else p["text_muted"]
            if self._floated:
                lbl_col = border_map.get(
                    mode if mode in ("error", "success") else "focus",
                    p["accent"])
            self._float_label.setStyleSheet(
                f"font-size: {'10px' if self._floated else '13px'}; "
                f"color: {lbl_col}; background: transparent;")

        # validation icon
        if mode == "error":
            self._val_icon.setPixmap(
                qta.icon("mdi6.alert-circle-outline",
                         color="#D32F2F").pixmap(20, 20))
            self._val_icon.show()
        elif mode == "success":
            self._val_icon.setPixmap(
                qta.icon("mdi6.check-circle-outline",
                         color="#388E3C").pixmap(20, 20))
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
        if not self._floating:
            return
        self._floated = floated
        ff = self._field_frame
        if floated:
            target = QtCore.QRect(16, 0, ff.width() - 20, 14)
            font_size = "10px"
        else:
            target = QtCore.QRect(16, ff.y() + 16, ff.width() - 20, 20)
            font_size = "13px"

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
        if self._floating:
            self._update_label_pos(self._floated, animate=False)

    def _on_text_changed(self, text: str) -> None:
        if self._clear_btn is not None:
            self._clear_btn.setVisible(bool(text))
        if self._floating:
            if text and not self._floated:
                self._update_label_pos(True)
            elif not text and self._floated and not self._edit.hasFocus():
                self._update_label_pos(False)
        self._apply_mode(self._mode)

    def _on_focus_in(self, event) -> None:
        QtWidgets.QLineEdit.focusInEvent(self._edit, event)
        if self._floating:
            self._update_label_pos(True)
        if self._mode not in ("error", "success"):
            self._apply_mode("focus")

    def _on_focus_out(self, event) -> None:
        QtWidgets.QLineEdit.focusOutEvent(self._edit, event)
        if self._floating and not self._edit.text():
            self._update_label_pos(False)
        if self._mode not in ("error", "success"):
            self._apply_mode("normal")

    def _toggle_reveal(self, revealed: bool) -> None:
        p = theme_manager.palette
        if revealed:
            self._edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            self._reveal_btn.setIcon(
                qta.icon("mdi6.eye-outline", color=p["text"]))
        else:
            self._edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self._reveal_btn.setIcon(
                qta.icon("mdi6.eye-off-outline", color=p["text_muted"]))


# ---------------------------------------------------------------------------
# NeuMultiline – themed multiline text field
# ---------------------------------------------------------------------------

class _NeuMultiline(QtWidgets.QWidget):
    """QPlainTextEdit with floating label and neumorphic shadow."""

    def __init__(self, label: str = "", theme: str = "classic",
                 height: int = 360, dynamic: bool = False) -> None:
        super().__init__()
        p = theme_manager.palette
        shadows = theme_manager.shadow_configs()
        tp = _theme_props(theme)

        outer = QtWidgets.QVBoxLayout(self)
        side = 10 if theme == "outline" else 0
        outer.setContentsMargins(side, 12 if label else 4, side, 0)
        outer.setSpacing(0)

        # Floating label above the field
        if label:
            self._float_lbl = QtWidgets.QLabel(label)
            self._float_lbl.setStyleSheet(
                f"font-size: 10px; color: {p['accent']}; "
                "background: transparent;")
            outer.addWidget(self._float_lbl)

        self._frame = QtWidgets.QFrame()
        if dynamic:
            self._frame.setMinimumHeight(50)
            self._frame.setMaximumHeight(height)
        else:
            self._frame.setFixedHeight(height)
        self._frame.setStyleSheet(f"""
            QFrame {{
                background: {tp['bg']};
                border: 2px solid {tp['border']};
                border-radius: 12px;
            }}
        """)
        shadow = BoxShadow(shadows[tp["shadow"]], smooth=True)
        self._frame.setGraphicsEffect(shadow)

        fl = QtWidgets.QVBoxLayout(self._frame)
        fl.setContentsMargins(2, 2, 2, 2)

        self._edit = QtWidgets.QPlainTextEdit()
        self._edit.setPlaceholderText(label or "Type here…")
        self._edit.setStyleSheet(
            f"background: transparent; border: none; color: {p['text']};")
        fl.addWidget(self._edit)

        outer.addWidget(self._frame)


# ---------------------------------------------------------------------------
# HeaderField – field with icon areas
# ---------------------------------------------------------------------------

class _HeaderField(QtWidgets.QWidget):
    """Input field with optional left/right icon area, matching Avalonia
    TextBoxHeader theme."""

    textChanged = QtCore.Signal(str)

    def __init__(self, placeholder: str = "", left_icon: str | None = None,
                 right_icon: str | None = None, rounded: bool = False,
                 width: int = 300, has_border: bool = False) -> None:
        super().__init__()
        p = theme_manager.palette
        shadows = theme_manager.shadow_configs()
        radius = 24 if rounded else 12

        self.setFixedWidth(width)

        outer = QtWidgets.QVBoxLayout(self)
        outer.setContentsMargins(0, 4, 0, 4)
        outer.setSpacing(0)

        self._frame = QtWidgets.QFrame()
        self._frame.setFixedHeight(42)
        border_col = p["text_muted"] if has_border else p["input_bg"]
        self._frame.setStyleSheet(f"""
            QFrame {{
                background: {p['input_bg']};
                border: 1px solid {border_col};
                border-radius: {radius}px;
            }}
        """)
        shadow = BoxShadow(shadows["input_inset"], smooth=True)
        self._frame.setGraphicsEffect(shadow)

        row = QtWidgets.QHBoxLayout(self._frame)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)

        # -- left icon area --
        if left_icon:
            left_area = QtWidgets.QFrame()
            left_area.setFixedSize(48, 42)
            left_area.setStyleSheet(
                f"background: rgba(128,128,128,0.12); border: none; "
                f"border-top-left-radius: {radius}px; "
                f"border-bottom-left-radius: {radius}px;")
            ll = QtWidgets.QHBoxLayout(left_area)
            ll.setContentsMargins(0, 0, 0, 0)
            ic = QtWidgets.QLabel()
            ic.setPixmap(qta.icon(left_icon,
                                  color=p["text_muted"]).pixmap(22, 22))
            ic.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            ll.addWidget(ic)
            row.addWidget(left_area)

        # -- line edit --
        self._edit = QtWidgets.QLineEdit()
        self._edit.setPlaceholderText(placeholder)
        self._edit.setStyleSheet(
            "background: transparent; border: none; padding: 0 12px;")
        row.addWidget(self._edit, stretch=1)
        self._edit.textChanged.connect(self.textChanged)

        # -- right icon area --
        if right_icon:
            right_area = QtWidgets.QFrame()
            right_area.setFixedSize(48, 42)
            right_area.setStyleSheet(
                f"background: rgba(128,128,128,0.08); border: none; "
                f"border-top-right-radius: {radius}px; "
                f"border-bottom-right-radius: {radius}px;")
            rl = QtWidgets.QHBoxLayout(right_area)
            rl.setContentsMargins(0, 0, 0, 0)
            ic2 = QtWidgets.QLabel()
            ic2.setPixmap(qta.icon(right_icon,
                                   color=p["text_muted"]).pixmap(22, 22))
            ic2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            rl.addWidget(ic2)
            row.addWidget(right_area)

        outer.addWidget(self._frame)

    def text(self) -> str:
        return self._edit.text()

    def setText(self, t: str) -> None:
        self._edit.setText(t)


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------

def _build_field_column(theme: str) -> QtWidgets.QWidget:
    """Build a complete single-line + multi-line column for *theme*."""
    p = theme_manager.palette
    col = QtWidgets.QWidget()
    lay = QtWidgets.QHBoxLayout(col)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(16)

    # --- Single-line fields ---
    single = QtWidgets.QWidget()
    sl = QtWidgets.QVBoxLayout(single)
    sl.setContentsMargins(0, 0, 0, 0)
    sl.setSpacing(4)
    sl.addWidget(_sub_label("Single-Line fields"))

    # 1. Regular watermarked (non-floating)
    sl.addWidget(FloatingLabelField(
        "Regular watermarked textbox", "Regular watermarked textbox",
        theme=theme, floating=False))

    # 2. Floating watermark
    sl.addWidget(FloatingLabelField(
        "Floating watermark TextBox", theme=theme))

    # 3. Password with reveal
    sl.addWidget(FloatingLabelField(
        "Password", password=True, theme=theme))

    # 4. Clear button
    sl.addWidget(FloatingLabelField(
        "Text field", theme=theme, clear_button=True))

    # 5. Validation (error)
    val_field = FloatingLabelField(
        "Text field with validation", theme=theme)
    val_field.setText("12345")
    val_field.setMode("error", "Only letters are allowed.")
    sl.addWidget(val_field)

    # 6. Disabled
    dis_field = FloatingLabelField(
        "Disabled Field", theme=theme)
    dis_field.setText("Disabled Field")
    dis_field.setEnabled(False)
    sl.addWidget(dis_field)

    sl.addStretch()
    lay.addWidget(single, stretch=1)

    # --- Multi-line fields ---
    multi = QtWidgets.QWidget()
    ml = QtWidgets.QVBoxLayout(multi)
    ml.setContentsMargins(0, 0, 0, 0)
    ml.setSpacing(4)
    ml.addWidget(_sub_label("Multi-Line fields"))

    ml.addWidget(_NeuMultiline(
        "Multiline Test fixed height", theme=theme, height=300))

    if theme == "classic":
        ml.addWidget(_NeuMultiline(
            "Multiline Test dynamic height", theme=theme,
            height=300, dynamic=True))

    ml.addStretch()
    lay.addWidget(multi, stretch=1)
    return col


def _build_header_section() -> QtWidgets.QWidget:
    """Build the Header fields section."""
    w = QtWidgets.QWidget()
    lay = QtWidgets.QVBoxLayout(w)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(12)

    # 1. Left icon
    lay.addWidget(_HeaderField(
        "Header field with left icon",
        left_icon="mdi6.magnify"))

    # 2. Right icon
    lay.addWidget(_HeaderField(
        "Header field with right icon",
        right_icon="mdi6.magnify"))

    # 3. Custom search (left + right)
    lay.addWidget(_HeaderField(
        "Custom search field",
        left_icon="mdi6.magnify",
        right_icon="mdi6.cog-outline",
        width=360))

    # 4. Email with border, pill shape, left icon
    lay.addWidget(_HeaderField(
        "Enter your email",
        left_icon="mdi6.email-outline",
        rounded=True, has_border=True, width=350))

    # 5. Email with left + right, pill shape
    lay.addWidget(_HeaderField(
        "Enter your email",
        left_icon="mdi6.email-outline",
        right_icon="mdi6.comment-question-outline",
        rounded=True, has_border=True, width=350))

    return w


def _build_numeric_section() -> QtWidgets.QWidget:
    """Build the Numeric Up Down section."""
    p = theme_manager.palette
    shadows = theme_manager.shadow_configs()

    w = QtWidgets.QWidget()
    lay = QtWidgets.QVBoxLayout(w)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(12)

    def _styled_spin(minimum: int = 0, maximum: int = 100,
                     step: int = 1, value: int | None = None,
                     prefix: str = "", suffix: str = "",
                     width: int = 0, enabled: bool = True
                     ) -> QtWidgets.QWidget:
        spin = QtWidgets.QSpinBox()
        spin.setRange(minimum, maximum)
        spin.setSingleStep(step)
        if value is not None:
            spin.setValue(value)
        if prefix:
            spin.setPrefix(prefix)
        if suffix:
            spin.setSuffix(suffix)
        if width:
            spin.setFixedWidth(width)
        spin.setEnabled(enabled)
        spin.setMinimumHeight(42)
        spin.setStyleSheet(f"""
            QSpinBox {{
                background: {p['input_bg']};
                border: 2px solid {p['input_bg']};
                border-radius: 10px;
                padding: 6px 10px;
            }}
            QSpinBox:focus {{
                border: 2px solid {p['accent']};
            }}
        """)
        shadow = BoxShadow(shadows["input_inset"], smooth=True)
        spin.setGraphicsEffect(shadow)
        return spin

    # 1. Default 0–100
    lay.addWidget(_styled_spin(0, 100, 1, 0))

    # 2. Left-spinner, watermarked, -1000..1000 step 10
    spin2 = _styled_spin(-1000, 1000, 10, width=160)
    spin2.findChild(QtWidgets.QSpinBox) or spin2  # just the widget
    lay.addWidget(spin2)

    # 3. Percent, rounded, small
    lay.addWidget(_styled_spin(0, 100, 1, suffix=" %", width=110))

    # 4. Disabled
    lay.addWidget(_styled_spin(-100, 100, 10, enabled=False))

    return w


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
        "Form input fields with animated floating labels, validation, "
        "password reveal, and multiple neumorphic themes."
    )
    desc.setWordWrap(True)
    desc.setProperty("subheading", True)
    layout.addWidget(desc)

    # ── Classic Fields ────────────────────────────────────────────────────
    g_classic = QtWidgets.QGroupBox("Classic Fields")
    gc = QtWidgets.QVBoxLayout(g_classic)
    gc.setContentsMargins(16, 24, 16, 16)
    gc.addWidget(_build_field_column("classic"))
    layout.addWidget(_neu_group(g_classic))

    # ── Filled Fields ────────────────────────────────────────────────────
    g_filled = QtWidgets.QGroupBox("Filled Fields")
    gf = QtWidgets.QVBoxLayout(g_filled)
    gf.setContentsMargins(16, 24, 16, 16)
    gf.addWidget(_build_field_column("filled"))
    layout.addWidget(_neu_group(g_filled))

    # ── Outline Fields ───────────────────────────────────────────────────
    g_outline = QtWidgets.QGroupBox("Outline Fields")
    go = QtWidgets.QVBoxLayout(g_outline)
    go.setContentsMargins(16, 24, 16, 16)
    go.addWidget(_build_field_column("outline"))
    layout.addWidget(_neu_group(g_outline))

    # ── Header Fields ────────────────────────────────────────────────────
    g_header = QtWidgets.QGroupBox("Header Fields")
    gh = QtWidgets.QVBoxLayout(g_header)
    gh.setContentsMargins(16, 24, 16, 16)
    gh.addWidget(_build_header_section())
    layout.addWidget(_neu_group(g_header))

    # ── Numeric Up Down ──────────────────────────────────────────────────
    g_num = QtWidgets.QGroupBox("Numeric Up Down")
    gn = QtWidgets.QVBoxLayout(g_num)
    gn.setContentsMargins(16, 24, 16, 16)
    gn.addWidget(_build_numeric_section())
    layout.addWidget(_neu_group(g_num))

    # ── Live Validation ──────────────────────────────────────────────────
    g_live = QtWidgets.QGroupBox("Live Validation")
    gl = QtWidgets.QVBoxLayout(g_live)
    gl.setContentsMargins(16, 24, 16, 16)
    gl.setSpacing(12)

    live_email = FloatingLabelField("Email", "")
    result_lbl = QtWidgets.QLabel("Type a valid email address.")
    result_lbl.setStyleSheet(
        f"font-size: 12px; color: {p['text_muted']}; "
        "background: transparent;")

    def _validate_email(text: str) -> None:
        if not text:
            live_email.setMode("normal", "")
            result_lbl.setText("Type a valid email address.")
            result_lbl.setStyleSheet(
                f"font-size: 12px; color: {p['text_muted']}; "
                "background: transparent;")
        elif "@" in text and "." in text.split("@")[-1]:
            live_email.setMode("success", "Looks good!")
            result_lbl.setText("✓ Valid email format")
            result_lbl.setStyleSheet(
                "font-size: 12px; color: #388E3C; "
                "background: transparent;")
        else:
            live_email.setMode("error", "Enter a valid email address.")
            result_lbl.setText("✗ Invalid format")
            result_lbl.setStyleSheet(
                "font-size: 12px; color: #D32F2F; "
                "background: transparent;")

    live_email.textChanged.connect(_validate_email)

    submit_btn = QtWidgets.QPushButton("Submit")
    submit_btn.setProperty("accentButton", True)
    submit_btn.setIcon(qta.icon("mdi6.send-outline", color="#FFFFFF"))

    gl.addWidget(live_email)
    gl.addWidget(result_lbl)
    gl.addWidget(submit_btn)
    layout.addWidget(_neu_group(g_live))

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
        "Form input field widgets matching Neumorphism.Avalonia themes:\n\n"
        "  • Classic – inset shadow for recessed look\n"
        "  • Filled – darker background + inset shadow\n"
        "  • Outline – outset + inset shadow for prominent border\n"
        "  • Header – iconic fields with left/right content areas\n"
        "  • Numeric Up Down – spin-box variants\n\n"
        "Each theme supports:\n"
        "  – Floating / non-floating watermark labels\n"
        "  – Password reveal toggle\n"
        "  – Clear button\n"
        "  – Validation feedback (error / success)\n"
        "  – Disabled state\n"
        "  – Single-line and multi-line variants\n\n"
        "FloatingLabelField is importable as:\n"
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
