"""Reusable custom progress widgets for circular, spiral, and neumorphic linear indicators."""

from __future__ import annotations

import math
from typing import Iterable

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QTimer, Property


class roundProgressBar(QtWidgets.QWidget):
    """PySide6 round progress bar with a PySide2extn-like API subset."""

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self._minimum = 0
        self._maximum = 100
        self._value = 35
        self._line_width = 10
        self._path_width = 10
        self._line_color = QtGui.QColor(0, 159, 227)
        self._path_color = QtGui.QColor(75, 75, 75)
        self._text_color = QtGui.QColor(230, 230, 230)
        self._bar_style = "Donet"
        self._text_format = "Percentage"
        self.setMinimumSize(120, 120)

    def rpb_setRange(self, minimum: int, maximum: int) -> None:
        self._minimum, self._maximum = sorted((int(minimum), int(maximum)))
        self.rpb_setValue(self._value)

    def rpb_setMaximum(self, maximum: int) -> None:
        self._maximum = int(maximum)
        self.rpb_setValue(self._value)

    def rpb_setMinimum(self, minimum: int) -> None:
        self._minimum = int(minimum)
        self.rpb_setValue(self._value)

    def rpb_setValue(self, value: int) -> None:
        self._value = max(self._minimum, min(int(value), self._maximum))
        self.update()

    def rpb_setLineWidth(self, width: int) -> None:
        self._line_width = max(1, int(width))
        self.update()

    def rpb_setPathWidth(self, width: int) -> None:
        self._path_width = max(1, int(width))
        self.update()

    def rpb_setLineColor(self, color: tuple[int, int, int]) -> None:
        self._line_color = QtGui.QColor(*color)
        self.update()

    def rpb_setPathColor(self, color: tuple[int, int, int]) -> None:
        self._path_color = QtGui.QColor(*color)
        self.update()

    def rpb_setBarStyle(self, style: str) -> None:
        self._bar_style = style
        self.update()

    def rpb_setTextFormat(self, text_type: str) -> None:
        self._text_format = text_type
        self.update()

    def _ratio(self) -> float:
        span = max(1, self._maximum - self._minimum)
        return (self._value - self._minimum) / span

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:  # noqa: N802
        del event
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        side = min(self.width(), self.height())
        margin = max(self._line_width, self._path_width) + 4
        rect = QtCore.QRectF(
            (self.width() - side) / 2 + margin,
            (self.height() - side) / 2 + margin,
            side - 2 * margin,
            side - 2 * margin,
        )

        painter.setPen(QtGui.QPen(self._path_color, float(self._path_width), Qt.SolidLine, Qt.RoundCap))
        painter.drawArc(rect, 90 * 16, -360 * 16)

        sweep = int(-360 * 16 * self._ratio())
        painter.setPen(QtGui.QPen(self._line_color, float(self._line_width), Qt.SolidLine, Qt.RoundCap))

        if self._bar_style in {"Pizza", "Pie"}:
            painter.setBrush(QtGui.QBrush(self._line_color))
            painter.setPen(Qt.NoPen)
            painter.drawPie(rect, 90 * 16, sweep)
        else:
            painter.setBrush(Qt.NoBrush)
            painter.drawArc(rect, 90 * 16, sweep)

        if self._text_format == "Value":
            text = str(self._value)
        else:
            text = f"{int(self._ratio() * 100)}%"

        painter.setPen(self._text_color)
        font = painter.font()
        font.setPointSize(max(9, int(side / 9)))
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, text)


