import json
from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import Slot, QEvent, Signal
from PySide6.QtWidgets import QTextEdit, QApplication


class HeadersQTextEdit(QTextEdit):
    refresh = Signal()

    def __init__(self, parent: QTextEdit):
        super(HeadersQTextEdit, self).__init__(parent=parent)
        self.setAcceptRichText(False)
        self.installEventFilter(self)

    def eventFilter(self, source: QTextEdit, event: QMouseEvent):
        if event.type() == QEvent.MouseButtonDblClick:
            # 格式化组件中的内容
            # 或者尝试解析从浏览器中直接复制过来的 request headers
            formatted_content = ''
            content = source.toPlainText()
            try:
                formatted_content = json.dumps(json.loads(content), ensure_ascii=False, indent=4)
            except Exception:
                try:
                    tmp_config = {}
                    for line in content.split('\n'):
                        line = line.strip()
                        if line == '':
                            continue
                        if line.startswith(':'):
                            continue
                        kv = line.split(':', maxsplit=1)
                        if len(kv) == 1:
                            tmp_config[kv[0].strip()] = ''
                        else:
                            tmp_config[kv[0].strip()] = kv[1].strip()
                    formatted_content = json.dumps(tmp_config, ensure_ascii=False, indent=4)
                except Exception:
                    pass
            if formatted_content != '':
                source.setText(formatted_content)
                self.refresh.emit()
            return True
        return super(HeadersQTextEdit, self).eventFilter(source, event)


class CommandQTextEdit(QTextEdit):

    def __init__(self, parent: QTextEdit):
        super(CommandQTextEdit, self).__init__(parent=parent)

    @Slot()
    def copy_text(self):
        QApplication.clipboard().setText(self.toPlainText().strip())