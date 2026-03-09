"""Neumorphism theme manager with light / dark mode support."""

from __future__ import annotations

import os
import tempfile

from PySide6 import QtCore, QtGui, QtWidgets


# ---------------------------------------------------------------------------
# Arrow SVG generator – tiny coloured triangles for QSS ``image: url(…)``
# ---------------------------------------------------------------------------

_arrow_cache: dict[str, str] = {}  # key → file path

def _arrow_svg_path(direction: str, color: str) -> str:
    """Return the path to a small SVG arrow pointing *direction* (up/down).

    Files are created once in a temp directory and cached for the process
    lifetime.  ``color`` must be a hex colour like ``#8E8E93``.
    """
    key = f"{direction}_{color}"
    if key in _arrow_cache:
        return _arrow_cache[key].replace("\\", "/")

    if direction == "down":
        points = "2,3 8,3 5,8"
    else:  # up
        points = "2,8 8,8 5,3"

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">'
        f'<polygon points="{points}" fill="{color}"/>'
        '</svg>'
    )
    tmp_dir = os.path.join(tempfile.gettempdir(), "neu_arrows")
    os.makedirs(tmp_dir, exist_ok=True)
    fpath = os.path.join(tmp_dir, f"{direction}_{color.lstrip('#')}.svg")
    if not os.path.exists(fpath):
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(svg)
    _arrow_cache[key] = fpath
    return fpath.replace("\\", "/")


# ---------------------------------------------------------------------------
# Palettes – colour dicts keyed by theme name
# ---------------------------------------------------------------------------

_PALETTES: dict[str, dict] = {
    "light": {
        "bg":             "#E0E5EC",
        "bg_secondary":   "#D5DAE1",
        "sidebar":        "#E0E5EC",
        "topbar":         "#E0E5EC",
        "text":           "#616163",
        "text_heading":   "#333333",
        "text_muted":     "#8E8E93",
        "accent":         "#9C27B0",
        "accent_hover":   "#AB47BC",
        "accent_secondary": "#AEEA00",
        "card_bg":        "#E0E5EC",
        "menu_active":    "#D5DAE1",
        "menu_hover":     "#D8DDE4",
        "border":         "transparent",
        "input_bg":       "#E0E5EC",
        "shadow_dark":    "rgba(0,0,0,51)",
        "shadow_light":   "rgba(255,255,255,204)",
        "button_light":   "#EDF2F9",
        "button_dark":    "#5C5E62",
    },
    "dark": {
        "bg":             "#2C3135",
        "bg_secondary":   "#252A2E",
        "sidebar":        "#2C3135",
        "topbar":         "#2C3135",
        "text":           "#FFFFFF",
        "text_heading":   "#CCCCCC",
        "text_muted":     "#888888",
        "accent":         "#CE93D8",
        "accent_hover":   "#E1BEE7",
        "accent_secondary": "#AEEA00",
        "card_bg":        "#2C3135",
        "menu_active":    "#353A3F",
        "menu_hover":     "#323940",
        "border":         "transparent",
        "input_bg":       "#2C3135",
        "shadow_dark":    "rgba(0,0,0,136)",
        "shadow_light":   "rgba(255,255,255,34)",
        "button_light":   "#3A3F44",
        "button_dark":    "#1A1D20",
    },
}


# ---------------------------------------------------------------------------
# Accent colour presets  (pass any of these to ThemeManager.set_accent())
# ---------------------------------------------------------------------------

ACCENT_PURPLE = "#9C27B0"   # Default — purple
ACCENT_BLUE   = "#1976D2"   # Material Blue 700
ACCENT_TEAL   = "#00897B"   # Material Teal 600
ACCENT_CORAL  = "#E64A19"   # Material Deep Orange 700
ACCENT_PINK   = "#E91E63"   # Material Pink 500


