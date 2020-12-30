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
        video_id = yt_video.video_id
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
            'saved_path': f'{save_video}', 'log': f'{log}', 'nu_sev': nu_sev, 'video_id': video_id}

def download_yt_video_dlYoutube(video_url, path2save, subtype='mp4'):

    ydl = youtube_dl.YoutubeDL(
        {'outtmpl': f'{path2save}\%(id)s.%(ext)s'})

    with ydl:
        result = ydl.extract_info(
            f'{video_url}',
            download=True
        )
    video = result
    name_video = f"{video['id']}.{subtype}"
    saved_path = fr"{path2save}\{name_video}"


    print(video)
    return {'nome_video': name_video, 'video_exists': True,
            'saved_path': saved_path, 'log': None, 'nu_sev': 0, 'video_id': video['id']}

def get_infos_yt_video_dlYoutube(video_url, opt):

    ydl = youtube_dl.YoutubeDL(
        {'outtmpl': f'%(id)s.%(ext)s'})

    with ydl:
        result = ydl.extract_info(
            f'{video_url}',
            download=False  # We just want to extract the info
        )
    video = result
    name_video = f"{video['id']}.mp4"

    if 'tags_yt' in opt:
        tags = video['tags']
        tags_str = ''
        for tag in tags:
            tags_str = f'{tags_str},{tag}'

        return tags_str

    print(video)
    return video

def download_yt_video(video_url, path2save, subtype='mp4'):
    try:
        res = download_yt_video_pyTube(video_url, path2save, subtype)
        return res

    except Exception as ex:
        res = download_yt_video_dlYoutube(video_url, path2save, subtype)
        return res

def download_yt_best_audio(video_url, path2save, opt):
    extractaudio = False
    audioformat = 'mp3'
    noplaylist = True
    listformats = True
    format = ''
    if 'extractaudio' in opt:
        extractaudio = opt['extractaudio']
    if 'audioformat' in opt:
        audioformat = opt['audioformat']
    if 'noplaylist' in opt:
        noplaylist = opt['noplaylist']
    if 'format' in opt:
        format = opt['format']

    options = {
        'format': f'{format}',  # choice of quality
        'outtmpl': f'{path2save}\%(id)s.%(ext)s',
        'extractaudio': extractaudio,  # only keep the audio
        'audioformat': f"{audioformat}",  # convert to mp3
        'noplaylist': noplaylist,  # only download single song, not playlist
        'listformats': listformats,  # print a list of the formats to stdout and exit
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        result = ydl.extract_info(
            f'{video_url}',
            download=True
        )
    return {'nome_video': 'name_video', 'video_exists': True,
            'saved_path': path2save, 'log': None, 'nu_sev': 0}

def download_yt_best_video(video_url, path2save, subtype='mp4'):
    pass

download_yt_video_dlYoutube('https://youtu.be/ZyfgqMt96uU', path2save='E:\\PODCASTS INTEIROS' )
#print(get_infos_yt_video_dlYoutube('https://www.youtube.com/watch?v=Wh3cjQsc598', {'tags_yt': True}))
config = {'format':'bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4'}
#download_yt_best_audio('https://youtu.be/XKMnTGmotQY', r'C:\Users\Usuario\Documents\Jobs\Melhores Podcasts\\', config)

