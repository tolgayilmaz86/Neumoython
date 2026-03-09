"""Main window and dialog wrappers for the showcase application."""

import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QMainWindow

import qtawesome as qta

from generated.main_window_ui import Ui_MainWindow

from generated.dialog_ui import Ui_Dialog

from generated.error_ui import Ui_Error

from windows.window_logic import UIFunction
from widgets.catalog import discover_demos
from windows.showcase import build_showcase
from styles.theme_manager import theme_manager


class dialogUi(QDialog):
    """Dialog window wrapper that wires generated UI and runtime behavior."""
    def __init__(self, parent=None):

        super(dialogUi, self).__init__(parent)
        self.d = Ui_Dialog()
        self.d.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.d.bn_min.clicked.connect(lambda: self.showMinimized())

        self.d.bn_close.clicked.connect(lambda: self.close())

        self.d.bn_east.clicked.connect(lambda: self.close())
        self.d.bn_west.clicked.connect(lambda: self.close())

        self.dragPos = self.pos()
        def movedialogWindow(event):
            # Move dialog while dragging the custom title area.
            if event.buttons() == Qt.MouseButton.LeftButton:
                self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
                self.dragPos = event.globalPosition().toPoint()
                event.accept()

        self.d.frame_top.mouseMoveEvent = movedialogWindow
    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def dialogConstrict(self, heading, message, icon, btn1, btn2):
        self.d.lab_heading.setText(heading)
        self.d.lab_message.setText(message)
        self.d.bn_east.setText(btn2)
        self.d.bn_west.setText(btn1)
        pixmap = QtGui.QPixmap(icon)
        self.d.lab_icon.setPixmap(pixmap)


class errorUi(QDialog):
    """Error dialog wrapper that wires generated UI and runtime behavior."""
    def __init__(self, parent=None):

        super(errorUi, self).__init__(parent)
        self.e = Ui_Error()
        self.e.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.e.bn_ok.clicked.connect(lambda: self.close())

        self.dragPos = self.pos()
        def moveWindow(event):
            # Move dialog while dragging the custom title area.
            if event.buttons() == Qt.MouseButton.LeftButton:
                self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
                self.dragPos = event.globalPosition().toPoint()
                event.accept()

        self.e.frame_top.mouseMoveEvent = moveWindow
    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def errorConstrict(self, heading, icon, btnOk):
        self.e.lab_heading.setText(heading)
        self.e.bn_ok.setText(btnOk)
        pixmap2 = QtGui.QPixmap(icon)
        self.e.lab_icon.setPixmap(pixmap2)


