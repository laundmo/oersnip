import pyperclip
from pynput import keyboard
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt

from .snippet_handler import SnippetsSearch
from .utils import force_focus_windows
from .widgets import SnippetWidget


class MyWidget(QtWidgets.QWidget):
    def __init__(self, search):
        super().__init__()

        self.button = QtWidgets.QPushButton("Hide!")
        self.input = QtWidgets.QLineEdit(self)
        self.list_view = QtWidgets.QListWidget(self)
        self.list_view.setSpacing(0)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.list_view)

        self.button.clicked.connect(self.toggle_visible)
        self.input.textChanged.connect(self.input_text_changed)
        self.list_view.itemClicked.connect(self.snippet_selected)

        self.search: SnippetsSearch = search
        self.input.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowState(QtCore.Qt.WindowActive)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.input_text_changed("")

    def add_list_item(self, snippet):
        item = QtWidgets.QListWidgetItem()
        item.setData(Qt.UserRole, snippet)
        widget = SnippetWidget(snippet)

        item.setSizeHint(widget.sizeHint())

        self.list_view.addItem(item)
        self.list_view.setItemWidget(item, widget)

    @QtCore.Slot()
    def toggle_visible(self):
        if self.isVisible():
            print("Hiding popup")
            self.hide()
        else:
            print("Showing popup")
            self.show()
            force_focus_windows(self.winId())
            self.activateWindow()
            self.input.raise_()
            self.input.grabKeyboard()
            self.input.setFocus()

    @QtCore.Slot()
    def input_text_changed(self, text):
        print(text)
        self.list_view.clear()

        for snippet, _, _ in self.search.search_snippet(text):
            self.add_list_item(snippet)

    # TODO: Create custom list widget item that can provide title for
    # snippets that aren't strictly text (images, etc)
    @QtCore.Slot()
    def snippet_selected(self, item: QtWidgets.QListWidgetItem):
        # Copy text to window
        pyperclip.copy(item.data(Qt.UserRole).render())
        self.input.clear()
        self.toggle_visible()


class KeybindPressed(QtCore.QObject):
    keybind_pressed = QtCore.Signal()

    def __call__(self):
        self.keybind_pressed.emit()


def run():
    app = QtWidgets.QApplication([])
    search = SnippetsSearch()

    pressed = KeybindPressed()
    with keyboard.GlobalHotKeys({"<cmd>+<space>": pressed}):

        widget = MyWidget(search)
        pressed.keybind_pressed.connect(widget.toggle_visible)
        widget.resize(200, 200)
        widget.show()

        app.exec()


if __name__ == "__main__":
    run()
