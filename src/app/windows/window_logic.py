"""Window behavior helpers for dragging, navigation, and animations."""

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QPropertyAnimation
from PySide6.QtWidgets import QFrame, QSizeGrip

import qtawesome as qta


GLOBAL_STATE = 0
GLOBAL_TITLE_BAR = True
init = False


class UIFunction:
	"""Static helper methods for window movement, menu state, and UI interactions."""

	@staticmethod
	def _repolish(widget):
		widget.style().unpolish(widget)
		widget.style().polish(widget)
		widget.update()

	@staticmethod
	def _set_group_state(parent_frame, property_name, active_frame=None):
		for frame in parent_frame.findChildren(QFrame):
			frame.setProperty(property_name, "normal")
			UIFunction._repolish(frame)
		if active_frame is not None:
			active_frame.setProperty(property_name, "active")
			UIFunction._repolish(active_frame)

	# Placeholder retained for compatibility with older entry flows.
	def initStackTab(self):
		pass


	def labelTitle(self, appName):
		self.ui.lab_appname.setText(appName)


	def maximize_restore(self):
		global GLOBAL_STATE
		status = GLOBAL_STATE
		if status == 0:
			self.showMaximized()
			GLOBAL_STATE = 1
			self.ui.bn_max.setToolTip("Restore")
			self.ui.bn_max.setIcon(qta.icon("mdi6.window-restore", color="#888"))
			self.ui.frame_drag.hide()
		else:
			GLOBAL_STATE = 0
			self.showNormal()
			self.resize(self.width()+1, self.height()+1)
			self.ui.bn_max.setToolTip("Maximize")
			self.ui.bn_max.setIcon(qta.icon("mdi6.window-maximize", color="#888"))
			self.ui.frame_drag.show()


	def returStatus():
		return GLOBAL_STATE


	def setStatus(status):
		global GLOBAL_STATE
		GLOBAL_STATE = status


	def toodleMenu(self, maxWidth, clicked):

		UIFunction._set_group_state(self.ui.frame_bottom_west, "menuState")

		if clicked:
			from windows.showcase import navigate, set_nav_compact

			currentWidth = self.ui.frame_bottom_west.width()
			minWidth = 80
			current_id = getattr(self.ui, '_current_demo_id', 'home')

			if currentWidth == 80:
				extend = maxWidth
				self.ui.frame_bottom_west.setMaximumWidth(maxWidth)
				set_nav_compact(self, False)
				navigate(self, current_id, about=True)
			else:
				extend = minWidth
				set_nav_compact(self, True)
				navigate(self, current_id, about=False)

			self.animation = QPropertyAnimation(self.ui.frame_bottom_west, b"minimumWidth")
			self.animation.setDuration(300)
			self.animation.setStartValue(currentWidth)
			self.animation.setEndValue(extend)
			self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)

			if extend == minWidth:
				self.animation.finished.connect(
					lambda: self.ui.frame_bottom_west.setMaximumWidth(minWidth)
				)

			self.animation.start()


	def constantFunction(self):
		def maxDoubleClick(stateMouse):
			if stateMouse.type() == QtCore.QEvent.Type.MouseButtonDblClick:
				QtCore.QTimer.singleShot(250, lambda: UIFunction.maximize_restore(self))

		if True:
			self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
			self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
			self.ui.frame_appname.mouseDoubleClickEvent = maxDoubleClick
		else:
			self.ui.frame_close.hide()
			self.ui.frame_max.hide()
			self.ui.frame_min.hide()
			self.ui.frame_drag.hide()

		self.sizegrip = QSizeGrip(self.ui.frame_drag)
		self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

		self.ui.bn_min.clicked.connect(lambda: self.showMinimized())

		self.ui.bn_max.clicked.connect(lambda: UIFunction.maximize_restore(self))

		self.ui.bn_close.clicked.connect(lambda: self.close())
