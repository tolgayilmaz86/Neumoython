"""Reusable QSS snippet functions for neumorphic widgets.

Every function returns a plain string suitable for
:py:meth:`QWidget.setStyleSheet`.  Colours are resolved from the
active :pydata:`theme_manager` palette at call time, so results
stay correct after theme or accent-colour changes.

**Public API** (stable, intended for library consumers)::

    from styles import qss                  # recommended alias
    # or:  from styles.snippets import transparent_label, card_frame, ...

    lbl.setStyleSheet(qss.transparent_label("text_muted", 14, 600))
    frame.setStyleSheet(qss.card_frame(16))
    cal.setStyleSheet(qss.calendar_qss())

Functions whose names start with ``_`` or that are marked *internal*
in their docstring are used by the showcase application and may
change without notice.
"""

from __future__ import annotations

from styles.theme_manager import theme_manager

# ── public surface ────────────────────────────────────────────────────────
__all__ = [
    # Labels
    "transparent_label",
    "section_heading",
    "value_label",
    # Cards / Frames
    "card_frame",
    "icon_circle",
    # Buttons
    "close_button",
    "outline_color_button",
    "accent_dot",
    "collapsible_toggle",
    # Dialogs
    "dialog_title",
    "dialog_message",
    "dialog_separator",
    "dialog_accent_button",
    "dialog_secondary_button",
    # Expanders
    "expander_default",
    "expander_circle",
    "expander_stroke",
    "expander_stroke_horizontal",
    # Calendar
    "calendar_qss",
]


# ---------------------------------------------------------------------------
# Labels
# ---------------------------------------------------------------------------

def transparent_label(color_key: str = "text", size: int = 13,
                      weight: int = 400, *, extra: str = "") -> str:
    """QSS for a label with transparent background.

    :param color_key: Palette key for the text colour (e.g. ``"text"``,
        ``"text_muted"``, ``"accent"``).
    :param size: Font size in pixels.
    :param weight: CSS font-weight (400 = normal, 600 = semi-bold, 700 = bold).
    :param extra: Additional raw CSS appended after ``background: transparent;``.

    Example::

        lbl.setStyleSheet(qss.transparent_label("text_muted", 14, 600))
    """
    p = theme_manager.palette
    fw = f"font-weight: {weight}; " if weight != 400 else ""
    ex = f" {extra}" if extra else ""
    return (
        f"color: {p[color_key]}; font-size: {size}px; {fw}"
        f"background: transparent;{ex}"
    )


def section_heading() -> str:
    """QSS for a demo section heading label (muted, bold, small top margin)."""
    return transparent_label("text_muted", 14, 600, extra=" margin-top: 8px;")


def value_label() -> str:
    """QSS for an accent-coloured value readout label."""
    return transparent_label("accent", 13, 600)


# ---------------------------------------------------------------------------
# Cards / Frames
# ---------------------------------------------------------------------------

def card_frame(radius: int = 16) -> str:
    """QSS for a flat card frame with the current theme background.

    :param radius: Border-radius in pixels.

    Example::

        frame.setStyleSheet(qss.card_frame(20))
    """
    p = theme_manager.palette
    return f"QFrame {{ background: {p['card_bg']}; border-radius: {radius}px; }}"


def icon_circle(radius: int = 26) -> str:
    """QSS for a circular icon holder with theme background."""
    p = theme_manager.palette
    return f"background: {p['bg']}; border-radius: {radius}px;"


# ---------------------------------------------------------------------------
# Buttons
# ---------------------------------------------------------------------------

def close_button() -> str:
    """QSS for a transparent close / dismiss button."""
    return "background: transparent; border: none;"


def outline_color_button(color: str) -> str:
    """QSS for a coloured outline button that fills on hover.

    :param color: Any valid CSS colour string (hex, named, etc.).

    Example::

        btn.setStyleSheet(qss.outline_color_button("#D32F2F"))
    """
    return f"""
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
    """


def accent_dot(color_hex: str, size: int = 28) -> str:
    """QSS for a small circular accent colour dot button."""
    r = size // 2
    return (
        f"background: {color_hex}; border-radius: {r}px;"
        f" border: none; padding: 0px;"
        f" min-width: {size}px; max-width: {size}px;"
        f" min-height: {size}px; max-height: {size}px;"
    )


def explore_link() -> str:
    """QSS for the showcase 'Explore →' card link label.  *Internal.*"""
    p = theme_manager.palette
    return (
        f"color: {p['accent']}; background: transparent; "
        "font-size: 12px; font-weight: 600;"
    )


# ---------------------------------------------------------------------------
# Dialogs
# ---------------------------------------------------------------------------

def dialog_card(lifted_bg: str, border_color: str) -> str:
    """QSS for the outer card of a frameless NeuDialog.  *Internal.*

    Targets the ``#neu_dialog_card`` object name used by the showcase
    dialog classes.  Prefer :func:`card_frame` for general-purpose cards.
    """
    return f"""
        QFrame#neu_dialog_card {{
            background: {lifted_bg};
            border-radius: 20px;
            border: 1px solid {border_color};
        }}
    """


def dialog_title() -> str:
    """QSS for a dialog title label."""
    return transparent_label("text_heading", 16, 700)


def dialog_message() -> str:
    """QSS for a dialog body message label."""
    return transparent_label("text", 13)


