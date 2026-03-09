"""Sliders demo – matching Neumorphism.Avalonia slider showcase.

Four sections: Horizontal, Vertical, Horizontal Outset, Vertical Outset.
Each section shows regular, accent-light with ticks, accent with icon thumb,
gradient with value-in-thumb, and disabled variants.
"""

from __future__ import annotations

import qtawesome as qta

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QSlider

from widgets.registry import registry, WidgetDemo
from widgets.box_shadow import BoxShadowWrapper
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


def _label(text: str) -> QtWidgets.QLabel:
    lbl = QtWidgets.QLabel(text)
    lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    lbl.setFixedWidth(40)
    return lbl


# ---------------------------------------------------------------------------
# Neumorphic painting helpers
# ---------------------------------------------------------------------------

def _parse_rgba(s: str) -> QtGui.QColor:
    """Parse an 'rgba(r,g,b,a)' palette string into QColor."""
    s = s.strip()
    if s.startswith("rgba("):
        parts = s[5:-1].split(",")
        return QtGui.QColor(int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]))
    return QtGui.QColor(s)


def _draw_inset_groove(p: QtGui.QPainter, groove: QtCore.QRectF, pal: dict,
                       radius: float = 3.0) -> None:
    """Paint a neumorphic inset (pressed-in) groove."""
    dark = _parse_rgba(pal['shadow_dark'])
    light = _parse_rgba(pal['shadow_light'])
    bg = QtGui.QColor(pal['bg'])

    # Outer dark shadow (top-left light source → shadow bottom-right)
    p.setPen(QtCore.Qt.PenStyle.NoPen)
    p.setBrush(dark)
    p.drawRoundedRect(groove.adjusted(-1, -1, 1, 1), radius + 1, radius + 1)

    # Inner light edge (highlight top-left)
    p.setBrush(light)
    p.drawRoundedRect(groove.adjusted(0, 0, 2, 2), radius + 1, radius + 1)

    # Fill the groove surface on top
    p.setBrush(bg)
    p.drawRoundedRect(groove, radius, radius)


def _draw_outset_thumb(p: QtGui.QPainter, center: QtCore.QPointF,
                       radius: float, fill: QtGui.QColor, pal: dict) -> None:
    """Paint a neumorphic outset (raised) circular thumb."""
    dark = _parse_rgba(pal['shadow_dark'])
    light = _parse_rgba(pal['shadow_light'])

    p.setPen(QtCore.Qt.PenStyle.NoPen)

    # Dark shadow offset (bottom-right)
    p.setBrush(dark)
    p.drawEllipse(center + QtCore.QPointF(2, 2), radius, radius)

    # Light highlight offset (top-left)
    p.setBrush(light)
    p.drawEllipse(center + QtCore.QPointF(-1.5, -1.5), radius, radius)

    # Thumb face
    p.setBrush(fill)
    p.drawEllipse(center, radius, radius)


# ---------------------------------------------------------------------------
# Base neumorphic slider – replaces plain QSlider for consistent look
# ---------------------------------------------------------------------------

