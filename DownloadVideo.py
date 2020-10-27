#from pytube3 import YouTube
import pytube
import os
from pathlib import Path
import re

import youtube_dl

import HelperFuncs as hF


def download_yt_video_pyTube(video_url, path2save, subtype='mp4'):
    print('tentando acessar video {}'.format(video_url))
    nu_sev = 0
    title = ''
    check = None
    log = '\n-'
    save_video = None
    try:
        yt_video = pytube.YouTube(f'{video_url}')
        title = yt_video.title
        name_video = f'{yt_video.video_id }.{subtype}'
        name_video = re.sub(r'\.mp4\.mp4$', r'.mp4', name_video, re.IGNORECASE)
        check = hF.check_exists_file(name_video, path2save)
        print(yt_video.title)
        if check == False:
            save_video = yt_video.streams.filter(progressive=True, subtype=f'{subtype}', res='720p') \
                .first().download(path2save)
        else:
            print('Video Baixado')
            save_video = Path(f'{path2save}\\{name_video}.mp4')
        log += 'Everthing went fine for {}'.format(video_url)
        #################################################################
        # This one should catch - pytube.exceptions.RegexMatchError:
        # regex pattern ((?:v=|\/)([0-9A-Za-z_-]{11}).*) had zero matches
        #################################################################
    except pytube.exceptions.RegexMatchError:
        exception_str = 'The Regex pattern did not return any matches for the video: {}'.format(video_url)
        log += exception_str
        print(exception_str)
        nu_sev = 3

    except pytube.exceptions.ExtractError:
        exception_str = 'An extraction error occurred for the video: {}'.format(video_url)
        log += exception_str
        print(exception_str)
        nu_sev = 3

    except pytube.exceptions.VideoUnavailable:
        exception_str = 'The following video is unavailable: {}'.format(video_url)
        log += exception_str
        print(exception_str)
        nu_sev = 3

    return {'nome_video': title, 'video_exists': check,
            'saved_path': f'{save_video}', 'log': f'{log}', 'nu_sev': nu_sev}


def download_yt_video_dlYoutube(video_url, path2save, subtype='mp4'):

    ydl = youtube_dl.YoutubeDL(
        {'outtmpl': f'{path2save}\%(id)s.%(ext)s'})

    with ydl:
        result = ydl.extract_info(
            f'{video_url}',
            download=True  # We just want to extract the info
        )
    video = result
    name_video = f"{video['id']}.mp4"
    saved_path = fr"{path2save}\{name_video}"


    print(video)
    return {'nome_video': name_video, 'video_exists': True,
            'saved_path': saved_path, 'log': None, 'nu_sev': 0}

def download_yt_video(video_url, path2save, subtype='mp4'):
    try:
        res = download_yt_video_pyTube(video_url, path2save, subtype)
        return res

    except Exception as ex:
        res = download_yt_video_dlYoutube(video_url, path2save, subtype)
        return res


