# XstreamDL-CLI
基于`python 3.7.4+`的，命令行版本的，HLS/DASH流下载器，仅支持**HLS标准AES-128-CBC**解密

## 使用

首先安装必要的库
```bash
pip install -r requirements.txt
```

```bash
python -m XstreamDL_CLI.cli [OPTION]... URL/FILE/FOLDER...
```

GUI INFO

![](/images/Snipaste_2021-08-07_16-00-35.png)

实例

1. 通过python执行下载模块
    ```bash
    python -m XstreamDL_CLI.cli --b64key oKi/hwKVuLveo/hISX1PQw== --hexiv b3d5ca56926d49d8e96b70aa5c7b358e --name 第一节总论 https://hls.videocc.net/d06ae002cb/2/d06ae002cb4a0bed78fb912c874fdbb2_2.m3u8
    ```
2. 通过exe直接下载
    ```bash
    XstreamDL-CLI_v1.3.1.exe --b64key oKi/hwKVuLveo/hISX1PQw== --hexiv b3d5ca56926d49d8e96b70aa5c7b358e --name 第一节总论 https://hls.videocc.net/d06ae002cb/2/d06ae002cb4a0bed78fb912c874fdbb2_2.m3u8
    ```
3. 如果使用`Windows Terminal`，可以将下面的命令保存为`bat`文件
    ```bash
    chcp 65001
    wt new-tab -p "Command Prompt" -d "%cd%" cmd /k "XstreamDL-CLI_v1.0.0.exe --b64key oKi/hwKVuLveo/hISX1PQw== --hexiv b3d5ca56926d49d8e96b70aa5c7b358e --name 第一节总论 https://hls.videocc.net/d06ae002cb/2/d06ae002cb4a0bed78fb912c874fdbb2_2.m3u8"
    ```
    
    ![](images/Snipaste_2021-02-04_19-13-09.png)

**合并需要先将ffmpeg置于环境变量**

**ISM EXAMPLE**

clear ism content

```bash
python -m XstreamDL_CLI.cli --select --overwrite http://playready.directtaps.net/smoothstreaming/SSWSS720H264/SuperSpeedway_720.ism/Manifest
```

drm ism content

```bash
python -m XstreamDL_CLI.cli --disable-auto-concat --select --overwrite https://akamaicdn.hbogo.eu/5acb29be-eba0-46b1-8646-0e8354ff9cda_hbo/COMP/140258727_adr_comp_0cc2c364-5dba-4f1c-96f9-5640f98f5bbb_3400000_v2.ism/manifest 
```

![](images/oCam_2021_08_03_18_19_56_590.gif)

**HELP INFO**

```bash
version 1.3.1, A downloader that download the HLS/DASH stream.
usage: XstreamDL-CLI [OPTION]... URL/FILE/FOLDER...

A downloader that download the HLS/DASH stream

positional arguments:
  URI                   URL/FILE/FOLDER string

optional arguments:
  -v, --version         print version and exit
  -h, --help            print help message and exit
  -live, --live         live mode
  -live-duration LIVE_DURATION, --live-duration LIVE_DURATION
                        live record time, format HH:MM:SS, example 00:00:30
                        will record about 30s
  -name NAME, --name NAME
                        specific stream base name
  -base-url BASE_URL, --base-url BASE_URL
                        set base url for Stream
  -prefer-content-base-url, --prefer-content-base-url
                        prefer use content base url for Stream
  -service-location SERVICE_LOCATION, --service-location SERVICE_LOCATION
                        set serviceLocation for BaseURL choose
  -save-dir SAVE_DIR, --save-dir SAVE_DIR
                        set save dir for Stream
  --select              show stream to select and download, default is to
                        download all
  --disable-force-close
                        default make all connections closed securely, but it
                        will make DL speed slower
  --limit-per-host LIMIT_PER_HOST
                        increase the value if your connection to the stream
                        host is poor, suggest >100 for DASH stream
  --user-agent USER_AGENT
                        set user-agent headers for request
  --referer REFERER     set custom referer for request
  --headers HEADERS     set custom headers for request, separators is |, e.g.
                        "header1:value1|header2:value2"
  --url-patch URL_PATCH
                        add some custom strings for all segments link
  --overwrite           overwrite output files
  --raw-concat          concat content as raw
  --disable-auto-concat
                        disable auto-concat
  --enable-auto-delete  enable auto-delete files after concat success
  --disable-auto-decrypt
                        disable auto-decrypt segments before dump to disk
  --key KEY             <id>:<k>, <id> is either a track ID in decimal or a
                        128-bit KID in hex, <k> is a 128-bit key in hex
  --b64key B64KEY       base64 format aes key, only for HLS standard
                        AES-128-CBC encryption
  --hexiv HEXIV         hex format aes iv
  --proxy PROXY         use http proxy, e.g. http://127.0.0.1:1080
  --split               dash option, split one stream to multi sections
  --disable-auto-exit   disable auto exit after download end, GUI will use
                        this option
  --parse-only          parse only, not to download
  --show-init           show initialization to help you identify same name
                        stream
  --add-index-to-name   some dash live have the same name for different
                        stream, use this option to avoid
  --log-level {DEBUG,INFO,WARNING,ERROR}
                        set log level, default is INFO
  --re-download-status RE_DOWNLOAD_STATUS
                        re-download set of response status codes , e.g.
                        500,502,503,504
```

部分参数说明

- `--select`
    选择要下载的流，如遇到master类型m3u8且不止一条流时
- `--disable-force-close`
    使用此选项可提升下载速度，但可能会造成部分连接在下载完成后无法关闭，影响网络连接性
- `--limit-per-host`
    设定单个域名的连接数，网络较差，使用代理等情况下适当增加可以提升下载速度
- `--proxy`
    暂时只支持HTTP代理

## pyinstaller打包

```bash
pyinstaller -i logo.ico -n XstreamDL-CLI_v1.3.1 -F XstreamDL_CLI\__main__.py
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

## 反馈 & FeedBack

- https://discord.gg/u385PRAUTG