# XstreamDL-CLI
基于`python 3.7.4+`的，命令行版本的，HLS/DASH流下载器，~~支持标准AES-128-CBC解密（新建文件）~~

## 使用

首先安装必要的库
```bash
pip install -r requirements.txt
```

```bash
python -m XstreamDL_CLI.cli FILEPATH/STREAMURL
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