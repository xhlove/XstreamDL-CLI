import os
import re
from urllib.parse import urlparse

from typing import Union
from PySide6.QtWidgets import QFileDialog, QLineEdit, QApplication
from PySide6.QtCore import Signal, Slot, QEvent, QUrl, QMimeData
from PySide6.QtGui import QDropEvent, QMouseEvent, QDragEnterEvent


class SaveDirQLineEdit(QLineEdit):
    update_name = Signal(str)

    def __init__(self, parent: QLineEdit):
        super(SaveDirQLineEdit, self).__init__(parent=parent)
        self.installEventFilter(self)

    def eventFilter(self, source: QLineEdit, event: Union[QDropEvent, QMouseEvent, QDragEnterEvent]):
        if event.type() == QEvent.DragEnter:
            event.accept()
        elif event.type() == QEvent.Drop:
            # 任何拖放事件 都先清空原来的内容
            source.clear()
            md = event.mimeData() # type: QMimeData
            if md.hasUrls() and len(md.urls()) == 1:
                path = md.urls()[0].toLocalFile()
                if os.path.exists(path):
                    source.setText(path)
                    self.update_name.emit(path)
            return True
        elif event.type() == QEvent.MouseButtonDblClick:
            # 选择本地headers.json文件
            filePath = QFileDialog.getExistingDirectory(None, "select save dir", './')
            if filePath and os.path.exists(filePath):
                source.clear()
                source.setText(filePath)
                self.update_name.emit(filePath)
            return True
        return super(SaveDirQLineEdit, self).eventFilter(source, event)

    @Slot()
    def tell_text(self):
        return self.update_name.emit(self.text())


class HeaderFileQLineEdit(QLineEdit):
    update_name = Signal(str)

    def __init__(self, parent: QLineEdit):
        super(HeaderFileQLineEdit, self).__init__(parent=parent)
        self.installEventFilter(self)

    def eventFilter(self, source: QLineEdit, event: Union[QDropEvent, QMouseEvent, QDragEnterEvent]):
        if event.type() == QEvent.DragEnter:
            event.accept()
        elif event.type() == QEvent.Drop:
            # 任何拖放事件 都先清空原来的内容
            source.clear()
            md = event.mimeData() # type: QMimeData
            if md.hasUrls() and len(md.urls()) == 1:
                path = md.urls()[0].toLocalFile()
                if os.path.exists(path):
                    source.setText(path)
                    self.update_name.emit(path)
            return True
        elif event.type() == QEvent.MouseButtonDblClick:
            # 选择本地headers.json文件
            fileName, selectedFilter = QFileDialog.getOpenFileUrl(None, caption="select headers.json", dir=QUrl("file://."))
            if isinstance(fileName, QUrl):
                path = fileName.toLocalFile()
                if os.path.exists(path):
                    source.clear()
                    source.setText(path)
                    self.update_name.emit(path)
            return True
        return super(HeaderFileQLineEdit, self).eventFilter(source, event)

    @Slot()
    def tell_text(self):
        return self.update_name.emit(self.text())


class URIQLineEdit(QLineEdit):

    # 这个信号用于更新name输入框内容
    # 不用textChanged是为了避免频繁更新name输入框内容
    update_name = Signal(str)

    def __init__(self, parent: QLineEdit):
        super(URIQLineEdit, self).__init__(parent=parent)
        self.installEventFilter(self)

    def eventFilter(self, source: QLineEdit, event: Union[QDropEvent, QMouseEvent, QDragEnterEvent]):
        if event.type() == QEvent.DragEnter:
            event.accept()
        elif event.type() == QEvent.Drop:
            # 任何拖放事件 都先清空原来的内容
            source.clear()
            md = event.mimeData() # type: QMimeData
            if md.hasUrls() and len(md.urls()) == 1:
                path = md.urls()[0].toLocalFile()
                if os.path.exists(path):
                    source.setText(path)
                    self.update_name.emit(path)
            return True
        elif event.type() == QEvent.MouseButtonDblClick:
            # 获取剪切板内容 看看有没有链接或者是文件
            clipboard = QApplication.clipboard()
            md = clipboard.mimeData()
            if md.hasUrls() and len(md.urls()) == 1:
                # 比如复制了文件 这里就可以获取到文件的路径 但超链接并不会在这里
                path = md.urls()[0].toLocalFile()
                if os.path.exists(path):
                    source.clear()
                    source.setText(path)
                    self.update_name.emit(path)
            elif md.hasText():
                # 检查是不是http(s)://开头的链接
                text = md.text()
                if re.match(r'^https?://', text):
                    source.clear()
                    source.setText(text)
                    self.update_name.emit(text)
            else:
                # 否则尝试选择本地元数据文件
                fileName, selectedFilter = QFileDialog.getOpenFileUrl(None, caption="选择元数据文件", dir=QUrl("file://."))
                if isinstance(fileName, QUrl):
                    path = fileName.toLocalFile()
                    if os.path.exists(path):
                        source.clear()
                        source.setText(path)
                        self.update_name.emit(path)
            return True
        return super(URIQLineEdit, self).eventFilter(source, event)

    @Slot()
    def tell_text(self):
        return self.update_name.emit(self.text())


class NameQLineEdit(QLineEdit):

    # 双击时发出这个信号 用于请求URI输入框内容
    # URI输入框接收到请求后 将内容发回本输入框
    ask_name = Signal()

    def __init__(self, parent: QLineEdit):
        super(NameQLineEdit, self).__init__(parent=parent)
        self.installEventFilter(self)

    def eventFilter(self, source: QLineEdit, event: Union[QDropEvent, QMouseEvent, QDragEnterEvent]):
        if event.type() == QEvent.MouseButtonDblClick:
            # 发出信号 问URI输入框要它的内容
            self.ask_name.emit()
            return True
        return super(NameQLineEdit, self).eventFilter(source, event)

    def fix_name(self, name: str):
        '''
        去除可能存在的非法字符
        '''
        exclude_chars = ["\\", "/", ":", "：", "*", "?", "\"", "<", ">", "|", "\r", "\n", "\t"]
        # 去除非法符号
        name = ''.join(char if char not in exclude_chars else ' ' for char in name)
        # 将之前连续的非法符号 改为单个 _
        return '_'.join(name.split())

    @Slot(str)
    def update_text(self, text: str):
        '''
        更新本输入框内容
        '''
        name = ''
        if re.match(r'^https?://', text):
            # 说明是链接
            name = os.path.basename(urlparse(text).path)
        else:
            if os.path.exists(text):
                name = os.path.basename(text)
        self.setText(self.fix_name(name))