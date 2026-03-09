"""Application entry point for launching the widget showcase."""

import sys
from PySide6.QtWidgets import QApplication

from styles.theme_manager import theme_manager
from windows.main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    theme_manager.apply(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())