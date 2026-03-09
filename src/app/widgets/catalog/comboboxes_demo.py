"""ComboBoxes demo – combo box and drop-down widgets with neumorphic theming.

Features icon items via QStyledItemDelegate, grouped sections,
editable combo, and a multi-column variant.
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
# Icon item delegate – renders qtawesome icon + text in QComboBox dropdown
# ---------------------------------------------------------------------------

class _IconDelegate(QtWidgets.QStyledItemDelegate):
    """Paints icon + text rows in a QComboBox dropdown."""

    ICON_SIZE = 18

    def paint(self, painter: QtGui.QPainter,
              option: QtWidgets.QStyleOptionViewItem,
              index: QtCore.QModelIndex) -> None:
        painter.save()
        p = theme_manager.palette

        is_selected = option.state & QtWidgets.QStyle.StateFlag.State_Selected
        is_separator = index.data(QtCore.Qt.ItemDataRole.UserRole + 1)

        if is_separator:
            # Draw a group header (bold, non-selectable, no hover)
            painter.fillRect(option.rect, QtGui.QColor(p["bg_secondary"]))
            painter.setPen(QtGui.QColor(p["text_muted"]))
            font = painter.font()
            font.setBold(True)
            font.setPointSize(font.pointSize() - 1)
            painter.setFont(font)
            text_rect = option.rect.adjusted(10, 0, 0, 0)
            painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignVCenter,
                             index.data())
            painter.restore()
            return

        bg = QtGui.QColor(p["accent"]) if is_selected else QtGui.QColor(p["card_bg"])
        painter.fillRect(option.rect, bg)

        # icon
        icon = index.data(QtCore.Qt.ItemDataRole.DecorationRole)
        x = option.rect.left() + 8
        y = option.rect.top() + (option.rect.height() - self.ICON_SIZE) // 2
        if icon and not icon.isNull():
            icon.paint(painter, QtCore.QRect(x, y, self.ICON_SIZE, self.ICON_SIZE))
        x += self.ICON_SIZE + 8

        # text
        txt_color = QtGui.QColor("#FFFFFF") if is_selected else QtGui.QColor(p["text"])
        painter.setPen(txt_color)
        text_rect = QtCore.QRect(x, option.rect.top(),
                                 option.rect.right() - x - 4,
                                 option.rect.height())
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignVCenter,
                         index.data() or "")
        painter.restore()

    def sizeHint(self, option, index) -> QtCore.QSize:
        is_separator = index.data(QtCore.Qt.ItemDataRole.UserRole + 1)
        h = 24 if is_separator else 36
        return QtCore.QSize(option.rect.width(), h)


def _make_icon_combo(items: list[tuple[str, str]]) -> QtWidgets.QComboBox:
    """Build a QComboBox with (label, mdi6-icon-name) items."""
    p = theme_manager.palette
    combo = QtWidgets.QComboBox()
    combo.setItemDelegate(_IconDelegate())
    for label, icon_name in items:
        icon = qta.icon(icon_name, color=p["text"])
        combo.addItem(icon, label)
    combo.setMinimumWidth(200)
    return combo


def _separator_item(combo: QtWidgets.QComboBox, label: str) -> None:
    """Add a non-selectable group header."""
    combo.addItem(label)
    idx = combo.count() - 1
    item = combo.model().item(idx)
    item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEnabled)
    combo.model().setData(
        combo.model().index(idx, 0),
        True,
        QtCore.Qt.ItemDataRole.UserRole + 1,
    )


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

    title = QtWidgets.QLabel("ComboBoxes")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    desc = QtWidgets.QLabel(
        "Drop-down combo box controls with icon items, group separators, "
        "editable variants, and multi-select display."
    )
    desc.setWordWrap(True)
    desc.setProperty("subheading", True)
    layout.addWidget(desc)

    # --- Basic combos ---
    group1 = QtWidgets.QGroupBox("Standard ComboBoxes")
    g1 = QtWidgets.QFormLayout(group1)
    g1.setContentsMargins(16, 24, 16, 16)
    g1.setSpacing(14)

    # Plain text
    plain_combo = QtWidgets.QComboBox()
    for item in ("Option 1", "Option 2", "Option 3", "Option 4", "Option 5"):
        plain_combo.addItem(item)
    plain_combo.setMinimumWidth(200)

    # Disabled
    disabled_combo = QtWidgets.QComboBox()
    disabled_combo.addItems(("Disabled A", "Disabled B"))
    disabled_combo.setMinimumWidth(200)
    disabled_combo.setEnabled(False)

    # Icon combo
    icon_combo = _make_icon_combo([
        ("Home",       "mdi6.home-outline"),
        ("Profile",    "mdi6.account-outline"),
        ("Settings",   "mdi6.cog-outline"),
        ("Notifications", "mdi6.bell-outline"),
        ("Help",       "mdi6.help-circle-outline"),
    ])

    sel_lbl = QtWidgets.QLabel(f"Selected: {icon_combo.currentText()}")
    sel_lbl.setStyleSheet(f"color: {p['accent']}; font-size: 12px; background: transparent;")
    icon_combo.currentTextChanged.connect(
        lambda t: sel_lbl.setText(f"Selected: {t}"))

    g1.addRow("Plain:", plain_combo)
    g1.addRow("Disabled:", disabled_combo)
    g1.addRow("With icons:", icon_combo)
    g1.addRow("", sel_lbl)
    layout.addWidget(_neu_group(group1))

    # --- Grouped items ---
    group2 = QtWidgets.QGroupBox("Grouped Items")
    g2 = QtWidgets.QFormLayout(group2)
    g2.setContentsMargins(16, 24, 16, 16)
    g2.setSpacing(14)

    grouped = QtWidgets.QComboBox()
    grouped.setItemDelegate(_IconDelegate())
    grouped.setMinimumWidth(240)

    _separator_item(grouped, "Fruits")
    for lbl, ic in [("Apple", "mdi6.food-apple-outline"),
                    ("Banana", "mdi6.fruit-cherries"),
                    ("Orange", "mdi6.fruit-citrus")]:
        grouped.addItem(qta.icon(ic, color=p["text"]), lbl)

    _separator_item(grouped, "Vegetables")
    for lbl, ic in [("Broccoli", "mdi6.leaf"),
                    ("Carrot", "mdi6.carrot"),
                    ("Tomato", "mdi6.food-outline")]:
        grouped.addItem(qta.icon(ic, color=p["text"]), lbl)

    g2.addRow("Category combo:", grouped)
    layout.addWidget(_neu_group(group2))

    # --- Editable combo ---
    group3 = QtWidgets.QGroupBox("Editable ComboBox")
    g3 = QtWidgets.QVBoxLayout(group3)
    g3.setContentsMargins(16, 24, 16, 16)
    g3.setSpacing(12)

    editable = QtWidgets.QComboBox()
    editable.setEditable(True)
    editable.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.InsertAtBottom)
    editable.addItems([
        "python", "pyside6", "neumorphism", "qt framework",
        "widget library",
    ])
    editable.setMinimumWidth(280)
    editable.setPlaceholderText("Type or select…")

    hint = QtWidgets.QLabel("Type a new value and press Enter to add it to the list.")
    hint.setStyleSheet(f"font-size: 11px; color: {p['text_muted']}; background: transparent;")
    hint.setWordWrap(True)

    g3.addWidget(editable)
    g3.addWidget(hint)
    layout.addWidget(_neu_group(group3))

    # --- Size variants ---
    group4 = QtWidgets.QGroupBox("Size Variants")
    g4 = QtWidgets.QHBoxLayout(group4)
    g4.setContentsMargins(16, 24, 16, 16)
    g4.setSpacing(16)

    for width, label in [(140, "Compact"), (220, "Standard"), (320, "Wide")]:
        combo = QtWidgets.QComboBox()
        combo.addItems(("Item A", "Item B", "Item C"))
        combo.setMinimumWidth(width)
        combo.setMaximumWidth(width)
        form = QtWidgets.QFormLayout()
        form.setContentsMargins(0, 0, 0, 0)
        lbl_w = QtWidgets.QLabel(label)
        lbl_w.setStyleSheet(f"font-size: 11px; color: {p['text_muted']}; background: transparent;")
        form.addRow(lbl_w, combo)
        g4.addLayout(form)
    g4.addStretch()

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

    title = QtWidgets.QLabel("About ComboBoxes")
    title.setProperty("heading", True)
    font = title.font()
    font.setPointSize(20)
    title.setFont(font)
    layout.addWidget(title)

    info = QtWidgets.QLabel(
        "Drop-down combo box widgets:\n\n"
        "  • Plain QComboBox – standard item list\n"
        "  • Icon items – via QStyledItemDelegate painting\n"
        "  • Grouped sections – bold non-selectable header items\n"
        "  • Editable combo – accepts free-text input\n"
        "  • Size variants – compact / standard / wide\n\n"
        "The _IconDelegate class is a QStyledItemDelegate subclass that\n"
        "paints QIcon + text rows, enabling Material Design icons from\n"
        "qtawesome in combo box drop-downs."
    )
    info.setWordWrap(True)
    layout.addWidget(info)
    layout.addStretch()
    return page


registry.register(WidgetDemo(
    id="comboboxes",
    name="ComboBoxes",
    create_page=create_page,
    create_about=create_about,
    description="Drop-down combo box controls with icon items and groups.",
))
