import datetime as dt
import time
import re


from DownloadVideo import download_yt_video
from FileEdits import cut_video_subclip
import HelperFuncs as hF
from EditPhotos import GDriveManagement as GDM
from UploadVideo import youtubeUploader, VideoDetails

from SpreedsheetCommunication import SpreedsheetCommunication

Rows="""
 Sent                                               
NomePodcast                            Flow Podcast
Link Podcast           https://youtu.be/FA3_KkE85gA
Tempo Inicio                                0:35:38
Tempo Final                                 0:36:50
Titulo Imagem       ESCREVER É COISA DE ESQUERDISTA
Titulo Video                                       
Imagem                                             
Data de Postagem                                   
Hora de Postagem     
"""

path2save_podcasts = 'E:\\PODCASTS INTEIROS'
path2save_trechos = 'E:\\PODCASTS TRECHOS'#'E:\\PODCASTS TRECHOS'

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    planilha = SpreedsheetCommunication()
    df = planilha.get_df_spreedsheet()
    print(df)

    for index, row in df.iterrows():
        line_index = index+2
        time.sleep(1)
        print(f'rodando o clipe: {row["Titulo Video"]}')
        current_time = dt.datetime.now().strftime('%d_%m_%y-%H_%M_%S')
        #dict_int_dweek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        #current_week_day = dict_int_dweek[current_time.today().weekday()]
        if re.search(r'^\btrue\b|verdadeiro$', row['Sent'], re.IGNORECASE):
            print('Clipe ja inserido')
            continue
        if re.search(r'error$|A POSTAR', row['Sent'], re.IGNORECASE):
            print('Clipe com possivel erro')
            continue
        if re.search(r'A POSTAR', row['Sent'], re.IGNORECASE):
            print('Clipe já cortado')
            continue
        res_download = download_yt_video(video_url=row['Link Podcast'], path2save=path2save_podcasts)
        row['Log'] += f"Download Video: severidade={res_download['nu_sev']},info={res_download['log']}"
        if res_download['nu_sev'] == 3:
            #todo adicionar o log na spreedsheets e tentar download com outro metodo
            continue

        path_video_podcast = res_download['saved_path']
        #todo Regex para eliminar lixo no time
        start_time_cut_str = f"{row['Tempo Inicio']}"
        end_time_cut_str = f"{row['Tempo Final']}"

        start_time_cut_seconds = hF.convert_time2secs(start_time_cut_str)
        end_time_cut_seconds = hF.convert_time2secs(end_time_cut_str)

        path_trecho = f'{path2save_trechos}\\{line_index}-{res_download["video_id"]}--{current_time}.mp4'
        print(f'''\npath2video={path_video_podcast},
                          path_clip={path_trecho},
                          start_video_sec={start_time_cut_seconds},
                          end_video_sec={end_time_cut_seconds}''')

        cut_video_subclip(path2video=path_video_podcast,
                          path_clip=path_trecho,
                          start_video_sec=start_time_cut_seconds,
                          end_video_sec=end_time_cut_seconds)
        print(row, '\n\n')

        id_image = row['Imagem de Fundo']
        id_image = re.sub(r'.*?d/(.*?)/view.+', r'\1', id_image)
        path2image_background = './TemplatesThumbs/imageBackThumb.png'
        path2thumb = 'Thumbnail.png'

        GDM.download_file_from_google_drive(id_image, path2image_background)

        options = {
            'format': 'png',
            'encoding': "iso-8859-1",
            'enable-local-file-access': None,
            }#'width': 600, 'disable-smart-width': ''

        html = GDM.prepare_html2conversion(path2html='',
                                       path2image=rf'{path2image_background}',
                                       title_image=f'{row["Titulo Imagem"]}')
        path2temporayHtml = './TemplatesThumbs/temporary.html'
        f = open(path2temporayHtml, "w")
        f.write(html)
        f.close()

        GDM.convert_html2image(path2html=path2temporayHtml,
                           path2image=rf'{path2thumb}', opt=options)

        Comment = """
        date_post_str = f"{row['Data de Postagem']} {row['Hora de Postagem']}"
        print(date_post_str)
        date_post = dt.datetime.strptime(date_post_str, "%d-%m-%Y %H:%M")

        
        time4post = hF.convert_to_RFC_datetime(year=date_post.year, month=date_post.month,
                                               day=date_post.day, hour=date_post.hour, minute=date_post.minute)
        print(f'I will upload your video {row["Titulo Video"]} forthe date {time4post}')
        youtubeUploader.post_new_video(path2video=f'{path_trecho}',
                       path2thumb=path2thumb,
                       infos={'title': f'{row["Titulo Video"]}',
                              'description': f'{row["Descrição"]}', 'publishAt': f'{time4post}'})

        
        #"""

        df['Sent'][index] = 'TRUE'

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
