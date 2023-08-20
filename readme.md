# Video Download & Translate & Upload

个人搬运工具，用于自动下载Youtube的播放列表中的视频、封面、字幕，并上传至bilibili。

## USAGE

yt-dlp: a youtube downloader to download videos from youtube.com or other video platforms

install/update with pip:

```
pip install yt-dlp
```

Whisper is used as  a general-purpose speech recognition model to generate subtitles. (ffmpeg is used to convert video to audio)

**download & upload:**

​	 set your config.yaml, cookies.json(upload to bilibili)(generate by [biliup-rs](https://github.com/biliup/biliup-rs)'s release). 

​	 **run:** Downloader.py ---> BiliUploader.py

**generate subtitle:**

​	 set whisper and translation keys.

​	 **run:** GenSubtitles.py

本个人项目用来搬运Youtube视频到Bilibili，同时在搬运过程中使用Whisper产生英文字幕并使用百度通用文本翻译翻译为中文。

项目依赖：

* [yt_dlp](https://github.com/yt-dlp/yt-dlp)

* [biliup](https://github.com/biliup/biliup)

* [whisper](https://github.com/openai/whisper)

第三方工具

* [ffmpeg](https://ffmpeg.org/)