class spiralProgressBar(QtWidgets.QWidget):
    """PySide6 spiral progress bar with a PySide2extn-like API subset."""

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.noProgBar = 3
        self._minimum = [0, 0, 0]
        self._maximum = [100, 100, 100]
        self._value = [65, 42, 80]
        self._line_width = 10
        self._gap = 8
        self._line_colors = [
            QtGui.QColor(0, 159, 227),
            QtGui.QColor(90, 193, 211),
            QtGui.QColor(42, 148, 125),
        ]
        self._path_colors = [QtGui.QColor(75, 75, 75)] * 3
        self._direction = [1, 1, 1]  # 1 clockwise, -1 anticlockwise
        self.setMinimumSize(160, 160)

    def _resize_lists(self, count: int) -> None:
        self._minimum = (self._minimum + [0] * count)[:count]
        self._maximum = (self._maximum + [100] * count)[:count]
        self._value = (self._value + [0] * count)[:count]
        self._line_colors = (self._line_colors + [QtGui.QColor(0, 159, 227)] * count)[:count]
        self._path_colors = (self._path_colors + [QtGui.QColor(75, 75, 75)] * count)[:count]
        self._direction = (self._direction + [1] * count)[:count]

    def spb_setNoProgressBar(self, num: int) -> None:
        num = max(2, min(6, int(num)))
        self.noProgBar = num
        self._resize_lists(num)
        self.update()

    def spb_setValue(self, values: Iterable[int] | int) -> None:
        if isinstance(values, int):
            values = [values] * self.noProgBar
        vals = list(values)
        self._resize_lists(self.noProgBar)
        for i in range(self.noProgBar):
            v = vals[i] if i < len(vals) else vals[-1]
            self._value[i] = max(self._minimum[i], min(int(v), self._maximum[i]))
        self.update()

    def spb_setRange(self, minimums: Iterable[int], maximums: Iterable[int]) -> None:
        mins = list(minimums)
        maxs = list(maximums)
        self._resize_lists(self.noProgBar)
        for i in range(self.noProgBar):
            low = mins[i] if i < len(mins) else mins[-1]
            high = maxs[i] if i < len(maxs) else maxs[-1]
            self._minimum[i], self._maximum[i] = sorted((int(low), int(high)))
        self.spb_setValue(self._value)

    def spb_lineWidth(self, width: int) -> None:
        self._line_width = max(1, int(width))
        self.update()

    def spb_setGap(self, gap: int) -> None:
        self._gap = max(0, int(gap))
        self.update()

    def spb_lineColor(self, colors: Iterable[tuple[int, int, int]]) -> None:
        seq = [QtGui.QColor(*c) for c in colors]
        if seq:
            self._line_colors = (seq + seq * self.noProgBar)[: self.noProgBar]
            self.update()

    def spb_pathColor(self, colors: Iterable[tuple[int, int, int]]) -> None:
        seq = [QtGui.QColor(*c) for c in colors]
        if seq:
            self._path_colors = (seq + seq * self.noProgBar)[: self.noProgBar]
            self.update()

    def spb_setDirection(self, directions: Iterable[str]) -> None:
        seq = list(directions)
        if not seq:
            return
        for i in range(self.noProgBar):
            text = seq[i] if i < len(seq) else seq[-1]
            self._direction[i] = 1 if str(text).lower().startswith("clock") else -1
        self.update()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:  # noqa: N802
        del event
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        side = min(self.width(), self.height())
        margin = 8
        start_radius = side / 2 - margin

        for i in range(self.noProgBar):
            radius = start_radius - i * (self._line_width + self._gap)
            if radius <= self._line_width:
                break

            rect = QtCore.QRectF(
                self.width() / 2 - radius,
                self.height() / 2 - radius,
                radius * 2,
                radius * 2,
            )

            painter.setPen(QtGui.QPen(self._path_colors[i], float(self._line_width), Qt.SolidLine, Qt.RoundCap))
            painter.drawArc(rect, 90 * 16, -360 * 16)

            span = max(1, self._maximum[i] - self._minimum[i])
            ratio = (self._value[i] - self._minimum[i]) / span
            sweep = int(360 * 16 * ratio) * self._direction[i]

            painter.setPen(QtGui.QPen(self._line_colors[i], float(self._line_width), Qt.SolidLine, Qt.RoundCap))
            painter.drawArc(rect, 90 * 16, sweep)

        text = ", ".join(f"{int(v)}" for v in self._value[: self.noProgBar])
        painter.setPen(QtGui.QColor(230, 230, 230))
        font = painter.font()
        font.setPointSize(max(8, int(side / 18)))
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, text)


# ---------------------------------------------------------------------------
# Neumorphic Linear Progress Bars
# ---------------------------------------------------------------------------

