# PySide6 Neumorphism Widget Library

A **distributable, feature-rich PySide6 widget library** with a soft Neumorphism visual style, inspired by [Neumorphism.Avalonia](https://github.com/flarive/Neumorphism.Avalonia). Includes a live interactive showcase app covering every widget.

> **Requirements:** Python 3.11+ · PySide6 ≥ 6.6 · qtawesome ≥ 1.3

---

## ✨ Highlights

| Area | What's included |
|---|---|
| **Shadow engine** | `BoxShadow` — multi-layer inset/outset shadows on any Qt widget |
| **Theme system** | Light/Dark runtime toggle · 5 accent presets · `set_accent()` API · focus indicators |
| **New widgets** | `ToggleSwitch` · `CollapsibleSection` · `Snackbar` · `AnimatedCard` · `RippleButton` |
| **Showcase** | 17 interactive demo pages auto-discovered from `widgets/catalog/` |
| **Packaging** | `pyproject.toml` (Hatch) — installable as `neumorphism-pyside6` |

---

## 🚀 Quickstart

```bash
git clone https://github.com/tolgayilmaz86/Neumoython.git
cd Neumoython
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
python src/app/main.py
```

> The app **must be launched from the repo root** (`python src/app/main.py`) or from `src/app/` (`python main.py`).

---

## 🎛️ Widget Catalog

### Core / Layout
| Widget | Module | Description |
|---|---|---|
| `BoxShadow` | `widgets.box_shadow` | `QGraphicsEffect` — multi-layer inset & outset shadows |
| `BoxShadowWrapper` | `widgets.box_shadow` | Convenience wrapper that adds shadow margins automatically |
| `AnimatedCard` | `widgets.animated_card` | Neumorphic card that smoothly elevates on hover via `QPropertyAnimation` |

### Controls
| Widget | Module | Description |
|---|---|---|
| `ToggleSwitch` | `widgets.toggle_switch` | Animated pill toggle — keyboard accessible (Space/Return) |
| `RippleButton` | `widgets.ripple_button` | `QPushButton` drop-in with Material ink-ripple on click |
| `CollapsibleSection` | `widgets.collapsible_section` | Animated accordion expander with `addContent()` API |

### Notifications
| Widget | Module | Description |
|---|---|---|
| `Snackbar` | `widgets.snackbar` | Overlay toast — 5 types · action button · auto-dismiss · slide animation |

### Progress
| Widget | Module | Description |
|---|---|---|
| `roundProgressBar` | `widgets.progress_widgets` | Animated circular progress bar |
| `spiralProgressBar` | `widgets.progress_widgets` | Spiral variant |

---

## 🖥️ Demo Pages

All 17 pages live in `src/app/widgets/catalog/` and are auto-discovered at startup.

| ID | Page | Covers |
|---|---|---|
| `buttons` | Buttons | Raised, accent, flat, disabled, checked states |
| `toggles` | Toggles | `ToggleSwitch`, checkboxes, radio buttons |
| `inputs` | Inputs | `QLineEdit`, `QTextEdit`, `QSpinBox` |
| `sliders` | Sliders | Horizontal, vertical, `QDial` |
| `progress_bars` | Progress | Circular, spiral, `QProgressBar` |
| `cards` | Cards | Raised, inset, nested shadow layers |
| `lists` | Lists | `QListWidget` with selection states |
| `tabs` | Tabs | All four `QTabWidget` orientations |
| `expanders` | Expanders | `CollapsibleSection`, `QToolBox` |
| `icons` | Icons | Material Design 6 icon browser |
| `snackbars` | Snackbars | Default / info / success / warning / error toasts |
| `fields` | Fields | `FloatingLabelField` — animated label, validation, password reveal |
| `datetime` | Date & Time | `QDateEdit`, `QTimeEdit`, neumorphic `QCalendarWidget` |
| `comboboxes` | Combo Boxes | Icon combos, grouped headers, editable, size variants |
| `dialogs` | Dialogs | `NeuDialog` — info/confirm/login/input factory methods |
| `menus` | Menus | `QMenuBar`, context menu, `QToolBar` |

---

## 🛠️ Integration Guide

### 1. Apply the theme

```python
from PySide6.QtWidgets import QApplication
from styles.theme_manager import theme_manager

app = QApplication([])
theme_manager.apply(app)          # inject full neumorphic QSS
theme_manager.set_theme("dark")   # or "light"
```

### 2. Change accent colour

Five built-in presets, or any hex colour:

```python
from styles.theme_manager import theme_manager, ACCENT_BLUE, ACCENT_TEAL

theme_manager.set_accent(ACCENT_BLUE)   # updates both light & dark palettes
theme_manager.apply()                   # re-applies QSS to the running app

theme_manager.set_accent("#E91E63")     # custom hex also works
```

Available presets: `ACCENT_PURPLE` (default) · `ACCENT_BLUE` · `ACCENT_TEAL` · `ACCENT_CORAL` · `ACCENT_PINK`

### 3. Add neumorphic shadows

```python
from widgets.box_shadow import BoxShadowWrapper
from styles.theme_manager import theme_manager

shadows = theme_manager.shadow_configs()
wrapper = BoxShadowWrapper(
    my_widget,
    shadow_list=shadows["outside_raised"],
    smooth=True,
    margins=(14, 14, 14, 14),
)
layout.addWidget(wrapper)
```

Shadow presets: `outside_raised` · `inside_pressed` · `button_raised` · `button_pressed` · `input_inset`

### 4. ToggleSwitch

```python
from widgets.toggle_switch import ToggleSwitch

switch = ToggleSwitch(checked=True, label="Enable Feature")
switch.toggled.connect(lambda on: print("on:", on))
```

### 5. Snackbar toast

```python
from widgets.snackbar import Snackbar

Snackbar.show(parent_widget, "File saved", snack_type="success")
Snackbar.show(parent_widget, "Item deleted",
              action_label="Undo", on_action=undo_fn, snack_type="warning")
```

### 6. AnimatedCard

```python
from widgets.animated_card import AnimatedCard
from PySide6.QtWidgets import QVBoxLayout, QLabel

card = AnimatedCard()
vbox = QVBoxLayout(card.content)
vbox.addWidget(QLabel("Hover me"))
```

### 7. CollapsibleSection

```python
from widgets.collapsible_section import CollapsibleSection

section = CollapsibleSection(title="Advanced Options", expanded=False)
section.addContent(my_form_widget)
```

---

## 📁 Project Structure

```
src/app/
├── main.py                      # Entry point
├── styles/
│   └── theme_manager.py         # ThemeManager singleton, palettes, QSS generator
├── widgets/
│   ├── __init__.py              # Public re-exports, __version__
│   ├── box_shadow.py            # BoxShadow engine + BoxShadowWrapper
│   ├── toggle_switch.py         # ToggleSwitch widget
│   ├── collapsible_section.py   # CollapsibleSection widget
│   ├── snackbar.py              # Snackbar overlay widget
│   ├── animated_card.py         # AnimatedCard widget
│   ├── ripple_button.py         # RippleButton widget
│   ├── progress_widgets.py      # roundProgressBar, spiralProgressBar
│   ├── registry.py              # WidgetDemo dataclass + WidgetRegistry
│   └── catalog/
│       ├── __init__.py          # Auto-discovers all demo modules
│       ├── buttons_demo.py
│       ├── toggles_demo.py
│       ├── inputs_demo.py
│       ├── sliders_demo.py
│       ├── progress_demo.py
│       ├── cards_demo.py
│       ├── lists_demo.py
│       ├── tabs_demo.py
│       ├── expanders_demo.py
│       ├── icons_demo.py
│       ├── snackbars_demo.py
│       ├── fields_demo.py
│       ├── datetime_demo.py
│       ├── comboboxes_demo.py
│       ├── dialogs_demo.py
│       └── menus_demo.py
├── windows/
│   ├── showcase.py              # Sidebar builder, router, home page + accent picker
│   ├── main_window.py
│   └── window_logic.py          # Frameless window, drag, animations
└── generated/                   # Qt Designer .ui → .py outputs
```

---

## ➕ Adding a New Demo Page

1. Create `src/app/widgets/catalog/my_widget_demo.py`
2. Register it at module level:
   ```python
   from widgets.registry import registry, WidgetDemo

   def create_page():
       ...
       return page_widget

   registry.register(WidgetDemo(
       id="my_widget",
       name="My Widget",
       description="Short description shown on the home card",
       create_page=create_page,
   ))
   ```
3. Add an icon entry to `_ICON_MAP` in `windows/showcase.py`.
4. Restart — the page appears in the sidebar automatically.

---

## 🎨 Credits

* **Neumorphism design:** Inspired by [Neumorphism.Avalonia](https://github.com/flarive/Neumorphism.Avalonia) by flarive.
* **Material icons:** [qtawesome](https://github.com/spyder-ide/qtawesome) by Spyder IDE.

