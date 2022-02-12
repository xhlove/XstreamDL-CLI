# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['XstreamDL_GUI\\gui.py'],
             pathex=['C:\\Users\\weimo\\Documents\\codes\\XstreamDL-CLI'],
             binaries=[],
             datas=[
                ("XstreamDL_GUI\\ui\\headersui.qm", "XstreamDL_GUI\\ui"),
                ("XstreamDL_GUI\\ui\\mainui.qm", "XstreamDL_GUI\\ui"),
             ],
             hiddenimports=["PySide6.QtCore", "PySide6.QtWidgets", "PySide6.QtGui"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='XstreamDL-GUI_v1.4.1',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='XstreamDL_GUI/ui/logo.ico')