def _shadow_configs(theme: str) -> dict[str, list[dict]]:
    """Shadow dicts keyed by usage (outside_raised, inside_pressed, etc.)."""
    if theme == "light":
        return {
            "outside_raised": [
                {"outside": True, "offset": [5, 5], "blur": 10,
                 "color": QtGui.QColor(0, 0, 0, 51)},       # #33000000
                {"outside": True, "offset": [-5, -5], "blur": 10,
                 "color": QtGui.QColor(255, 255, 255, 204)}, # #CCFFFFFF
            ],
            "inside_pressed": [
                {"inside": True, "offset": [4, 4], "blur": 8,
                 "color": QtGui.QColor(0, 0, 0, 40)},
                {"inside": True, "offset": [-4, -4], "blur": 8,
                 "color": QtGui.QColor(255, 255, 255, 180)},
            ],
            # Smaller shadows for buttons and compact widgets
            "button_raised": [
                {"outside": True, "offset": [3, 3], "blur": 6,
                 "color": QtGui.QColor(0, 0, 0, 45)},
                {"outside": True, "offset": [-3, -3], "blur": 6,
                 "color": QtGui.QColor(255, 255, 255, 200)},
            ],
            "button_pressed": [
                {"inside": True, "offset": [3, 3], "blur": 5,
                 "color": QtGui.QColor(0, 0, 0, 40)},
                {"inside": True, "offset": [-3, -3], "blur": 5,
                 "color": QtGui.QColor(255, 255, 255, 180)},
            ],
            # Input fields – inset shadow for recessed look
            "input_inset": [
                {"inside": True, "offset": [2, 2], "blur": 4,
                 "color": QtGui.QColor(0, 0, 0, 35)},
                {"inside": True, "offset": [-2, -2], "blur": 4,
                 "color": QtGui.QColor(255, 255, 255, 170)},
            ],
            # Outline fields – outset + inset for prominent border feel
            "input_outline": [
                {"outside": True, "offset": [3, 3], "blur": 6,
                 "color": QtGui.QColor(0, 0, 0, 40)},
                {"outside": True, "offset": [-3, -3], "blur": 6,
                 "color": QtGui.QColor(255, 255, 255, 190)},
                {"inside": True, "offset": [2, 2], "blur": 4,
                 "color": QtGui.QColor(0, 0, 0, 20)},
                {"inside": True, "offset": [-2, -2], "blur": 4,
                 "color": QtGui.QColor(255, 255, 255, 120)},
            ],
        }
    else:
        return {
            "outside_raised": [
                {"outside": True, "offset": [5, 5], "blur": 10,
                 "color": QtGui.QColor(0, 0, 0, 136)},      # #88000000
                {"outside": True, "offset": [-5, -5], "blur": 10,
                 "color": QtGui.QColor(255, 255, 255, 34)},  # #22FFFFFF
            ],
            "inside_pressed": [
                {"inside": True, "offset": [4, 4], "blur": 8,
                 "color": QtGui.QColor(0, 0, 0, 136)},
                {"inside": True, "offset": [-4, -4], "blur": 8,
                 "color": QtGui.QColor(255, 255, 255, 34)},
            ],
            "button_raised": [
                {"outside": True, "offset": [3, 3], "blur": 6,
                 "color": QtGui.QColor(0, 0, 0, 120)},
                {"outside": True, "offset": [-3, -3], "blur": 6,
                 "color": QtGui.QColor(255, 255, 255, 30)},
            ],
            "button_pressed": [
                {"inside": True, "offset": [3, 3], "blur": 5,
                 "color": QtGui.QColor(0, 0, 0, 120)},
                {"inside": True, "offset": [-3, -3], "blur": 5,
                 "color": QtGui.QColor(255, 255, 255, 30)},
            ],
            "input_inset": [
                {"inside": True, "offset": [2, 2], "blur": 4,
                 "color": QtGui.QColor(0, 0, 0, 100)},
                {"inside": True, "offset": [-2, -2], "blur": 4,
                 "color": QtGui.QColor(255, 255, 255, 25)},
            ],
            "input_outline": [
                {"outside": True, "offset": [3, 3], "blur": 6,
                 "color": QtGui.QColor(0, 0, 0, 110)},
                {"outside": True, "offset": [-3, -3], "blur": 6,
                 "color": QtGui.QColor(255, 255, 255, 25)},
                {"inside": True, "offset": [2, 2], "blur": 4,
                 "color": QtGui.QColor(0, 0, 0, 70)},
                {"inside": True, "offset": [-2, -2], "blur": 4,
                 "color": QtGui.QColor(255, 255, 255, 15)},
            ],
        }


# ---------------------------------------------------------------------------
# QSS generator
# ---------------------------------------------------------------------------

