from PySide6 import QtCore, QtWidgets, QtGui
from pynput import keyboard
from snippet_handler import SnippetsSearch
import os

windows = False
if os.name == "nt":
    import win32gui, win32con, win32process, win32api
    win32gui.SystemParametersInfo(win32con.SPI_SETFOREGROUNDLOCKTIMEOUT, 0, win32con.SPIF_SENDWININICHANGE | win32con.SPIF_UPDATEINIFILE)
    windows = True

class MyLineEdit(QtWidgets.QLineEdit):
    def focusOutEvent(self, event):
        self.parentWidget().toggle_visible()
        
class MyWidget(QtWidgets.QWidget):
    def __init__(self, search):
        super().__init__()

        self.button = QtWidgets.QPushButton("Hide!")
        self.input = MyLineEdit()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.input)

        self.button.clicked.connect(self.toggle_visible)
        self.input.textChanged.connect(self.input_text_changed)
        
        self.search = search
        self.input.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowState(QtCore.Qt.WindowActive)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
    
    @QtCore.Slot()
    def toggle_visible(self):
        if self.isVisible():
            print("Hiding popup")
            self.hide()
        else:
            print("Showing popup")
            self.show()
            if windows:
                fgwin = win32gui.GetForegroundWindow()
                fg = win32process.GetWindowThreadProcessId(fgwin)[0]
                current = win32api.GetCurrentThreadId()
                if current != fg:
                    win32process.AttachThreadInput(fg, current, True)
                    win32gui.SetForegroundWindow(self.winId())
                    win32process.AttachThreadInput(fg, win32api.GetCurrentThreadId(), False)
            self.activateWindow()
            self.input.raise_()
            self.input.grabKeyboard()
            self.input.setFocus()
    
    @QtCore.Slot()
    def input_text_changed(self, text):
        self.search.search_snippet(text)

class KeybindPressed(QtCore.QObject):
    keybind_pressed = QtCore.Signal()

    def __call__(self):
        self.keybind_pressed.emit()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    search = SnippetsSearch()

    pressed = KeybindPressed()
    with keyboard.GlobalHotKeys({"<cmd>+<space>": pressed}):

        widget = MyWidget(search)
        pressed.keybind_pressed.connect(widget.toggle_visible)
        widget.resize(200, 200)
        widget.show()

        app.exec()