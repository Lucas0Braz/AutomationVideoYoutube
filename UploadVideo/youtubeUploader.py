#!/usr/bin/python

import http.client
import httplib2
import os
import random
import time
from UploadVideo import VideoDetails
import HelperFuncs as hF

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from oauth2client import client  # Added
from oauth2client import tools  # Added
from oauth2client.file import Storage  # Added

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
                        http.client.IncompleteRead, http.client.ImproperConnectionState,
                        http.client.CannotSendRequest, http.client.CannotSendHeader,
                        http.client.ResponseNotReady, http.client.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

CLIENT_SECRETS_FILE = 'client_secret_data_yt.json'

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

VALID_PRIVACY_STATUSES = ('public', 'private', 'unlisted')


def get_authenticated_service():  # Modified
    credential_path = os.path.join('../', 'credentials.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRETS_FILE, SCOPES)
        credentials = tools.run_flow(flow, store)
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def initialize_upload(youtube, options):
    tags = None
    if options.keywords:
        tags = options.keywords.split(',')

    body = dict(
        snippet=dict(
            title=options.title,
            description=options.description,
            tags=tags,
            categoryId=options.category
        ),
        status=dict(
            privacyStatus=options.privacyStatus,
            publishAt=options.publishAt,
            selfDeclaredMadeForKids=False

        )
    )

    # Call the API's videos.insert method to create and upload the video.

    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=MediaFileUpload(options.path2video, chunksize=-1, resumable=True)
    )

    resumable_upload(insert_request, options, youtube)


# This method implements an exponential backoff strategy to resume a
# failed upload.
def resumable_upload(request, options, service):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print('Uploading file...')
            status, response = request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print('The video with the id %s was successfully uploaded!' % response['id'])

                    # upload thumbnail for Video
                    options.insertThumbnail(service, response['id'])
                else:
                    exit('The upload failed with an unexpected response: %s' % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = 'A retriable HTTP error %d occurred:\n%s' % (e.resp.status,
                                                                     e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = 'A retriable error occurred: %s' % e

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit('No longer attempting to retry.')

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print('Sleeping %f seconds and then retrying...') % sleep_seconds
            time.sleep(sleep_seconds)


def post_new_video(path2video, path2thumb, infos):

    args = VideoDetails.Video(path2video, path2thumb, infos)
    youtube = get_authenticated_service()

    try:
        initialize_upload(youtube, args)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s') % (e.resp.status, e.content)

#time4post = hF.convert_to_RFC_datetime(year=2020,month=10,day=18,hour=7,minute=15 )
#post_new_video(path2video = 'E:\\PODCASTS TRECHOS\\14--18_10_20-18_18_39.mp4',
#    path2thumb = 'E:\\TRECHOS THUMBS\\FALOU QUE IA ME CONVIDAR E NEM CHAMOU.png', infos={'title':'esse e o titulo',
#                                                                                         'description':'la\nla\nla','publishAt': f'{time4post}'} )