class NeuProgressBar(QtWidgets.QWidget):
    """Neumorphic *inset* linear progress bar.

    The groove is rendered as a sunken channel with inner shadows,
    and the filled portion uses the accent colour with a subtle highlight.
    Supports horizontal and vertical orientations, determinate and
    indeterminate modes.
    """

    valueChanged = QtCore.Signal(int)

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        orientation: Qt.Orientation = Qt.Orientation.Horizontal,
    ) -> None:
        super().__init__(parent)
        self._min = 0
        self._max = 100
        self._value = 0
        self._orientation = orientation
        self._indeterminate = False
        self._bar_height = 14           # groove thickness
        self._radius = 7                # corner rounding
        self._show_text = False
        self._accent: str | None = None  # override; None → use palette
        self._gradient_colors: list[str] | None = None

        # indeterminate animation
        self._anim_offset = 0.0
        self._anim_timer = QTimer(self)
        self._anim_timer.setInterval(16)  # ~60 fps
        self._anim_timer.timeout.connect(self._tick_indeterminate)

        if orientation == Qt.Orientation.Vertical:
            self.setMinimumSize(40, 120)
            self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed,
                               QtWidgets.QSizePolicy.Policy.Expanding)
        else:
            self.setMinimumSize(120, 32)
            self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                               QtWidgets.QSizePolicy.Policy.Fixed)

    # -- public API ----------------------------------------------------------

    def value(self) -> int:
        return self._value

    def setValue(self, v: int) -> None:
        v = max(self._min, min(int(v), self._max))
        if v != self._value:
            self._value = v
            self.valueChanged.emit(v)
            self.update()

    def setRange(self, lo: int, hi: int) -> None:
        self._min, self._max = sorted((int(lo), int(hi)))
        self.setValue(self._value)

    def minimum(self) -> int:
        return self._min

    def maximum(self) -> int:
        return self._max

    def setBarHeight(self, h: int) -> None:
        self._bar_height = max(4, int(h))
        self._radius = self._bar_height // 2
        self.update()

    def setShowText(self, show: bool) -> None:
        self._show_text = show
        self.update()

    def setAccentColor(self, color: str) -> None:
        self._accent = color
        self.update()

    def setGradientColors(self, colors: list[str]) -> None:
        self._gradient_colors = colors if len(colors) >= 2 else None
        self.update()

    def setIndeterminate(self, on: bool) -> None:
        self._indeterminate = on
        if on:
            self._anim_timer.start()
        else:
            self._anim_timer.stop()
        self.update()

    def orientation(self) -> Qt.Orientation:
        return self._orientation

    # -- helpers -------------------------------------------------------------

    def _ratio(self) -> float:
        span = max(1, self._max - self._min)
        return (self._value - self._min) / span

    def _palette(self) -> dict:
        from styles.theme_manager import theme_manager
        return theme_manager.palette

    def _tick_indeterminate(self) -> None:
        self._anim_offset += 0.012
        if self._anim_offset > 1.0:
            self._anim_offset -= 1.0
        self.update()

    def _fill_brush(self, rect: QtCore.QRectF) -> QtGui.QBrush:
        p = self._palette()
        if self._gradient_colors and len(self._gradient_colors) >= 2:
            grad = QtGui.QLinearGradient(rect.topLeft(), rect.topRight()
                if self._orientation == Qt.Orientation.Horizontal else rect.bottomLeft())
            step = 1.0 / (len(self._gradient_colors) - 1)
            for i, c in enumerate(self._gradient_colors):
                grad.setColorAt(i * step, QtGui.QColor(c))
            return QtGui.QBrush(grad)
        return QtGui.QBrush(QtGui.QColor(self._accent or p["accent"]))

    # -- painting ------------------------------------------------------------

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        del event
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        p = self._palette()
        horiz = self._orientation == Qt.Orientation.Horizontal

        # Groove rect centred in widget
        bh = self._bar_height
        if horiz:
            x = 4
            y = (self.height() - bh) / 2
            groove = QtCore.QRectF(x, y, self.width() - 8, bh)
        else:
            x = (self.width() - bh) / 2
            y = 4
            groove = QtCore.QRectF(x, y, bh, self.height() - 8)

        r = self._radius

        # 1) Groove background (sunken look)
        bg_color = QtGui.QColor(p["bg_secondary"])
        painter.setPen(Qt.NoPen)
        painter.setBrush(bg_color)
        painter.drawRoundedRect(groove, r, r)

        # 2) Inner shadows for inset effect
        painter.save()
        path = QtGui.QPainterPath()
        path.addRoundedRect(groove, r, r)
        painter.setClipPath(path)

        # Dark shadow (top-left)
        shadow_d = QtGui.QColor(0, 0, 0, 50)
        for i in range(3, 0, -1):
            shadow_d.setAlpha(15 + (3 - i) * 12)
            painter.setPen(QtGui.QPen(shadow_d, 1.0))
            painter.drawRoundedRect(groove.adjusted(i, i, -0.5, -0.5), r, r)

        # Light shadow (bottom-right)
        shadow_l = QtGui.QColor(255, 255, 255, 60)
        for i in range(3, 0, -1):
            shadow_l.setAlpha(20 + (3 - i) * 12)
            painter.setPen(QtGui.QPen(shadow_l, 1.0))
            painter.drawRoundedRect(groove.adjusted(-0.5, -0.5, -i, -i), r, r)

        painter.restore()

        # 3) Filled portion
        ratio = self._ratio()
        if self._indeterminate:
            pulse_w = 0.30
            start = self._anim_offset - pulse_w / 2
            end = self._anim_offset + pulse_w / 2
            if horiz:
                fx = groove.x() + groove.width() * max(0.0, start)
                fw = groove.width() * min(end, 1.0) - groove.width() * max(0.0, start)
                fill = QtCore.QRectF(fx, groove.y(), max(0, fw), groove.height())
            else:
                fy = groove.y() + groove.height() * (1.0 - min(end, 1.0))
                fh = groove.height() * min(end, 1.0) - groove.height() * max(0.0, start)
                fill = QtCore.QRectF(groove.x(), fy, groove.width(), max(0, fh))
        else:
            if horiz:
                fill = QtCore.QRectF(groove.x(), groove.y(),
                                     groove.width() * ratio, groove.height())
            else:
                fh = groove.height() * ratio
                fill = QtCore.QRectF(groove.x(), groove.bottom() - fh,
                                     groove.width(), fh)

        if fill.width() > 0 and fill.height() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self._fill_brush(fill))
            painter.drawRoundedRect(fill, r, r)

            # Subtle highlight on fill top edge
            painter.save()
            clip_path = QtGui.QPainterPath()
            clip_path.addRoundedRect(fill, r, r)
            painter.setClipPath(clip_path)
            highlight = QtGui.QColor(255, 255, 255, 55)
            painter.setPen(Qt.NoPen)
            if horiz:
                hl_rect = QtCore.QRectF(fill.x(), fill.y(), fill.width(), fill.height() * 0.4)
            else:
                hl_rect = QtCore.QRectF(fill.x(), fill.y(), fill.width() * 0.4, fill.height())
            painter.setBrush(highlight)
            painter.drawRoundedRect(hl_rect, r, r)
            painter.restore()

        # 4) Optional percentage text
        if self._show_text and not self._indeterminate:
            pct = f"{int(ratio * 100)}%"
            painter.setPen(QtGui.QColor(p["text"]))
            font = painter.font()
            font.setPixelSize(max(10, bh - 2))
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, pct)

        painter.end()


