import os
import sys
import locale
import platform
from pathlib import Path
from PySide6.QtCore import Slot, QTranslator
from PySide6.QtWidgets import QApplication, QMainWindow

# from XstreamDL_CLI.daemon import Daemon
from XstreamDL_GUI.ui.mainui import Ui_MainWindow
from XstreamDL_GUI.ui.widgets.headers_editor import EditorForm
from XstreamDL_GUI.handler import ArgsHandler

LOG_LEVEL_CONFIG = {
    0: 'INFO',
    1: 'DEBUG',
    2: 'WARNING',
    3: 'ERROR',
}

RESOLUTION_CONFIG = {
    0: '',
    1: '2160',
    2: '1080',
    3: '720',
    4: '576',
    5: '540',
    6: '480',
    7: '360',
    8: '270',
}


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        # self.daemon = None # type: Daemon
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.handler = ArgsHandler().load_config().save_config()
        # 根据本地配置设置界面
        self.refresh_ui_config()
        # 根据界面选择生成完整命令
        self.update_command()
        # 处理好界面配置后再关联信号槽 否则容易搞乱配置
        self.connect_signal_slot()

    def connect_signal_slot(self):
        '''
        连接信号槽
        '''
        self.ui.lineEdit_URI.update_name.connect(self.ui.lineEdit_name.update_text)
        self.ui.lineEdit_name.ask_name.connect(self.ui.lineEdit_URI.tell_text)
        self.ui.pushButton_do.clicked.connect(self.do_work)
        # 点击复制按钮 复制完整命令到剪切板
        self.ui.pushButton_copy_command.clicked.connect(self.ui.textEdit_command.copy_text)
        self.ui.pushButton_edit_headers.clicked.connect(self.show_headers_editor)
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
        self.ui.checkBox_best_quality.stateChanged.connect(self.update_command)
        self.ui.checkBox_video_only.stateChanged.connect(self.update_command)
        self.ui.checkBox_audio_only.stateChanged.connect(self.update_command)
        self.ui.checkBox_all_videos.stateChanged.connect(self.update_command)
        self.ui.checkBox_all_audios.stateChanged.connect(self.update_command)
        self.ui.checkBox_disable_auto_exit.stateChanged.connect(self.update_command)
        self.ui.checkBox_hide_load_metadata.stateChanged.connect(self.update_command)
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
        self.ui.spinBox_live_utc_offset.valueChanged.connect(self.update_command)
        self.ui.spinBox_live_refresh_interval.valueChanged.connect(self.update_command)
        self.ui.spinBox_live_duration_hour.valueChanged.connect(self.update_command)
        self.ui.spinBox_live_duration_minute.valueChanged.connect(self.update_command)
        self.ui.spinBox_live_duration_second.valueChanged.connect(self.update_command)
        # <------comboBox------>
        self.ui.comboBox_resolution.currentTextChanged.connect(self.update_command)
        self.ui.comboBox_log_level.currentTextChanged.connect(self.update_command)

    def fetch_ui_config(self):
        '''
        获取界面配置
        '''
        self.handler.live_utc_offset = self.ui.spinBox_live_utc_offset.value()
        self.handler.live_refresh_interval = self.ui.spinBox_live_refresh_interval.value()
        if self.handler.live_refresh_interval == 0:
            self.handler.live_refresh_interval = 3
        self.handler.resolution = RESOLUTION_CONFIG[self.ui.comboBox_resolution.currentIndex()]
        self.handler.best_quality = self.ui.checkBox_best_quality.isChecked()
        self.handler.video_only = self.ui.checkBox_video_only.isChecked()
        self.handler.audio_only = self.ui.checkBox_audio_only.isChecked()
        self.handler.all_videos = self.ui.checkBox_all_videos.isChecked()
        self.handler.all_audios = self.ui.checkBox_all_audios.isChecked()
        self.handler.save_dir = self.ui.lineEdit_save_dir.text().strip()
        self.handler.select = self.ui.checkBox_select.isChecked()
        self.handler.disable_force_close = self.ui.checkBox_disable_force_close.isChecked()
        self.handler.limit_per_host = self.ui.spinBox_limit_per_host.value()
        if self.handler.limit_per_host == 0:
            self.handler.limit_per_host = 4
        self.handler.overwrite = self.ui.checkBox_overwrite.isChecked()
        self.handler.raw_concat = self.ui.checkBox_raw_concat.isChecked()
        self.handler.disable_auto_concat = self.ui.checkBox_disable_auto_concat.isChecked()
        self.handler.enable_auto_delete = self.ui.checkBox_enable_auto_delete.isChecked()
        self.handler.disable_auto_decrypt = self.ui.checkBox_disable_auto_decrypt.isChecked()
        self.handler.proxy = self.ui.lineEdit_proxy.text().strip()
        self.handler.use_proxy = self.ui.checkBox_use_proxy.isChecked()
        self.handler.disable_auto_exit = self.ui.checkBox_disable_auto_exit.isChecked()
        self.handler.parse_only = self.ui.checkBox_parse_only.isChecked()
        self.handler.show_init = self.ui.checkBox_show_init.isChecked()
        self.handler.index_to_name = self.ui.checkBox_index_name.isChecked()
        self.handler.log_level = LOG_LEVEL_CONFIG[self.ui.comboBox_log_level.currentIndex()]
        self.handler.redl_code = self.ui.lineEdit_redl_code.text().strip()
        self.handler.hide_load_metadata = self.ui.checkBox_hide_load_metadata.isChecked()
        self.handler.save_config()

    def refresh_ui_config(self):
        '''
        根据配置刷新UI
        '''
        self.ui.spinBox_live_utc_offset.setValue(self.handler.live_utc_offset)
        self.ui.spinBox_live_refresh_interval.setValue(self.handler.live_refresh_interval)
        for index in range(self.ui.comboBox_resolution.count()):
            if self.handler.resolution == RESOLUTION_CONFIG[index]:
                self.ui.comboBox_resolution.setCurrentIndex(index)
                break
        self.ui.checkBox_best_quality.setChecked(self.handler.best_quality)
        self.ui.checkBox_video_only.setChecked(self.handler.video_only)
        self.ui.checkBox_audio_only.setChecked(self.handler.audio_only)
        self.ui.checkBox_all_videos.setChecked(self.handler.all_videos)
        self.ui.checkBox_all_audios.setChecked(self.handler.all_audios)
        self.ui.lineEdit_save_dir.setText(self.handler.save_dir)
        self.ui.checkBox_select.setChecked(self.handler.select)
        self.ui.checkBox_disable_force_close.setChecked(self.handler.disable_force_close)
        self.ui.spinBox_limit_per_host.setValue(self.handler.limit_per_host)
        self.ui.checkBox_overwrite.setChecked(self.handler.overwrite)
        self.ui.checkBox_raw_concat.setChecked(self.handler.raw_concat)
        self.ui.checkBox_disable_auto_concat.setChecked(self.handler.disable_auto_concat)
        self.ui.checkBox_enable_auto_delete.setChecked(self.handler.enable_auto_delete)
        self.ui.checkBox_disable_auto_decrypt.setChecked(self.handler.disable_auto_decrypt)
        self.ui.lineEdit_proxy.setText(self.handler.proxy)
        self.ui.checkBox_use_proxy.setChecked(self.handler.use_proxy)
        self.ui.checkBox_disable_auto_exit.setChecked(self.handler.disable_auto_exit)
        self.ui.checkBox_parse_only.setChecked(self.handler.parse_only)
        self.ui.checkBox_show_init.setChecked(self.handler.show_init)
        self.ui.checkBox_index_name.setChecked(self.handler.index_to_name)
        for index in range(self.ui.comboBox_log_level.count()):
            if self.handler.log_level == LOG_LEVEL_CONFIG[index]:
                self.ui.comboBox_log_level.setCurrentIndex(index)
                break
        self.ui.lineEdit_redl_code.setText(self.handler.redl_code)
        self.ui.checkBox_hide_load_metadata.setChecked(self.handler.hide_load_metadata)

    def closeEvent(self, event):
        if hasattr(self, 'headers_editor'):
            if self.headers_editor.isVisible():
                self.headers_editor.close()
        super(MainWindow, self).closeEvent(event)

    @Slot()
    def show_headers_editor(self):
        '''
        打开headers.json编辑界面
        '''
        self.headers_editor = EditorForm(self.windowIcon())
        self.headers_editor.show()

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
        self.fetch_ui_config()
        command = []
        if self.ui.checkBox_live.isChecked():
            command.append('--live')
            command.append('--live-duration')
            duration = (
                f'{self.ui.spinBox_live_duration_hour.value():0>2}:'
                f'{self.ui.spinBox_live_duration_minute.value():0>2}:'
                f'{self.ui.spinBox_live_duration_second.value():0>2}'
            )
            command.append(duration)
            if self.handler.live_utc_offset != 0:
                command.append('--live-utc-offset')
                command.append(str(self.handler.live_utc_offset))
            command.append('--live-refresh-interval')
            if self.handler.live_refresh_interval != 0:
                command.append(str(self.handler.live_refresh_interval))
            else:
                command.append('3')
        if self.handler.select:
            command.append('--select')
        if self.handler.disable_force_close:
            command.append('--disable-force-close')
        if self.handler.overwrite:
            command.append('--overwrite')
        if self.handler.raw_concat:
            command.append('--raw-concat')
        if self.handler.disable_auto_concat:
            command.append('--disable-auto-concat')
        if self.handler.enable_auto_delete:
            command.append('--enable-auto-delete')
        if self.handler.disable_auto_decrypt:
            command.append('--disable-auto-decrypt')
        if self.handler.parse_only:
            command.append('--parse-only')
        if self.handler.show_init:
            command.append('--show-init')
        if self.handler.best_quality:
            command.append('--best-quality')
        if self.handler.video_only:
            command.append('--video-only')
        if self.handler.audio_only:
            command.append('--audio-only')
        if self.handler.all_videos:
            command.append('--all-videos')
        if self.handler.all_audios:
            command.append('--all-audios')
        if self.handler.disable_auto_exit:
            command.append('--disable-auto-exit')
        if self.handler.hide_load_metadata:
            command.append('--hide-load-metadata')
        if self.handler.index_to_name:
            command.append('--index-to-name')
        if self.handler.use_proxy and self.handler.proxy:
            command.append('--proxy')
            command.append(self.handler.proxy)
        if self.handler.log_level != 'INFO':
            command.append('--log-level')
            command.append(self.handler.log_level)
        if self.handler.resolution != '':
            command.append('--resolution')
            command.append(self.handler.resolution)
        if self.handler.redl_code:
            command.append('--redl_code')
            command.append(self.handler.redl_code)
        if self.handler.save_dir:
            command.append('--save-dir')
            command.append(f'"{self.handler.save_dir}"')
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
        command.append(str(self.handler.limit_per_host))
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
    trans = QTranslator()
    if locale.getdefaultlocale()[0] == 'zh_CN':
        if getattr(sys, 'frozen', False):
            app_path = Path(__file__).parent / 'XstreamDL_GUI'
        else:
            app_path = Path(__file__).parent
        trans.load('ui/headersui', app_path.resolve().as_posix())
        trans.load('ui/mainui', app_path.resolve().as_posix())
    app.installTranslator(trans)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())