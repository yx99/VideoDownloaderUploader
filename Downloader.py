import yt_dlp
import yaml

with open('config.yaml', encoding='utf-8') as f:
    config = yaml.load(f.read(), Loader=yaml.FullLoader)
f.close()
URLS = [config['url']]
path = config['path']
proxy = config['proxy']
ydl_opts = {'download_archive': 'videos.txt',
 'extract_flat': 'discard_in_playlist',
 'fragment_retries': 10,
 'ignoreerrors': 'only_download',
 'outtmpl': {'default': path+'%(playlist_title)s/%(title)s.%(ext)s'},
 'postprocessors': [{'key': 'FFmpegConcat',
                     'only_multi_video': True,
                     'when': 'playlist'}],
 'proxy': proxy,
 'retries': 10,
 'writeautomaticsub': True,
 'writeinfojson': True,
 'writethumbnail': True}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    error_code = ydl.download(URLS)

