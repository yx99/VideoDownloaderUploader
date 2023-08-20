from script.biliup_tool import BiliBili, Data
import yaml
import os 
import json
import time

def getFileNames(file_path):
    videoFile = []
    files = os.listdir(file_path)
    files = sorted(files,  key=lambda x: os.path.getctime(os.path.join(file_path, x)))
    for i in range(len(files)):
        if (files[i][-4:] == "webm" or files[i][-4:] == ".mkv"):
            videoFile.append(files[i])
    return videoFile

if __name__ == '__main__':
    with open('config.yaml', encoding='utf-8') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
    f.close()
    fullpath = config['path']+config['dir']
    videoFile = getFileNames(fullpath)
    biliname = config['biliname']
    tid = config['tid']
    listpath = fullpath+r'\\'+config['dir']+'.info.json'
    # with open(listpath, 'r', encoding='utf-8') as flistinfo:
    #     listdictinfo = json.load(flistinfo)
    #     listtitle = listdictinfo['title']
    #     listdesp = listdictinfo['description']
    #     listurl = listdictinfo['webpage_url']
    #     uploader = listdictinfo['uploader_id']
    #     uploaderdate = listdictinfo['modified_date']
    #     tegs = listdictinfo['tags']
    # flistinfo.close()

    for file in videoFile:
        filename = file.split('.',1)[0]
        filepath = os.path.join(fullpath, file)
        srtpath = os.path.join(fullpath, filename + '.srt')
        srtpathzh = os.path.join(fullpath, filename + '-zh.srt')
        infopath = os.path.join(fullpath, filename + '.info.json')
        with open(infopath, 'r', encoding='utf-8') as f1:
            info_data = json.load(f1)
            f1.close()
            title = info_data['title']
            title = config['prefix'] + title
            if len(title)>80:
                title = title[:80]
            thumbnail = info_data['thumbnail']
            desp = info_data["description"]
            uploader = info_data["uploader"]
            uploaderdate = info_data["upload_date"]
            desp0 = '作者：'+uploader+'\n发布时间：'+uploaderdate+'\n搬运：'+biliname+'\n原简介：'+desp
            if len(desp0)>1900:
                desp0 = desp0[:1900]
            tegs = info_data["tags"]
            tags = []
            for i in tegs:
                if ' ' not in i:
                    tags.append(i)
            if len(tags)>9:
                tags = tags[:10]
            if len(tags)==0:
                tags.append('搬运')
            webpage_url = info_data['webpage_url']
        video = Data()
        video.title = title # title
        video.desc = desp0  # 简介
        cover = os.path.join(fullpath, filename + '.webp')    # cover
        video.source = webpage_url     #'添加转载地址说明'
        video.tid = tid # 设置视频分区,默认为122 野生技能协会
        video.set_tag(tags) # 设置标签
        # video.dynamic = '动态内容'
        lines = 'cs-bda2' #auto
        tasks = 3
        dtime = 0 # 延后时间，单位秒
        sessdata = ''
        bili_jct = ''
        dedeuserid_ckmd5 = ''
        dedeuserid = ''
        access_token = ''

        with open('cookie.json', 'r') as f:
            cookie_contents = json.loads(f.read())
        f.close()
        if 'cookie_info' in cookie_contents:
            cookies = cookie_contents['cookie_info']['cookies']
            for cookie in cookies:
                if cookie['name'] == 'SESSDATA':
                    sessdata = cookie['value']
                elif cookie['name'] == 'bili_jct':
                    bili_jct = cookie['value']
                elif cookie['name'] == 'DedeUserID__ckMd5':
                    dedeuserid_ckmd5 = cookie['value']
                elif cookie['name'] == 'DedeUserID':
                    dedeuserid = cookie['value']
        else:
            print("[error ] 请先登录获取cookie")

        if 'token_info' in cookie_contents:
            access_token = cookie_contents['token_info']['access_token']
        else:
            print("[error ] 请先登录获取cookie")

        login_access = {
            'cookies': {
                'SESSDATA': sessdata,
                'bili_jct': bili_jct,
                'DedeUserID__ckMd5': dedeuserid_ckmd5,
                'DedeUserID': dedeuserid
            },
            'access_token': access_token
        }

        with BiliBili(video) as bili:
            bili.login("bili.cookie", login_access)
            # bili.login_by_password("username", "password")
            video_part = bili.upload_file(filepath, lines=lines, tasks=tasks)  # 上传视频，默认线路AUTO自动选择，线程数量3。
            video.append(video_part)  # 添加已经上传的视频
            video.videos[0]['title'] = video.title
            video.delay_time(dtime) # 设置延后发布（2小时~15天）
            video.cover = bili.cover_up(cover).replace('http:', '')
            # ret = bili.submit()  # 提交视频
            ret = bili.submit_client()  # 提交视频
        time.sleep(10)

    

        