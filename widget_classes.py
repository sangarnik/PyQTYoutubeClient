# Clases que se usan a lo largo del programa, usualmente para ahorrar lineas de código o por conveniencia
from PyQt5 import QtCore, QtGui, QtWidgets
import styles

"""Clases genéricas"""
class vLayoutWidget(QtWidgets.QFrame): # Widget vacío con alineación interna vertical
    def __init__(self, widgetName=""):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        if not widgetName == "":
            self.setObjectName(widgetName)

    def clearLayout(self): # Resetear los contenidos del widget
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

class hLayoutWidget(QtWidgets.QFrame): # Widget vacío con alineación interna horizontal
    def __init__(self, widgetName=""):
        super().__init__()
        self.layout = QtWidgets.QHBoxLayout(self)
        if not widgetName == "":
            self.setObjectName(widgetName)

    def clearLayout(self): # Resetear los contenidos del widget
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

class gridLayoutWidget(QtWidgets.QFrame): # Widget vacío con alineación interna de tablas (para alinear)
    def __init__(self, widgetName=""):
        super().__init__()
        self.layout = QtWidgets.QGridLayout(self)
        if not widgetName == "":
            self.setObjectName(widgetName)

    def clearLayout(self): # Resetear los contenidos del widget
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

"""Classes de uso específico"""
class setupLoadingObjects(vLayoutWidget): # Widget para la pantalla de carga
    def __init__(self):
        super().__init__()
        # Label de carga
        self.loadingLabel = QtWidgets.QLabel()
        self.loadingLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.loadingLabel)

        # Label del proceso actual que se carga
        self.loadingLabelCurrent = QtWidgets.QLabel()
        self.loadingLabelCurrent.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.loadingLabelCurrent)

        # Barra de carga
        self.loadingBar = QtWidgets.QProgressBar()
        self.loadingBar.setStyleSheet(styles.loadingBarStyle)
        self.loadingBar.setValue(0)
        self.loadingBar.setMinimumSize(QtCore.QSize(800,40))
        self.layout.addWidget(self.loadingBar)