def _generate_qss(p: dict) -> str:
    """Return a full QSS string for the given palette dict."""
    return f"""
/* ===== Neumorphism theme – auto-generated by ThemeManager ===== */

/* --- Global --- */
QWidget {{
    background: {p['bg']};
    color: {p['text']};
    font-family: "Segoe UI", sans-serif;
}}

QMainWindow {{
    background: {p['bg']};
}}

QLabel {{
    background: transparent;
    color: {p['text']};
}}

/* --- Top bar (60 px Color-Zone) --- */
#frame_top {{
    background: {p['topbar']};
    min-height: 60px;
    max-height: 60px;
}}

#frame_top_east {{
    background: {p['topbar']};
}}

#frame_appname {{
    background: transparent;
}}

#frame_appname QLabel,
#lab_appname {{
    color: {p['text_heading']};
    background: transparent;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.5px;
}}

#lab_user {{
    color: {p['text_muted']};
    background: transparent;
    font-size: 11px;
}}

/* --- Window control button containers --- */
#frame_min, #frame_max, #frame_close, #frame_theme_toggle {{
    background: transparent;
}}

#frame_close {{
    padding-right: 4px;
}}

/* --- Window control buttons --- */
#bn_min, #bn_max, #bn_close, #bn_theme_toggle {{
    border: none;
    background-color: transparent;
    border-radius: 8px;
    color: {p['text']};
    padding: 0px;
    min-width: 36px;
    min-height: 36px;
    max-width: 36px;
    max-height: 36px;
}}
#bn_min:hover, #bn_max:hover, #bn_theme_toggle:hover {{
    background-color: {p['menu_hover']};
}}
#bn_close:hover {{
    background-color: #E04848;
    color: #FFFFFF;
    border-radius: 8px;
}}
#bn_min:pressed, #bn_max:pressed, #bn_close:pressed, #bn_theme_toggle:pressed {{
    background-color: transparent;
}}

/* --- Sidebar (Navigation Drawer) --- */
#frame_bottom_west {{
    background: {p['sidebar']};
    border-right: 1px solid {p['bg_secondary']};
}}

/* --- Sidebar menu frames --- */
QFrame[menuState="normal"] {{
    background: {p['sidebar']};
    border: none;
    border-left: 3px solid transparent;
}}

QFrame[menuState="active"] {{
    background: {p['menu_active']};
    border: none;
    border-left: 3px solid {p['accent']};
    border-radius: 0px;
}}

QFrame[subMenuState="normal"] {{
    background: {p['sidebar']};
}}

QFrame[subMenuState="active"] {{
    background: {p['menu_active']};
}}

/* --- Sidebar navigation buttons (48 px height, icon + label) --- */
#frame_bottom_west QPushButton[flat="true"],
#bn_widgets {{
    border: none;
    background-color: transparent;
    color: {p['text_muted']};
    text-align: left;
    padding-left: 12px;
    font-size: 13px;
    font-weight: 500;
}}

#frame_bottom_west QPushButton[flat="true"]:hover,
#bn_widgets:hover {{
    background-color: {p['menu_hover']};
    color: {p['text']};
    border-radius: 0px;
}}

#frame_bottom_west QPushButton[flat="true"]:pressed,
#bn_widgets:pressed {{
    background-color: transparent;
}}

/* Active nav button text color */
QFrame[menuState="active"] QPushButton[flat="true"] {{
    color: {p['accent']};
    font-weight: 600;
}}

/* --- Toggle (hamburger) --- */
#toodle {{
    border: none;
    background-color: transparent;
    color: {p['text']};
    border-radius: 8px;
    min-width: 40px;
    min-height: 40px;
}}
#toodle:hover {{
    background-color: {p['menu_hover']};
}}

#frame_toodle {{
    background: {p['sidebar']};
    border-bottom: 1px solid {p['bg_secondary']};
}}

/* --- Main content area --- */
#frame_bottom_east, #frame {{
    background: {p['bg']};
}}

QStackedWidget {{
    background: {p['bg']};
}}

/* --- Status / tab bar (breadcrumb) --- */
#frame_tab {{
    background: {p['topbar']};
    border-top: 1px solid {p['bg_secondary']};
}}

#lab_tab {{
    color: {p['text_muted']};
    background: transparent;
    font-size: 11px;
    padding-left: 8px;
}}

#frame_drag {{
    background: {p['topbar']};
}}

#frame_low {{
    background: {p['topbar']};
}}

/* --- Showcase cards (Home page – neumorphic raised panels) --- */
#showcase_card {{
    background: {p['card_bg']};
    border: none;
    border-radius: 16px;
    padding: 4px;
}}

#showcase_card:hover {{
    background: {p['menu_hover']};
}}

#showcase_card QLabel {{
    color: {p['text']};
    background: transparent;
}}

/* --- Group boxes (neumorphic containers) --- */
QGroupBox {{
    background: {p['card_bg']};
    border: none;
    border-radius: 14px;
    margin-top: 14px;
    padding: 20px 14px 14px 14px;
    color: {p['text_heading']};
    font-weight: 600;
    font-size: 13px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 16px;
    padding: 2px 10px;
    background: {p['card_bg']};
    color: {p['text_heading']};
    font-size: 13px;
    border-radius: 8px;
}}

/* --- Buttons (neumorphic raised) --- */
QPushButton {{
    background: {p['card_bg']};
    color: {p['text']};
    border: none;
    border-radius: 12px;
    padding: 10px 24px;
    font-weight: 600;
    font-size: 13px;
}}

QPushButton:hover {{
    background: {p['menu_hover']};
    color: {p['text_heading']};
}}

QPushButton:pressed {{
    background: {p['bg_secondary']};
    padding: 11px 24px 9px 24px;
}}

QPushButton:disabled {{
    color: {p['text_muted']};
    background: {p['bg']};
}}

QPushButton:checked {{
    background: {p['accent']};
    color: #FFFFFF;
}}

QPushButton:flat {{
    border: none;
    background-color: transparent;
}}
QPushButton:flat:hover {{
    background-color: {p['menu_hover']};
}}

/* --- Accent button class (primary action) --- */
QPushButton[accentButton="true"] {{
    background: {p['accent']};
    color: #FFFFFF;
    border: none;
    border-radius: 12px;
    padding: 10px 24px;
    font-weight: 600;
    font-size: 13px;
}}

QPushButton[accentButton="true"]:hover {{
    background: {p['accent_hover']};
}}

QPushButton[accentButton="true"]:pressed {{
    padding: 11px 24px 9px 24px;
}}

/* --- Light button variant --- */
QPushButton[buttonVariant="light"] {{
    background: {p['button_light']};
    color: {p['text']};
    border: none;
    border-radius: 12px;
    padding: 10px 24px;
    font-weight: 600;
    font-size: 13px;
}}
QPushButton[buttonVariant="light"]:hover {{
    background: {p['menu_hover']};
}}
QPushButton[buttonVariant="light"]:pressed {{
    background: {p['bg_secondary']};
    padding: 11px 24px 9px 24px;
}}

/* --- Dark button variant --- */
QPushButton[buttonVariant="dark"] {{
    background: {p['button_dark']};
    color: #FFFFFF;
    border: none;
    border-radius: 12px;
    padding: 10px 24px;
    font-weight: 600;
    font-size: 13px;
}}
QPushButton[buttonVariant="dark"]:hover {{
    opacity: 0.85;
}}
QPushButton[buttonVariant="dark"]:pressed {{
    padding: 11px 24px 9px 24px;
}}

/* --- Gradient button variant --- */
QPushButton[buttonVariant="gradient"] {{
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 {p['accent']},
        stop:1 {p['accent_hover']}
    );
    color: #FFFFFF;
    border: none;
    border-radius: 12px;
    padding: 10px 24px;
    font-weight: 600;
    font-size: 13px;
}}
QPushButton[buttonVariant="gradient"]:hover {{
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 {p['accent_hover']},
        stop:1 {p['accent']}
    );
}}
QPushButton[buttonVariant="gradient"]:pressed {{
    padding: 11px 24px 9px 24px;
}}

/* --- Outline button variant --- */
QPushButton[buttonVariant="outline"] {{
    background: transparent;
    color: {p['text']};
    border: 2px solid {p['text_muted']};
    border-radius: 12px;
    padding: 8px 22px;
    font-weight: 600;
    font-size: 13px;
}}
QPushButton[buttonVariant="outline"]:hover {{
    background: {p['menu_hover']};
    border-color: {p['text']};
}}
QPushButton[buttonVariant="outline"]:pressed {{
    background: {p['bg_secondary']};
    padding: 9px 22px 7px 22px;
}}
QPushButton[buttonVariant="outline"]:disabled {{
    color: {p['text_muted']};
    border-color: {p['bg_secondary']};
    background: transparent;
}}

/* --- Outline Light --- */
QPushButton[buttonVariant="outline-light"] {{
    background: transparent;
    color: {p['text']};
    border: 2px solid {p['button_light']};
    border-radius: 12px;
    padding: 8px 22px;
    font-weight: 600;
    font-size: 13px;
}}
QPushButton[buttonVariant="outline-light"]:hover {{
    background: {p['button_light']};
}}

/* --- Outline Dark --- */
QPushButton[buttonVariant="outline-dark"] {{
    background: transparent;
    color: {p['text']};
    border: 2px solid {p['button_dark']};
    border-radius: 12px;
    padding: 8px 22px;
    font-weight: 600;
    font-size: 13px;
}}
QPushButton[buttonVariant="outline-dark"]:hover {{
    background: {p['button_dark']};
    color: #FFFFFF;
}}

/* --- Outline Accent --- */
QPushButton[buttonVariant="outline-accent"] {{
    background: transparent;
    color: {p['accent']};
    border: 2px solid {p['accent']};
    border-radius: 12px;
    padding: 8px 22px;
    font-weight: 600;
    font-size: 13px;
}}
QPushButton[buttonVariant="outline-accent"]:hover {{
    background: {p['accent']};
    color: #FFFFFF;
}}

/* --- Icon button (circular, no text) --- */
QPushButton[buttonVariant="icon"] {{
    background: transparent;
    border: none;
    border-radius: 20px;
    padding: 8px;
    min-width: 40px;
    max-width: 40px;
    min-height: 40px;
    max-height: 40px;
}}
QPushButton[buttonVariant="icon"]:hover {{
    background: {p['menu_hover']};
}}
QPushButton[buttonVariant="icon"]:pressed {{
    background: {p['bg_secondary']};
}}

/* --- Icon Light --- */
QPushButton[buttonVariant="icon-light"] {{
    background: {p['button_light']};
    border: none;
    border-radius: 20px;
    padding: 8px;
    min-width: 40px; max-width: 40px;
    min-height: 40px; max-height: 40px;
}}
QPushButton[buttonVariant="icon-light"]:hover {{
    background: {p['menu_hover']};
}}

/* --- Icon Dark --- */
QPushButton[buttonVariant="icon-dark"] {{
    background: {p['button_dark']};
    border: none;
    border-radius: 20px;
    padding: 8px;
    min-width: 40px; max-width: 40px;
    min-height: 40px; max-height: 40px;
}}
QPushButton[buttonVariant="icon-dark"]:hover {{
    opacity: 0.85;
}}

/* --- Icon Accent --- */
QPushButton[buttonVariant="icon-accent"] {{
    background: {p['accent']};
    border: none;
    border-radius: 20px;
    padding: 8px;
    min-width: 40px; max-width: 40px;
    min-height: 40px; max-height: 40px;
}}
QPushButton[buttonVariant="icon-accent"]:hover {{
    background: {p['accent_hover']};
}}

/* --- Floating Action Button (FAB) --- */
QPushButton[buttonVariant="fab"] {{
    background: {p['card_bg']};
    border: none;
    border-radius: 28px;
    padding: 0px;
    min-width: 56px; max-width: 56px;
    min-height: 56px; max-height: 56px;
    font-size: 14px;
}}
QPushButton[buttonVariant="fab"]:hover {{
    background: {p['menu_hover']};
}}
QPushButton[buttonVariant="fab"]:pressed {{
    background: {p['bg_secondary']};
}}
QPushButton[buttonVariant="fab"]:disabled {{
    color: {p['text_muted']};
    background: {p['bg']};
}}

/* --- FAB Light --- */
QPushButton[buttonVariant="fab-light"] {{
    background: {p['button_light']};
    border: none;
    border-radius: 28px;
    padding: 0px;
    min-width: 56px; max-width: 56px;
    min-height: 56px; max-height: 56px;
}}
QPushButton[buttonVariant="fab-light"]:hover {{
    background: {p['menu_hover']};
}}

/* --- FAB Dark --- */
QPushButton[buttonVariant="fab-dark"] {{
    background: {p['button_dark']};
    border: none;
    border-radius: 28px;
    padding: 0px;
    min-width: 56px; max-width: 56px;
    min-height: 56px; max-height: 56px;
}}
QPushButton[buttonVariant="fab-dark"]:hover {{
    opacity: 0.85;
}}

/* --- FAB Accent --- */
QPushButton[buttonVariant="fab-accent"] {{
    background: {p['accent']};
    border: none;
    border-radius: 28px;
    padding: 0px;
    min-width: 56px; max-width: 56px;
    min-height: 56px; max-height: 56px;
}}
QPushButton[buttonVariant="fab-accent"]:hover {{
    background: {p['accent_hover']};
}}
QPushButton[buttonVariant="fab-accent"]:disabled {{
    background: {p['bg']};
    color: {p['text_muted']};
}}

/* --- Mini FAB (40 px) --- */
QPushButton[buttonVariant="fab-mini"] {{
    background: {p['card_bg']};
    border: none;
    border-radius: 20px;
    padding: 0px;
    min-width: 40px; max-width: 40px;
    min-height: 40px; max-height: 40px;
}}
QPushButton[buttonVariant="fab-mini"]:hover {{
    background: {p['menu_hover']};
}}

QPushButton[buttonVariant="fab-light-mini"] {{
    background: {p['button_light']};
    border: none; border-radius: 20px; padding: 0px;
    min-width: 40px; max-width: 40px;
    min-height: 40px; max-height: 40px;
}}
QPushButton[buttonVariant="fab-light-mini"]:hover {{
    background: {p['menu_hover']};
}}

QPushButton[buttonVariant="fab-dark-mini"] {{
    background: {p['button_dark']};
    border: none; border-radius: 20px; padding: 0px;
    min-width: 40px; max-width: 40px;
    min-height: 40px; max-height: 40px;
}}
QPushButton[buttonVariant="fab-dark-mini"]:hover {{
    opacity: 0.85;
}}

QPushButton[buttonVariant="fab-accent-mini"] {{
    background: {p['accent']};
    border: none; border-radius: 20px; padding: 0px;
    min-width: 40px; max-width: 40px;
    min-height: 40px; max-height: 40px;
}}
QPushButton[buttonVariant="fab-accent-mini"]:hover {{
    background: {p['accent_hover']};
}}

/* --- Extended FAB --- */
QPushButton[buttonVariant="fab-extended"] {{
    background: {p['card_bg']};
    color: {p['text']};
    border: none;
    border-radius: 24px;
    padding: 12px 24px;
    font-weight: 600;
    font-size: 13px;
    min-height: 48px;
}}
QPushButton[buttonVariant="fab-extended"]:hover {{
    background: {p['menu_hover']};
}}

QPushButton[buttonVariant="fab-extended-light"] {{
    background: {p['button_light']};
    color: {p['text']};
    border: none; border-radius: 24px;
    padding: 12px 24px; font-weight: 600; font-size: 13px;
    min-height: 48px;
}}
QPushButton[buttonVariant="fab-extended-light"]:hover {{
    background: {p['menu_hover']};
}}

QPushButton[buttonVariant="fab-extended-dark"] {{
    background: {p['button_dark']};
    color: #FFFFFF;
    border: none; border-radius: 24px;
    padding: 12px 24px; font-weight: 600; font-size: 13px;
    min-height: 48px;
}}
QPushButton[buttonVariant="fab-extended-dark"]:hover {{
    opacity: 0.85;
}}

QPushButton[buttonVariant="fab-extended-accent"] {{
    background: {p['accent']};
    color: #FFFFFF;
    border: none; border-radius: 24px;
    padding: 12px 24px; font-weight: 600; font-size: 13px;
    min-height: 48px;
}}
QPushButton[buttonVariant="fab-extended-accent"]:hover {{
    background: {p['accent_hover']};
}}

/* --- Custom gradient button --- */
QPushButton[buttonVariant="custom-gradient"] {{
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 transparent,
        stop:1 rgba(102, 102, 102, 85)
    );
    color: {p['text_muted']};
    border: 1px solid {p['shadow_light']};
    border-radius: 12px;
    padding: 10px 24px;
    font-weight: 600;
    font-size: 13px;
    min-width: 130px;
}}
QPushButton[buttonVariant="custom-gradient"]:hover {{
    border-color: {p['text_muted']};
}}

/* --- Custom outline gradient --- */
QPushButton[buttonVariant="custom-outline-gradient"] {{
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 transparent,
        stop:1 rgba(187, 187, 187, 204)
    );
    color: {p['text_muted']};
    border: 1px solid {p['shadow_light']};
    border-radius: 12px;
    padding: 10px 24px;
    font-weight: 600;
    font-size: 13px;
    min-width: 130px;
}}
QPushButton[buttonVariant="custom-outline-gradient"]:hover {{
    border-color: {p['text_muted']};
}}

/* --- Tool buttons --- */
QToolButton {{
    background: {p['card_bg']};
    color: {p['text']};
    border: none;
    border-radius: 10px;
    padding: 6px 12px;
}}

QToolButton:hover {{
    background: {p['menu_hover']};
}}

QToolButton:pressed {{
    background: {p['bg_secondary']};
}}

/* --- Inputs (neumorphic inset feel) --- */
QLineEdit, QTextEdit, QPlainTextEdit {{
    background: {p['input_bg']};
    color: {p['text']};
    border: 2px solid {p['input_bg']};
    border-radius: 12px;
    padding: 10px 14px;
    selection-background-color: {p['accent']};
    selection-color: #FFFFFF;
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    background: {p['input_bg']};
    border: 2px solid {p['accent']};
    padding: 10px 14px;
}}

/* --- Spin boxes --- */
QSpinBox, QDoubleSpinBox {{
    background: {p['input_bg']};
    color: {p['text']};
    border: 2px solid {p['input_bg']};
    border-radius: 10px;
    padding: 6px 10px;
}}

QSpinBox:focus, QDoubleSpinBox:focus {{
    border: 2px solid {p['accent']};
    padding: 6px 10px;
}}

QSpinBox::up-button, QDoubleSpinBox::up-button,
QSpinBox::down-button, QDoubleSpinBox::down-button {{
    border: none;
    background: transparent;
    width: 20px;
    border-radius: 4px;
}}

QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
    background: {p['menu_hover']};
}}

QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
    image: url({_arrow_svg_path('up', p['text_muted'])});
    width: 10px;
    height: 10px;
}}

QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
    image: url({_arrow_svg_path('down', p['text_muted'])});
    width: 10px;
    height: 10px;
}}

/* --- Combo box --- */
QComboBox {{
    background: {p['input_bg']};
    color: {p['text']};
    border: 2px solid {p['input_bg']};
    border-radius: 10px;
    padding: 6px 12px;
}}

QComboBox:hover {{
    background: {p['input_bg']};
    border: 2px solid {p['menu_hover']};
}}

QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: center right;
    border: none;
    background: transparent;
    width: 28px;
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
}}

QComboBox::drop-down:hover {{
    background: {p['menu_hover']};
}}

QComboBox::down-arrow {{
    image: url({_arrow_svg_path('down', p['text_muted'])});
    width: 10px;
    height: 10px;
}}

QComboBox QAbstractItemView {{
    background: {p['card_bg']};
    color: {p['text']};
    border: none;
    border-radius: 6px;
    selection-background-color: {p['accent']};
    selection-color: #FFFFFF;
}}

/* --- Date / Time --- */
QDateEdit, QTimeEdit, QDateTimeEdit {{
    background: {p['input_bg']};
    color: {p['text']};
    border: 2px solid {p['input_bg']};
    border-radius: 10px;
    padding: 6px 10px;
}}

QDateEdit:focus, QTimeEdit:focus, QDateTimeEdit:focus {{
    border: 2px solid {p['accent']};
    padding: 6px 10px;
}}

/* Drop-down button (calendar popup trigger) */
QDateEdit::drop-down, QDateTimeEdit::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: center right;
    width: 28px;
    border: none;
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
    background: transparent;
}}

QDateEdit::drop-down:hover, QDateTimeEdit::drop-down:hover {{
    background: {p['menu_hover']};
}}

QDateEdit::down-arrow, QDateTimeEdit::down-arrow {{
    image: url({_arrow_svg_path('down', p['text_muted'])});
    width: 10px;
    height: 10px;
}}

/* Up/down spinner buttons for time / date editors */
QDateEdit::up-button, QTimeEdit::up-button, QDateTimeEdit::up-button,
QDateEdit::down-button, QTimeEdit::down-button, QDateTimeEdit::down-button {{
    border: none;
    background: transparent;
    width: 20px;
    border-radius: 4px;
}}

QDateEdit::up-button:hover, QTimeEdit::up-button:hover, QDateTimeEdit::up-button:hover,
QDateEdit::down-button:hover, QTimeEdit::down-button:hover, QDateTimeEdit::down-button:hover {{
    background: {p['menu_hover']};
}}

QDateEdit::up-arrow, QTimeEdit::up-arrow, QDateTimeEdit::up-arrow {{
    image: url({_arrow_svg_path('up', p['text_muted'])});
    width: 10px;
    height: 10px;
}}

QDateEdit::down-arrow, QTimeEdit::down-arrow, QDateTimeEdit::down-arrow {{
    image: url({_arrow_svg_path('down', p['text_muted'])});
    width: 10px;
    height: 10px;
}}

/* --- Sliders --- */
QSlider::groove:horizontal {{
    height: 6px;
    background: {p['bg_secondary']};
    border-radius: 3px;
}}

QSlider::handle:horizontal {{
    background: {p['accent']};
    width: 18px;
    margin: -6px 0;
    border-radius: 9px;
}}

QSlider::sub-page:horizontal {{
    background: {p['accent']};
    border-radius: 3px;
}}

/* --- Dial --- */
QDial {{
    background: transparent;
}}

/* --- Radio / Checkbox --- */
QRadioButton, QCheckBox {{
    color: {p['text']};
    spacing: 8px;
    background: transparent;
}}

QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid {p['text_muted']};
    border-radius: 11px;
    background: {p['input_bg']};
}}

QRadioButton::indicator:checked {{
    background: {p['accent']};
    border-color: {p['accent']};
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid {p['text_muted']};
    border-radius: 5px;
    background: {p['input_bg']};
}}

QCheckBox::indicator:checked {{
    background: {p['accent']};
    border-color: {p['accent']};
}}

/* --- Progress bar --- */
QProgressBar {{
    background: {p['bg_secondary']};
    border: none;
    border-radius: 6px;
    text-align: center;
    color: {p['text']};
    height: 12px;
}}

QProgressBar::chunk {{
    background: {p['accent']};
    border-radius: 6px;
}}

/* --- Tab widget --- */
QTabWidget::pane {{
    background: {p['card_bg']};
    border: none;
    border-radius: 10px;
    padding: 4px;
}}

QTabBar::tab {{
    background: {p['bg_secondary']};
    color: {p['text_muted']};
    padding: 8px 18px;
    margin: 2px;
    border: none;
    border-radius: 8px;
}}

QTabBar::tab:selected {{
    background: {p['menu_hover']};
    color: {p['accent']};
    font-weight: bold;
    border-bottom: 2px solid {p['accent']};
}}

QTabBar::tab:hover:!selected {{
    background: {p['menu_hover']};
    color: {p['text']};
}}

/* --- Scroll area --- */
QScrollArea {{
    background: transparent;
    border: none;
}}

QScrollArea > QWidget > QWidget {{
    background: transparent;
}}

QScrollBar:vertical {{
    background: {p['bg']};
    width: 8px;
    border-radius: 4px;
}}

QScrollBar::handle:vertical {{
    background: {p['text_muted']};
    border-radius: 4px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: {p['accent']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

QScrollBar:horizontal {{
    background: {p['bg']};
    height: 8px;
    border-radius: 4px;
}}

QScrollBar::handle:horizontal {{
    background: {p['text_muted']};
    border-radius: 4px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {p['accent']};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}

/* --- Dialog / Error popups --- */
QDialog#Dialog {{
    background: {p['card_bg']};
}}

QDialog#Dialog QFrame#frame_2 {{
    background: {p['card_bg']};
}}

QDialog#Dialog QFrame#frame_top,
QDialog#Dialog QFrame#frame_bottom {{
    background: {p['topbar']};
}}

QDialog#Dialog QLabel#lab_heading,
QDialog#Dialog QLabel#lab_message {{
    color: {p['text_heading']};
}}

QDialog#Dialog QPushButton#bn_min,
QDialog#Dialog QPushButton#bn_close {{
    border: none;
    background-color: {p['card_bg']};
}}

QDialog#Dialog QPushButton#bn_min:hover,
QDialog#Dialog QPushButton#bn_close:hover {{
    background-color: {p['accent']};
    color: #FFFFFF;
}}

QDialog#Dialog QPushButton#bn_east,
QDialog#Dialog QPushButton#bn_west,
QDialog#Error QPushButton#bn_ok {{
    border: none;
    border-radius: 10px;
    color: {p['text']};
    background-color: {p['card_bg']};
    padding: 8px 20px;
}}

QDialog#Dialog QPushButton#bn_east:hover,
QDialog#Dialog QPushButton#bn_west:hover,
QDialog#Error QPushButton#bn_ok:hover {{
    background-color: {p['accent']};
    color: #FFFFFF;
}}

QDialog#Error QFrame#frame {{
    background: {p['card_bg']};
}}

QDialog#Error QFrame#frame_top,
QDialog#Error QFrame#frame_bottom {{
    background: {p['topbar']};
}}

QDialog#Error QLabel#lab_heading {{
    color: {p['text_heading']};
}}

/* --- Form layout labels --- */
QFormLayout QLabel {{
    color: {p['text']};
    background: transparent;
}}

/* --- Nav label (for sidebar icon+text items) --- */
#frame_bottom_west QLabel {{
    color: {p['text_muted']};
    background: transparent;
    font-size: 12px;
    font-weight: 500;
}}

QFrame[menuState="active"] QLabel {{
    color: {p['accent']};
}}

/* --- Page heading / description utility classes --- */
QLabel[heading="true"] {{
    color: {p['text_heading']};
    background: transparent;
    font-size: 20px;
    font-weight: 700;
}}

QLabel[subheading="true"] {{
    color: {p['text_muted']};
    background: transparent;
    font-size: 11px;
}}

/* --- List widget --- */
QListWidget {{
    background: {p['input_bg']};
    border: none;
    border-radius: 10px;
    padding: 4px;
    outline: 0;
}}

QListWidget::item {{
    padding: 8px 12px;
    border-radius: 8px;
    color: {p['text']};
}}

QListWidget::item:selected {{
    background: {p['accent']};
    color: #FFFFFF;
}}

QListWidget::item:hover:!selected {{
    background: {p['menu_hover']};
}}

/* --- Tool box (expanders/accordion) --- */
QToolBox {{
    background: transparent;
}}

QToolBox::tab {{
    background: {p['card_bg']};
    color: {p['text']};
    border: none;
    border-radius: 10px;
    padding: 10px 16px;
    font-weight: 600;
    font-size: 13px;
}}

QToolBox::tab:selected {{
    color: {p['accent']};
}}

QToolBox::tab:hover {{
    background: {p['menu_hover']};
}}

/* Ensure QToolBox tab buttons have enough height for text */
QToolBox > QAbstractButton {{
    min-height: 40px;
}}

/* --- Tab close button --- */
QTabBar::close-button {{
    image: none;
    subcontrol-position: right;
    border: none;
    padding: 4px;
}}

QTabBar::close-button:hover {{
    background: {p['menu_hover']};
    border-radius: 4px;
}}

/* --- Vertical slider --- */
QSlider::groove:vertical {{
    width: 6px;
    background: {p['bg_secondary']};
    border-radius: 3px;
}}

QSlider::handle:vertical {{
    background: {p['accent']};
    height: 18px;
    margin: 0 -6px;
    border-radius: 9px;
}}

QSlider::sub-page:vertical {{
    background: {p['bg_secondary']};
    border-radius: 3px;
}}

QSlider::add-page:vertical {{
    background: {p['accent']};
    border-radius: 3px;
}}

/* --- Tooltip --- */
QToolTip {{
    background: {p['card_bg']};
    color: {p['text']};
    border: none;
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 12px;
}}

/* ===== Focus indicators (keyboard accessibility) ===== */
QPushButton:focus {{
    border: 2px solid {p['accent']};
    outline: none;
}}

QComboBox:focus {{
    border: 2px solid {p['accent']};
}}

QCheckBox:focus {{
    border: 1px solid {p['accent']};
    border-radius: 5px;
    padding: 2px;
}}

QRadioButton:focus {{
    border: 1px solid {p['accent']};
    border-radius: 5px;
    padding: 2px;
}}

QListWidget:focus {{
    border: 2px solid {p['accent']};
}}

QAbstractItemView::item:focus {{
    background: {p['menu_hover']};
    border-radius: 4px;
}}
"""


