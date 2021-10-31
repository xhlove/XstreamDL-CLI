from PySide6.QtCore import Slot
from PySide6.QtWidgets import QTextEdit, QApplication


class CommandQTextEdit(QTextEdit):

    def __init__(self, parent: QTextEdit):
        super(CommandQTextEdit, self).__init__(parent=parent)

    @Slot()
    def copy_text(self):
        QApplication.clipboard().setText(self.toPlainText().strip())