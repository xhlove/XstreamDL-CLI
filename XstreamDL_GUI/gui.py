import os
import sys
import platform
from pathlib import Path
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QMainWindow

# from XstreamDL_CLI.daemon import Daemon
from XstreamDL_GUI.ui.mainui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # self.daemon = None # type: Daemon
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect_signal_slot()
        self.update_command()

    def connect_signal_slot(self):
        '''
        连接信号槽
        '''
        self.ui.lineEdit_URI.update_name.connect(self.ui.lineEdit_name.update_text)
        self.ui.lineEdit_name.ask_name.connect(self.ui.lineEdit_URI.tell_text)
        self.ui.pushButton_do.clicked.connect(self.do_work)
        # 点击复制按钮 复制完整命令到剪切板
        self.ui.pushButton_copy_command.clicked.connect(self.ui.textEdit_command.copy_text)
        # 数据变化更新command内容
        # <------checkBox------>
        self.ui.checkBox_live.stateChanged.connect(self.update_command)
        self.ui.checkBox_show_init.stateChanged.connect(self.update_command)
        self.ui.checkBox_disable_force_close.stateChanged.connect(self.update_command)
        self.ui.checkBox_select.stateChanged.connect(self.update_command)
        self.ui.checkBox_parse_only.stateChanged.connect(self.update_command)
        self.ui.checkBox_disable_auto_concat.stateChanged.connect(self.update_command)
        self.ui.checkBox_overwrite.stateChanged.connect(self.update_command)
        self.ui.checkBox_raw_concat.stateChanged.connect(self.update_command)
        self.ui.checkBox_enable_auto_delete.stateChanged.connect(self.update_command)
        self.ui.checkBox_index_name.stateChanged.connect(self.update_command)
        self.ui.checkBox_disable_auto_decrypt.stateChanged.connect(self.update_command)
        self.ui.checkBox_use_proxy.stateChanged.connect(self.update_command)
        # <------lineEdit------>
        self.ui.lineEdit_redl_code.textChanged.connect(self.update_command)
        self.ui.lineEdit_save_dir.textChanged.connect(self.update_command)
        self.ui.lineEdit_proxy.textChanged.connect(self.update_command)
        self.ui.lineEdit_b64key.textChanged.connect(self.update_command)
        self.ui.lineEdit_hexiv.textChanged.connect(self.update_command)
        self.ui.lineEdit_url_patch.textChanged.connect(self.update_command)
        self.ui.lineEdit_key.textChanged.connect(self.update_command)
        self.ui.lineEdit_base_url.textChanged.connect(self.update_command)
        self.ui.lineEdit_name.textChanged.connect(self.update_command)
        self.ui.lineEdit_URI.textChanged.connect(self.update_command)
        # <------spinBox------>
        self.ui.spinBox_limit_per_host.valueChanged.connect(self.update_command)
        self.ui.spinBox_live_duration_hour.valueChanged.connect(self.update_command)
        self.ui.spinBox_live_duration_minute.valueChanged.connect(self.update_command)
        self.ui.spinBox_live_duration_second.valueChanged.connect(self.update_command)

    @Slot()
    def do_work(self):
        '''
        only support Windows now
        '''
        # 先刷新一下命令
        self.update_command()
        if platform.system() != 'Windows':
            return
        if not self.ui.lineEdit_URI.text().strip():
            return
        # 调用可执行文件 进行下载
        if getattr(sys, 'frozen', False):
            app_path = Path(sys.executable).parent
        else:
            app_path = Path(__file__).parent.parent
        executable = None # type: Path
        for path in app_path.iterdir():
            if path.is_dir():
                continue
            if path.suffix == '.exe' and path.stem.startswith('XstreamDL-CLI'):
                if executable is None:
                    executable = path
                    continue
                # 根据文件创建时间 选择最新的版本
                if path.stat().st_ctime > executable.stat().st_ctime:
                    executable = path
        exec_dir = executable.parent.resolve().as_posix()
        os.system(
            f'start cmd /K "cd {exec_dir} && {executable.name} '
            f'{self.ui.textEdit_command.toPlainText().strip()}"'
        )

    @Slot()
    def update_command(self):
        '''
        点击后组合命令 弹出终端调用CLI
        '''
        command = []
        if self.ui.checkBox_live.isChecked():
            command.append('--live')
            command.append('--live-duration')
            duration = (
                f'{self.ui.spinBox_live_duration_hour.value()}:'
                f'{self.ui.spinBox_live_duration_minute.value()}:'
                f'{self.ui.spinBox_live_duration_second.value()}'
            )
            command.append(duration)
        if self.ui.checkBox_select.isChecked():
            command.append('--select')
        if self.ui.checkBox_disable_force_close.isChecked():
            command.append('--disable-force-close')
        if self.ui.checkBox_overwrite.isChecked():
            command.append('--overwrite')
        if self.ui.checkBox_raw_concat.isChecked():
            command.append('--raw-concat')
        if self.ui.checkBox_disable_auto_concat.isChecked():
            command.append('--disable-auto-concat')
        if self.ui.checkBox_enable_auto_delete.isChecked():
            command.append('--enable-auto-delete')
        if self.ui.checkBox_disable_auto_decrypt.isChecked():
            command.append('--disable-auto-decrypt')
        if self.ui.checkBox_parse_only.isChecked():
            command.append('--parse-only')
        if self.ui.checkBox_show_init.isChecked():
            command.append('--show-init')
        if self.ui.checkBox_index_name.isChecked():
            command.append('--index-to-name')
        if self.ui.checkBox_use_proxy.isChecked():
            command.append('--proxy')
            command.append(self.ui.lineEdit_proxy.text().strip())
        redl_code = self.ui.lineEdit_redl_code.text().strip()
        if redl_code:
            command.append('--redl_code')
            command.append(redl_code)
        save_dir = self.ui.lineEdit_save_dir.text().strip()
        if save_dir:
            command.append('--save-dir')
            command.append(f'"{save_dir}"')
        b64key = self.ui.lineEdit_b64key.text().strip()
        if b64key:
            command.append('--b64key')
            command.append(b64key)
        hexiv = self.ui.lineEdit_hexiv.text().strip()
        if hexiv:
            command.append('--hexiv')
            command.append(hexiv)
        url_patch = self.ui.lineEdit_url_patch.text().strip()
        if url_patch:
            command.append('--url-patch')
            command.append(f'"{url_patch}"')
        key = self.ui.lineEdit_key.text().strip()
        if key:
            command.append('--key')
            command.append(key)
        base_url = self.ui.lineEdit_base_url.text().strip().rstrip('/')
        if base_url:
            command.append('--base-url')
            command.append(base_url)
        name = self.ui.lineEdit_name.text().strip()
        if name:
            command.append('--name')
            command.append(name)
        command.append('--limit-per-host')
        command.append(str(self.ui.spinBox_limit_per_host.value()))
        uri = self.ui.lineEdit_URI.text().strip()
        if uri:
            command.append(f'"{uri}"')
        self.ui.textEdit_command.setText(' '.join(command))

    @Slot()
    def do_work_future(self):
        '''
        点击后组合命令 编程调用CLI
        '''
        pass

    def update_config(self):
        '''
        更新配置文件
        '''
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())