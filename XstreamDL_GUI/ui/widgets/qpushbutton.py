from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QPushButton


class DoQPushButton(QPushButton):

    do_ = Signal(str, int)

    def __init__(self, parent: QPushButton):
        super(DoQPushButton, self).__init__(parent=parent)

    def switch_value(self, value: int):
        self.update_value.emit(self.objectName(), value)

    @Slot(bool)
    def enable(self, flag: bool):
        # 改变控件状态
        self.setEnabled(flag)
        self.setValue(self.minimum())