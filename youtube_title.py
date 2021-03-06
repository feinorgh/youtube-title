#!/usr/bin/env python2

import re
import sys
from apiclient.discovery import build

def get_api_key():
    f = open('api.key', 'r')
    line = f.readline()
    f.close()
    return line.strip()

def parse_iso8601_duration(duration):
    re_duration = re.compile(
        """
        P
        (?:(?P<days>\d+)D)?
        T
        (?:(?P<hours>\d+)H)?
        (?:(?P<minutes>\d+)M)?
        (?:(?P<seconds>\d+)S)
        """,
        re.MULTILINE | re.VERBOSE
    )
    d = re_duration.match(duration).groupdict()
    parts = []
    for span in ('days', 'hours', 'minutes', 'seconds'):
        if d[span]:
            parts.append("%s %s" % (d[span], span))
    return ", ".join(parts)


def get_video_title(url):
    youtube = build("youtube", "v3", developerKey = get_api_key())
    re_id   = re.compile("v=(\w+)")
    video_id = re_id.search(url).group(1)

    videos_list = youtube.videos().list(
            id         = video_id,
            part       = "snippet,contentDetails",
            maxResults = 1
    ).execute()

    if not videos_list["items"]:
        print("Video '%s' was not found.", video_id)

    video = videos_list["items"][0]
    duration = parse_iso8601_duration(video["contentDetails"]["duration"])
    output = video["snippet"]["title"] + " (" + duration + ")"
    return output


if __name__ == "__main__":
    if ( sys.argv.__len__() < 2 ):
        print("Please provide a YouTube URL")
        exit(1)

    url     = sys.argv[1]
    if url:
        print get_video_title(url)

