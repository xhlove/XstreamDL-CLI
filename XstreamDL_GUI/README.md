# XstreamDL-GUI

XstreamDL-CLI的可视化界面

## 转换ui到py文件

```bash
pyside6-uic -g python -o XstreamDL_GUI/ui/mainui.py --from-imports XstreamDL_GUI/ui/main.ui
pyside6-uic -g python -o XstreamDL_GUI/ui/headersui.py --from-imports XstreamDL_GUI/ui/headers.ui
```

## 转换qrc到py文件

```bash
pyside6-rcc XstreamDL_GUI/ui/res.qrc -o XstreamDL_GUI/ui/res_rc.py
```

## 启动

```bash
python -m XstreamDL_GUI.gui
```

## 打包

打包前先修改`XstreamDL-GUI.spec`中的`pathex`为自己的`XstreamDL-CLI`文件夹路径

```bash
pyinstaller XstreamDL-GUI.spec
```

use pyinstaller 4.6