from PySide6 import QtWidgets
from PySide6.QtCore import QCoreApplication, QRect, Qt

from .flow_layout import FlowLayout


class MarkdownLabel(QtWidgets.QLabel):
    def __init__(self, label):
        super().__init__()
        self.setTextFormat(Qt.MarkdownText)
        self.setText(self.tr(label))
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setMargin(0)


def TitleLabel(label):
    return MarkdownLabel("## " + label)


class SnippetTagsWidget(QtWidgets.QWidget):
    def __init__(self, tags):
        super().__init__()
        flowLayout = FlowLayout(self)
        for tag in tags:
            flowLayout.addWidget(QtWidgets.QLabel(tag))
        self.setLayout(flowLayout)
        self.setMinimumWidth(100)


class SnippetWidget(QtWidgets.QWidget):
    def __init__(self, snippet):
        super().__init__()

        widgetText = TitleLabel(snippet.name)
        layout = QtWidgets.QGridLayout(self)
        layout.setVerticalSpacing(0)
        layout.setHorizontalSpacing(10)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(widgetText, 0, 0)
        layout.addWidget(SnippetTagsWidget(snippet.tags), 0, 1)
        self.setLayout(layout)
        self.setContentsMargins(0, 0, 0, 0)
