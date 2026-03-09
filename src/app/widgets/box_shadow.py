"""Neumorphic box-shadow effect and wrapper widgets for PySide6."""

# BoxShadow graphics effect for PySide6 neumorphism.

from __future__ import annotations

from PySide6 import QtCore, QtGui, QtWidgets


class BoxShadow(QtWidgets.QGraphicsEffect):
    """QGraphicsEffect that renders inside and/or outside box-shadows."""

    def __init__(self, shadow_list: list[dict] | None = None,
                 border: int = 0, smooth: bool = False) -> None:
        super().__init__()
        self._shadow_list: list[dict] = []
        self._max_x_offset = 0
        self._max_y_offset = 0
        self._border = 0
        self._smooth = smooth
        self._cache_outside: QtGui.QPixmap | None = None
        self._cache_inside: QtGui.QPixmap | None = None
        self._cache_size: QtCore.QSize | None = None
        self.setShadowList(shadow_list)
        self.setBorder(border)

    # -- public API ----------------------------------------------------------

    def setShadowList(self, shadow_list: list[dict] | None = None) -> None:
        self._shadow_list = shadow_list or []
        self._set_max_offset()
        self._invalidate_cache()

    def setBorder(self, border: int) -> None:
        self._border = max(0, border)
        self._invalidate_cache()

    def _invalidate_cache(self) -> None:
        self._cache_outside = None
        self._cache_inside = None
        self._cache_size = None

    def necessary_indentation(self) -> tuple[int, int]:
        return self._max_x_offset, self._max_y_offset

    def boundingRectFor(self, rect):
        return rect.adjusted(-self._max_x_offset, -self._max_y_offset,
                             self._max_x_offset, self._max_y_offset)

    # -- private helpers -----------------------------------------------------

    def _set_max_offset(self) -> None:
        mx = my = 0
        for s in self._shadow_list:
            if "outside" in s:
                mx = max(mx, abs(s["offset"][0]) + s["blur"] * 2)
                my = max(my, abs(s["offset"][1]) + s["blur"] * 2)
        self._max_x_offset = mx
        self._max_y_offset = my

    @staticmethod
    def _blur_pixmap(src: QtGui.QPixmap, blur_radius: int) -> QtGui.QPixmap:
        w, h = src.width(), src.height()
        effect = QtWidgets.QGraphicsBlurEffect(blurRadius=blur_radius)
        scene = QtWidgets.QGraphicsScene()
        item = QtWidgets.QGraphicsPixmapItem()
        item.setPixmap(QtGui.QPixmap(src))
        item.setGraphicsEffect(effect)
        scene.addItem(item)
        res = QtGui.QImage(QtCore.QSize(w, h),
                           QtGui.QImage.Format.Format_ARGB32)
        res.fill(QtCore.Qt.GlobalColor.transparent)
        ptr = QtGui.QPainter(res)
        ptr.setRenderHints(
            QtGui.QPainter.RenderHint.Antialiasing |
            QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        scene.render(ptr, QtCore.QRectF(), QtCore.QRectF(0, 0, w, h))
        ptr.end()
        return QtGui.QPixmap(res)

    @staticmethod
    def _colored_pixmap(color: QtGui.QColor, pixmap: QtGui.QPixmap) -> QtGui.QPixmap:
        new_pixmap = QtGui.QPixmap(pixmap)
        new_pixmap.fill(color)
        painter = QtGui.QPainter(new_pixmap)
        painter.setTransform(QtGui.QTransform())
        painter.setRenderHints(
            QtGui.QPainter.RenderHint.Antialiasing |
            QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        painter.setCompositionMode(
            QtGui.QPainter.CompositionMode.CompositionMode_DestinationIn)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        return new_pixmap

    @staticmethod
    def _cut_shadow(pixmap: QtGui.QPixmap, source: QtGui.QPixmap,
                    offset_x: float, offset_y: float) -> QtGui.QPixmap:
        painter = QtGui.QPainter(pixmap)
        painter.setTransform(QtGui.QTransform())
        painter.setRenderHints(
            QtGui.QPainter.RenderHint.Antialiasing |
            QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        painter.setCompositionMode(
            QtGui.QPainter.CompositionMode.CompositionMode_DestinationOut)
        painter.drawPixmap(offset_x, offset_y, source)
        painter.end()
        return pixmap

    # -- smooth rendering paths ----------------------------------------------

    def _smooth_outside_shadow(self) -> QtGui.QPixmap:
        source = self.sourcePixmap(QtCore.Qt.CoordinateSystem.DeviceCoordinates)
        if isinstance(source, tuple):
            source = source[0]
        w, h = source.width(), source.height()

        parts: list[QtGui.QPixmap] = []
        for s in self._shadow_list:
            if "outside" not in s:
                continue
            shadow = QtGui.QPixmap(source.size())
            shadow.fill(QtCore.Qt.GlobalColor.transparent)
            p = QtGui.QPainter(shadow)
            p.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing |
                             QtGui.QPainter.RenderHint.SmoothPixmapTransform)
            p.setTransform(QtGui.QTransform())
            p.drawPixmap(s["offset"][0], s["offset"][1], w, h,
                         self._colored_pixmap(QtGui.QColor(s["color"]), source))
            p.end()
            parts.append(shadow)

        result = QtGui.QPixmap(source.size())
        result.fill(QtCore.Qt.GlobalColor.transparent)
        rp = QtGui.QPainter(result)
        rp.setTransform(QtGui.QTransform())
        rp.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing |
                          QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        for i, px in enumerate(parts):
            rp.drawPixmap(0, 0, w, h, self._blur_pixmap(px, self._shadow_list[i]["blur"]))
        rp.end()

        # Cut out the widget area
        rp2 = QtGui.QPainter(result)
        rp2.setTransform(QtGui.QTransform())
        rp2.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing |
                           QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        rp2.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_DestinationOut)
        rp2.drawPixmap(0, 0, w, h, source)
        rp2.end()
        return result

    def _smooth_inside_shadow(self) -> QtGui.QPixmap:
        source = self.sourcePixmap(QtCore.Qt.CoordinateSystem.DeviceCoordinates)
        if isinstance(source, tuple):
            source = source[0]
        w, h = source.width(), source.height()

        parts: list[QtGui.QPixmap] = []
        for s in self._shadow_list:
            if "inside" not in s:
                continue
            shadow = QtGui.QPixmap(source.size())
            shadow.fill(QtCore.Qt.GlobalColor.transparent)
            p = QtGui.QPainter(shadow)
            p.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing |
                             QtGui.QPainter.RenderHint.SmoothPixmapTransform)
            p.setTransform(QtGui.QTransform())
            new_source = self._colored_pixmap(QtGui.QColor(s["color"]), source)
            p.drawPixmap(0, 0, w, h,
                         self._cut_shadow(new_source, source,
                                          s["offset"][0] / 2, s["offset"][1] / 2))
            p.end()
            parts.append(shadow)

        result = QtGui.QPixmap(source.size())
        result.fill(QtCore.Qt.GlobalColor.transparent)
        rp = QtGui.QPainter(result)
        rp.setTransform(QtGui.QTransform())
        rp.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing |
                          QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        inside_shadows = [s for s in self._shadow_list if "inside" in s]
        for i, px in enumerate(parts):
            rp.drawPixmap(0, 0, w, h, self._blur_pixmap(px, inside_shadows[i]["blur"]))
        rp.end()

        # Clip to widget shape
        rp2 = QtGui.QPainter(result)
        rp2.setTransform(QtGui.QTransform())
        rp2.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing |
                           QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        rp2.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_DestinationIn)
        rp2.drawPixmap(0, 0, w, h, source)
        rp2.end()
        return result

    # -- non-smooth rendering paths ------------------------------------------

    def _outside_shadow(self) -> QtGui.QPixmap:
        source = self.sourcePixmap(QtCore.Qt.CoordinateSystem.DeviceCoordinates)
        if isinstance(source, tuple):
            source = source[0]
        mask = source.createMaskFromColor(QtGui.QColor(0, 0, 0, 0),
                                          QtCore.Qt.MaskMode.MaskInColor)

        parts: list[QtGui.QPixmap] = []
        for s in self._shadow_list:
            if "outside" not in s:
                continue
            shadow = QtGui.QPixmap(mask.size())
            shadow.fill(QtCore.Qt.GlobalColor.transparent)
            sp = QtGui.QPainter(shadow)
            sp.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing |
                              QtGui.QPainter.RenderHint.SmoothPixmapTransform)
            sp.setTransform(QtGui.QTransform())
            sp.setPen(QtGui.QColor(s["color"]))
            sp.drawPixmap(s["offset"][0], s["offset"][1], mask)
            sp.end()
            parts.append(shadow)

        result = QtGui.QPixmap(mask.size())
        result.fill(QtCore.Qt.GlobalColor.transparent)
        rp = QtGui.QPainter(result)
        rp.setTransform(QtGui.QTransform())
        rp.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing |
                          QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        outside_shadows = [s for s in self._shadow_list if "outside" in s]
        for i, px in enumerate(parts):
            rp.drawPixmap(0, 0, self._blur_pixmap(px, outside_shadows[i]["blur"]))
        rp.end()

        # Re-read source for mask
        source2 = self.sourcePixmap(QtCore.Qt.CoordinateSystem.DeviceCoordinates)
        if isinstance(source2, tuple):
            source2 = source2[0]
        mask2 = source2.createMaskFromColor(QtGui.QColor(0, 0, 0, 0),
                                            QtCore.Qt.MaskMode.MaskOutColor)
        result.setMask(mask2)
        return result

    def _inside_shadow(self) -> QtGui.QPixmap:
        source = self.sourcePixmap(QtCore.Qt.CoordinateSystem.DeviceCoordinates)
        if isinstance(source, tuple):
            source = source[0]
        mask = source.createMaskFromColor(QtGui.QColor(0, 0, 0, 0),
                                          QtCore.Qt.MaskMode.MaskInColor)

        parts: list[QtGui.QPixmap] = []
        for s in self._shadow_list:
            if "inside" not in s:
                continue
            shadow = QtGui.QPixmap(mask.size())
            shadow.fill(QtCore.Qt.GlobalColor.transparent)
            sp = QtGui.QPainter(shadow)
            sp.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing |
                              QtGui.QPainter.RenderHint.SmoothPixmapTransform)

            removed_color = "#000000"
            color = QtGui.QColor(s["color"])
            if removed_color == color.name():
                removed_color = "#FFFFFF"

            sp.setTransform(QtGui.QTransform())
            sp.setPen(color)
            sp.drawPixmap(0, 0, mask)
            sp.setPen(QtGui.QColor(removed_color))
            sp.drawPixmap(s["offset"][0], s["offset"][1], mask)

            shadow_mask = shadow.createMaskFromColor(color, QtCore.Qt.MaskMode.MaskOutColor)
            shadow.fill(QtCore.Qt.GlobalColor.transparent)
            sp.setPen(color)
            sp.drawPixmap(0, 0, shadow_mask)
            sp.end()
            shadow.scaled(mask.size())
            parts.append(shadow)

        result = QtGui.QPixmap(mask.size())
        result.fill(QtCore.Qt.GlobalColor.transparent)
        rp = QtGui.QPainter(result)
        rp.setTransform(QtGui.QTransform())
        rp.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing |
                          QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        inside_shadows = [s for s in self._shadow_list if "inside" in s]
        for i, px in enumerate(parts):
            rp.drawPixmap(0, 0, self._blur_pixmap(px, inside_shadows[i]["blur"]))
        rp.end()
        result.setMask(mask)
        return result

    # -- draw ----------------------------------------------------------------

    def draw(self, painter: QtGui.QPainter) -> None:
        painter.setRenderHints(
            QtGui.QPainter.RenderHint.Antialiasing |
            QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        restore = painter.worldTransform()

        source_rect = self.boundingRectFor(
            self.sourceBoundingRect(QtCore.Qt.CoordinateSystem.DeviceCoordinates)
        ).toRect()
        x, y, w, h = source_rect.getRect()

        source = self.sourcePixmap(QtCore.Qt.CoordinateSystem.DeviceCoordinates)
        if isinstance(source, tuple):
            source = source[0]

        painter.setTransform(QtGui.QTransform())

        current_size = source.size()
        if (self._cache_outside is None or self._cache_size != current_size):
            if self._smooth:
                self._cache_outside = self._smooth_outside_shadow()
                self._cache_inside = self._smooth_inside_shadow()
            else:
                self._cache_outside = self._outside_shadow()
                self._cache_inside = self._inside_shadow()
            self._cache_size = current_size

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawPixmap(x, y, w, h, self._cache_outside)
        painter.drawPixmap(x, y, source)
        painter.drawPixmap(x + self._border, y + self._border,
                           w - self._border * 2, h - self._border * 2, self._cache_inside)
        painter.setWorldTransform(restore)


class BoxShadowWrapper(QtWidgets.QWidget):
    """Convenience wrapper that applies BoxShadow to a child widget."""

    def __init__(self, widget: QtWidgets.QWidget,
                 shadow_list: list[dict] | None = None,
                 border: int = 0,
                 disable_margins: bool = False,
                 margins: tuple | None = None,
                 smooth: bool = False) -> None:
        super().__init__()
        self._widget = widget
        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.addWidget(self._widget)

        self.boxShadow = BoxShadow(shadow_list, border, smooth)
        self._widget.setGraphicsEffect(self.boxShadow)

        self._custom_margins = disable_margins or margins is not None

        if not self._custom_margins:
            mx, my = self.boxShadow.necessary_indentation()
            self._layout.setContentsMargins(mx, my, mx, my)
        elif margins is not None:
            if len(margins) == 2:
                self._layout.setContentsMargins(margins[0], margins[1],
                                                margins[0], margins[1])
            elif len(margins) == 4:
                self._layout.setContentsMargins(*margins)

    def setShadowList(self, shadow_list: list[dict] | None = None) -> None:
        self.boxShadow.setShadowList(shadow_list)
        if not self._custom_margins:
            mx, my = self.boxShadow.necessary_indentation()
            self._layout.setContentsMargins(mx, my, mx, my)

    def setBorder(self, border: int) -> None:
        self.boxShadow.setBorder(border)