class NeuProgressBarOutset(QtWidgets.QWidget):
    """Neumorphic *outset* (raised) linear progress bar.

    The groove appears to protrude from the surface with outer shadows,
    and the fill sits on top.
    """

    valueChanged = QtCore.Signal(int)

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        orientation: Qt.Orientation = Qt.Orientation.Horizontal,
    ) -> None:
        super().__init__(parent)
        self._min = 0
        self._max = 100
        self._value = 0
        self._orientation = orientation
        self._indeterminate = False
        self._bar_height = 14
        self._radius = 7
        self._show_text = False
        self._accent: str | None = None
        self._gradient_colors: list[str] | None = None

        self._anim_offset = 0.0
        self._anim_timer = QTimer(self)
        self._anim_timer.setInterval(16)
        self._anim_timer.timeout.connect(self._tick_indeterminate)

        if orientation == Qt.Orientation.Vertical:
            self.setMinimumSize(48, 120)
            self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed,
                               QtWidgets.QSizePolicy.Policy.Expanding)
        else:
            self.setMinimumSize(120, 38)
            self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                               QtWidgets.QSizePolicy.Policy.Fixed)

    # -- public API (same as NeuProgressBar) ---------------------------------

    def value(self) -> int:
        return self._value

    def setValue(self, v: int) -> None:
        v = max(self._min, min(int(v), self._max))
        if v != self._value:
            self._value = v
            self.valueChanged.emit(v)
            self.update()

    def setRange(self, lo: int, hi: int) -> None:
        self._min, self._max = sorted((int(lo), int(hi)))
        self.setValue(self._value)

    def minimum(self) -> int:
        return self._min

    def maximum(self) -> int:
        return self._max

    def setBarHeight(self, h: int) -> None:
        self._bar_height = max(4, int(h))
        self._radius = self._bar_height // 2
        self.update()

    def setShowText(self, show: bool) -> None:
        self._show_text = show
        self.update()

    def setAccentColor(self, color: str) -> None:
        self._accent = color
        self.update()

    def setGradientColors(self, colors: list[str]) -> None:
        self._gradient_colors = colors if len(colors) >= 2 else None
        self.update()

    def setIndeterminate(self, on: bool) -> None:
        self._indeterminate = on
        if on:
            self._anim_timer.start()
        else:
            self._anim_timer.stop()
        self.update()

    def orientation(self) -> Qt.Orientation:
        return self._orientation

    # -- helpers -------------------------------------------------------------

    def _ratio(self) -> float:
        span = max(1, self._max - self._min)
        return (self._value - self._min) / span

    def _palette(self) -> dict:
        from styles.theme_manager import theme_manager
        return theme_manager.palette

    def _tick_indeterminate(self) -> None:
        self._anim_offset += 0.012
        if self._anim_offset > 1.0:
            self._anim_offset -= 1.0
        self.update()

    def _fill_brush(self, rect: QtCore.QRectF) -> QtGui.QBrush:
        p = self._palette()
        if self._gradient_colors and len(self._gradient_colors) >= 2:
            grad = QtGui.QLinearGradient(rect.topLeft(), rect.topRight()
                if self._orientation == Qt.Orientation.Horizontal else rect.bottomLeft())
            step = 1.0 / (len(self._gradient_colors) - 1)
            for i, c in enumerate(self._gradient_colors):
                grad.setColorAt(i * step, QtGui.QColor(c))
            return QtGui.QBrush(grad)
        return QtGui.QBrush(QtGui.QColor(self._accent or p["accent"]))

    # -- painting ------------------------------------------------------------

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        del event
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        p = self._palette()
        horiz = self._orientation == Qt.Orientation.Horizontal

        bh = self._bar_height
        margin = 8  # space for outer shadow
        if horiz:
            groove = QtCore.QRectF(margin, (self.height() - bh) / 2,
                                   self.width() - margin * 2, bh)
        else:
            groove = QtCore.QRectF((self.width() - bh) / 2, margin,
                                   bh, self.height() - margin * 2)

        r = self._radius

        # 1) Outer shadows (raised look)
        dark = QtGui.QColor(0, 0, 0, 40)
        light = QtGui.QColor(255, 255, 255, 90)
        if p["bg"] == "#2C3135":  # dark theme
            dark = QtGui.QColor(0, 0, 0, 100)
            light = QtGui.QColor(255, 255, 255, 20)

        for i in range(3, 0, -1):
            dark.setAlpha(max(10, dark.alpha() - i * 5))
            painter.setPen(Qt.NoPen)
            painter.setBrush(dark)
            painter.drawRoundedRect(groove.adjusted(-i + 2, -i + 2, i, i), r + 1, r + 1)

        for i in range(3, 0, -1):
            light.setAlpha(max(10, light.alpha() - i * 8))
            painter.setPen(Qt.NoPen)
            painter.setBrush(light)
            painter.drawRoundedRect(groove.adjusted(-i, -i, i - 2, i - 2), r + 1, r + 1)

        # 2) Groove background (raised surface)
        bg_color = QtGui.QColor(p["card_bg"])
        painter.setPen(Qt.NoPen)
        painter.setBrush(bg_color)
        painter.drawRoundedRect(groove, r, r)

        # 3) Filled portion
        ratio = self._ratio()
        if self._indeterminate:
            pulse_w = 0.30
            start = self._anim_offset - pulse_w / 2
            end = self._anim_offset + pulse_w / 2
            if horiz:
                fx = groove.x() + groove.width() * max(0.0, start)
                fw = groove.width() * min(end, 1.0) - groove.width() * max(0.0, start)
                fill = QtCore.QRectF(fx, groove.y(), max(0, fw), groove.height())
            else:
                fy = groove.y() + groove.height() * (1.0 - min(end, 1.0))
                fh = groove.height() * min(end, 1.0) - groove.height() * max(0.0, start)
                fill = QtCore.QRectF(groove.x(), fy, groove.width(), max(0, fh))
        else:
            if horiz:
                fill = QtCore.QRectF(groove.x(), groove.y(),
                                     groove.width() * ratio, groove.height())
            else:
                fh = groove.height() * ratio
                fill = QtCore.QRectF(groove.x(), groove.bottom() - fh,
                                     groove.width(), fh)

        if fill.width() > 0 and fill.height() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self._fill_brush(fill))
            painter.drawRoundedRect(fill, r, r)

            # Highlight strip
            painter.save()
            clip_path = QtGui.QPainterPath()
            clip_path.addRoundedRect(fill, r, r)
            painter.setClipPath(clip_path)
            highlight = QtGui.QColor(255, 255, 255, 50)
            painter.setPen(Qt.NoPen)
            if horiz:
                hl_rect = QtCore.QRectF(fill.x(), fill.y(), fill.width(), fill.height() * 0.35)
            else:
                hl_rect = QtCore.QRectF(fill.x(), fill.y(), fill.width() * 0.35, fill.height())
            painter.setBrush(highlight)
            painter.drawRoundedRect(hl_rect, r, r)
            painter.restore()

        # 4) Optional percentage text
        if self._show_text and not self._indeterminate:
            pct = f"{int(ratio * 100)}%"
            painter.setPen(QtGui.QColor(p["text"]))
            font = painter.font()
            font.setPixelSize(max(10, bh - 2))
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, pct)

        painter.end()


