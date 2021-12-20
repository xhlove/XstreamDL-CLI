import os
import sys
import json
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtCore import Slot, Signal, QUrl, QSize
from PySide6.QtWidgets import QWidget, QFileDialog, QLineEdit, QListWidgetItem

from XstreamDL_GUI.ui.headersui import Ui_Form


class CustomLineEdit(QLineEdit):
    update_config = Signal(int, str, str)

    def __init__(self, item: QListWidgetItem, data_type: str, line_index: int, header_data, parent: 'EditorForm'):
        super(CustomLineEdit, self).__init__(parent=parent)
        self.item = item
        self.data_type = data_type
        self.line_index = line_index - 1
        self.header_data = header_data
        self.setText(self.header_data)
        self.update_config.connect(self.parent().update_config)
        self.textChanged.connect(self.send_index)

    def send_index(self):
        self.update_config.emit(self.line_index, self.header_data, self.data_type)
        self.header_data = self.text().strip()

    def resizeEvent(self, event):
        # https://github.com/PyQt5/PyQt/blob/48ef9a5b884091b3b034ba01f86528e2415a1890/QListWidget/FoldWidget.py#L52
        # 解决item的高度问题
        super(CustomLineEdit, self).resizeEvent(event)
        self.item.setSizeHint(QSize(self.minimumWidth(), self.height()))


class EditorForm(QWidget, Ui_Form):
    def __init__(self, icon: QIcon):
        super(EditorForm, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(icon)
        self.config = {}
        self.has_refresh = False
        self.pushButton_select.clicked.connect(self.select_header_file)
        self.pushButton_add.clicked.connect(self.add_header_key_value)
        self.pushButton_save.clicked.connect(self.save_header_file)
        self.textEdit_headers_content.refresh.connect(lambda: self.load_from_content())
        self.refresh_ui()

    def refresh_ui(self):
        '''
        界面初始化后设置各个框框的内容
        '''
        if self.has_refresh:
            return
        self.has_refresh = True
        if self.lineEdit_headers_path.text().strip() == '':
            self.textEdit_headers_content.setText(json.dumps(self.config, ensure_ascii=False, indent=4))
            return
        self.load_from_file()

    def load_from_file(self):
        try:
            file_path = Path(self.lineEdit_headers_path.text().strip())
            if file_path.exists() and file_path.is_file():
                self.config = json.loads(file_path.read_text(encoding='utf-8'))
            self.textEdit_headers_content.setText(json.dumps(self.config, ensure_ascii=False, indent=4))
            self.show_key_value()
        except Exception:
            # 异常则清空路径
            self.lineEdit_headers_path.setText('')

    def load_from_content(self):
        try:
            self.config = json.loads(self.textEdit_headers_content.toPlainText())
            self.show_key_value()
        except Exception:
            pass

    def show_key_value(self):
        '''
        创建对应的编辑列表
        '''
        self.listWidget_headers_key.clear()
        self.listWidget_headers_value.clear()
        for header_key, header_value in self.config.items():
            # 设置 header_key 到 listWidget_headers_key
            item = QListWidgetItem(self.listWidget_headers_key)
            lineedit = CustomLineEdit(item, 'header_key', self.listWidget_headers_key.count(), header_key, self)
            self.listWidget_headers_key.setItemWidget(item, lineedit)
            # 设置 header_value 到 listWidget_headers_value
            item = QListWidgetItem(self.listWidget_headers_value)
            lineedit = CustomLineEdit(item, 'header_value', self.listWidget_headers_value.count(), header_value, self)
            self.listWidget_headers_value.setItemWidget(item, lineedit)

    @Slot(int, str, str)
    def update_config(self, target_index: int, origin_data: str, data_type: str):
        '''
        listWidget中key或value内容变化时发送对应的索引
        通过索引获取key和value的值
        '''
        # data_type是header_key 尝试去除原有的header_key
        if data_type == 'header_key' and origin_data != '' and self.config.get(origin_data) is not None:
            _ = self.config.pop(origin_data)
        item = self.listWidget_headers_key.item(target_index)
        lineedit = self.listWidget_headers_key.itemWidget(item) # type: CustomLineEdit
        header_key = lineedit.text().strip()
        if header_key != '':
            item = self.listWidget_headers_value.item(target_index)
            lineedit = self.listWidget_headers_value.itemWidget(item) # type: CustomLineEdit
            header_value = lineedit.text().strip()
            self.config[header_key] = header_value
        self.textEdit_headers_content.setText(json.dumps(self.config, ensure_ascii=False, indent=4))

    @Slot()
    def select_header_file(self):
        '''
        通过点击select按钮选择headers.json
        '''
        fileName, selectedFilter = QFileDialog.getOpenFileUrl(None, caption="select headers.json", dir=QUrl("file://."))
        if isinstance(fileName, QUrl):
            path = fileName.toLocalFile()
            if os.path.exists(path):
                self.lineEdit_headers_path.clear()
                self.lineEdit_headers_path.setText(path)
                self.load_from_file()

    @Slot()
    def add_header_key_value(self):
        '''
        添加一对key value
        '''
        item = QListWidgetItem(self.listWidget_headers_key)
        lineedit = CustomLineEdit(item, 'header_key', self.listWidget_headers_key.count(), '', self)
        self.listWidget_headers_key.setItemWidget(item, lineedit)
        item = QListWidgetItem(self.listWidget_headers_value)
        lineedit = CustomLineEdit(item, 'header_value', self.listWidget_headers_value.count(), '', self)
        self.listWidget_headers_value.setItemWidget(item, lineedit)

    @Slot()
    def save_header_file(self):
        '''
        保存key value
        '''
        path_text = self.lineEdit_headers_path.text().strip()
        if path_text == '':
            # 弹窗保存文件的对话框
            if getattr(sys, 'frozen', False):
                app_path = Path(sys.executable).parent.resolve().as_posix()
            else:
                app_path = Path(__file__).parent.parent.parent.parent.resolve().as_posix()
            path_text, selectedFilter = QFileDialog.getSaveFileName(None, caption="save as *.json", dir=app_path, filter='Json (*.json)')
        if not path_text:
            return
        Path(path_text).write_text(json.dumps(self.config, ensure_ascii=False, indent=4), encoding='utf-8')