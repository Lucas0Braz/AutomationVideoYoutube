import os
from pathlib import Path
from datetime import datetime, timezone

from PIL import Image
from glob import glob

def convert_time2secs(time):
    return sum(x * int(t) for x, t in zip([3600, 60, 1], time.split(":")))
#print(convert_time2secs('0:06:40'))
#225 400

def check_exists_file(yt_video_title, path_check, type_file='.mp4'):
    str_path = f"{path_check}\\{yt_video_title}{type_file}"
    str_path = str_path.replace('#', '')
    path_w10 = Path(str_path)
    print(str_path)
    exists = os.path.exists(path_w10)
    return exists

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime(year, month, day, hour, minute, 0).isoformat() + '.000Z'
    return dt

def resize_image(path2image):
    file = glob(path2image)
    img = Image.open(file)
    width, height = img.size
    (new_width, new_height) = (width/2, height/2)

    img = img.resize(
        (round(new_width),
         round(new_height)),
        Image.ANTIALIAS)
    img.save(file, format='png')

#print (convert_to_RFC_datetime(2020,12,14,13,15))

#datetime.now().strftime("%d-%m-%y %H:%M:%S")
#datetime.now().strftime("%Y-%m-%dT%H:%M:%S.")
    #YYYY-MM-DDThh:mm:ss.sZ %Y-%m-%dT%H:%M:%SZ
    #2020-12-14T13:15:00Z



def utcformat(dt, timespec='milliseconds'):
    """convert datetime to string in UTC format (YYYY-mm-ddTHH:MM:SS.mmmZ)"""
    iso_str = dt.astimezone(timezone.utc).isoformat('T', timespec)
    return iso_str.replace('+00:00', 'Z')


def fromutcformat(utc_str, tz=None):
    iso_str = utc_str.replace('Z', '+00:00')
    return datetime.fromisoformat(iso_str).astimezone(tz)


#now = datetime.now(tz=timezone.utc)
#print(now)

# default with milliseconds ('2020-08-28T02:57:54.640Z')
#print('utcformat: ', utcformat(now))
#1994-11-05T08:15:30-05:00

# without milliseconds ('2020-08-28T02:57:54Z')
#print('utcformat with seconds: ', utcformat(now, timespec='seconds'))