def dialog_separator() -> str:
    """QSS for a thin horizontal separator."""
    p = theme_manager.palette
    return f"background: {p['bg_secondary']}; border: none; max-height: 1px;"


def dialog_accent_button(color: str) -> str:
    """QSS for an accent-coloured dialog action button."""
    return f"""
        QPushButton {{
            background: {color};
            color: #FFFFFF;
            border-radius: 10px;
            padding: 8px 20px;
            font-weight: 600;
            font-size: 13px;
            border: none;
        }}
        QPushButton:hover {{
            background: {color}CC;
        }}
    """


def dialog_secondary_button() -> str:
    """QSS for a secondary (non-accent) dialog action button."""
    p = theme_manager.palette
    return f"""
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
    """


# ---------------------------------------------------------------------------
# Collapsible / Expander headers
# ---------------------------------------------------------------------------

def collapsible_toggle() -> str:
    """QSS for a collapsible section toggle button."""
    p = theme_manager.palette
    return f"""
        QPushButton {{
            text-align: left;
            padding: 12px 16px;
            font-weight: 600;
            font-size: 13px;
            color: {p['text_heading']};
            background: {p['card_bg']};
            border: none;
            border-radius: 12px;
        }}
        QPushButton:hover {{
            background: {p['menu_hover']};
        }}
        QPushButton:focus {{
            border: 2px solid {p['accent']};
        }}
    """


def expander_default(obj: str, *, horizontal: bool = False) -> str:
    """QSS for the default-theme expander header."""
    p = theme_manager.palette
    align = "" if horizontal else "text-align: left;\n            "
    return f"""
        #{obj} {{
            {align}padding: 10px 16px;
            font-weight: 600;
            font-size: 13px;
            color: {p['text_heading']};
            background: {p['card_bg']};
            border: none;
            border-radius: 12px;
        }}
        #{obj}:hover {{ background: {p['menu_hover']}; }}
        #{obj}:disabled {{
            color: {p['text_muted']};
            background: {p['bg_secondary']};
        }}
    """


def expander_circle(obj: str) -> str:
    """QSS for the circle-theme expander toggle."""
    p = theme_manager.palette
    return f"""
        #{obj} {{
            background: {p['card_bg']};
            border: none;
            border-radius: 16px;
        }}
        #{obj}:hover {{
            background: {p['menu_hover']};
        }}
        #{obj}:disabled {{
            background: {p['bg_secondary']};
        }}
    """


def expander_stroke(obj: str) -> str:
    """QSS for the stroke-theme expander header."""
    p = theme_manager.palette
    return f"""
        #{obj} {{
            text-align: left;
            padding: 10px 16px;
            font-weight: 600;
            font-size: 13px;
            color: {p['text_heading']};
            background: transparent;
            border: 2px solid {p['text_muted']};
            border-radius: 14px;
        }}
        #{obj}:hover {{
            border-color: {p['accent']};
            color: {p['accent']};
        }}
        #{obj}:disabled {{
            color: {p['text_muted']};
            border-color: {p['bg_secondary']};
            background: {p['bg_secondary']};
        }}
    """


def expander_stroke_horizontal(obj: str) -> str:
    """QSS for the stroke-theme horizontal expander header."""
    p = theme_manager.palette
    return f"""
        #{obj} {{
            background: transparent;
            border: 2px solid {p['text_muted']};
            border-radius: 14px;
            color: {p['text_heading']};
            font-weight: 600;
            font-size: 13px;
        }}
        #{obj}:hover {{
            border-color: {p['accent']};
            color: {p['accent']};
        }}
        #{obj}:disabled {{
            color: {p['text_muted']};
            border-color: {p['bg_secondary']};
            background: {p['bg_secondary']};
        }}
    """


# ---------------------------------------------------------------------------
# Calendar
# ---------------------------------------------------------------------------

def calendar_qss() -> str:
    """Full QSS for a ``QCalendarWidget`` in the neumorphic theme.

    Apply to any calendar widget to get themed navigation bar,
    selection colours, and spin-box styling::

        cal = QCalendarWidget()
        cal.setStyleSheet(qss.calendar_qss())
    """
    p = theme_manager.palette
    return f"""
        QCalendarWidget {{
            background: {p['card_bg']};
            color: {p['text']};
        }}
        QCalendarWidget QAbstractItemView {{
            background: {p['card_bg']};
            color: {p['text']};
            selection-background-color: {p['accent']};
            selection-color: #FFFFFF;
            gridline-color: {p['bg_secondary']};
            border: none;
            border-radius: 8px;
        }}
        QCalendarWidget QAbstractItemView:disabled {{
            color: {p['text_muted']};
        }}
        QCalendarWidget QToolButton {{
            background: {p['card_bg']};
            color: {p['text']};
            border: none;
            border-radius: 8px;
            padding: 4px 8px;
            font-weight: 600;
        }}
        QCalendarWidget QToolButton:hover {{
            background: {p['menu_hover']};
        }}
        QCalendarWidget QSpinBox {{
            background: {p['input_bg']};
            color: {p['text']};
            border: none;
            border-radius: 6px;
            padding: 2px 6px;
        }}
        QCalendarWidget QWidget#qt_calendar_navigationbar {{
            background: {p['bg_secondary']};
            border-radius: 10px;
            padding: 4px;
        }}
        QCalendarWidget QWidget {{
            background: {p['card_bg']};
        }}
    """