class NeuProgressBarDeepInset(QtWidgets.QWidget):
    """Neumorphic *deep inset* linear progress bar.

    Thicker groove with stronger inner shadows for a deeply sunken appearance.
    """

    valueChanged = QtCore.Signal(int)

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        orientation: Qt.Orientation = Qt.Orientation.Horizontal,
    ) -> None:
        super().__init__(parent)
        self._min = 0
        self._max = 100
        self._value = 0
        self._orientation = orientation
        self._indeterminate = False
        self._bar_height = 28
        self._radius = 14
        self._show_text = True
        self._accent: str | None = None
        self._gradient_colors: list[str] | None = None

        self._anim_offset = 0.0
        self._anim_timer = QTimer(self)
        self._anim_timer.setInterval(16)
        self._anim_timer.timeout.connect(self._tick_indeterminate)

        if orientation == Qt.Orientation.Vertical:
            self.setMinimumSize(52, 120)
            self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed,
                               QtWidgets.QSizePolicy.Policy.Expanding)
        else:
            self.setMinimumSize(120, 44)
            self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                               QtWidgets.QSizePolicy.Policy.Fixed)

    # -- public API ----------------------------------------------------------

    def value(self) -> int:
        return self._value

    def setValue(self, v: int) -> None:
        v = max(self._min, min(int(v), self._max))
        if v != self._value:
            self._value = v
            self.valueChanged.emit(v)
            self.update()

    def setRange(self, lo: int, hi: int) -> None:
        self._min, self._max = sorted((int(lo), int(hi)))
        self.setValue(self._value)

    def setBarHeight(self, h: int) -> None:
        self._bar_height = max(8, int(h))
        self._radius = self._bar_height // 2
        self.update()

    def setShowText(self, show: bool) -> None:
        self._show_text = show
        self.update()

    def setAccentColor(self, color: str) -> None:
        self._accent = color
        self.update()

    def setGradientColors(self, colors: list[str]) -> None:
        self._gradient_colors = colors if len(colors) >= 2 else None
        self.update()

    def setIndeterminate(self, on: bool) -> None:
        self._indeterminate = on
        if on:
            self._anim_timer.start()
        else:
            self._anim_timer.stop()
        self.update()

    def orientation(self) -> Qt.Orientation:
        return self._orientation

    # -- helpers -------------------------------------------------------------

    def _ratio(self) -> float:
        span = max(1, self._max - self._min)
        return (self._value - self._min) / span

    def _palette(self) -> dict:
        from styles.theme_manager import theme_manager
        return theme_manager.palette

    def _tick_indeterminate(self) -> None:
        self._anim_offset += 0.012
        if self._anim_offset > 1.0:
            self._anim_offset -= 1.0
        self.update()

    def _fill_brush(self, rect: QtCore.QRectF) -> QtGui.QBrush:
        p = self._palette()
        if self._gradient_colors and len(self._gradient_colors) >= 2:
            grad = QtGui.QLinearGradient(rect.topLeft(), rect.topRight()
                if self._orientation == Qt.Orientation.Horizontal else rect.bottomLeft())
            step = 1.0 / (len(self._gradient_colors) - 1)
            for i, c in enumerate(self._gradient_colors):
                grad.setColorAt(i * step, QtGui.QColor(c))
            return QtGui.QBrush(grad)
        return QtGui.QBrush(QtGui.QColor(self._accent or p["accent"]))

    # -- painting ------------------------------------------------------------

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        del event
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        p = self._palette()
        horiz = self._orientation == Qt.Orientation.Horizontal

        bh = self._bar_height
        if horiz:
            groove = QtCore.QRectF(4, (self.height() - bh) / 2,
                                   self.width() - 8, bh)
        else:
            groove = QtCore.QRectF((self.width() - bh) / 2, 4,
                                   bh, self.height() - 8)

        r = self._radius

        # 1) Groove background
        bg = QtGui.QColor(p["bg_secondary"])
        darker = bg.darker(115)
        painter.setPen(Qt.NoPen)
        painter.setBrush(darker)
        painter.drawRoundedRect(groove, r, r)

        # 2) Strong inner shadows (deep inset)
        painter.save()
        path = QtGui.QPainterPath()
        path.addRoundedRect(groove, r, r)
        painter.setClipPath(path)

        shadow_d = QtGui.QColor(0, 0, 0, 70)
        for i in range(5, 0, -1):
            shadow_d.setAlpha(12 + (5 - i) * 12)
            painter.setPen(QtGui.QPen(shadow_d, 1.2))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(groove.adjusted(i, i, -0.5, -0.5), r, r)

        shadow_l = QtGui.QColor(255, 255, 255, 70)
        for i in range(5, 0, -1):
            shadow_l.setAlpha(12 + (5 - i) * 12)
            painter.setPen(QtGui.QPen(shadow_l, 1.2))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(groove.adjusted(-0.5, -0.5, -i, -i), r, r)

        painter.restore()

        # 3) Filled portion
        ratio = self._ratio()
        if self._indeterminate:
            pulse_w = 0.30
            start = self._anim_offset - pulse_w / 2
            end = self._anim_offset + pulse_w / 2
            if horiz:
                fx = groove.x() + groove.width() * max(0.0, start)
                fw = groove.width() * min(end, 1.0) - groove.width() * max(0.0, start)
                fill = QtCore.QRectF(fx, groove.y(), max(0, fw), groove.height())
            else:
                fy = groove.y() + groove.height() * (1.0 - min(end, 1.0))
                fh = groove.height() * min(end, 1.0) - groove.height() * max(0.0, start)
                fill = QtCore.QRectF(groove.x(), fy, groove.width(), max(0, fh))
        else:
            if horiz:
                fill = QtCore.QRectF(groove.x(), groove.y(),
                                     groove.width() * ratio, groove.height())
            else:
                fh = groove.height() * ratio
                fill = QtCore.QRectF(groove.x(), groove.bottom() - fh,
                                     groove.width(), fh)

        if fill.width() > 0 and fill.height() > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self._fill_brush(fill))
            painter.drawRoundedRect(fill, r, r)

            # Glossy highlight
            painter.save()
            clip_path = QtGui.QPainterPath()
            clip_path.addRoundedRect(fill, r, r)
            painter.setClipPath(clip_path)
            if horiz:
                hl = QtCore.QRectF(fill.x(), fill.y(), fill.width(), fill.height() * 0.4)
            else:
                hl = QtCore.QRectF(fill.x(), fill.y(), fill.width() * 0.4, fill.height())
            painter.setBrush(QtGui.QColor(255, 255, 255, 55))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(hl, r, r)
            painter.restore()

        # 4) Percentage text
        if self._show_text and not self._indeterminate:
            pct = f"{int(ratio * 100)}%"
            painter.setPen(QtGui.QColor(p["text"]))
            font = painter.font()
            font.setPixelSize(max(10, bh - 8))
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, pct)

        painter.end()
