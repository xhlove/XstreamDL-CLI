![XstreamDL-GUI](images/oCam_2021_12_19_00_07_34_559.gif)

[XstreamDL-GUI](https://github.com/xhlove/XstreamDL-CLI/releases/download/1.3.8/XstreamDL-GUI_v1.3.8.exe)

**XstreamDL-GUI must use with XstreamDL-CLI**

---

The tool is unfriendly, read README carefully if you want to use it.

# FIRST

put ffmpeg, mp4decrypt to binaries folder, please download from here

- https://github.com/xhlove/XstreamDL-CLI/releases/download/1.3.1/binaries.7z

files structure:

**for source code**

```bash
XstreamDL-CLI
    logs
    binaries
        ffmpeg.exe
        mp4decrypt.exe
    XstreamDL_CLI
        cli.py
```

**for executable**

```bash
some_folder
    logs
    binaries
        ffmpeg.exe
        mp4decrypt.exe
    XstreamDL-CLI_v1.4.1.exe
```

## tips

- recommend **miniconda** to manage your virtual python environment

# FEEDBACK

**to reproduce your problem, please provide detail info as you can**

check following items before you feedback

- do you use the latest version ?
    - please use the latest version
- do you input a wrong link ?
    - program accept a link which contains metadata info about stream, the content of the link should be readable
- do you input a m3u8 live link ?
    - **program not support m3u8 live**
- if it need to vpn to access the link ?
    - program default not use any proxy, check --proxy option if you need
- link is different from the link(raw.json) that in the browser/captured ?
    - if they are same, maybe you need to set cookie or particular header
    - if raw.json link is the part of correct link, maybe you need to use --url-patch option
    - if raw.json link end part is the part of correct link, maybe you need to use --base-url option
    - if raw.json link front part is the part of correct link, but end part is not matched, report to me

**feedback points**

- description of your question
- log file
- version(file name if you use executable version)
- full command that you used
- traceback info(**screenshot or text**)
- correct init segment link and any segment link except init segment
- have ip restriction or not, tell ip area which can access the link if yes
- target link's online page link
- have time limit or not(especially for live stream), tell the detail time limit
- if request to access the link need auth, please provide link content directly

if you want to privacy protection, you can

- send detail to my mail
- delete your username in the log file

**feedback example template**

```bash
[question]: download successfully, but cannot decrypt
[version]: XstreamDL-CLI_v1.4.1.exe
[command]: XstreamDL-CLI_v1.4.1.exe --select --raw-concat "https://ec05-poz1.waw2.cache.orange.pl/canal/v/canal/vod/store01/FPL_Y6mY2VScXBCoXRHn6R9K/_/hd4-hssdrm02.ism/manifest"
[traceback]:
[init segment]:
[sample segment]:
[ip restriction]: EU area
[time limit]:
[online page]:
[log file]:(attachment)
[link content]:(attachment)
```

# EXAMPLE COMMAND

if you use executable version, replace `python -m XstreamDL_CLI.cli` to `xxx.exe`

**download and decrypt example**

```bash
python -m XstreamDL_CLI.cli --select --disable-force-close --limit-per-host 100 --key f31203576a323d09d0c305d236a0c793:00fa546ee19f98fc0044237d2ceb820b "https://akamaicdn.hbogo.eu/a9626f47-b065-2a26-43f9-a3094fb7c4d3_hbo/COMP/29223422_hun_comp_d35eda69-a367-4b47-aa0c-a51032d94be2_3400000_v2.ism/manifest"
```

if you only want to get encrypted content

```bash
python -m XstreamDL_CLI.cli --select --disable-force-close --limit-per-host 100 --raw-concat "https://akamaicdn.hbogo.eu/a9626f47-b065-2a26-43f9-a3094fb7c4d3_hbo/COMP/29223422_hun_comp_d35eda69-a367-4b47-aa0c-a51032d94be2_3400000_v2.ism/manifest"
```

if you only want to get segment list

```bash
python -m XstreamDL_CLI.cli --select --parse-only "https://akamaicdn.hbogo.eu/a9626f47-b065-2a26-43f9-a3094fb7c4d3_hbo/COMP/29223422_hun_comp_d35eda69-a367-4b47-aa0c-a51032d94be2_3400000_v2.ism/manifest"
```

if you only want to download best quality audio and video at once

```bash
python -m XstreamDL_CLI.cli --select --best-quality "https://akamaicdn.hbogo.eu/a9626f47-b065-2a26-43f9-a3094fb7c4d3_hbo/COMP/29223422_hun_comp_d35eda69-a367-4b47-aa0c-a51032d94be2_3400000_v2.ism/manifest"
```

read **HELP INFO** for more option

# HELP INFO

```bash
version 1.4.1, A downloader that download the HLS/DASH stream.
usage: XstreamDL-CLI [OPTION]... URL/FILE/FOLDER...

A downloader that download the HLS/DASH stream

positional arguments:
  URI                   URL/FILE/FOLDER string

optional arguments:
  -v, --version         print version and exit
  -h, --help            print help message and exit
  --speed-up            speed up at end
  --speed-up-left SPEED_UP_LEFT
                        speed up when left count less than this value
  --live                live mode
  --name-from-url       get name from segment url
  --live-duration LIVE_DURATION
                        live record time, format HH:MM:SS, example 00:00:30
                        will record about 30s
  --live-utc-offset LIVE_UTC_OFFSET
                        the value is used to correct utc time
  --live-refresh-interval LIVE_REFRESH_INTERVAL
                        live refresh interval
  --name NAME           specific stream base name
  --base-url BASE_URL   set base url for Stream
  --ad-keyword AD_KEYWORD
                        skip #EXT-X-DISCONTINUITY which segment url has this
                        keyword
  --resolution {,270,360,480,540,576,720,1080,2160}
                        auto choose target quality
  --best-quality        auto choose best quality for dash streams
  --video-only          only choose video stream when use --best-quality
  --audio-only          only choose audio stream when use --best-quality
  --all-videos          choose all video stream to download
  --all-audios          choose all audio stream to download
  --service SERVICE     set serviceLocation for BaseURL choose
  --save-dir SAVE_DIR   set save dir for Stream
  --select              show stream to select and download, default is to
                        download all
  --multi-s             use this option when S tag number > 0
  --disable-force-close
                        default make all connections closed securely, but it
                        will make DL speed slower
  --limit-per-host LIMIT_PER_HOST
                        increase the value if your connection to the stream
                        host is poor, suggest >100 for DASH stream
  --headers HEADERS     read headers from headers.json, you can also use
                        custom config
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
  --proxy PROXY         use socks/http proxy, e.g. socks5://127.0.0.1:10808 or
                        http://127.0.0.1:10809
  --disable-auto-exit   disable auto exit after download end, GUI will use
                        this option
  --parse-only          parse only, not to download
  --show-init           show initialization to help you identify same name
                        stream
  --index-to-name       some dash live have the same name for different
                        stream, use this option to avoid
  --log-level {DEBUG,INFO,WARNING,ERROR}
                        set log level, default is INFO
  --redl-code REDL_CODE
                        re-download set of response status codes , e.g.
                        408,500,502,503,504
  --hide-load-metadata  hide `Load #EXT-X-MEDIA metadata` balabala
```