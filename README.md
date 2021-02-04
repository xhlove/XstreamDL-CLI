# XstreamDL-CLI
基于`python 3.7.4+`的，命令行版本的，HLS/DASH流下载器，支持标准AES-128-CBC解密

## 使用

首先安装必要的库
```bash
pip install -r requirements.txt
```

```bash
python -m XstreamDL_CLI.cli FILEPATH/STREAMURL
```

实例

1. 通过python执行下载模块
    ```bash
    python -m XstreamDL_CLI.cli --b64key oKi/hwKVuLveo/hISX1PQw== --hexiv b3d5ca56926d49d8e96b70aa5c7b358e --name 第一节总论 https://hls.videocc.net/d06ae002cb/2/d06ae002cb4a0bed78fb912c874fdbb2_2.m3u8
    ```
2. 通过exe直接下载
    ```bash
    XstreamDL-CLI_v1.0.0.exe --b64key oKi/hwKVuLveo/hISX1PQw== --hexiv b3d5ca56926d49d8e96b70aa5c7b358e --name 第一节总论 https://hls.videocc.net/d06ae002cb/2/d06ae002cb4a0bed78fb912c874fdbb2_2.m3u8
    ```
3. 如果使用`Windows Terminal`，可以将下面的命令保存为`bat`文件
    ```bash
    chcp 65001
    wt new-tab -p "Command Prompt" -d "%cd%" cmd /k "XstreamDL-CLI_v1.0.0.exe --b64key oKi/hwKVuLveo/hISX1PQw== --hexiv b3d5ca56926d49d8e96b70aa5c7b358e --name 第一节总论 https://hls.videocc.net/d06ae002cb/2/d06ae002cb4a0bed78fb912c874fdbb2_2.m3u8"
    ```
    
    ![](images/Snipaste_2021-02-04_19-13-09.png)

**合并需要先将ffmpeg置于环境变量**

## pyinstaller打包

```bash
pyinstaller -i logo.ico -n XstreamDL-CLI_v1.0.0 -F XstreamDL_CLI\__main__.py
```

## 示意

- 普通m3u8下载

![](images/normal_m3u8.gif)

- master m3u8下载

![](images/master_m3u8.gif)

- 特殊master m3u8下载

![](images/camf_master_m3u8.gif)

## 特性

- 基于aiohttp

## 其他

- 逐步完善中

# 参考

- https://tools.ietf.org/html/rfc8216