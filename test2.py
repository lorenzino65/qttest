#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QSortFilterProxyModel
from PySide6.QtWidgets import QCompleter, QComboBox, QLineEdit


class ExtendedComboBox(QComboBox):

    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        # add a filter model to filter matching items
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.test = QLineEdit()
        self.setLineEdit(self.test)
        self.setCompleter(self.completer)

        # connect signals
        self.test.textChanged.connect(
            self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)

    def keyPressEvent(self, event):
        # Check if the dropdown is open
        if self.view().isVisible():
            # Capture key events here
            self.test.insert(event.text())
        else:
            # Call the base class implementation
            super().keyPressEvent(event)

    # on selection of an item from the completer, select the corresponding item from combobox
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.activated[str].emit(self.itemText(index))

    # on model change, update the models of the filter and completer as well
    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)

    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    string_list = ['hola muchachos', 'adios amigos', 'hello world', 'good bye']

    combo = ExtendedComboBox()

    # either fill the standard model of the combobox
    combo.addItems(string_list)

    # or use another model
    #combo.setModel(QStringListModel(string_list))

    combo.resize(300, 40)
    combo.show()

    sys.exit(app.exec_())
