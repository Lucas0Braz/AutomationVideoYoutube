from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import ffmpeg
# ffmpeg_extract_subclip("full.mp4", start_seconds, end_seconds, targetname="cut.mp4")

def cut_video_subclip(path2video, path_clip, start_video_sec, end_video_sec):
    ffmpeg_extract_subclip(f"{path2video}", start_video_sec, end_video_sec, targetname=f"{path_clip}")


#cut_video_subclip(path2video='E:\PODCASTS INTEIROS\XKMnTGmotQY.mp4', path_clip=r'E:\PODCASTS TRECHOS TESTE\thumbTest4-14_10_20-18_19_06.mp4',
#                start_video_sec=300, end_video_sec=1200 )

def unify_audio_video(path2video, path2audio, path2save_video):
    video = ffmpeg.input(f'{path2video}')
    audio = ffmpeg.input(f'{path2audio}')
    out = ffmpeg.output(video, audio, path2save_video, vcodec='copy', acodec='aac', strict='experimental')
    out.run()

