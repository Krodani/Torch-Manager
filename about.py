from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
import os, sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

form = resource_path("about.ui")
Ui_MainWindow, QtBaseClass = uic.loadUiType(form)

class About(QMainWindow):
    def __init__(self):
        super(About,self).__init__()
        uic.loadUi(form,self)