class _NeuSlider(QtWidgets.QAbstractSlider):
    """Fully custom-painted neumorphic slider (inset groove + outset thumb).

    Supports variants:
      - "" (default)    : accent-coloured fill & thumb
      - "accent-light"  : accent_hover colour
      - "outset"        : raised groove with border shadows
    Supports tick marks and disabled state.
    """

    _THUMB_SIZE = 18
    _GROOVE_THICK = 6

    def __init__(self, orientation, *, variant: str = "",
                 tick_interval: int = 0, parent=None):
        super().__init__(parent)
        self.setOrientation(orientation)
        self._variant = variant
        self._tick_interval = tick_interval
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent; border: none;")

    # -- geometry helpers ---------------------------------------------------

    def _groove_rect(self) -> QtCore.QRectF:
        ts = self._THUMB_SIZE
        gt = self._GROOVE_THICK
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            return QtCore.QRectF(
                ts / 2, self.height() / 2 - gt / 2,
                self.width() - ts, gt)
        else:
            return QtCore.QRectF(
                self.width() / 2 - gt / 2, ts / 2,
                gt, self.height() - ts)

    def _frac(self) -> float:
        rng = self.maximum() - self.minimum()
        return (self.value() - self.minimum()) / rng if rng else 0.0

    def _thumb_center(self) -> QtCore.QPointF:
        ts = self._THUMB_SIZE
        frac = self._frac()
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            x = ts / 2 + frac * (self.width() - ts)
            return QtCore.QPointF(x, self.height() / 2)
        else:
            y = self.height() - ts / 2 - frac * (self.height() - ts)
            return QtCore.QPointF(self.width() / 2, y)

    # -- colours based on variant / enabled ---------------------------------

    def _accent_color(self, pal: dict) -> QtGui.QColor:
        if not self.isEnabled():
            return QtGui.QColor(pal['text_muted'])
        if self._variant == "accent-light":
            return QtGui.QColor(pal['accent_hover'])
        return QtGui.QColor(pal['accent'])

    # -- paint --------------------------------------------------------------

    def paintEvent(self, event):  # noqa: N802
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        pal = theme_manager.palette
        accent = self._accent_color(pal)
        groove = self._groove_rect()
        frac = self._frac()

        # --- groove ---
        if self._variant == "outset":
            self._draw_outset_groove(p, groove, pal)
        else:
            _draw_inset_groove(p, groove, pal, radius=3.0)

        # --- filled portion ---
        p.setPen(QtCore.Qt.PenStyle.NoPen)
        p.setBrush(accent)
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            filled = QtCore.QRectF(groove.left(), groove.top(),
                                   groove.width() * frac, groove.height())
        else:
            filled = QtCore.QRectF(groove.left(),
                                   groove.top() + groove.height() * (1 - frac),
                                   groove.width(), groove.height() * frac)
        p.drawRoundedRect(filled, 3, 3)

        # --- tick marks (if any) ---
        if self._tick_interval > 0:
            self._draw_ticks(p, pal)

        # --- thumb ---
        center = self._thumb_center()
        ts = self._THUMB_SIZE
        if self._variant == "outset":
            self._draw_outset_variant_thumb(p, center, ts / 2, accent, pal)
        else:
            _draw_outset_thumb(p, center, ts / 2 - 1, accent, pal)

        p.end()

    # -- outset groove (raised) ---------------------------------------------

    @staticmethod
    def _draw_outset_groove(p: QtGui.QPainter, groove: QtCore.QRectF,
                            pal: dict, radius: float = 4.0) -> None:
        dark = _parse_rgba(pal['shadow_dark'])
        light = _parse_rgba(pal['shadow_light'])
        bg = QtGui.QColor(pal['bg_secondary'])

        p.setPen(QtCore.Qt.PenStyle.NoPen)
        # Light highlight (top-left) → appears raised
        p.setBrush(light)
        p.drawRoundedRect(groove.adjusted(-1.5, -1.5, 0, 0), radius, radius)
        # Dark shadow (bottom-right)
        p.setBrush(dark)
        p.drawRoundedRect(groove.adjusted(0, 0, 1.5, 1.5), radius, radius)
        # Surface
        p.setBrush(bg)
        p.drawRoundedRect(groove, radius, radius)

    # -- outset variant thumb (with border highlight) -----------------------

    @staticmethod
    def _draw_outset_variant_thumb(p: QtGui.QPainter, center: QtCore.QPointF,
                                   radius: float, fill: QtGui.QColor,
                                   pal: dict) -> None:
        dark = _parse_rgba(pal['shadow_dark'])
        light = _parse_rgba(pal['shadow_light'])

        p.setPen(QtCore.Qt.PenStyle.NoPen)
        # Dark shadow (bottom-right)
        p.setBrush(dark)
        p.drawEllipse(center + QtCore.QPointF(2.5, 2.5), radius, radius)
        # Light highlight (top-left)
        p.setBrush(light)
        p.drawEllipse(center + QtCore.QPointF(-2, -2), radius, radius)
        # Thumb face
        p.setBrush(fill)
        p.drawEllipse(center, radius, radius)
        # Border ring
        pen = QtGui.QPen(light, 2)
        p.setPen(pen)
        p.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        p.drawEllipse(center, radius - 1, radius - 1)

    # -- tick marks ---------------------------------------------------------

    def _draw_ticks(self, p: QtGui.QPainter, pal: dict) -> None:
        tick_color = QtGui.QColor(pal['text_muted'])
        tick_color.setAlpha(120)
        p.setPen(QtGui.QPen(tick_color, 1))

        rng = self.maximum() - self.minimum()
        if rng <= 0 or self._tick_interval <= 0:
            return

        ts = self._THUMB_SIZE
        steps = rng // self._tick_interval
        horiz = self.orientation() == QtCore.Qt.Orientation.Horizontal

        for i in range(steps + 1):
            frac = (i * self._tick_interval) / rng
            if horiz:
                x = ts / 2 + frac * (self.width() - ts)
                y_start = self.height() / 2 + self._GROOVE_THICK / 2 + 3
                p.drawLine(QtCore.QPointF(x, y_start),
                           QtCore.QPointF(x, y_start + 5))
            else:
                y = self.height() - ts / 2 - frac * (self.height() - ts)
                x_start = self.width() / 2 + self._GROOVE_THICK / 2 + 3
                p.drawLine(QtCore.QPointF(x_start, y),
                           QtCore.QPointF(x_start + 5, y))

    # -- sizing -------------------------------------------------------------

    def minimumSizeHint(self):
        ts = self._THUMB_SIZE
        extra = 14 if self._tick_interval > 0 else 4
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            return QtCore.QSize(120, ts + extra)
        return QtCore.QSize(ts + extra, 120)

    def sizeHint(self):
        return self.minimumSizeHint()

    # -- interaction --------------------------------------------------------

    def mousePressEvent(self, event):
        self._set_value_from_pos(event.position())

    def mouseMoveEvent(self, event):
        self._set_value_from_pos(event.position())

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        step = max(1, (self.maximum() - self.minimum()) // 20)
        self.setValue(self.value() + (step if delta > 0 else -step))

    def _set_value_from_pos(self, pos):
        ts = self._THUMB_SIZE
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            frac = (pos.x() - ts / 2) / max(self.width() - ts, 1)
        else:
            frac = 1.0 - (pos.y() - ts / 2) / max(self.height() - ts, 1)
        frac = max(0.0, min(1.0, frac))
        self.setValue(int(self.minimum() + frac * (self.maximum() - self.minimum())))


# ---------------------------------------------------------------------------
# Custom slider that paints the value inside an oversized thumb
# ---------------------------------------------------------------------------

class _ValueThumbSlider(QtWidgets.QAbstractSlider):
    """Slider with an enlarged circular thumb that shows the current value."""

    def __init__(self, orientation, *, thumb_size: int = 40, gradient: bool = False,
                 parent=None):
        super().__init__(parent)
        self.setOrientation(orientation)
        self._thumb_size = thumb_size
        self._gradient = gradient
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent; border: none;")

    def _groove_rect(self) -> QtCore.QRectF:
        ts = self._thumb_size
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            return QtCore.QRectF(
                ts / 2, self.height() / 2 - 3,
                self.width() - ts, 6)
        else:
            return QtCore.QRectF(
                self.width() / 2 - 3, ts / 2,
                6, self.height() - ts)

    def _frac(self) -> float:
        rng = self.maximum() - self.minimum()
        return (self.value() - self.minimum()) / rng if rng else 0.0

    def _thumb_center(self) -> QtCore.QPointF:
        ts = self._thumb_size
        frac = self._frac()
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            x = ts / 2 + frac * (self.width() - ts)
            return QtCore.QPointF(x, self.height() / 2)
        else:
            y = self.height() - ts / 2 - frac * (self.height() - ts)
            return QtCore.QPointF(self.width() / 2, y)

    def paintEvent(self, event):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        pal = theme_manager.palette
        accent = QtGui.QColor(pal['accent'])
        ts = self._thumb_size
        groove = self._groove_rect()
        frac = self._frac()

        # Neumorphic inset groove
        _draw_inset_groove(p, groove, pal, radius=3.0)

        # Filled portion on top of groove
        p.setPen(QtCore.Qt.PenStyle.NoPen)
        if self._gradient:
            grad_color = QtGui.QColor("#5cbcd6")
            if self.orientation() == QtCore.Qt.Orientation.Horizontal:
                grad = QtGui.QLinearGradient(groove.left(), 0, groove.right(), 0)
                grad.setColorAt(0.0, QtGui.QColor("#77dbf0"))
                grad.setColorAt(0.8, grad_color)
                filled = QtCore.QRectF(groove.left(), groove.top(),
                                       groove.width() * frac, groove.height())
            else:
                grad = QtGui.QLinearGradient(0, groove.bottom(), 0, groove.top())
                grad.setColorAt(0.0, QtGui.QColor("#77dbf0"))
                grad.setColorAt(0.8, grad_color)
                filled = QtCore.QRectF(groove.left(),
                                       groove.top() + groove.height() * (1 - frac),
                                       groove.width(), groove.height() * frac)
            p.setBrush(QtGui.QBrush(grad))
        else:
            if self.orientation() == QtCore.Qt.Orientation.Horizontal:
                filled = QtCore.QRectF(groove.left(), groove.top(),
                                       groove.width() * frac, groove.height())
            else:
                filled = QtCore.QRectF(groove.left(),
                                       groove.top() + groove.height() * (1 - frac),
                                       groove.width(), groove.height() * frac)
            p.setBrush(accent)
        p.drawRoundedRect(filled, 3, 3)

        # Neumorphic outset thumb with value text
        center = self._thumb_center()
        thumb_color = QtGui.QColor("#5cbcd6") if self._gradient else accent
        _draw_outset_thumb(p, center, ts / 2 - 1, thumb_color, pal)

        # Value text inside thumb
        p.setPen(QtGui.QColor("#FFFFFF"))
        font = p.font()
        font.setPixelSize(max(ts // 3, 10))
        font.setBold(True)
        p.setFont(font)
        text_rect = QtCore.QRectF(center.x() - ts / 2, center.y() - ts / 2, ts, ts)
        p.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, str(self.value()))
        p.end()

    def minimumSizeHint(self):
        ts = self._thumb_size
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            return QtCore.QSize(120, ts + 4)
        return QtCore.QSize(ts + 4, 120)

    def sizeHint(self):
        return self.minimumSizeHint()

    def mousePressEvent(self, event):
        self._set_value_from_pos(event.position())

    def mouseMoveEvent(self, event):
        self._set_value_from_pos(event.position())

    def _set_value_from_pos(self, pos):
        ts = self._thumb_size
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            frac = (pos.x() - ts / 2) / max(self.width() - ts, 1)
        else:
            frac = 1.0 - (pos.y() - ts / 2) / max(self.height() - ts, 1)
        frac = max(0.0, min(1.0, frac))
        val = int(self.minimum() + frac * (self.maximum() - self.minimum()))
        self.setValue(val)


# ---------------------------------------------------------------------------
# Custom slider with icon-painted thumb
# ---------------------------------------------------------------------------

class _IconThumbSlider(QtWidgets.QAbstractSlider):
    """Slider with an accent-colored thumb containing a Material icon."""

    def __init__(self, orientation, *, icon_name: str = "mdi6.volume-high",
                 thumb_size: int = 30, parent=None):
        super().__init__(parent)
        self.setOrientation(orientation)
        self._icon_name = icon_name
        self._thumb_size = thumb_size
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent; border: none;")

    def _groove_rect(self) -> QtCore.QRectF:
        ts = self._thumb_size
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            return QtCore.QRectF(ts / 2, self.height() / 2 - 3, self.width() - ts, 6)
        else:
            return QtCore.QRectF(self.width() / 2 - 3, ts / 2, 6, self.height() - ts)

    def _frac(self) -> float:
        rng = self.maximum() - self.minimum()
        return (self.value() - self.minimum()) / rng if rng else 0.0

    def _thumb_center(self) -> QtCore.QPointF:
        ts = self._thumb_size
        frac = self._frac()
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            x = ts / 2 + frac * (self.width() - ts)
            return QtCore.QPointF(x, self.height() / 2)
        else:
            y = self.height() - ts / 2 - frac * (self.height() - ts)
            return QtCore.QPointF(self.width() / 2, y)

    def paintEvent(self, event):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        pal = theme_manager.palette
        accent = QtGui.QColor(pal['accent'])
        ts = self._thumb_size
        groove = self._groove_rect()
        frac = self._frac()

        # Neumorphic inset groove
        _draw_inset_groove(p, groove, pal, radius=3.0)

        # Filled portion
        p.setPen(QtCore.Qt.PenStyle.NoPen)
        p.setBrush(accent)
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            filled = QtCore.QRectF(groove.left(), groove.top(),
                                   groove.width() * frac, groove.height())
        else:
            filled = QtCore.QRectF(groove.left(),
                                   groove.top() + groove.height() * (1 - frac),
                                   groove.width(), groove.height() * frac)
        p.drawRoundedRect(filled, 3, 3)

        # Neumorphic outset thumb with icon
        center = self._thumb_center()
        _draw_outset_thumb(p, center, ts / 2 - 1, accent, pal)

        # Icon – use QIcon.paint() for proper centering regardless of DPI
        icon_size = int(ts * 0.55)
        icon_rect = QtCore.QRect(
            round(center.x() - icon_size / 2),
            round(center.y() - icon_size / 2),
            icon_size, icon_size,
        )
        qta.icon(self._icon_name, color="#FFFFFF").paint(p, icon_rect)
        p.end()

    def minimumSizeHint(self):
        ts = self._thumb_size
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            return QtCore.QSize(120, ts + 4)
        return QtCore.QSize(ts + 4, 120)

    def sizeHint(self):
        return self.minimumSizeHint()

    def mousePressEvent(self, event):
        self._set_value_from_pos(event.position())

    def mouseMoveEvent(self, event):
        self._set_value_from_pos(event.position())

    def _set_value_from_pos(self, pos):
        ts = self._thumb_size
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            frac = (pos.x() - ts / 2) / max(self.width() - ts, 1)
        else:
            frac = 1.0 - (pos.y() - ts / 2) / max(self.height() - ts, 1)
        frac = max(0.0, min(1.0, frac))
        self.setValue(int(self.minimum() + frac * (self.maximum() - self.minimum())))


# ---------------------------------------------------------------------------
# Row builder helpers
# ---------------------------------------------------------------------------

_H = QtCore.Qt.Orientation.Horizontal
_V = QtCore.Qt.Orientation.Vertical


def _make_slider(orientation, value, *, variant: str = "",
                 ticks: int = 0, enabled: bool = True) -> _NeuSlider:
    s = _NeuSlider(orientation, variant=variant, tick_interval=ticks)
    s.setRange(0, 100)
    s.setValue(value)
    s.setEnabled(enabled)
    return s


def _h_row(slider_w, value_text: str = "") -> QtWidgets.QWidget:
    """Horizontal row: [slider] [value label]."""
    row = QtWidgets.QWidget()
    lay = QtWidgets.QHBoxLayout(row)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(8)
    lay.addWidget(slider_w, 1)
    lbl = _label(value_text or str(slider_w.value() if hasattr(slider_w, 'value') else ""))
    if hasattr(slider_w, 'valueChanged'):
        slider_w.valueChanged.connect(lambda v, lb=lbl: lb.setText(str(v)))
    lay.addWidget(lbl)
    return row


def _h_section(title: str, variant: str = "") -> tuple[QtWidgets.QGroupBox, QtWidgets.QVBoxLayout]:
    group = QtWidgets.QGroupBox(title)
    lay = QtWidgets.QVBoxLayout(group)
    lay.setContentsMargins(16, 24, 16, 16)
    lay.setSpacing(14)

    # 1 – Regular
    s1 = _make_slider(_H, 80, variant=variant)
    lay.addWidget(_h_row(s1))

    # 2 – Accent-light with ticks
    s2 = _make_slider(_H, 50, variant=variant or "accent-light", ticks=10)
    lay.addWidget(_h_row(s2))

    # 3 – Accent with icon thumb
    s3 = _IconThumbSlider(_H, icon_name="mdi6.volume-high", thumb_size=32)
    s3.setRange(0, 100)
    s3.setValue(50)
    lay.addWidget(_h_row(s3))

    # 4 – Gradient with value in thumb
    s4 = _ValueThumbSlider(_H, thumb_size=44, gradient=True)
    s4.setRange(0, 100)
    s4.setValue(30)
    s4.setMinimumHeight(52)
    lay.addWidget(_h_row(s4))

    # 5 – Disabled
    s5 = _make_slider(_H, 20, variant=variant, ticks=10, enabled=False)
    lay.addWidget(_h_row(s5))

    return group, lay


def _v_section(title: str, variant: str = "") -> tuple[QtWidgets.QGroupBox, QtWidgets.QHBoxLayout]:
    group = QtWidgets.QGroupBox(title)
    lay = QtWidgets.QHBoxLayout(group)
    lay.setContentsMargins(16, 24, 16, 16)
    lay.setSpacing(20)

    def _col(slider_w):
        c = QtWidgets.QVBoxLayout()
        c.setSpacing(4)
        c.addWidget(slider_w, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        lbl = _label(str(slider_w.value()))
        slider_w.valueChanged.connect(lambda v, lb=lbl: lb.setText(str(v)))
        c.addWidget(lbl, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        return c

    # 1 – Regular
    s1 = _make_slider(_V, 80, variant=variant)
    s1.setMinimumHeight(180)
    lay.addLayout(_col(s1))

    # 2 – Accent-light with ticks
    s2 = _make_slider(_V, 50, variant=variant or "accent-light", ticks=10)
    s2.setMinimumHeight(200)
    lay.addLayout(_col(s2))

    # 3 – Icon thumb
    s3 = _IconThumbSlider(_V, icon_name="mdi6.volume-high", thumb_size=32)
    s3.setRange(0, 100)
    s3.setValue(50)
    s3.setMinimumHeight(140)
    lay.addLayout(_col(s3))

    # 4 – Gradient value thumb
    s4 = _ValueThumbSlider(_V, thumb_size=44, gradient=True)
    s4.setRange(0, 100)
    s4.setValue(30)
    s4.setMinimumHeight(200)
    s4.setMinimumWidth(52)
    lay.addLayout(_col(s4))

    # 5 – Disabled
    s5 = _make_slider(_V, 20, variant=variant, ticks=10, enabled=False)
    s5.setMinimumHeight(200)
    lay.addLayout(_col(s5))

    lay.addStretch()
    return group, lay


# ---------------------------------------------------------------------------
# Page factory
# ---------------------------------------------------------------------------

def create_page() -> QtWidgets.QWidget:
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
    f = title.font()
    f.setPointSize(20)
    title.setFont(f)
    layout.addWidget(title)

    desc = QtWidgets.QLabel(
        "Regular and neumorphic outset sliders in horizontal and vertical orientations.\n"
        "Variants include accent-light, icon thumb, gradient value-in-thumb, and disabled."
    )
    desc.setWordWrap(True)
    desc.setProperty("subheading", True)
    layout.addWidget(desc)

    # 1 – Horizontal
    g1, _ = _h_section("Horizontal")
    layout.addWidget(_neu_group(g1))

    # 2 – Vertical
    g2, _ = _v_section("Vertical")
    layout.addWidget(_neu_group(g2))

    # 3 – Horizontal Outset
    g3, _ = _h_section("Horizontal Outset", variant="outset")
    layout.addWidget(_neu_group(g3))

    # 4 – Vertical Outset
    g4, _ = _v_section("Vertical Outset", variant="outset")
    layout.addWidget(_neu_group(g4))

    layout.addStretch()
    scroll.setWidget(inner)

    outer = QtWidgets.QVBoxLayout(page)
    outer.setContentsMargins(0, 0, 0, 0)
    outer.addWidget(scroll)
    return page


def create_about() -> QtWidgets.QWidget:
    page = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(page)
    layout.setContentsMargins(24, 24, 24, 24)

    title = QtWidgets.QLabel("About Sliders")
    title.setProperty("heading", True)
    f = title.font()
    f.setPointSize(20)
    title.setFont(f)
    layout.addWidget(title)

    info = QtWidgets.QLabel(
        "Slider controls inspired by Neumorphism.Avalonia:\n\n"
        "  • Regular – default QSlider with accent handle\n"
        "  • Accent-light – lighter accent with tick marks\n"
        "  • Icon thumb – enlarged thumb with a Material icon\n"
        "  • Value-in-thumb – gradient track, number shown inside thumb\n"
        "  • Disabled – muted colours\n\n"
        "Each variant is available in both regular and outset (neumorphic raised)\n"
        "groove styles, in horizontal and vertical orientations."
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
