set "myDate=%date:~0,4%%date:~5,2%%date:~8,2%"
set "Dir=.\video_file\file_%myDate%"
md "%Dir%"
cd %Dir%

rem yt-dlp --proxy socks://127.0.0.1:7890 --write-info-json --merge-output-format mp4 https://www.youtube.com/watch?v=nLc84OXLtq0 https://www.youtube.com/watch?v=MAddbFfCsIo
--write-info-json
yt-dlp --proxy socks://127.0.0.1:7890 --write-thumbnail --write-auto-subs --write-info-json --download-archive videos.txt https://www.youtube.com/playlist?list=PLx7-Q20A1VYLRKxauztmyLx7eXKbg1Ez4 -o %(playlist_title)s/%(title)s.%(ext)s
--merge-output-format mp4  

--write-auto-subs

https://www.youtube.com/playlist?list=PLx7-Q20A1VYI6IML8c5jZkd_rbM1ko7mD
yt-dlp --proxy socks://127.0.0.1:7890 --write-thumbnail --write-auto-subs --write-info-json --download-archive videos.txt https://www.youtube.com/playlist?list=PLx7-Q20A1VYI6IML8c5jZkd_rbM1ko7mD -o %(playlist_title)s/%(title)s.%(ext)s