class MainWindow(QMainWindow):
    """Top-level application window that hosts the dynamic showcase."""
    def __init__(self):

        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Discover all widget demos and build the showcase UI
        discover_demos()
        build_showcase(self)

        applicationName = "Widget Showcase"
        self.setWindowTitle(applicationName)
        UIFunction.labelTitle(self, applicationName)

        UIFunction.constantFunction(self)

        # Toggle sidebar width (compact/expanded).
        self.ui.toodle.clicked.connect(lambda: UIFunction.toodleMenu(self, 220, True))

        # Install and sync top-bar theme toggle and control icons.
        self._install_theme_toggle()
        self._apply_material_icons()
        self._clear_inline_styles()

        self.diag = dialogUi()
        self.error = errorUi()


        self.dragPos = self.pos()
        def moveWindow(event):
            if UIFunction.returStatus() == 1:
                UIFunction.maximize_restore(self)

            # Move the main window while dragging the custom title area.
            if event.buttons() == Qt.MouseButton.LeftButton:
                self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
                self.dragPos = event.globalPosition().toPoint()
                event.accept()

        self.ui.frame_appname.mouseMoveEvent = moveWindow

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def _install_theme_toggle(self):
        """Insert a light/dark toggle button into the top bar."""
        from PySide6.QtWidgets import QPushButton, QFrame, QHBoxLayout
        from PySide6.QtCore import QSize

        frame = QFrame(self.ui.frame_top_east)
        frame.setObjectName("frame_theme_toggle")
        frame.setFixedSize(QSize(44, 44))
        frame.setFrameShape(QFrame.Shape.NoFrame)

        layout = QHBoxLayout(frame)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        btn = QPushButton(frame)
        btn.setObjectName("bn_theme_toggle")
        btn.setFixedSize(QSize(36, 36))
        btn.setFlat(False)
        btn.setToolTip("Toggle light / dark theme")
        self._update_theme_icon(btn)
        layout.addWidget(btn)

        # Insert before the person/min/max/close frames
        idx = self.ui.horizontalLayout_4.indexOf(self.ui.frame_person)
        self.ui.horizontalLayout_4.insertWidget(idx, frame)

        btn.clicked.connect(self._on_theme_toggle)
        self._theme_btn = btn

    def _on_theme_toggle(self):
        theme_manager.toggle()
        theme_manager.apply()
        self._update_theme_icon(self._theme_btn)
        self._apply_material_icons()
        # Clear inline stylesheets that override the theme
        self._clear_inline_styles()

    def _update_theme_icon(self, btn):
        p = theme_manager.palette
        if theme_manager.theme == "light":
            btn.setIcon(qta.icon("mdi6.weather-night", color=p["text"]))
            btn.setToolTip("Switch to dark mode")
        else:
            btn.setIcon(qta.icon("mdi6.weather-sunny", color=p["text"]))
            btn.setToolTip("Switch to light mode")
        btn.setIconSize(QtCore.QSize(32, 32))
        btn.setText("")

    def _apply_material_icons(self):
        """Apply qtawesome Material Design icons to window controls and sidebar toggle."""
        p = theme_manager.palette
        icon_color = p["text"]
        size = QtCore.QSize(18, 18)

        # Window control buttons
        self.ui.bn_min.setIcon(qta.icon("mdi6.window-minimize", color=icon_color))
        self.ui.bn_min.setIconSize(size)
        self.ui.bn_min.setText("")

        self.ui.bn_max.setIcon(qta.icon("mdi6.window-maximize", color=icon_color))
        self.ui.bn_max.setIconSize(size)
        self.ui.bn_max.setText("")

        self.ui.bn_close.setIcon(qta.icon("mdi6.window-close", color=icon_color))
        self.ui.bn_close.setIconSize(size)
        self.ui.bn_close.setText("")

        # Sidebar hamburger toggle
        self.ui.toodle.setIcon(qta.icon("mdi6.menu", color=icon_color))
        self.ui.toodle.setIconSize(QtCore.QSize(22, 22))
        self.ui.toodle.setText("")

    def _clear_inline_styles(self):
        """Remove inline setStyleSheet calls that conflict with the theme."""
        # Walk all widgets and clear inline styles set by the generated UI.
        # The theme QSS uses object-name selectors so it takes over.
        for widget in self.findChildren(QtWidgets.QWidget):
            if widget.styleSheet():
                widget.setStyleSheet("")
        # Also clear centralwidget
        if self.ui.centralwidget.styleSheet():
            self.ui.centralwidget.setStyleSheet("")
        # Unset flat flag on window control buttons so QSS hover backgrounds render
        for btn in (self.ui.bn_min, self.ui.bn_max, self.ui.bn_close):
            btn.setFlat(False)
            btn.setMaximumSize(QtCore.QSize(36, 36))
            btn.setMinimumSize(QtCore.QSize(36, 36))

        # Center buttons within their container frames
        for frame in (self.ui.frame_min, self.ui.frame_max, self.ui.frame_close):
            frame.setFixedSize(QtCore.QSize(44, 44))
            layout = frame.layout()
            if layout:
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def dialogexec(self, heading, message, icon, btn1, btn2):
        dialogUi.dialogConstrict(self.diag, heading, message, icon, btn1, btn2)
        self.diag.exec()


    def errorexec(self, heading, icon, btnOk):
        errorUi.errorConstrict(self.error, heading, icon, btnOk)
        self.error.exec()


