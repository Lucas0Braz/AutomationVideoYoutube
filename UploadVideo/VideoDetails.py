import os
from googleapiclient.http import MediaFileUpload

import datetime

class Video:

    path2video = ''
    path2thumb = ''
    title = ''
    description = ""
    category = "22"
    keywords = ""
    privacyStatus = "private"
    publishAt = ''
    #YYYY-MM-DDThh:mm:ss.sZ %Y-%m-%dT%H:%M:%SZ
    #2020-12-14T13:15:00Z

    def __init__(self, _path2video, _path2thumb, infos):
        self.path2video = _path2video
        self.path2thumb = _path2thumb
        self.title = infos['title']
        self.description = infos['description']
        if 'category' in infos:
            self.category = infos["category"]
        if 'keywords' in infos:
            self.keywords = infos["keywords"]
        if 'privacyStatus' in infos:
            self.privacyStatus = infos["privacyStatus"]
        if 'publishAt' in infos:
            self.publishAt = infos["publishAt"]
        if 'keywords' in infos:
            self.keywords = infos["keywords"]



    def insertThumbnail(self, youtube, videoId):
        # todo checar se é um diretórtio mesmo path2thumb
        if self.path2thumb:
            request = youtube.thumbnails().set(
                videoId=videoId,
                media_body=MediaFileUpload(self.path2thumb)
            )
            response = request.execute()
            print(response)
        else:
            print('path2thumb is None')