# ---------------------------------------------------------------------------
# ThemeManager singleton
# ---------------------------------------------------------------------------

class ThemeManager(QtCore.QObject):
    """Singleton that manages the current neumorphism theme (light / dark)."""

    theme_changed = QtCore.Signal(str)  # emits "light" or "dark"

    _instance: ThemeManager | None = None

    def __new__(cls) -> ThemeManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_initialised"):
            return
        super().__init__()
        self._initialised = True
        self._theme = "light"
        self._radius_overrides: dict[str, int] = {}

    # -- public API ---------------------------------------------------------

    @property
    def theme(self) -> str:
        return self._theme

    @property
    def palette(self) -> dict:
        return _PALETTES[self._theme]

    def shadow_configs(self) -> dict[str, list[dict]]:
        return _shadow_configs(self._theme)

    def qss(self) -> str:
        return _generate_qss(self.palette)

    def set_theme(self, theme: str) -> None:
        if theme not in _PALETTES:
            return
        if theme == self._theme:
            return
        self._theme = theme
        self.theme_changed.emit(theme)

    def toggle(self) -> None:
        self.set_theme("dark" if self._theme == "light" else "light")

    def set_accent(self, color_hex: str) -> None:
        """Override the accent colour for both light and dark themes.

        The dark-theme accent is automatically lightened for legibility.
        Call :py:meth:`apply` afterwards to update the live stylesheet.
        """
        c = QtGui.QColor(color_hex)
        h, s, light, a = c.getHslF()
        # Light theme hover: slightly lighter
        hover_light = QtGui.QColor.fromHslF(h, s, min(light * 1.15, 1.0), a)
        # Dark theme: much lighter for visibility on dark background
        dark_accent = QtGui.QColor.fromHslF(h, max(s * 0.7, 0.3), min(light * 1.5, 0.85), a)
        dark_hover  = QtGui.QColor.fromHslF(h, max(s * 0.5, 0.2), min(light * 1.7, 0.93), a)
        _PALETTES["light"]["accent"]       = color_hex
        _PALETTES["light"]["accent_hover"] = hover_light.name()
        _PALETTES["dark"]["accent"]        = dark_accent.name()
        _PALETTES["dark"]["accent_hover"]  = dark_hover.name()
        self.theme_changed.emit(self._theme)

    def set_radius_override(self, widget_type: str, px: int) -> None:
        """Override the border-radius for a widget category.

        *widget_type* values: ``"button"`` (default 12 px), ``"input"`` (12 px),
        ``"card"`` (16 px), ``"groupbox"`` (14 px), ``"combo"`` (10 px).
        Call :py:meth:`apply` afterwards to update the live stylesheet.
        """
        self._radius_overrides[widget_type] = px

    def apply(self, app: QtWidgets.QApplication | None = None) -> None:
        """(Re-)apply QSS to the running application."""
        if app is None:
            app = QtWidgets.QApplication.instance()
        if app:
            app.setStyleSheet(self.qss())


# Module-level convenience
theme_manager = ThemeManager()
